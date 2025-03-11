#!/bin/bash
apt update && apt install -y ffmpeg portaudio19-dev
pip install -r requirements.txt
python app.py
