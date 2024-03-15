from fastapi import FastAPI, HTTPException, Request
import auth
import prikazy
from modely import LoginARegisterBody
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

"""
origins = [
    "http://localhost:5173",
]
"""
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/prihlaseni")
async def login(body: LoginARegisterBody):
    user = prikazy.get_user(body.username)
    if user is None:
        raise HTTPException(status_code=400, detail="takovy uzivatel neexistuje")

    if not auth.porovnej_heslo(str.encode(body.password), user.hash_heslo):
        raise HTTPException(status_code=400, detail="spatny heslo")

    return auth.token_respose(user.jmeno)


@app.post("/registrace")
async def register(body: LoginARegisterBody):
    return body


@app.get("/ucet")
async def ucet(req: Request):
    token = req.headers.get("authorization")
    if token is None:
        raise HTTPException(status_code=400, detail="potrebujeme token")

    username = auth.token_decode(token)
    if username == "":
        raise HTTPException(status_code=401, detail="token je starej")

    return prikazy.get_user(username)
