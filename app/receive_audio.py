from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/audio/receive")
async def websocket_audio_receive(websocket: WebSocket):
    await websocket.accept()
    try:
        with open("received_audio.wav", "wb") as f:
            while True:
                data = await websocket.receive_bytes()
                f.write(data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8087)