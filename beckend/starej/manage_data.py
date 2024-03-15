import hashlib
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, Request
from passlib.context import CryptContext
from models import FormData, TokenData, User
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta
from jose import JWTError, jwt
import sqlite3

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

con = sqlite3.connect("users.db", check_same_thread=False)

ACCESS_TOKEN_EXPIRES_MINUTES = 30
SECRET_KEY = "75017fe6e3bf084e3056c2ddb9d7e6fbd0d66f2cfa8b0502608fa2c9a79d114f"

#//////////////////////////////////////////////////

#//////////////////////////////////////////////////
def increase_level(id: int):
  cur = con.cursor()
  cur.execute("UPDATE users SET levels = levels + 1 WHERE id = %s",(id,))
  return cur.fetchall()[0][0]

def hash_password(password):
    return pwd_context.hash(password)

def authorized(req: Request) -> bool:
    token = get_token(req)
    if token is None:
        return False
    if not user_exists(token["name"]):
        return False
    return True

def get_token(req):
    try:
        token = req.headers["Authorization"].split()[1]
        return jwt.decode(token, SECRET_KEY)
    except:
        return None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_levels(name: str):
    cur = con.cursor()

    sql_select_levels = "SELECT levels FROM users wehre username = ?;"
    cur.execute(sql_select_levels, (name, ))

    item = cur.fetchone()
    data = {"message": "ok", "users": item}
    return data

def get_all():
    cur = con.cursor()

    sql_select_all = "SELECT * FROM users;"
    cur.execute(sql_select_all)

    items = cur.fetchall()
    data = {"message": "ok", "users": []}
    for i in range(len(items)):
        data["users"].append({"id": items[i][0], "username": items[i][1], "hashed_password": items[i][2], "levels": items[i][3], "aktivni": items[i][4]})
    return data

def get_password(name: str) -> str:
    cur = con.cursor()
    sql_get_password = "select hashed_password from users where username = ?"
    cur.execute(sql_get_password,(name,))
    a = cur.fetchall()[0][0]
    print(a, " in get password")
    return a

def get_user(name: str): #gets user from db by name, should return all values as keys : value #FIXME empty == all, specified == true/false
    cur = con.cursor()
    sql_get_user = "select * from users where username = ?"
    cur.execute(sql_get_user,(name,))
    a = cur.fetchall()[0]
    print(a, " in get_user")
    return a

def user_exists(name: str) -> bool:
    cur = con.cursor()
    sql_user_exists = "select username from users where username = ?"
    cur.execute(sql_user_exists, (name,))
    if len(cur.fetchall()) > 0:
        return True
    return False

def authenticate_user(username, password): #gets user, checks if the user exists --> password is correct
    print(get_user(username), "get_user in authenticate_user")

    user = get_user(username)
    print("user in method authenticate user", user)
    if not user:
        print("not user in authenticate_user")
        return False
    if not verify_password(password, get_password(username)): #not hashed password, hashed password
        print("false in verify password")
        return False
    return user

def create_access_token(login_item: FormData, expires_delta: timedelta): #copy dict, gets expire, adds a "exp":expire to data, encodes
    new_dict = {'user': login_item["sub"], 'exp': None}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    new_dict.update({"exp": expire})
    encoded_jwt = jwt.encode(new_dict, SECRET_KEY)

    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)): #parse token, 
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="could not authorized user", headers={"WWW-Authenticate":"Bearer"})
    try: 
        payload = jwt.decode(token, SECRET_KEY)
        print(token, payload, " token, payload")
        username: str = payload.get("user")
        if username is None:
            print("username none in get_curr_user")
            raise credential_exception
    except JWTError:
        print("JWTERROR")
        raise credential_exception
    
    user = get_user(username) #empty if i need it all
    print(user, "user in get curr user")
    if user is None:
        raise credential_exception
    
    print(user, " in get current user")
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    print(current_user, "current user")
    if not current_user[4]:
        raise HTTPException(status_code=400, detail="inactive user")
    print(current_user, " in curr active user")
    return current_user
