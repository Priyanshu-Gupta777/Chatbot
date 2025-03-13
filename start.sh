#!/bin/bash
set -e

echo "Updating package list..."
apt update

echo "Installing dependencies..."
apt install -y ffmpeg portaudio19-dev python3-pip

echo "Installing Python requirements..."
pip install -r requirements.txt

echo "Running the application..."
python app.py
