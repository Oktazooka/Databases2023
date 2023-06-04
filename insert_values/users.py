import pymysql
import random
import string
from datetime import datetime, timedelta


def generate_date_of_birth(n, start_date, end_date):

    dates = []
    ages = []
    for i in range(n):
        start_date1 = datetime.strptime(str(start_date), "%Y-%m-%d")
        end_date1 = datetime.strptime(str(end_date), "%Y-%m-%d")
        days_range = (end_date1 - start_date1).days
        random_days = random.randint(0, days_range)
        random_date = start_date1 + timedelta(days=random_days)
        random_year = random_date.year
        random_date = random_date.strftime("%Y-%m-%d")
        # random_date = datetime.strptime(random_date,"%Y-%m-%d")
        dates.append(random_date)

        today = datetime.now()
        year = today.year
        age = year - random_year
        ages.append(int(age))

    return dates, ages

def generate_name(n):
    # List of sample first names
    first_names = ['John', 'Emma', 'Michael', 'Sophia', 'William', 'Olivia', 'James', 'Ava', 'Benjamin', 'Isabella', 'Cathrine', 'Maria','Eve','Peter','Joshua']

    # List of sample last names
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Wilson', 'Anderson','Pugh','Mandel']

    firstnames = []
    lastnames = []
    for _ in range(n):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        firstnames.append(first_name)
        lastnames.append(last_name)

    return firstnames, lastnames

def generate_usernames(n):
    adjectives = ['happy', 'brave', 'clever', 'swift', 'calm', 'gentle', 'kind', 'vivid', 'wild', 'daring']
    nouns = ['tiger', 'eagle', 'lion', 'panther', 'dolphin', 'falcon', 'jaguar', 'hawk', 'leopard', 'gazelle']
    numbers = [str(random.randint(10, 99)) for _ in range(n)]  # Generate random 2-digit numbers

    random_usernames = []
    used_usernames = set()
    for i in range(n):
        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        number = numbers[i]

        username = adjective + noun + number

        while username in used_usernames:
            adjective = random.choice(adjectives)
            noun = random.choice(nouns)
            number = random.choice(numbers)
            username = adjective + noun + number

        random_usernames.append(username)
        used_usernames.add(username)

    return random_usernames


def generate_passwords(n):

    passw = []

    for i in range(n):
        length = random.randint(6,30)
        allowed_chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(allowed_chars) for _ in range(length))
        passw.append(password)

    return passw

def generate_phone_number():
    # Generate a random 10-digit number
    number = random.randint(1000000000, 9999999999)
    return number

connection = pymysql.connect(
    host="localhost",
    port=3306,
    user='root',
    password='peponi123!',
    database='test_db'
)
cursor = connection.cursor()

sql_admin = "INSERT INTO Admin(Username, Password) VALUES (%s, %s)"
sql_user = "INSERT INTO User_account(User_ID, User_firstname, User_lastname, Username, Password, User_role, User_date_of_birth, User_age, School_ID, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
sql_authentication_system = "INSERT INTO Authentication_system(Username, Password) VALUES (%s, %s)"
sql_operator = "INSERT INTO Operator(School_ID, User_ID, Username, Password)  VALUES (%s, %s, %s, %s)"
# sql_school_unit = "INSERT INTO School_unit(School_ID, School_name, School_street, School_street_number , School_postal_code, School_operator_firstname, School_operator_lastname, School_headmaster_firstname,School_headmaster_lastname, School_email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s))"
# sql_school_phone = "INSERT INTO School_phone(Shool_ID, School_phone)"
# school_names = ['Evergreen High School', 'East Bridge School', 'Skyline Elementary', 'Frozen Lake Charter School', 'Canyon View Middle School']
# school_streets = ['El Dorado', 'Squaw Creek', 'Tanglewood', 'W. Rockaway', 'Sulphur Springs']
# school_emails = ['evergreensch@gmail.com','eabridge@hotmail.com', 'skyline_elem@gmail.com', 'FLCS@edu.uk', 'Canyon_view@edu.uk']
# school_headmaster_firstname, school_headmaster_lastname = generate_name(4)

c = 1
for j in range(1,5):

    sid = j
    cur = 0
    # Generate user_account credentials for each school
    username = generate_usernames(42)
    password = generate_passwords(42)
    firstname, lastname = generate_name(42)
    start_date = '2006-01-01'
    end_date = '2008-01-01'
    dob_st, age_st = generate_date_of_birth(31, start_date, end_date)
    start_date = '1956-01-01'
    end_date = '1999-01-01'
    dob_te, age_te = generate_date_of_birth(11,  start_date, end_date)

    values_student = []
    values_teacher = []
    values_auth = [[us, pa] for us,pa in zip(username,password)]
    operator_id = random.randint(32,42)
    operator_firstname, operator_lastname = firstname[operator_id-1], lastname[operator_id-1]
    # School_unit
    # school_unit = [sid, school_names[j-1], school_streets[j-1], random.randint(1,1000), random.randint(10000,99999), \
    #                 operator_firstname , operator_lastname, school_headmaster_firstname[j-1], \
    #                 school_headmaster_lastname[j-1],school_emails[j-1]]

    # Operator
    username_operator = generate_usernames(1)
    password_operator = generate_passwords(1)
    # operator = [sid, operator_id, username_operator, password_operator]

    # Students
    for s in range(31):
        role = 0
        row_student = [c, firstname[cur], lastname[cur], username[cur], password[cur],role, dob_st[s], age_st[s], sid, True]
        values_student.append(row_student)
        c += 1
        cur+=1
    # Teachers
    for t in range(11):
        role = 1
        row_teacher = [c, firstname[cur], lastname[cur], username[cur], password[cur],role, dob_te[t], age_te[t], sid, True]
        values_teacher.append(row_teacher)
        c += 1
        cur+=1

    # School Phone
    # phone_num = random.randint(4)
    # for p in range(phone_num):
    #     school_phone_values = [sid, generate_phone_number()]
    #     cursor.execute(sql_school_phone, school_phone_values)

    # Execute sql queries
    # cursor.execute(sql_school_unit, school_unit)
    # cursor.executemany(sql_school_phone, school_phone_values)
    cursor.executemany(sql_authentication_system, values_auth)
    cursor.executemany(sql_user, values_student)
    cursor.executemany(sql_user, values_teacher)
    # cursor.execute(sql_operator, operator)


# Admin
admin_username = generate_usernames(1)
admin_password = generate_passwords(1)
cursor.execute(sql_authentication_system,[admin_username, admin_password])
cursor.execute(sql_admin, [admin_username, admin_password])

connection.commit()

cursor.close()
connection.close()
