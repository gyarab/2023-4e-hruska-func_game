import hashlib
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, Request
from passlib.context import CryptContext
from models import FormData, TokenData, User
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta
from jose import JWTError, jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 30
SECRET_KEY = "75017fe6e3bf084e3056c2ddb9d7e6fbd0d66f2cfa8b0502608fa2c9a79d114f"

def increase_level(connection, id: int):
  cur = connection.cursor()
  cur.execute("UPDATE users SET levels = levels + 1 WHERE id = %s",(id,))
  return cur.fetchall()[0][0]

def hash_password(password):
    return pwd_context.hash(password)

def authorized(connection ,req: Request) -> bool:
    token = get_token(req)
    if token is None:
        return False
    if not user_exists(connection, token["name"]):
        return False
    return True

def get_token(req):
    try:
        token = req.headers["Authorization"].split()[1]
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[
                ALGORITHM,
            ],
        )
    except:
        return None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_levels(connection, name: str):
    cur = connection.cursor()

    sql_select_levels = "SELECT levels FROM users wehre username = ?;"
    cur.execute(sql_select_levels, (name, ))

    item = cur.fetchone()
    data = {"message": "ok", "users": item}
    return data

def get_all(connection):
    cur = connection.cursor()

    sql_select_all = "SELECT * FROM users;"
    cur.execute(sql_select_all)

    items = cur.fetchall()
    data = {"message": "ok", "users": []}
    for i in range(len(items)):
        data["users"].append({"id": items[i][0], "username": items[i][1], "hashed_password": items[i][2]})
    return data

def get_password(connection, name: str) -> str:
    cur = connection.cursor()
    sql_get_password = "select hashed_password from users where username = ?"
    cur.execute(sql_get_password,(name,))
    return cur.fetchall()[0][0]

def get_user(connection, name: str): #gets user from db by name, should return all values as keys : value #FIXME
    cur = connection.cursor()
    sql_get_user = "select hashed_password from users where username = ?"
    cur.execute(sql_get_user,(name,))
    return cur.fetchall()[0][0]

def user_exists(connection, name: str) -> bool:
    cur = connection.cursor()
    sql_user_exists = "select username from users where username = ?"
    cur.execute(sql_user_exists, (name,))
    if len(cur.fetchall()) > 0:
        return True
    return False

def authenticate_user(connection, username, password): #gets user, checks if the user exists --> password is correct
    user = get_user(connection, username)
    print(f"user in method authenticate user: {user}")
    if not user:
        return False
    if get_password(connection, username) == password:
        print("they are metched u moron")
    if not verify_password(password, get_password(connection, username)): #password, hashed password
        return False

    return user

def create_access_token(connection, login_item: FormData, expires_delta: timedelta): #copy dict, gets expire, adds a "exp":expire to data, encodes
    to_encode = get_user(connection, login_item["sub"]) #email, hashed
    new_dict = {'hashed': to_encode, 'exp': None}
    print(f"aaaaaaaaaaaaaaaaaaaaa   {new_dict}")
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    new_dict.update({"exp": expire})
    encoded_jwt = jwt.encode(new_dict, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

async def get_current_user(connection, token: str = Depends(oauth2_scheme)): #parse token, 
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="could not authorized user", headers={"WWW-Authenticate":"Bearer"})
    try: 
        payload = jwt.encode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    
    user = get_user(connection, username=token_data.username)
    if user is None:
        raise credential_exception
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="inactive user")
    
    return current_user
