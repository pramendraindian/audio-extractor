#!/usr/bin/env bash
set -euo pipefail

# Installs system dependencies required to build and install PyAudio on Debian/Ubuntu
# Run this script with sudo: sudo ./scripts/install_dependencies.sh

apt-get update
apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libsndfile1 \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    pkg-config \
    ca-certificates

# Finally install python requirements
pip install --upgrade pip
pip install -r /content/audio-extractor/requirements.txt
