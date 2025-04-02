import asyncio
import websockets
import wave
import os
import datetime

WS_URL = "ws://localhost:8086"
OUTPUT_DIR = "./output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHANNELS = 1
RATE = 16000
SAMPLE_WIDTH = 2  # 16bit = 2 Bytes

async def receive_audio():
    # Dynamischer Dateiname
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(OUTPUT_DIR, f"received_audio_{timestamp}.wav")

    print(f"Verbinde zu {WS_URL} ...")
    audio_frames = []

    async with websockets.connect(WS_URL) as websocket:
        print(f"Verbunden. Empfange Audio ... (STRG+C zum Beenden)")

        try:
            while True:
                data = await websocket.recv()
                if isinstance(data, bytes):
                    audio_frames.append(data)
        except KeyboardInterrupt:
            print("\nEmpfang manuell beendet.")
        except websockets.exceptions.ConnectionClosed:
            print("\nWebSocket-Verbindung wurde geschlossen.")

    # WAV-Datei schreiben
    with wave.open(output_path, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(SAMPLE_WIDTH)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(audio_frames))

    print(f"Audio gespeichert unter: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    try:
        asyncio.run(receive_audio())
    except KeyboardInterrupt:
        print("\nTest manuell abgebrochen")
