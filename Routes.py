from flask import Flask, render_template, request, flash, redirect, url_for, abort, request, get_flashed_messages, session
from flask_mysqldb import MySQL
from gui import app, db
import Forms
from datetime import date, timedelta, datetime
import traceback


@app.route("/")
def firstpage():
    form = Forms.login_form()
    return render_template("login.html",pageTitle = "Username", form = form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # Database query to retrieve stored credentials
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        cursor = db.connection.cursor()
        query = "SELECT Username, Password FROM Authentication_system WHERE Username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result and password == result[1]:

            query_admin = "SELECT Username,Password FROM Admin"
            cursor.execute(query_admin)
            result_admin = cursor.fetchone()
            if result_admin[1] == result[1] and result_admin[0] == result[0]:
                return redirect("/success_admin")

            query_user = "SELECT User_role, User_ID, School_ID, Username, Password FROM User_account WHERE Username = %s"
            cursor.execute(query_user, (username, ))
            result_user = cursor.fetchone()

            # to do --> add unique field in authentication phase
            # Maybe multiple accounts with same username and password..
            session['user_role'] = result_user[0]
            session['user_id'] = result_user[1]
            session['school_id'] = result_user[2]
            session['username'] = result_user[3]
            session['password'] = result_user[4]


            if result_user[0] == 0:
                print('student_successfully_login')
                return redirect("/success_student")
            else:
                query_operator = "SELECT User_ID FROM Operator"
                cursor.execute(query_operator)
                result_operator = cursor.fetchall()
                operator_user_ids = [row[0] for row in result_operator]  # Extract User_ID values from the result_operator

                if result_user[1] in operator_user_ids:
                    return redirect("/success_operator")
                else:
                    return redirect("/success_teacher")

        else:
            flash('Invalid credentials. Please try again.', 'error')
            return redirect("/")

@app.route("/success_student", methods=['GET', 'POST'])
def success_student():

    form = Forms.my_account()

    if request.method == 'POST':
        if form.myaccount.data:
            return redirect('/student_credentials')
        elif form.search.data:
            return redirect('/book_search')
        elif form.issues.data:
            return redirect('/user_issues')

    return render_template("success_student.html", form=form)


@app.route("/student_credentials", methods=['GET', 'POST'])
def student_credentials():
    # Retrieve the student data from the session variable
    cursor = db.connection.cursor()
    student_id = session.get('user_id')
    # Prepare the format string and parameters
    format_string = "%d-%m-%Y"
    params = (format_string,)

    query = "SELECT User_firstname, User_lastname, DATE_FORMAT(User_date_of_birth, %s) FROM User_account WHERE User_account.User_ID = %s"
    cursor.execute(query, (params, student_id,))
    student = cursor.fetchone()

    if student:
        return render_template("student_credentials.html", student=student)
    else:
        # Handle the case when the student data is not available
        return "Student data not found."

@app.route('/book_search', methods=['GET', 'POST'])
def book_search():
    form = Forms.choose_book()
    school_id = session.get('school_id')

    if request.method == 'POST':
        # Handle form submission for search
        book_title = request.form['book_title']
        category = request.form['category']
        author = request.form['author']
        cursor = db.connection.cursor()

        # Perform the search query with the provided filters
        # query 3.3.1
        query_search = "SELECT br.Book_title, bc.Book_category, ba.Book_author_name, br.Book_ID \
                        FROM Book_records as br INNER JOIN Book_category as bc \
                        ON br.Book_ID = bc.Book_ID \
                        INNER JOIN Book_author AS ba \
                        ON br.Book_ID = ba.Book_ID \
                        WHERE br.School_ID = %s \
                        AND (br.Book_title = %s OR %s = '') \
                        AND (bc.Book_category = %s OR %s = '') \
                        AND (ba.Book_author_name = %s OR %s = '')"

        cursor.execute(query_search, (school_id, book_title, book_title, category, category, author, author))
        books = cursor.fetchall()

        # Fetch all available book titles, categories, and authors
        cursor.execute("SELECT DISTINCT Book_title FROM Book_records")
        book_titles = [title[0] for title in cursor.fetchall()]  # Extract values from tuples
        cursor.execute("SELECT DISTINCT Book_category FROM Book_category")
        categories = [category[0] for category in cursor.fetchall()]  # Extract values from tuples
        cursor.execute("SELECT DISTINCT Book_author_name FROM Book_author")
        authors = [author[0] for author in cursor.fetchall()]  # Extract values from tuples

        return render_template("book_search.html", form=form,book_titles=book_titles, categories=categories, authors=authors, books=books)

    else:
        # Fetch all available book titles, categories, and authors
        cursor = db.connection.cursor()
        cursor.execute("SELECT DISTINCT Book_title FROM Book_records")
        book_titles = [title[0] for title in cursor.fetchall()]  # Extract values from tuples
        cursor.execute("SELECT DISTINCT Book_category FROM Book_category")
        categories = [category[0] for category in cursor.fetchall()]  # Extract values from tuples
        cursor.execute("SELECT DISTINCT Book_author_name FROM Book_author")
        authors = [author[0] for author in cursor.fetchall()]  # Extract values from tuples

        # Render the initial page with the search form
        return render_template("book_search.html", form=form, book_titles=book_titles, categories=categories, authors=authors)


@app.route('/book_search/book/<int:book_id>', methods=['POST','GET'])
def handle_book_action(book_id):
    if 'reservation' in request.form:
        # Handle reservation logic
        session['book_id'] = book_id
        return redirect('/reservation')

    if 'issue' in request.form:
        # Handle issue logic
        session['book_id'] = book_id
        return redirect('/issue_book')

    if 'review' in request.form:
        # Handle review logic
        session['book_id'] = book_id
        return redirect('/review')

@app.route('/issue_book', methods=['POST','GET'])
def issue_book():
    book_id = session.get('book_id')
    current_date = date.today()
    due_date = current_date + timedelta(days=7)
    due_date = due_date.strftime("%Y-%m-%d")

    user_id = session.get('user_id')
    school_id = session.get('school_id')
    query = "INSERT INTO Issue (Start_date, Due_date, Book_ID, User_ID, School_ID, Pending) VALUES (%s,%s, %s, %s, %s, 1)"
    try:
        cursor = db.connection.cursor()
        cursor.execute(query, (current_date, due_date,book_id, user_id, school_id))
        db.connection.commit()  # Commit the changes to the database
        return 'Successfully made issue'
    except Exception as e:
        print('Error:', str(e))
        return 'Failed to issue book'


@app.route("/user_issues")
def user_issues():
    school_id = session.get('school_id')
    user_id = session.get('user_id')

    # query 3.3.2
    query32 = " SELECT br.Book_title, iss.Start_date, iss.Completed \
            FROM User_account AS ua \
            INNER JOIN Issue AS iss ON ua.User_ID = iss.User_ID     \
            INNER JOIN Book_records AS br ON iss.Book_ID = br.Book_ID \
            WHERE iss.User_ID = %s AND iss.School_ID = %s AND iss.Pending = 0"

    cursor = db.connection.cursor()
    cursor.execute(query32, (user_id, school_id))
    issues = cursor.fetchall()  # If stored in the session
    if issues:
        return render_template("user_issues.html", issues = issues)
    else:
        return "No issues"

@app.route("/reservation/",methods=['GET', 'POST'])
def reservation():
    form = Forms.reservation()
    book_id = session.get('book_id')
    user_id = session.get('user_id')
    school_id = session.get('school_id')
    if request.method == 'POST':
        # Handle review logic
        start_date = form.date_reservation.data
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()  # Convert start_date to datetime object
        due_date = start_date + timedelta(days=7)
        due_date = due_date.strftime("%Y-%m-%d")
        print('values',start_date,due_date,book_id, user_id, school_id)
        query = "INSERT INTO Reservation (Start_date, Due_date, Book_ID, User_ID, School_ID, Pending) VALUES (%s,%s, %s, %s, %s, 1)"
        try:
            cursor = db.connection.cursor()
            cursor.execute(query, (start_date,due_date,book_id, user_id, school_id,))
            db.connection.commit()  # Commit the changes to the database
            return 'Successfully made reservation'
        except Exception as e:
            print('Error:', str(e))
            return 'Failed to reserve book'

    return render_template('reservation.html', form=form, book_id=book_id)

@app.route("/review/", methods=['GET', 'POST'])
def review():
    book_id = session.get('book_id')
    user_role = session.get('user_role')
    user_id = session.get('user_id')
    school_id = session.get('school_id')
    form = Forms.review()
    if request.method == 'POST':
        # Handle review logic
        rating = form.rating.data
        comment = form.comment.data
        # Save the review to the database or perform any other necessary actions
        if user_role == 1:
            query = "INSERT INTO Review (Rating, Review_text, User_ID, School_ID, Book_ID) VALUES (%s,%s, %s, %s, %s)"
            try:
                cursor = db.connection.cursor()
                cursor.execute(query, (rating, comment, user_id, school_id,book_id,))
                db.connection.commit()  # Commit the changes to the database
                return 'Successfully made review'
            except Exception as e:
                print('Error:', str(e))
                return 'Failed to review book'
        # return redirect('/review')

    return render_template('review.html', form=form, book_id=book_id)


@app.route("/success_teacher",  methods=['GET', 'POST'])
def success_teacher():
    form = Forms.my_account()
    if request.method == 'POST':
        if form.myaccount.data:
            return redirect('/teacher_credentials')
        elif form.search.data:
            return redirect('/book_search')
        elif form.issues.data:
            return redirect('/user_issues')

    return render_template("success_teacher.html", form=form)

@app.route("/teacher_credentials", methods=['GET', 'POST'])
def teacher_credentials():

    # Retrieve the student data from the session variable
    cursor = db.connection.cursor()
    teacher_id = session.get('user_id')
    # Prepare the format string and parameters
    format_string = "%d-%m-%Y"
    params = (format_string,)
    form = Forms.credentials()
    query = "SELECT User_firstname, User_lastname, DATE_FORMAT(User_date_of_birth, %s) FROM User_account WHERE User_account.User_ID = %s"
    cursor.execute(query, (params, teacher_id,))
    teacher = cursor.fetchone()

    if teacher:
        form = Forms.change_credentials()

        if request.method == 'POST':
            return redirect('/change_credentials')

        return render_template("teacher_credentials.html", teacher = teacher, form = form)
    else:
        # Handle the case when the student data is not available
        return "Teacher data not found."

@app.route("/change_credentials", methods=['POST','GET'])
def change_credentials():
    teacher_id = session.get('user_id')
    form = Forms.credentials()

    if request.method == 'POST':
        # Retrieve form data
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        date_of_birth = request.form['date_of_birth']
        username = request.form['username']
        password = request.form['password']
        old_password = session.get('password')
        old_username= session.get('username')

        # Prepare the SQL query
        query = "UPDATE User_account SET User_firstname = %s, User_lastname = %s, User_date_of_birth = %s WHERE User_ID = %s"
        query2 = "UPDATE Authentication_system SET Username = %s, Password = %s WHERE Password = %s AND Username = %s"
        # Execute the query
        cursor = db.connection.cursor()

        cursor.execute(query2, (username, password, old_password, old_username))
        db.connection.commit()  # Commit the changes to the database

        cursor.execute(query, (firstname, lastname, date_of_birth, teacher_id))

        try:
            db.connection.commit()  # Commit the changes to the database
            return 'Succesfully updated credentials'

        except:
            return 'Failed to update'

    return render_template("change_credentials.html", form = form)



@app.route("/success_operator", methods=['POST','GET'])
def success_operator():
        form = Forms.operator_queries()
        results = []
        school_id = session['school_id']

        if request.method == 'POST':
            query = None
            if 'view_issues' in request.form:
                return redirect('/view_issues')

            if 'view_delayed_issues' in request.form:
                return redirect('/view_delayed_issues')

            if 'change_theme' in request.form:
                return redirect('/success_teacher')

            for field_name in form.data:
                if form[field_name].data:
                    query = field_name
                    break

            if query and query == 'query1':
                query1_title = form.query1_title.data
                query1_category = form.query1_category.data
                query1_author = form.query1_author.data
                query1_copies = form.query1_copies.data
                temp_query = "SELECT UNIQUE br.Book_title, ba.Book_author_name\
                            FROM Book_records AS br\
                            INNER JOIN Book_author AS ba ON br.Book_ID = ba.Book_ID\
                            INNER JOIN Book_category AS bc ON br.Book_ID = bc.Book_ID\
                            WHERE (bc.Book_category = %s OR %s = '')\
                              AND (br.Book_title = %s OR %s = '')\
                              AND (ba.Book_author_name = %s OR %s = '')\
                              AND (br.Book_copies = %s OR %s = '')\
                              AND br.School_ID = %s"
                cursor = db.connection.cursor()
                cursor.execute(temp_query, (query1_category, query1_category,query1_title,query1_title,query1_author,query1_author,query1_copies,query1_copies,school_id,))
                results = cursor.fetchall()

            if query and query == 'query2':
                query2_firstname = form.query2_firstname.data
                query2_lastname = form.query2_lastname.data
                query2_days_delayed = form.query2_days_delayed.data

                temp_query = "SELECT ua.User_ID \
                            FROM User_account AS ua\
                            INNER JOIN Issue AS iss ON ua.User_ID = iss.User_ID\
                            INNER JOIN Delayed_issue AS dis ON dis.Issue_ID = iss.Issue_ID\
                            WHERE (ua.User_firstname = %s  OR %s = '')\
                              AND (ua.User_lastname = %s OR %s = '')\
                              AND (dis.Days_delayed = %s OR %s = '')\
                              AND ua.School_ID = %s\
                            GROUP BY ua.User_ID\
                            HAVING COUNT(*) >= 1;"

                cursor = db.connection.cursor()
                cursor.execute(temp_query, (query2_firstname,query2_firstname,query2_lastname,query2_lastname,query2_days_delayed,query2_days_delayed,school_id,))
                results = cursor.fetchall()

            if query and query == 'query3':
                query3_category = form.query3_category.data
                query3_userid = form.query3_userid.data

                temp_query = "SELECT ua.User_ID, AVG(r.Rating), bc.Book_category\
                                FROM User_account AS ua\
                                INNER JOIN Review AS r ON ua.User_ID = r.User_ID\
                                INNER JOIN Book_category AS bc ON r.Book_ID = bc.Book_ID\
                                WHERE (ua.User_ID = %s OR %s = '')\
                                  AND (bc.Book_category = %s OR %s ='')\
                                  AND ua.School_ID = %s\
                                GROUP BY ua.User_ID, bc.Book_category;"

                cursor = db.connection.cursor()
                cursor.execute(temp_query, (query3_userid,query3_userid,query3_category,query3_category,school_id,))
                results = cursor.fetchall()

        return render_template("success_operator.html", form=form, results=results)

@app.route("/view_issues")
def view_issues():
    school_id = session['school_id']
    cursor = db.connection.cursor()
    # Retrieve the issues from the database for the given school_id
    query = "SELECT * FROM Issue WHERE School_ID = %s ORDER BY Pending DESC"
    cursor.execute(query, (school_id,))
    issues = cursor.fetchall()

    return render_template("view_issues.html", issues=issues)

@app.route("/view_delayed_issues")
def view_delayed_issues():
    school_id = session['school_id']
    cursor = db.connection.cursor()
    # Retrieve the issues from the database for the given school_id
    query = "SELECT iss.Issue_ID, iss.Book_ID,iss.User_ID,iss.Start_date,iss.Completed, di.Days_delayed FROM Delayed_issue di INNER JOIN Issue iss ON iss.Issue_ID=di.Issue_ID WHERE iss.School_ID = %s"
    cursor.execute(query, (school_id,))
    issues = cursor.fetchall()

    return render_template("view_delayed_issues.html", issues=issues)

@app.route("/view_issues/update/<int:issue_id>",  methods=['POST','GET'])
def update_issue(issue_id):
    # Update the 'pending' status in the database for the selected issue
    query = "UPDATE Issue SET Pending = 0 WHERE Issue_ID = %s"
    cursor = db.connection.cursor()
    cursor.execute(query, (issue_id,))
    db.connection.commit()
    # Redirect to the view_issues page
    return redirect("/view_issues")

@app.route("/success_admin", methods=['POST', 'GET'])
def success_admin():
    form = Forms.admin_queries()
    results = []
    if request.method == 'POST':
        query = None
        for field_name in form.data:
            if form[field_name].data:
                query = field_name
                break
        if query and query == 'query1':
            query1_year = form.query1_year.data
            query1_month = form.query1_month.data
            temp_query = "SELECT iss.School_ID, COUNT(*) AS TotalIssues \
                          FROM Issue AS iss \
                          WHERE (YEAR(iss.Start_date) = %s OR %s = '') \
                          AND (MONTH(iss.Start_date) = %s  OR %s = '')\
                          GROUP BY iss.School_ID;"
            cursor = db.connection.cursor()
            print(query1_month)
            cursor.execute(temp_query, (query1_year,query1_year, query1_month,  query1_month))
            results = cursor.fetchall()

            formatted_results = []
            for result in results:
                school_id, total_issues = result
                formatted_result = f"School ID: {school_id}, Total Issues: {total_issues}"
                formatted_results.append(formatted_result)
            results = formatted_results

        if query and query == 'query2':
            query2_category = form.query2_category.data

            temp_query = "SELECT ba.Book_author_name \
                          FROM Book_records AS br \
                          INNER JOIN Book_category AS bc ON bc.Book_ID = br.Book_ID \
                          INNER JOIN Book_author AS ba ON ba.Book_ID = br.Book_ID \
                          WHERE bc.Book_category = %s;"

            temp_query2 = "SELECT ua.User_firstname, ua.User_lastname \
                           FROM User_account AS ua \
                           WHERE ua.User_role = 1 \
                           AND ua.User_ID IN ( \
                           SELECT iss.User_ID \
                           FROM Issue AS iss \
                           INNER JOIN Book_category AS bc ON bc.Book_ID = iss.Book_ID \
                           WHERE bc.Book_category= %s AND YEAR(iss.Start_date) = 2023 \
                           GROUP BY ua.User_ID)"

            cursor = db.connection.cursor()
            cursor.execute(temp_query, (query2_category,))
            results = cursor.fetchall()

            formatted_results = []
            for result in results:
                formatted_result = result[0]  # Assuming the result is a single value
                formatted_results.append(formatted_result)
            results = formatted_results

            cursor.execute(temp_query2, (query2_category,))
            additional_results = cursor.fetchall()

            formatted_additional_results = []
            for additional_result in additional_results:
                firstname, lastname = additional_result
                formatted_additional_result = f"Firstname: {firstname}, Lastname: {lastname}"
                formatted_additional_results.append(formatted_additional_result)
            results.extend(formatted_additional_results)

        if query and query == 'query3':
            temp_query = "SELECT ua.User_firstname, ua.User_lastname, COUNT(*) AS num_issues \
                          FROM Issue AS iss \
                          INNER JOIN User_account AS ua ON iss.User_ID = ua.User_ID \
                          WHERE ua.User_role = 1 AND ua.User_age < 40 \
                          GROUP BY ua.User_ID \
                          ORDER BY num_issues DESC \
                          LIMIT 5;"
            cursor = db.connection.cursor()
            cursor.execute(temp_query)
            results = cursor.fetchall()

            formatted_results = []
            for result in results:
                firstname, lastname, num_issues = result
                formatted_result = f"Firstname: {firstname}, Lastname: {lastname}, Num Issues: {num_issues}"
                formatted_results.append(formatted_result)
            results = formatted_results

        if query and query == 'query4':
            temp_query = "SELECT ba.Book_author_name \
                          FROM Book_author AS ba \
                          WHERE ba.Book_ID NOT IN ( \
                          SELECT iss.Book_ID \
                          FROM Issue AS iss) \
                          GROUP BY ba.Book_author_name"
            cursor = db.connection.cursor()
            cursor.execute(temp_query)
            results = cursor.fetchall()

            formatted_results = []
            for result in results:
                formatted_result = result[0]  # Assuming the result is a single value
                formatted_results.append(formatted_result)
            results = formatted_results

        if query and query == 'query5':
            temp_query = "SELECT ua.User_firstname, ua.User_lastname \
                          FROM User_account AS ua \
                          WHERE ua.User_ID = ( \
                              SELECT op.User_ID \
                              FROM Operator AS op \
                              INNER JOIN Issue AS iss ON op.School_ID = iss.School_ID \
                              GROUP BY op.User_ID, YEAR(iss.Start_date) \
                              HAVING COUNT(iss.Issue_ID) > 20)"
            cursor = db.connection.cursor()
            cursor.execute(temp_query)
            results = cursor.fetchall()

            formatted_results = []
            for result in results:
                firstname, lastname = result
                formatted_result = f"Firstname: {firstname}, Lastname: {lastname}"
                formatted_results.append(formatted_result)
            results = formatted_results

        if query and query == 'query6':
            temp_query = "SELECT DISTINCT \
                            LEAST(bc1.Book_category, bc2.Book_category) AS category1, \
                            GREATEST(bc1.Book_category, bc2.Book_category) AS category2, \
                            COUNT(*) AS num_borrowings \
                          FROM Book_records AS br \
                          JOIN Book_category AS bc1 ON br.Book_ID = bc1.Book_ID \
                          JOIN Book_category AS bc2 ON br.Book_ID = bc2.Book_ID AND bc1.Book_category <> bc2.Book_category \
                          GROUP BY category1, category2 \
                          ORDER BY num_borrowings DESC \
                          LIMIT 3;"
            cursor = db.connection.cursor()
            cursor.execute(temp_query)
            results = cursor.fetchall()

            formatted_results = []
            for result in results:
                category1, category2, num_borrowings = result
                formatted_result = f"Category 1: {category1}, Category 2: {category2}, Num Borrowings: {num_borrowings}"
                formatted_results.append(formatted_result)
            results = formatted_results

        if query and query == 'query7':
            temp_query = "SELECT ba2.Book_author_name AS authors \
                          FROM Book_author AS ba2 \
                          GROUP BY ba2.Book_author_name \
                          HAVING COUNT(*) + 5 < \
                            (SELECT MAX(book_counts) \
                            FROM ( \
                              SELECT COUNT(*) AS book_counts \
                              FROM Book_author AS ba \
                              GROUP BY ba.Book_author_name \
                            ) AS subquery );"

            cursor = db.connection.cursor()
            cursor.execute(temp_query)
            results = cursor.fetchall()

            formatted_results = []
            for result in results:
                formatted_result = result[0]  # Assuming the result is a single value
                formatted_results.append(formatted_result)
            results = formatted_results

    return render_template("success_admin.html", form=form, results=results)
