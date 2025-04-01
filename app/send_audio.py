from fastapi import FastAPI, WebSocket
import asyncio
import os

app = FastAPI()

@app.websocket("/audio/send")
async def websocket_audio_send(websocket: WebSocket):
    await websocket.accept()
    wav_path = "audio.wav"

    try:
        with open(wav_path, "rb") as audio_file:
            while chunk := audio_file.read(4096):
                await websocket.send_bytes(chunk)
                await asyncio.sleep(0.02)

        print("Audio sent")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8086)