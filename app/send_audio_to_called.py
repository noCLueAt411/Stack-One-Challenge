import asyncio
import websockets
import subprocess

WEBSOCKET_PORT = 8087

async def handler(websocket):
    print(f"Neue WebSocket-Verbindung auf Port {WEBSOCKET_PORT}")
    
    # Starte paplay mit virtuellem Sink
    paplay = subprocess.Popen(
        ["paplay", "--device=v1", "--raw", "--format=s16le", "--rate=16000", "--channels=1"],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    received_bytes = 0

    try:
        async for message in websocket:
            if not message:
                continue
            paplay.stdin.write(message)
            received_bytes += len(message)
            await websocket.send(f"Received {len(message)} bytes".encode())

    except websockets.exceptions.ConnectionClosed:
        print("WebSocket-Verbindung wurde vom Client geschlossen.")

    finally:
        try:
            paplay.stdin.close()
            paplay.wait(timeout=2)
        except Exception as e:
            print(f"paplay konnte nicht sauber beendet werden: {e}")

        # Optional: Fehlerausgabe von paplay anzeigen
        stderr = paplay.stderr.read().decode().strip()
        if stderr:
            print(f"paplay Fehler: {stderr}")

        print(f"Gesamt empfangene Bytes: {received_bytes}")
        print("WebSocket-Verbindung geschlossen.")
        await websocket.close()

async def main():
    print(f"Starte WebSocket-Server auf Port {WEBSOCKET_PORT} (Audio-Eingabe)")
    async with websockets.serve(handler, "0.0.0.0", WEBSOCKET_PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
