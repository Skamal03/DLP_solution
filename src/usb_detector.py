import os
import sys
import ctypes
import string

def get_available_drives():
    """Returns a list of available drive letters (e.g. ['C:\\', 'D:\\'])."""
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(f"{letter}:\\")
        bitmask >>= 1
    return drives

def get_removable_drives():
    """Returns a list of drive letters that are removable (USB)."""
    removable_drives = []
    
    # Windows Drive Type Constants
    DRIVE_REMOVABLE = 2
    
    drives = get_available_drives()
    for drive in drives:
        drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive)
        if drive_type == DRIVE_REMOVABLE:
            removable_drives.append(drive)
            
    return removable_drives

if __name__ == "__main__":
    print(f"Available Drives: {get_available_drives()}")
    print(f"Removable Drives (USB): {get_removable_drives()}")
