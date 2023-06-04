import pymysql
import random
import string

text_list_good = ['Very good book', 'I really enjoyed reading this book.', 'I would definitely recommend this book to everyone.','Really liked the book, everyone should read it.']
text_list_bad = ['Not so interesting..', 'I was bored when reading this book.','Left me unsatisfied...' ,'The plot was average.', "I wouldn't recommend this book"]

connection = pymysql.connect(
    host="localhost",
    port=3306,
    user='root',
    password='peponi123!',
    database='test_db'
)
cursor = connection.cursor()

sql_backup = "INSERT INTO Backup(School_ID, Backup_ID, Filename) VALUES (%s, %s, %s)"
sql_review = "INSERT INTO Review(School_ID, Review_ID, Book_ID, Rating, Review_text)  VALUES (%s, %s, %s, %s, %s)"

backup_values = []
for i in range(1,4):
    filename = 'backup_file.bak'
    backup_values.append([i, i, filename])

cursor.executemany(sql_backup, backup_values)

review_values = []
rid = 1
for j in range(1,5):
    num_reviews = random.randint(1,15)
    sid = j
    for r in range(num_reviews):
        bid = random.randint(101*(j-1) + 1, 101*j)
        rating = random.randint(1,5)
        if rating >= 3:
            txt = random.choice(text_list_good)
        else:
            txt = random.choice(text_list_bad)
        review_values.append([sid, rid, bid, rating, txt])
        rid+=1


cursor.executemany(sql_review, review_values)

connection.commit()

cursor.close()
connection.close()
