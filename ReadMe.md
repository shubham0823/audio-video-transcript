# Transcription System

A Python-based transcription system that automatically transcribes media files in a monitored directory using OpenAI's Whisper model.

## Features

- 🎙️ Supports multiple media formats: `.mp3`, `.wav`, `.mp4`, `.mkv`, `.mov`, `.flv`, `.aac`, `.m4a`
- 📂 Monitors a directory for new files and automatically transcribes them
- 📝 Saves transcriptions as `.txt` files with the same name as the source file
- 🔄 Tracks processed files to avoid duplicate transcriptions
- 🖥️ Works in the background with real-time monitoring

## Requirements

- Python 3.7+
- whisper (OpenAI's Whisper model)
- watchdog (for file system monitoring)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/shubham0823/audio-video-transcript.git
   cd transcription-system
   ```

2. Install dependencies:
   ```bash
   for linux
   
   python3 -m venv venv
   pip install -r requirements.txt
   ```

3. Install Whisper model dependencies:
   ```bash
   pip install git+https://github.com/openai/whisper.git
   ```

## Usage

1. Run the script:
   ```bash
   python transcription_system.py
   ```

2. Enter the directory path you want to monitor when prompted.

3. The system will:
   - Process existing files in the directory
   - Monitor for new files
   - Save transcriptions as `.txt` files

4. To stop monitoring, press `Ctrl+C`


