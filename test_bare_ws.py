from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()

@app.websocket("/ws")
async def test_ws(ws: WebSocket):
    await ws.accept()
    await ws.send_text("Hello")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
