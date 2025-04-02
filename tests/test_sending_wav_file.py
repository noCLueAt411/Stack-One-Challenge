import asyncio
import websockets
import wave
import os
import time

AUDIO_WS_URL = "ws://localhost:8087"
WAV_FILE = "audio.wav"  # Pfad zur Audiodatei
CHUNK_SIZE = 320  # 20ms bei 16kHz, 16bit mono

async def send_audio():
    if not os.path.exists(WAV_FILE):
        print(f"WAV-Datei nicht gefunden: {WAV_FILE}")
        return

    with wave.open(WAV_FILE, "rb") as wf:
        channels = wf.getnchannels()
        framerate = wf.getframerate()
        sampwidth = wf.getsampwidth()

        print(f"WAV-Datei: {channels} Kanal(e), {framerate} Hz, {sampwidth * 8} Bit")

        if channels != 1 or framerate != 16000 or sampwidth != 2:
            print("WAV-Datei muss Mono, 16kHz, 16bit PCM sein!")
            return

        print(f"Verbinde zu {AUDIO_WS_URL} ...")
        start_time = time.time()
        total_bytes = 0
        ack_count = 0

        try:
            async with websockets.connect(AUDIO_WS_URL) as websocket:
                print(f"Sende Audio-Stream ...")
                while True:
                    chunk = wf.readframes(160)  # 320 Bytes → 20ms
                    if not chunk:
                        break
                    await websocket.send(chunk)
                    try:
                        ack = await websocket.recv()
                        ack_count += 1
                        print(f"ACK: {ack.decode()}")
                    except websockets.exceptions.ConnectionClosedOK:
                        print("Server hat Verbindung korrekt geschlossen.")
                        break

                await websocket.close()

        except Exception as e:
            print(f"Fehler beim Senden: {e}")

        duration = time.time() - start_time
        print(f"Test abgeschlossen.")
        print(f"Gesendete Bytes: {wf.getnframes() * sampwidth}")
        print(f"Empfangene ACKs: {ack_count}")
        print(f"Dauer: {duration:.2f} Sekunden")

if __name__ == "__main__":
    asyncio.run(send_audio())
