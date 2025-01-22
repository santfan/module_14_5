import sqlite3

def initiate_db():
    connection = sqlite3.connect('Products.db')


    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    describtion TEXT NOT NULL,
    price INTEGER NOT NULL
    )
    ''')

    # title = ['Спирулина', 'Йохимбе', 'Инозитол', 'Макка']
    # description = ['Superfood', 'YOHIMBE', 'Максиферт', 'перуанская']
    # price = [1200, 1000, 1470, 1300]
    #
    # for i in range(len(title)):
    #     cursor.execute('INSERT INTO Products(title, describtion, price) VALUES (?, ?, ?)',
    #                    (f'{title[i]}', f'{description[i]}', f'{price[i]}'))
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    age INTEGER NOT NULL,
    email TEXT NOT NULL,
    balance UNTEGER NOT NULL
    )
    ''')
    connection.commit()
    connection.close()
initiate_db()

def add_user(username, email, age):
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    number_cat = cursor.execute("SELECT COUNT(*) FROM Users").fetchone()[0] + 1
    cursor.execute(f'''INSERT INTO Users VALUES ('{number_cat}','{username}', '{email}', '{age}','1000')''')

    connection.commit()

def is_included(username):
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    check_user = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
    if check_user is None:
        return False
    connection.commit()
    return True

def get_all_products():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    db = cursor.fetchall()
    return list(db)