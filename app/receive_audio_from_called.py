import asyncio
import websockets
import subprocess
import wave
import datetime
import os

WEBSOCKET_PORT = 8086
SAMPLE_RATE = 16000
CHANNELS = 1
SAMPLE_WIDTH = 2

OUTPUT_DIR = "/app/received_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def handler(websocket):
    print(f"Neue WebSocket-Verbindung auf Port {WEBSOCKET_PORT}")

    # Datei vorbereiten
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(OUTPUT_DIR, f"call_audio_{timestamp}.wav")

    with wave.open(output_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(SAMPLE_WIDTH)
        wf.setframerate(SAMPLE_RATE)

        # Starte Aufnahme
        parec = subprocess.Popen(
            ["parec", "-d", "v1.monitor", "--raw", "--format=s16le", "--rate=16000", "--channels=1"],
            stdout=subprocess.PIPE
        )

        try:
            while True:
                data = parec.stdout.read(320)
                if not data:
                    break
                await websocket.send(data)     
                wf.writeframes(data)           
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket-Verbindung geschlossen.")
        finally:
            parec.terminate()
            print(f"Audio-Datei gespeichert: {output_path}")

async def main():
    print(f"Starte WebSocket-Server auf Port {WEBSOCKET_PORT} (Audio-Ausgabe)")
    async with websockets.serve(handler, "0.0.0.0", WEBSOCKET_PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())