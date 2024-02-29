from models import User
from fastapi import FastAPI
import mysql.connector
from mysql.connector import errorcode

app = FastAPI()

try:
  cnx = mysql.connector.connect(
    user="root",
    password="DbJakHajzl5",
    host="127.0.0.1",
    database="users"
)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()

@app.get("/")
def read_root():
    return {"Message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
