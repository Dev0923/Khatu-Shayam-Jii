"""
WebSocket-based real-time alert system.

- /api/v1/alerts/ws   — WebSocket endpoint for user clients
- /api/v1/alerts/send — POST endpoint for admin to broadcast a message
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/v1/alerts", tags=["alerts"])


class ConnectionManager:
    """Keeps track of every active WebSocket connection."""

    def __init__(self) -> None:
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket) -> None:
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, message: dict) -> None:
        """Send *message* to every connected client, silently dropping dead sockets."""
        dead: list[WebSocket] = []
        for ws in self.active:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)


manager = ConnectionManager()


# ── WebSocket endpoint (users connect here) ─────────────────────
@router.websocket("/ws")
async def alert_ws(ws: WebSocket):
    print("WS ENDPOINT STARTED")
    try:
        await manager.connect(ws)
        print("WS ACCEPTED")
        while True:
            data = await ws.receive_text()
            print("WS RECEIVED:", data)
    except Exception as e:
        print("WS EXCEPTION:", repr(e))
    finally:
        manager.disconnect(ws)
        print("WS DISCONNECTED")


# ── Broadcast endpoint (admin calls this) ───────────────────────
class AlertPayload(BaseModel):
    message: str
    severity: str = "info"  # info | warning | critical


@router.post("/send")
async def send_alert(payload: AlertPayload):
    """Broadcast an alert to every connected user client."""
    data = {
        "type": "alert",
        "message": payload.message,
        "severity": payload.severity,
        "timestamp": datetime.utcnow().isoformat(),
    }
    await manager.broadcast(data)
    return {
        "status": "sent",
        "recipients": len(manager.active),
        "message": payload.message,
    }
