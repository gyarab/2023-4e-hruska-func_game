import sqlite3
from modely import User
import math, random
from auth import hash_heslo


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

def insert_user_to_db(username: str, password: str):
    cur = con.cursor()
    hashed_potatoes = hash_heslo(password)
    cur.execute("INSERT INTO users (jmeno, hash_heslo) VALUES (?, ?);", (username, hashed_potatoes))
    print("[DB] inserted")
    cur.close()

def generate_circle(): #random circle
    x = random.randint(-3, 3)
    y = random.randint(-3, 3)
    r = 1
    
    return [x, y, r]

def circles_do_not_overlap(circles):
    for i in range(len(circles)):
        for j in range(i+1, len(circles)):
            # Check if the distance between centers is greater than the sum of the radii
            if ((circles[i][0] - circles[j][0])**2 + (circles[i][1] - circles[j][1])**2) < (circles[i][2] + circles[j][2])**2:
                return False
    return True

def generate_three_circles():
    circle1 = [0, 0, 1] #jeden vždy na středu s rand r

    #generuje dokud najde nepřekrývající
    while True:
        circles = [circle1]
        for _ in range(2):
            circle = generate_circle()
            circles.append(circle)
        
        if circles_do_not_overlap(circles):
            return circles
