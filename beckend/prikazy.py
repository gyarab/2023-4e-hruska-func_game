import sqlite3
from modely import User

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
