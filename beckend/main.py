from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect, Query
import auth
import prikazy
from modely import LoginARegisterBody
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import json


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

groups = {}

class ConnectionManager:
    def __init__(self):
        print("[WHERE] in init")
        self.group_conns: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        print("[WHERE] in connect")
        await websocket.accept()
        self.group_conns.append(websocket)

    def disconnect(self, websocket: WebSocket):
        print("[WHERE] in disconnect")
        self.group_conns.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        print("[WHERE] in send_personal_data")
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        print("[WHERE] in broadcast")     
        for connection in self.group_conns:
            print(self.group_conns)
            print(message)
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/home")
async def handle_websocket(websocket: WebSocket):
    print("in home")
    await websocket.accept()
    game_id: str | None = None

    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            message = data.strip()
            print(f"Received message: {message}")
            if not game_id and len(message) == 6 and message.isdigit() and message in groups: #má gameId (digit) --> conn to gane
                print("1. if")
                game_id = message
                groups[game_id].append(websocket)
                print(f"Player connected to group {game_id}")
                await websocket.send_json({"message": "connected", "data": game_id})

            elif not game_id and message == '1': #nemá gameId a chce hrát(1) --> generate new gameId
                print("2. if (1. elif)")
                game_id = prikazy.generate_game_id(groups)
                groups[game_id] = [websocket]
                print(f"New group {game_id} created")
                await websocket.send_json({"message": "gameId", "data" : game_id})

            elif game_id and groups.get(game_id): #má gameId, které je zároveň sesh --> posílají si msgs
                print(f"Data received from player in group {game_id}: {message}")
                for player in groups[game_id]:
                    if player != websocket:
                        await player.send_json({"message": "data", "data" : message})

            else:
                print("last else")
                await websocket.send_json({"message": "chyba", "data" : "něco se posralo"})

    except WebSocketDisconnect:
        print("in websocket disconnect")
        if game_id and groups.get(game_id):
            index = groups[game_id].index(websocket)
            if index > -1:
                groups[game_id].pop(index)
                print(f"Player disconnected from group {game_id}")
                for player in groups[game_id]:
                    print("Sent reload")
                    await player.send_text("playersreload\n")
            if len(groups[game_id]) == 0:
                del groups[game_id]
                print(f"Group {game_id} deleted")

@app.websocket('/graf')
async def websocket_endpoint(websocket: WebSocket):
    

    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            datovka = json.loads(data)
            game_id = datovka["gameId"]
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{game_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{game_id} left the chat")