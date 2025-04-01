FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    baresip \
    ffmpeg \
    python3 \
    python3-pip \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app/ /app

RUN pip3 install fastapi uvicorn websockets pydantic tqdm

CMD ["sh", "-c", "mkdir -p /etc/baresip && echo \"sip:${SIP_USER}@${SIP_SERVER};auth_user=${SIP_USER};auth_pass=${SIP_PASSWORD}\" > /etc/baresip/accounts && baresip -f /etc/baresip -m & uvicorn api:app --host 0.0.0.0 --port 8085 & python3 send_audio.py & python3 receive_audio.py"]