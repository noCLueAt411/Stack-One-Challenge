#!/bin/bash

set -e

echo "Starte D-Bus..."
rm -f /run/dbus/pid
mkdir -p /run/dbus
dbus-daemon --system --fork || true

export XDG_RUNTIME_DIR=/tmp 

echo "Starte Pipewire..."
pipewire &> /dev/null &
wireplumber &> /dev/null &
pipewire-pulse &> /dev/null &

echo "Warte auf Pipewire-Server..."
for i in {1..10}; do
    if pactl info > /dev/null 2>&1; then
        echo "Pipewire-Server läuft."
        break
    fi
    echo "Warte auf PulseAudio..."
    sleep 1
done

echo "Richte virtuelle Audio-Sink ein..."
pactl load-module module-virtual-sink sink_name=v1 || true
pactl set-default-sink v1 || true
pactl set-default-source v1.monitor || true

mkdir -p /etc/baresip
echo "sip:${SIP_USER}@${SIP_SERVER};auth_user=${SIP_USER};auth_pass=${SIP_PASSWORD}" > /etc/baresip/accounts

echo "Starte baresip..."
baresip -f /etc/baresip &

echo "Starte REST API & WebSockets..."
uvicorn api:app --host 0.0.0.0 --port 8085 &> /dev/null &
python3 send_audio_to_called.py &> /dev/null &
python3 receive_audio_from_called.py &> /dev/null &

echo "Container ist bereit."

wait