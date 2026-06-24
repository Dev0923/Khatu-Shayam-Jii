import asyncio
import websockets

async def test():
    try:
        async with websockets.connect('ws://127.0.0.1:8000/api/v1/alerts/ws', extra_headers={"Origin": "http://localhost:5173"}) as ws:
            print('Connected!')
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test())
