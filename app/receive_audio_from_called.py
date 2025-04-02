import asyncio
import websockets
import subprocess


#Takes audio from sink and returns it via websocket

AUDIO_SERVER_URL = "ws://localhost:8086"

async def stream_audio():
    # Audio aufnehmen vom virtuellen Monitor-Device
    parec = subprocess.Popen(
        ["parec", "-d", "v1.monitor", "--raw", "--format=s16le", "--rate=16000", "--channels=1"],
        stdout=subprocess.PIPE
    )
    async with websockets.connect(AUDIO_SERVER_URL) as websocket:
        while True:
            data = parec.stdout.read(320)  # 20ms bei 16kHz, 16bit mono
            if not data:
                break
            await websocket.send(data)

asyncio.run(stream_audio())