from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class login_form(FlaskForm):
    username = StringField(label = "Username", validators = [DataRequired(message = "Username is a required field.")])
    password = StringField(label = "Password", validators = [DataRequired(message = "Password is a required field.")])

class my_account(FlaskForm):
    myaccount =  SubmitField('My_account')
    search = SubmitField('Browse books')
    issues = SubmitField('Show issued books')

class choose_book(FlaskForm):
    book_title = StringField('Book Title')
    category = StringField('Category')
    author = StringField('Author')
    submit = SubmitField('Search')

class change_credentials(FlaskForm):
    change_credentials =  SubmitField('Change')

class credentials(FlaskForm):
    firstname = StringField("Firstname", validators=[DataRequired()])
    lastname = StringField("Lastname", validators=[DataRequired()])
    date_of_birth = StringField("Date of birth", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])

class admin_queries(FlaskForm):
    query1 = SubmitField('Query1')
    query1_year = StringField('Year')
    query1_month = StringField('Month')
    query2 = SubmitField('Query2')
    query2_category = StringField('Category')
    query3 = SubmitField('Query3')
    query4 = SubmitField('Query4')
    query5 = SubmitField('Query5')
    query6 = SubmitField('Query6')
    query7 = SubmitField('Query7')

class operator_queries(FlaskForm):
    change_theme = SubmitField('Teacher view')
    view_issues = SubmitField('View issues')
    view_delayed_issues = SubmitField('View delayed issues')
    query1 = SubmitField('Query1')
    query1_title = StringField('Title')
    query1_category = StringField('Category')
    query1_author = StringField('Author')
    query1_copies = StringField('Copies')
    query2 = SubmitField('Query2')
    query2_firstname = StringField('Firstname')
    query2_lastname = StringField('Lastname')
    query2_days_delayed = StringField('Days delayed')
    query3 = SubmitField('Query3')
    query3_category = StringField('Category')
    query3_userid = StringField('User ID')

class reservation(FlaskForm):
    date_reservation = StringField("Start date reservation", validators=[DataRequired()])

class review(FlaskForm):
    rating = IntegerField('Rating')
    comment = TextAreaField('Comment')
    submit = SubmitField('Submit Review')
