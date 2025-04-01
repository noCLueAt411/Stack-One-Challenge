# SIP Client Docker Proof of Concept

## Beschreibung

Dieser Container:
- Meldet sich bei einem SIP-Server an
- Startet Anrufe per REST API (Port 8085)
- Streamt Audio an den Angerufenen über WebSocket (Port 8086)
- Empfängt Audio über WebSocket (Port 8087)

## Start

1. `.env` mit der folgenden Struktur anlegen:
SIP_SERVER=sip.fonial.de

SIP_USER=DEINE_SIP_NUMMER

SIP_PASSWORD=DEIN_SIP_PASSWORT


2. **Build & Start**
```bash
docker-compose up --build
docker-compose up
```

3. **Call auslösen bzw. testen** 

Eine Datei mit dem Namen audio.wav anlegen im Projekt Ordner

```bash
curl -X POST http://localhost:8085/call -H "Content-Type: application/json" -d '{"number": "1002"}'
```

bzw. testen mit 

```bash
"python3 tests/test_call.py"
```