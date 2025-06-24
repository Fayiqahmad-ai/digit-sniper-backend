import os, asyncio, json
import websockets
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

DERIV_WS = "wss://ws.deriv.com/websockets/v3"

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

clients = set()

async def deriv_tick_loop():
    async with websockets.connect(DERIV_WS) as ws:
        await ws.send(json.dumps({"ticks": "R_100", "subscribe": 1}))
        async for message in ws:
            data = json.loads(message)
            if "tick" in data:
                for client in clients.copy():
                    await client.send_json(data["tick"])

@app.on_event("startup")
async def start_background_loop():
    asyncio.create_task(deriv_tick_loop())

@app.websocket("/stream")
async def stream_ws(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except:
        pass
    finally:
        clients.remove(websocket)
