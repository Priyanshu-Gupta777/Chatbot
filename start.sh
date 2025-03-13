#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e

echo "Updating package list..."
sudo apt update

echo "Installing system-level dependencies (ffmpeg, portaudio, pip)..."
sudo apt install -y ffmpeg portaudio19-dev python3-pip

echo "Activating virtual environment..."
source .\venv\Scripts\activate  # Assumes your virtual environment is in the 'venv' directory

echo "Installing Python requirements..."
pip install -r requirements.txt

echo "Running the chatbot application..."
python app.py
