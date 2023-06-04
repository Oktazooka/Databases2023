import pymysql
import random
import string
from datetime import datetime, timedelta


def generate_date(start_date, end_date):

    start_date1 = datetime.strptime(str(start_date), "%Y-%m-%d")
    end_date1 = datetime.strptime(str(end_date), "%Y-%m-%d")
    days_range = (end_date1 - start_date1).days
    random_days = random.randint(0, days_range)
    random_date_start = start_date1 + timedelta(days=random_days)
    random_date_end = random_date_start + timedelta(days = 7)
    random_date_start, random_date_end  = random_date_start.strftime("%Y-%m-%d"), random_date_end.strftime("%Y-%m-%d")

    return random_date_start, random_date_end

def generate_delayed_date():
    random_days = random.randint(1, 60)
    return random_days


connection = pymysql.connect(
    host="localhost",
    port=3306,
    user='root',
    password='peponi123!',
    database='test_db'
)
cursor = connection.cursor()

sql_reservation = "INSERT INTO Reservation(Reservation_ID, School_ID, User_ID, Book_ID, Start_date, Due_date, On_hold) VALUES (%s, %s, %s, %s, %s,%s, %s)"
sql_issue = "INSERT INTO Issue(Issue_ID, School_ID, User_ID,Book_ID, Start_date, Due_date) VALUES (%s, %s, %s, %s, %s, %s)"
sql_delayed_issue = "INSERT INTO Delayed_issue(Issue_ID, Days_delayed) VALUES (%s, %s)"

rid = 1
iid = 1
reservation_values = []
issue_values = []
delayed_issue_values = []
for j in range(1,5):
    sid = j
    # Reservations
    for i in range(51):
        uid = random.randint(42*(j-1) + 1, 42*j)
        bid = random.randint(101*(j-1) + 1, 101*j)
        startdate, duedate = generate_date('2021-01-01', '2023-05-31')
        reservation_values.append([rid, sid, uid, bid, startdate, duedate, False])
        rid += 1
    for k in range(41):
        uid = random.randint(42*(j-1) + 1, 42*j)
        bid = random.randint(101*(j-1) + 1, 101*j)
        startdate, duedate = generate_date('2021-01-01', '2023-05-31')
        issue_values.append([iid, sid, uid, bid, startdate, duedate])
        iid += 1

    lst = list(range(42*(j-1) + 1, 41*j))
    indices = random.sample(lst, 10)
    indices_new = list(set(indices))

    for idx in indices_new:
        days_delayed = generate_delayed_date()
        delayed_issue_values.append([issue_values[idx][0],days_delayed])

cursor.executemany(sql_reservation, reservation_values)
cursor.executemany(sql_issue, issue_values)
cursor.executemany(sql_delayed_issue, delayed_issue_values)

connection.commit()

cursor.close()
connection.close()
