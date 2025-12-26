import argparse
import sys
import os
import time
import threading
from src.monitor import SystemMonitor
from src.logger import logger
from src.usb_detector import get_removable_drives
from src.banner import show_banner

def poll_usb_drives(monitor, interval=5):
    """
    Background thread checking for new USB drives.
    """
    logger.info("External Drive Scanner started. Waiting for USB...")
    known_drives = set()
    
    # Initialize with currently connected USBs to avoid re-scanning old ones if possible,
    # or just let add_path handle duplicates (which it does).
    current_drives = get_removable_drives()
    for d in current_drives:
        known_drives.add(d)
        monitor.add_path(d) # Add existing ones immediately

    while True:
        try:
            current_drives = get_removable_drives()
            for drive in current_drives:
                if drive not in known_drives:
                    logger.info(f"New external drive detected: {drive}")
                    monitor.add_path(drive) # Dynamically add to watchdog
                    known_drives.add(drive)
            
            # Simple logic: If a drive is removed, we don't explicitly 'remove' it from watchdog 
            # because watchdog handles lost paths gracefully usually, or we just ignore it.
            # Removing is harder with watchdog.Observer, duplicate check prevents re-adding.
            
            time.sleep(interval)
        except Exception as e:
            logger.error(f"USB Polling Error: {e}")
            time.sleep(interval)

def main():
    show_banner()
    parser = argparse.ArgumentParser(description="DLP Solution - Monitor & Detect")
    parser.add_argument("--path", type=str, default=".", help="Directory path to monitor (default: current dir)")
    parser.add_argument("--user-dirs", action="store_true", help="Monitor User Desktop, Documents, and Downloads")
    parser.add_argument("--external", action="store_true", help="Enable External Drive Scanner (USB)")
    args = parser.parse_args()

    # Collect paths to monitor
    paths_to_watch = []
    
    # Always include the explicitly requested path (default is current dir)
    if args.path:
        paths_to_watch.append(args.path)

    # Add user directories if requested
    if args.user_dirs:
        home = os.path.expanduser("~")
        user_dirs = [
            os.path.join(home, "Desktop"),
            os.path.join(home, "Documents"),
            os.path.join(home, "Downloads")
        ]
        for d in user_dirs:
            if os.path.exists(d):
                paths_to_watch.append(d)
                
    # Remove duplicates
    paths_to_watch = list(set(paths_to_watch))

    logger.info("Starting DLP Solution...")
    logger.info(f"Monitoring directories: {paths_to_watch}")
    
    monitor = SystemMonitor(watch_paths=paths_to_watch)

    # Start USB Poller if requested
    if args.external:
        usb_thread = threading.Thread(target=poll_usb_drives, args=(monitor,), daemon=True)
        usb_thread.start()

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
