import asyncio
import websockets
import wave

async def send_wav():
    uri = "ws://localhost:8087"

    with wave.open("audio.wav", "rb") as wf:
        print(f"WAV-Datei: {wf.getnchannels()} Kanäle, {wf.getframerate()} Hz, {wf.getsampwidth() * 8} Bit")

        if wf.getnchannels() != 1 or wf.getframerate() != 16000 or wf.getsampwidth() != 2:
            print("WAV-Datei muss Mono, 16kHz, 16bit PCM sein")
            return

        async with websockets.connect(uri) as websocket:
            print("Sende Audio...")
            while True:
                chunk = wf.readframes(160)  # 320 Bytes = 20ms bei 16kHz, 16bit
                if not chunk:
                    break
                await websocket.send(chunk)
                ack = await websocket.recv()
                print(f"ACK: {ack.decode()}")

    print("Audio-Streaming abgeschlossen.")

asyncio.run(send_wav())