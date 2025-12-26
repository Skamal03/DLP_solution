# DLP Solution Documentation

## 1. How It Works
The system acts as a background security guard for your computer. It continuously watches sensitive locations where data often leaves an organization:
1.  **File System**: It watches specific folders (Project, Desktop, Documents, USBs). If you create or modify a file, it reads the content.
2.  **Clipboard**: It checks whatever you "Copy" (Ctrl+C).

Once it captures text, it sends it to the **Detector**, which scans it for sensitive information. If sensitive data is found, it logs a warning.

## 2. Features
- **Real-Time Clipboard Monitoring**: Detects sensitive data the moment it enters your clipboard.
- **File System Monitoring**: Watch specific directories for new or modified files.
- **Auto-Scan Existing Files**: Checks files immediately on startup.
- **Smart User Directory Monitoring**: Can automatically watch Desktop, Documents, and Downloads.
- **External Drive Scanner**: Automatically detects and monitors USB drives when plugged in.
- **Hybrid Detection**: Uses Regex (Patterns) and NLP (AI/Context).
- **Smart Logging**: Deduplicates alerts to prevent log spam and highlights warnings in red.

## 3. Usage Guide

### Basic Usage
Monitor the current directory:
```bash
python main.py
```

### Advanced Monitoring
1.  **User Directories**: To monitor your key work folders (`Desktop`, `Documents`, `Downloads`):
    ```bash
    python main.py --user-dirs
    ```
2.  **External Drives (USB)**: To automatically detect and scan USB sticks when plugged in:
    ```bash
    python main.py --external
    ```
3.  **Combined**: For maximum protection:
    ```bash
    python main.py --user-dirs --external
    ```

## 4. Components & Architecture

### Files
| File | Purpose |
| :--- | :--- |
| `main.py` | The **Manager**. Handles flags (`--user-dirs`, `--external`) and starts the monitors and background polling threads. |
| `src/monitor.py` | The **Eyes**. Manages the `watchdog` observers. It now supports multiple path monitoring and adding paths dynamically (for USBs). |
| `src/detector.py` | The **Brain**. Contains logic for Regex patterns and Spacy NLP model. |
| `src/logger.py` | The **Scribe**. Handles logging with deduplication and red console highlighting. |
| `src/usb_detector.py` | The **scout**. Uses Windows API (`ctypes`) to list drive letters and identify which ones are Removable (USB). |

### Libraries
| Library | Role |
| :--- | :--- |
| **`watchdog`** | Efficiently waits for file system events. |
| **`pyperclip`** | Reads the system clipboard. |
| **`spacy`** | NLP library for Named Entity Recognition (NER). |
| **`colorama`** | Colors the console output (Red warnings). |
| **`ctypes`** | (Built-in) Accesses Windows low-level API for drive detection. |

## 5. Constraints & Rules (Detection Logic)

### File Constraints
- **Monitored Extensions**: `.txt`, `.csv`, `.log`, `.md`, `.json`, `.xml`
- **Ignored**: Source code (`.py`), Project artifacts (`task.md`), log files, and `src` folders.

### Detection Rules (Sample)
- **Strict Patterns**: Emails, SSNs, Credit Cards, Keywords ("Confidential").
- **Smart Context**: Names (PERSON), Companies (ORG), Countries (GPE), Money.

## 6. External Drive Scanner Details
The USB feature works by running a background thread in `main.py`.
1.  Every 5 seconds, it calls `src/usb_detector.py`.
2.  `usb_detector.py` asks Windows for a list of logical drives (A:\ to Z:\).
3.  It checks the `DriveType`. If it is "Removable" (Type 2), it is flagged.
4.  If a **new** removable drive is seen, `monitor.add_path("E:\")` is called.
5.  The system immediately scans existing files on that USB and keeps watching for changes.
