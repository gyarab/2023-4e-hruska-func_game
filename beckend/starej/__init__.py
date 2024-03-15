import sqlite3
from manage_data import hash_password

con = sqlite3.connect("users.db")
cur = con.cursor()
#""" #if delete needed

cur.execute("DROP TABLE users;")
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(255) NOT NULL, hashed_password VARCHAR(255) NOT NULL, levels INTEGER, aktivni BOOLEAN DEFAULT TRUE);")

users_data = [
    ('user1', hash_password('password1'), 0),
    ('user2', hash_password('password2'), 0),
    ('user3', hash_password('password3'), 0),
    ('user4', hash_password('password4'), 0),
    ('user5', hash_password('password5'), 0),
    ('user6', hash_password('password6'), 0),
    ('user7', hash_password('password7'), 0),
    ('user8', hash_password('password8'), 0),
    ('user9', hash_password('password9'), 0),
    ('user10', hash_password('password10'), 0)
]

sql_insert_users = "INSERT OR IGNORE INTO users (username, hashed_password, levels) VALUES (?, ?, ?);"

cur.executemany(sql_insert_users, users_data)
#""" #if delete needed

#cur.execute("delete from users") # only for clearing db

con.commit()
con.close()