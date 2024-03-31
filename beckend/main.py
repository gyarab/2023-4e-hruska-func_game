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
    print(body.username)
    print(body.password)
    prikazy.insert_user_to_db(body.username, body.password)


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
circles = {}

class ConnectionManager:
    def __init__(self):
        print("[WHERE] in init")
        self.group_conns: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        print("[WHERE] in connect")
        print(f"group_conns: {self.group_conns}")
        await websocket.accept()
        self.group_conns.append(websocket)

    def disconnect(self, websocket: WebSocket):
        print("[WHERE] in disconnect")
        print(f"group_conns: {self.group_conns}")
        self.group_conns.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        print("[WHERE] in send_personal_data")
        print(f"group_conns: {self.group_conns}")
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        print("[WHERE] in broadcast")     
        for connection in self.group_conns:
            print(f"group_conns: {self.group_conns}")
            print(message)
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket('/play')
async def handle_websocket(websocket: WebSocket):
    print("in home")
    await websocket.accept()
    game_id: str | None = None

    try:
        while True:
            data = await websocket.receive_text()
            a = json.loads(data)
            message = a["message"] #should be 1
            nickname = a["username"] #some sort of name
            print(f"[RECIEVED] message: {message}, {nickname}")
            print(f"[GROUPS].. {groups}")
            free_lobby_id = prikazy.find_free_lobby(groups)
            print(f"[FREE LOBBY] {free_lobby_id}")

            if free_lobby_id is None and message == '1': #chce hrát(1) a není volné lobby --> generate new gameId
                game_id = prikazy.generate_game_id(groups)
                kruhomir = prikazy.generate_three_circles()
                groups[game_id] = [websocket]
                circles[game_id] = kruhomir
                print(f"[CREATED] New group {game_id} created")
                print(f"[GROUPS] {groups}")
                await websocket.send_json({"message": "new lobby", "data" : game_id, "who first": "you", "nickname": nickname, "circles": kruhomir}) # / (poslat ho do waiting room)


            elif free_lobby_id and message == '1':
                groups[free_lobby_id].append(websocket)
                print(f"[CONN] Player connected to group {free_lobby_id}")   
                await websocket.send_json({"message": "connected", "data": free_lobby_id, "who first": "not you", "nickname": nickname, "circles": circles[free_lobby_id]})
                del circles[free_lobby_id]
            else:
                print("[WHERE] last else")
                await websocket.send_json({"message": "chyba", "data" : "něco se posralo"})
                websocket.close(reason="conn v /graf")

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
    #websocket.close()
    print("groups", groups)

@app.websocket('/graf')
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            datovka = json.loads(data)
            game_id = datovka["gameId"]
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{game_id} left the chat")