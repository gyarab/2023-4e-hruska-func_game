import sqlite3
from modely import User
import math, random

con = sqlite3.connect("databaze.sqlite")

def get_user(jmeno: str = "", id: int = -1) -> User:
    cur = con.cursor()
    user_row = None

    if id == -1:
        user_row = cur.execute("SELECT * FROM users WHERE jmeno = ?", [jmeno]).fetchone()
    else:
        user_row = cur.execute("SELECT * FROM users WHERE id = ?", [id]).fetchone()
    
    if user_row is None: 
        return None
    
    cur.close()
    print(*user_row)
    return User(*user_row)

def generate_game_id(groups):
    while True:
        game_id = str(random.randint(0, 999999)).zfill(6)
        if game_id not in groups:
            return game_id

def find_free_lobby(groups):
    for lobby_id in range(1000000):  # IDs from 0 to 999999
        lobby_id_str = str(lobby_id).zfill(6)  # Convert to string with leading zeros
        if lobby_id_str in groups and len(groups[lobby_id_str]) == 1:
            return lobby_id_str
    return None
