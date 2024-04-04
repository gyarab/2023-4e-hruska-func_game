import sqlite3
from auth import hash_heslo

con = sqlite3.connect("databaze.sqlite")
cursor = con.cursor()

cursor.execute("DROP TABLE users;")
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, jmeno VARCHAR(20), hash_heslo VARCHAR(255), number_of_wins INTEGER DEFAULT 0, number_of_games INTEGER DEFAULT 0);")
#users (jmeno, hash_heslo, aktivni, number_of_wins, number_of_games)

uzivatele = [
    ("user1", hash_heslo("nene")),
    ("user2", hash_heslo("nene")),
    ("user3", hash_heslo("nene")),
    ("user4", hash_heslo("nene")),
    ("user5", hash_heslo("nene")),
]

cursor.executemany("INSERT INTO users (jmeno, hash_heslo) VALUES (?, ?);", uzivatele)

con.commit()
con.close()