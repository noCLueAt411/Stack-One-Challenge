import asyncio
import websockets
import subprocess

# Takes file uploaded via websocket and feeds it to sink

WEBSOCKET_PORT = 8087

async def handler(websocket):
    print(f"Neue WebSocket-Verbindung auf Port {WEBSOCKET_PORT}")
    
    # Audio-Wiedergabe mit paplay in den virtuellen Sink
    paplay = subprocess.Popen(
        ["paplay", "--device=v1", "--raw", "--format=s16le", "--rate=16000", "--channels=1"],
        stdin=subprocess.PIPE
    )
    try:
        async for message in websocket:
            paplay.stdin.write(message)
            await websocket.send(f"Received {len(message)} bytes".encode())  # optional ACK
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket-Verbindung geschlossen.")
    finally:
        paplay.stdin.close()
        paplay.terminate()
        await websocket.close()

async def main():
    print(f"Starte WebSocket-Server auf Port {WEBSOCKET_PORT} (Audio-Eingabe)")
    async with websockets.serve(handler, "0.0.0.0", WEBSOCKET_PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())