import pymysql
import random
import requests
import os


def get_book_details(num_titles):
    book_details = []

    while len(book_details) < num_titles:
        response = requests.get('https://www.googleapis.com/books/v1/volumes?q=python')
        data = response.json()
        items = data['items']

        for item in items:
            volume_info = item['volumeInfo']
            categories = volume_info.get('categories', [])


            book_details.append({'category':categories})

    return book_details[:num_titles]


# Establish a connection to the database
connection = pymysql.connect(
    host="localhost",
    port=3306,
    user='root',
    password='peponi123!',
    database='test_db'
)

cursor = connection.cursor()
#
# table_name = "Book_category"
# delete_query = f"DELETE FROM {table_name}"
# cursor.execute(delete_query)
#
# table_name = "Book_author"
# delete_query = f"DELETE FROM {table_name}"
# cursor.execute(delete_query)
#
# table_name = "Book_records"
# delete_query = f"DELETE FROM {table_name}"
# cursor.execute(delete_query)
#
# connection.commit()
# cursor.close()
# connection.close()
# quit();
# Define the SQL INSERT statement
sql_category = "INSERT INTO Book_category (Book_ID,  Book_category) VALUES (%s, %s)"
bid = list(range(1, 400))
bdet = get_book_details(20)
bcategories = [d["category"] for d in bdet]

for i in range(403):
    cat = random.choice(bcategories)
    bid_chosen = i+1
    row_category = []
    num_cat = random.randint(1,4)
    unique_category = []
    sample_cat = random.sample(bcategories, num_cat)
    for k in sample_cat:
        if not k in unique_category:
            unique_category.append(k)

    for c in unique_category:
        if not(c == []):
            print(c, bid_chosen)
            row_category = [bid_chosen, c]
            cursor.execute(sql_category, row_category)

connection.commit()

cursor.close()
connection.close()
