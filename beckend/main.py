from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
import uvicorn
import auth
import asyncio
import prikazy
from modely import LoginARegisterBody
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List

app = FastAPI()

groups: Dict[str, List[WebSocket]] = {}

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

groups = {game_id: [] for game_id in range(1, 10000)}

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()


@app.websocket("/")
async def handle_websocket(websocket: WebSocket):
    await websocket.accept()
    game_id: str | None = None

    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            message = data.strip()
            print(f"Received message: {message}")
            if not game_id and len(message) == 6 and message.isdigit() and message in groups: #má gameId (digit) --> conn to gane
                game_id = message
                groups[game_id].append(websocket)
                print(f"Player connected to group {game_id}")
                await websocket.send_json({"message": "connected", "data": game_id})

            elif not game_id and message == '1': #nemá gameId a chce hrát(1) --> generate new gameId
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
                await websocket.send_json({"message": "chyba", "data" : "něco se posralo"})

    except WebSocketDisconnect:
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



@app.websocket("/graf/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    print("in websocket /graf/hovno")
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")