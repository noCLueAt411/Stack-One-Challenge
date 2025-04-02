FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    baresip \
    ffmpeg \
    python3 \
    python3-pip \
    dbus-x11 \
    pipewire \
    pipewire-pulse \
    wireplumber \
    alsa-utils \
    psmisc \
    procps \
    pulseaudio-utils \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install fastapi uvicorn websockets pydantic tqdm

WORKDIR /app

COPY app/ /app
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

RUN mkdir -p /run/user/1000 && chmod 700 /run/user/1000

ENTRYPOINT ["/app/entrypoint.sh"]