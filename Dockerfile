FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# --- System-Pakete installieren ---
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

# --- Python Dependencies ---
RUN pip3 install fastapi uvicorn websockets pydantic tqdm

# --- Arbeitsverzeichnis ---
WORKDIR /app

# --- Projektdateien kopieren ---
COPY app/ /app
COPY entrypoint.sh /app/entrypoint.sh

# --- Ausführbar machen ---
RUN chmod +x /app/entrypoint.sh

# --- Pipewire Runtime Directory ---
RUN mkdir -p /run/user/1000 && chmod 700 /run/user/1000

# --- Entrypoint ---
ENTRYPOINT ["/app/entrypoint.sh"]