import asyncio
import websockets

async def send_audio():
    uri = "ws://localhost:8087"
    async with websockets.connect(uri) as websocket:
        print("Sende Stille Audio...")
        for _ in range(100):
            await websocket.send(b'\x00' * 320)
            ack = await websocket.recv()
            print(f"ACK: {ack.decode()}")
        print("Audio senden abgeschlossen.")

asyncio.run(send_audio())