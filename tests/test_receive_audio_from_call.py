import asyncio
import websockets

async def receive_audio():
    uri = "ws://localhost:8086"
    async with websockets.connect(uri) as websocket:
        with open("received_audio.raw", "wb") as f:
            print("Empfange Audio...")
            try:
                while True:
                    data = await websocket.recv()
                    f.write(data)
                    print(f"Empfangen: {len(data)} Bytes")
            except websockets.exceptions.ConnectionClosed:
                print("Verbindung geschlossen.")

asyncio.run(receive_audio())