import os
import time
import whisper
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import json
import warnings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

class TranscriptionHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        # Supported media formats
        self.supported_formats = {
            '.mp3', '.wav', '.mp4', '.mkv', 
            '.mov', '.flv', '.aac', '.m4a'
        }
        # Load Whisper model
        self.model = whisper.load_model("base")
        # Track processed files
        self.processed_files = self.load_processed_files()

    def load_processed_files(self):
        """Load list of previously processed files"""
        try:
            with open('processed_files.json', 'r') as f:
                return set(json.load(f))
        except FileNotFoundError:
            return set()

    def save_processed_files(self):
        """Save list of processed files"""
        with open('processed_files.json', 'w') as f:
            json.dump(list(self.processed_files), f)

    def is_media_file(self, path):
        """Check if file is a supported media format"""
        return Path(path).suffix.lower() in self.supported_formats

    def transcribe_file(self, file_path):
        """Transcribe a media file"""
        try:
            # Skip if already processed
            if file_path in self.processed_files:
                logging.info(f"Skipping already processed file: {file_path}")
                return

            logging.info(f"Transcribing: {file_path}")
            result = self.model.transcribe(file_path)
            output_path = Path(file_path).with_suffix('.txt')
            
            # Save transcription
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result["text"])
            
            # Mark as processed
            self.processed_files.add(file_path)
            self.save_processed_files()
            
            logging.info(f"Transcription completed: {output_path}")
            
        except Exception as e:
            logging.error(f"Error transcribing {file_path}: {str(e)}")

    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return
        
        if self.is_media_file(event.src_path):
            self.transcribe_file(event.src_path)

    def process_existing_files(self, directory):
        """Process existing files in directory"""
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if self.is_media_file(file_path):
                    self.transcribe_file(file_path)

def main():
    watch_directory = input("Enter directory path to monitor: ").strip()
    
    if not os.path.exists(watch_directory):
        logging.error("Directory does not exist!")
        return

    
    event_handler = TranscriptionHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_directory, recursive=True)
    
    logging.info("Processing existing files...")
    event_handler.process_existing_files(watch_directory)
    
    # Start monitoring
    logging.info(f"Starting to monitor directory: {watch_directory}")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Monitoring stopped")
    
    observer.join()

if __name__ == "__main__":
    main()