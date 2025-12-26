import argparse
import sys
import time
from src.monitor import SystemMonitor
from src.logger import logger

def main():
    parser = argparse.ArgumentParser(description="DLP Solution - Monitor & Detect")
    parser.add_argument("--path", type=str, default=".", help="Directory path to monitor (default: current dir)")
    args = parser.parse_args()

    logger.info("Starting DLP Solution...")
    logger.info(f"Monitoring directory: {args.path}")
    
    monitor = SystemMonitor(watch_path=args.path)

    try:
        # This will start the file system monitor in a thread and then block on the clipboard monitor
        monitor.start_filesystem_monitor()
        monitor.start_clipboard_monitor() # Blocking call loop
    except KeyboardInterrupt:
        logger.info("Stopping...")
        monitor.stop()
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
