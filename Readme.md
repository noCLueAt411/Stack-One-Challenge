# SIP Client Docker Proof of Concept

## Beschreibung

**Ansatz**

Basiert auf https://github.com/louisoutin/Docker-Virtual-XVFB-pipewire

- SIP-Client (baresip)
  - Meldet sich beim SIP-Server an.
  - Startet ausgehende Anrufe.
  - Nutzt eine virtuelle Audio-Quelle (v1.monitor) als Mikrofon-Eingabe.
  - Gibt empfangenes Audio an eine virtuelle Sink (v1) aus.
- REST API (Port 8085)
  - Bietet eine API zur Steuerung von Anrufen.
  - Über einen POST /call-Request mit Zielnummer im JSON-Body wird ein Anruf initiiert.
- WebSocket-Server für Audio-Eingabe (Port 8087 → send_audio_to_called.py)
  - Empfängt Audiodaten im PCM-Format (Mono, 16kHz, 16bit) über eine WebSocket-Verbindung.
  - Gibt die empfangenen Audio-Bytes mittels paplay in die virtuelle Sink (v1) aus.
  - baresip verwendet die zugehörige Quelle (v1.monitor) als Mikrofon-Eingang.
  - Die über WebSocket gesendeten Audiodaten werden dadurch in den SIP-Call eingespeist.
- WebSocket-Server für Audio-Ausgabe (Port 8086 → receive_audio_from_called.py)
  - Streamt das empfangene Audio des Gesprächspartners.
  - Nutzt parec, um den Audio-Output der virtuellen Sink (v1.monitor) auszulesen.
  - Überträgt den Audiodaten-Stream per WebSocket an den verbundenen Client.
  - Dadurch kann das empfangene Audio gespeichert oder weiterverarbeitet werden.

## Prerequisites

Es müssen Docker, docker-compose und python3 (um die Tests auszuführen) auf dem Rechner installiert sein.

## Start

1. `.env` mit der folgenden Struktur anlegen:

```bash
SIP_SERVER=sip.fonial.de
SIP_USER=DEINE_SIP_NUMMER
SIP_PASSWORD=DEIN_SIP_PASSWORT
```

2. **Build & Start**
```bash
docker-compose up --build
```

3. **Call auslösen bzw. testen** 

```bash
curl -X POST http://localhost:8085/call -H "Content-Type: application/json" -d '{"number": "1002"}'
```

4. **Audio über Websocket senden**

Für 20ms Stille

```bash
cd tests
python3 test_sending_silent_20ms.py
```

Für file mit Audio

```bash
cd tests
python3 test_sending_wav_file.py
```

5. **Audio über Websocket empfangen**

```bash
cd tests
python3 test_receive_audio_from_call.py
```

6. **Call auflegen**
```bash
curl -X POST http://localhost:8085/hangup
```



**Optional: Eigene Audio anlegen**

- Momentane Audio löschen
- Eine .wav Datei in den Test-Ordner einfügen. Die Datei sollte nicht länger als 5 Sekunden sein. 
- Vorsichtshalber .wav Datei in das richtige Format  bringen mit: 
```bash
ffmpeg -i input.wav -ar 16000 -ac 1 -sample_fmt s16 audio.wav
```
- Falls keine Formatierung vorgenommen werden musste einfach die Datei in audio.wav umwandeln