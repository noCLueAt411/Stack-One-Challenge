import requests
import asyncio
import websockets
from tqdm import tqdm

async def send_audio():
    uri = "ws://localhost:8086/audio/send"
    async with websockets.connect(uri) as websocket:
        print("Audio sending started")
        with open("audio.wav", "rb") as f:
            while chunk := f.read(4096):
                await websocket.send(chunk)
                await asyncio.sleep(0.02)
        print("Audio sending finished")

async def receive_audio():
    uri = "ws://localhost:8087/audio/receive"
    async with websockets.connect(uri) as websocket:
        with open("received_from_test.wav", "wb") as f:
            print("Receiving audio...")
            for _ in tqdm(range(100)):  # Demo - 100 chunks
                data = await websocket.recv()
                f.write(data)

def test_all():
    # Trigger Call
    print("Triggering SIP call...")
    r = requests.post("http://localhost:8085/call", json={"number": "1002"})
    print(r.json())

    # Send & Receive Audio
    asyncio.run(send_audio())
    asyncio.run(receive_audio())

if __name__ == "__main__":
    test_all()