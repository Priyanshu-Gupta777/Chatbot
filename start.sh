#!/bin/bash
set -e

echo "Installing system dependencies (ffmpeg, portaudio)..."
apt update && apt install -y ffmpeg portaudio19-dev

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install --no-cache-dir python-dotenv
pip install --no-cache-dir -r requirements.txt

echo "Running the chatbot application..."
python app.py
