import argparse
import sys
import os
import time
import threading
from src.monitor import SystemMonitor
from src.logger import logger
from src.usb_detector import get_removable_drives
from src.banner import show_banner
from colorama import Fore, Style

# Global USB Thread Control
usb_thread_running = False

def poll_usb_drives(monitor, interval=5):
    """
    Background thread checking for new USB drives.
    """
    global usb_thread_running
    logger.info("External Drive Scanner started. Waiting for USB...")
    known_drives = set()
    
    current_drives = get_removable_drives()
    for d in current_drives:
        known_drives.add(d)
        monitor.add_path(d)

    while usb_thread_running:
        try:
            current_drives = get_removable_drives()
            for drive in current_drives:
                if drive not in known_drives:
                    logger.info(f"New external drive detected: {drive}")
                    monitor.add_path(drive) 
                    known_drives.add(drive)
            time.sleep(interval)
        except Exception as e:
            logger.error(f"USB Polling Error: {e}")
            time.sleep(interval)

def show_menu(monitor, args, monitor_started=False, clear_screen_on_start=True):
    """Displays the interactive menu and handles user input."""
    global usb_thread_running
    status_message = ""
    
    first_run = True

    while True:
        # Clear screen and show logo each time to create a "static" UI feel
        # UNLESS it is the very first run and we want to preserve previous logs
        if first_run and not clear_screen_on_start:
            # Skip banner on startup to avoid "sandwiching" the logs
            pass
            first_run = False
        else:
            show_banner(clear_screen=True)
        
        # Print Status Message if exists (e.g., "USB Enabled")
        if status_message:
            print(f"{Fore.GREEN} >> {status_message} <<{Style.RESET_ALL}\n")
            status_message = "" # Reset

        print("="*60)    
        print("             Zer0Leaks - INTERACTIVE MENU")
        print("="*60)
        print(" [1] Add Directory to Monitor")
        print(" [2] Remove Directory")
        print(" [3] List Monitored Directories")
        print(f" [4] Toggle USB Scanner (Current: {'ON' if usb_thread_running else 'OFF'})")
        
        print(" [5] Open Log File")
        print("")
        start_resume_text = "Resume Monitoring" if monitor_started else "Start Monitoring"
        print(f" [6] {start_resume_text}")
        print("")
        print(" [0] Exit")
        print("="*60)
        
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            print("\n--- Add Directory ---")
            new_path = input("Enter full path to monitor: ").strip()
            if os.path.exists(new_path):
                monitor.add_path(new_path)
                status_message = f"Path added: {new_path}"
            else:
                status_message = f"Error: Path does not exist: {new_path}"
                
        elif choice == '2':
            print("\n--- Remove Directory ---")
            print("Currently Monitored:")
            for i, p in enumerate(monitor.watch_paths):
                print(f" - {p}")
            path_to_remove = input("Enter path to remove (exact string): ").strip()
            if path_to_remove in monitor.watch_paths:
                monitor.remove_path(path_to_remove)
                status_message = f"Path removed: {path_to_remove}"
            else:
                status_message = "Path not found in list."
            
        elif choice == '3':
            # For listing, we might want to pause to let them read
            print("\n--- Monitored Directories ---")
            for p in monitor.watch_paths:
                print(f" - {p}")
            input("\nPress Enter to return to menu...")
            
        elif choice == '4':
            if usb_thread_running:
                usb_thread_running = False
                status_message = "USB Scanner Disabled."
            else:
                usb_thread_running = True
                u_thread = threading.Thread(target=poll_usb_drives, args=(monitor,), daemon=True)
                u_thread.start()
                status_message = "USB Scanner Enabled."
        
        elif choice == '5':
             log_path = "dlp_log.log"
             if os.path.exists(log_path):
                if os.name == 'nt':
                    os.startfile(log_path)
                else:
                    import subprocess
                    opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
                    subprocess.call([opener, log_path])
                status_message = "Log file opened."
             else:
                status_message = "Log file does not exist yet."

        elif choice == '6':
            os.system('cls' if os.name == 'nt' else 'clear')
            show_banner()
            action = "Resuming" if monitor_started else "Starting"
            print(f"{action}...")
            return # Exit menu loop, go back to main loop
            
        elif choice == '0':
            print("goodbye.")
            monitor.stop()
            usb_thread_running = False
            sys.exit(0)
        else:
            status_message = "Invalid selection."

def main():
    show_banner()
    parser = argparse.ArgumentParser(description="DLP Solution - Monitor & Detect")
    parser.add_argument("--path", type=str, default=".", help="Directory path to monitor (default: current dir)")
    parser.add_argument("--no-user-dirs", action="store_true", help="DISABLE monitoring of User Desktop, Documents, and Downloads")
    parser.add_argument("--external", action="store_true", help="Enable External Drive Scanner (USB)")
    args = parser.parse_args()

    # Collect paths to monitor
    paths_to_watch = []
    if args.path: paths_to_watch.append(args.path)

    # By default, we MONITOR user dirs unless explicitly disabled
    if not args.no_user_dirs:
        home = os.path.expanduser("~")
        user_dirs = [os.path.join(home, "Desktop"), os.path.join(home, "Documents"), os.path.join(home, "Downloads")]
        for d in user_dirs:
            if os.path.exists(d): paths_to_watch.append(d)
                
    paths_to_watch = list(set(paths_to_watch))

    logger.info("Starting DLP Solution...")
    logger.info(f"Monitoring directories")
    
    monitor = SystemMonitor(watch_paths=paths_to_watch)
    logger.info("System Monitors Active...")
    print("")

    # Start USB Poller if requested
    global usb_thread_running
    if args.external:
        usb_thread_running = True
        usb_thread = threading.Thread(target=poll_usb_drives, args=(monitor,), daemon=True)
        usb_thread.start()

    # Main "Run Loop"
    monitor_started = False
    
    # Show menu ONCE before starting
    # We pass clear_screen_on_start=False so the startup logs above remain visible
    show_menu(monitor, args, monitor_started=False, clear_screen_on_start=False)
    monitor_started = True

            # After returning from menu, we loop back to 'try' and restart monitors
            
    while True:
        try:
            logger.info("System Monitors Active...")
            
            # Re-announce status because previous logs were cleared by the menu
            if usb_thread_running:
                 logger.info("External Drive Scanner is Active.")
            
            logger.info(f"Monitoring directories: {monitor.watch_paths}")

            
            monitor.start_filesystem_monitor()
            monitor.start_clipboard_monitor() # Blocking call
        except KeyboardInterrupt:
            # When user presses Ctrl+C, pause and show menu
            monitor.stop_filesystem_monitor() 
            monitor.running = False # Stop clipboard loop
            
            show_menu(monitor, args, monitor_started=True)
            
            # After returning from menu, we loop back to 'try' and restart monitors
            logger.info("Resuming System Monitors...")
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
