import sqlite3
from models import FormData, Token
from manage_data import *
from fastapi import FastAPI
import json

app = FastAPI()

con = sqlite3.connect("users.db", check_same_thread=False)


@app.get("/users")
def get_all_users():
  return get_all(con)

@app.post("/registrace")
def create_user(fdata: FormData):
  pass

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"in post /token, formdata: {form_data.username}, {form_data.password}")
    user = authenticate_user(con, form_data.username, form_data.password)
    #print(f"user in /token post: {user}")
    """
    if user: #kinda bad???????????????????? bylo to bez not
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                           detail="incorrect username or password", headers={"WWW-Authenticate":"Bearer"})
    """
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES) 
    access_token = create_access_token(con ,{"sub": form_data.username}, expires_delta=access_token_expires) #data={"sub": form_data.username}
    print(access_token)

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
   return current_user

@app.get("/users/me/levels", response_model=User)
async def read_own_levels(current_user: User = Depends(get_current_active_user)):
   return get_levels(con, current_user)
