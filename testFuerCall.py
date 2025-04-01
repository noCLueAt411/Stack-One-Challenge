import asyncio
import websockets

async def send_audio():
    async with websockets.connect("ws://localhost:8086/audio/send") as websocket:
        with open("audio.wav", "rb") as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                await websocket.send(data)
                await asyncio.sleep(0.01)

asyncio.run(send_audio())
