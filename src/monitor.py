import time
import os
import pyperclip
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .logger import logger
from .detector import PII_Detector

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, detector):
        self.detector = detector

    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def process_file(self, file_path):
        """Reads file content and scans for PII"""
        try:
            # Simple text file check for now
            if not self.should_scan(file_path):
                return
            
            logger.info(f"Scanning file: {file_path}")

            # Brief sleep to ensure file write is complete (prevents empty reads on some editors)
            time.sleep(0.5)

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            matches = self.detector.scan_text(content)
            if matches:
                 logger.log_batch(source=f"file {file_path}", matches=matches)
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")

    def should_scan(self, file_path):
        """Decides if a file should be scanned."""
        filename = os.path.basename(file_path)
        
        # 1. Ignore specific system/project files
        ignored_files = {
            'dlp_log.log', 'requirements.txt', 'task.md', 'implementation_plan.md', 
            'walkthrough.md', 'verify_setup.py', 'monitor.py', 'detector.py', 
            'logger.py', 'main.py'
        }
        if filename in ignored_files:
            return False

        # 2. Ignore specific directories
        # Check if any part of the path is in ignored list
        parts = file_path.split(os.sep)
        ignored_dirs = {'.git', '.vscode', '__pycache__', '.venv', 'env', 'src', '.gemini'}
        if any(p in ignored_dirs for p in parts):
            return False

        # 3. Inclusion Rules (Only scan specific text formats)
        valid_extensions = ('.txt', '.csv', '.log', '.md', '.json', '.xml')
        if not file_path.endswith(valid_extensions):
            return False
            
        return True

class SystemMonitor:
    def __init__(self, watch_path="."):
        self.detector = PII_Detector()
        self.watch_path = watch_path
        self.observer = Observer()
        self.running = False

    def scan_existing_files(self):
        """Scans all existing files in the watch path on startup."""
        logger.info(f"Performing initial scan of: {self.watch_path}")
        event_handler = FileEventHandler(self.detector)
        for root, dirs, files in os.walk(self.watch_path):
            for file in files:
                file_path = os.path.join(root, file)
                event_handler.process_file(file_path)
        logger.info("Initial scan completed.")

    def start_filesystem_monitor(self):
        logger.info(f"File system monitor started on: {os.path.abspath(self.watch_path)}")
        
        event_handler = FileEventHandler(self.detector)
        self.observer.schedule(event_handler, self.watch_path, recursive=True)
        self.observer.start()

    def start_clipboard_monitor(self, interval=1.0):
        logger.info("Clipboard monitor started.")
        
        # Perform initial file scan now that everything is started
        self.scan_existing_files()

        self.running = True
        last_content = ""
        
        try:
            while self.running:
                content = pyperclip.paste()
                if content != last_content:
                    last_content = content
                    if content.strip():
                        # Scan new clipboard content
                        matches = self.detector.scan_text(content)
                        if matches:
                            logger.log_batch(source="Clipboard", matches=matches)
                                
                            # Optional: Clear clipboard if sensitive?
                            # pyperclip.copy("") 
                            
                time.sleep(interval)
        except KeyboardInterrupt:
            self.stop()

    def start_all(self):
        self.start_filesystem_monitor()
        self.start_clipboard_monitor()

    def stop(self):
        self.running = False
        self.observer.stop()
        self.observer.join()
        logger.info("Monitors stopped.")
