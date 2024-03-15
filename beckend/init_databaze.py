import sqlite3
from auth import hash_heslo

con = sqlite3.connect("databaze.sqlite")
cursor = con.cursor()

cursor.execute("DROP TABLE users;")
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, jmeno VARCHAR(20), hash_heslo VARCHAR(255), aktivni BOOLEAN DEFAULT TRUE);")

uzivatele = [
    ("user1", hash_heslo("ne")),
]

cursor.executemany("INSERT INTO users (jmeno, hash_heslo) VALUES (?, ?);", uzivatele)

con.commit()
con.close()