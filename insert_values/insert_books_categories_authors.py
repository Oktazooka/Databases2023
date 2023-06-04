import pymysql
import random
import requests
import os

def find_jpg_files(directory):
    jpg_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.png'):
                jpg_files.append(os.path.join(root, file))
    return jpg_files

def get_book_details(num_titles):
    book_details = []

    while len(book_details) < num_titles:
        response = requests.get('https://www.googleapis.com/books/v1/volumes?q=python')
        data = response.json()
        items = data['items']

        for item in items:
            volume_info = item['volumeInfo']
            title = volume_info.get('title', '')
            abstract = volume_info.get('description', '')
            keywords = volume_info.get('keywords', [])
            authors = volume_info.get('authors', [])
            categories = volume_info.get('categories', [])
            pages = volume_info.get('pageCount', 0)
            language = volume_info.get('language', '')
            publisher = volume_info.get('publisher', '')

            book_details.append({
                'title': title,
                'abstract': abstract,
                'keywords': keywords,
                'authors': authors,
                'categories': categories,
                'pages': pages,
                'language': language,
                'publisher': publisher
            })

    return book_details[:num_titles]

def generate_isbn(num_isbn):
    isbn_set = set()  # To store unique ISBN-13 numbers
    while len(isbn_set) < num_isbn:
        digits = [random.randint(0, 9) for _ in range(12)]
        check_sum = sum((digits[i] if i % 2 == 0 else digits[i] * 3) for i in range(12))
        check_digit = (10 - (check_sum % 10)) % 10
        isbn = ''.join(str(digit) for digit in digits) + str(check_digit)
        isbn_set.add(isbn)
    return list(isbn_set)

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
sql_book = "INSERT INTO Book_records (Book_ID, Book_ISBN, Book_title, Book_pages, Book_keywords, Book_abstract, Book_image, Book_language, Book_copies, Book_publisher, School_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# sql_category = "INSERT INTO Book_category (Book_ID,  Book_category) VALUES (%s, %s)"
sql_author = "INSERT INTO Book_author (Book_ID, Book_author_name) VALUES (%s, %s)"
bid = list(range(1, 405))

for j in range(1, 5):
    bisbn = generate_isbn(101)
    book_details = get_book_details(101)
    bkeywords   = [d["keywords"] for d in book_details]
    bauthors    = [d["authors"] for d in book_details]
    bcategories = [d["categories"] for d in book_details]
    btitle = [d["title"] for d in book_details]
    babstract =[d["abstract"] for d in book_details]
    bpages =[d["pages"] for d in book_details]
    blanguage =[d["language"] for d in book_details]
    bpublisher =[d["publisher"] for d in book_details]

    bimage = find_jpg_files('/home/oktazooka/Documents/PythonProjects/Databases2023/images/')
    values_book = []
    sid = j
    bcopies = [random.randint(1, 20) for _ in range(101)]
    print(len(bkeywords), len(bauthors), len(bcategories), len(btitle), len(babstract), len(bpages), len(blanguage), len(bpublisher))
    for i in range(101):

        row_book = [bid[(j-1)*101 + i],bisbn[i],btitle[i],bpages[i],','.join(bkeywords[i]),babstract[i],bimage[i],blanguage[i],bcopies[i],bpublisher[i],sid]
        values_book.append(row_book)
    cursor.executemany(sql_book, values_book)
    for i in range(101):
        print(len(bcategories[i]))
        # for cat in bcategories[i]:
        #     row_category = [bid[(j-1)*101 + i], cat]
        #     cursor.execute(sql_category, row_category)

        for auth in bauthors[i]:
            row_author = [bid[(j-1)*101 + i], auth]
            cursor.execute(sql_author, row_author)
connection.commit()

cursor.close()
connection.close()
