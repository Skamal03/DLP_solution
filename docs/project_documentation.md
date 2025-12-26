# Zer0Leaks - Data Leakage Prevention (DLP) Solution

## 1. How It Works
The system acts as a background security guard for your computer. It continuously watches three main "exit points" where data often leaves an organization:
1.  **File System**: It watches specified folders (including Desktop, Documents, Downloads). If you create or modify a file there, it immediately reads the content.
2.  **Clipboard**: It checks whatever you "Copy" (Ctrl+C).
3.  **External Drives (USB)**: It automatically detects when a USB drive is inserted and begins monitoring it for sensitive files.

Once it captures text, it sends it to the **Detector**, which scans it for sensitive information. If sensitive data is found, it logs a warning in color-coded text and saves it to a log file.

## 2. Features
- **Interactive CLI Menu**: A user-friendly dashboard to add/remove directories, toggle USB scanning, and open logs while the tool runs.
- **Visual Feedback**: 
    - **Startup Banner**: Displays "Zer0Leaks" ASCII art with a clear status summary.
    - **Color-Coded Logs**: 
        - 🔴 **Red**: Monitoring Warnings (Local Files).
        - 🟣 **Purple**: USB/External Drive Warnings.
        - 🟡 **Yellow**: Clipboard Warnings.
        - 🔵 **Blue**: Informational messages.
- **Real-Time Clipboard Monitoring**: Detects sensitive data the moment it enters your clipboard.
- **File System Monitoring**: Watch specific directories (plus default user dirs) for new or modified files.
- **USB Auto-Detection**: Automatically identifies Removable Media and adds it the monitoring list.
- **Hybrid Detection**: Uses both strict rules (Regex) and smart guessing (AI/NLP).
- **Startup Scan**: Scans existing files in watched directories immediately upon start.

## 3. What is NLP (Natural Language Processing)?
**NLP** is a field of Artificial Intelligence that helps computers understand human language.
- **Standard Programming (Regex)**: Looks for exact shapes. E.g., "Find a word with an @ symbol". This is rigid.
- **NLP (Spacy)**: Reads the *context*. It knows that "Apple" in "Apple is a fruit" is different from "Apple" in "Apple Inc. stock price".
    - In this project, we use NLP to detect **Named Entities**. These are proper nouns like Names of People, Organizations, Countries, and Monetary values, which are infinite in variety and impossible to list manually.

## 4. Components & Libraries

### Files
| File | Purpose |
| :--- | :--- |
| `main.py` | The **Manager**. Handles arguments, displays the Interactive Menu, and orchestrates the monitors. |
| `src/monitor.py` | The **Eyes**. Listens for file changes (`watchdog`) and clipboard updates (`pyperclip`). Manages the list of watched paths dynamically. |
| `src/detector.py` | The **Brain**. Decides if text is "sensitive". Holds Regex patterns and loads the Spacy NLP model. |
| `src/logger.py` | The **Scribe**. Custom logging system that applies colors to the console and saves records to `dlp_log.log`. |
| `src/banner.py` | The **Face**. Handles the ASCII art display and screen clearing logic. |
| `src/usb_detector.py` | The **Gatekeeper**. Uses Windows API to find Removable Drives. |

### Libraries
| Library | Role |
| :--- | :--- |
| **`watchdog`** | Efficiently waits for file system events (Create/Modify). |
| **`pyperclip`** | Allows Python to read/write to the system clipboard. |
| **`spacy`** | Industrial-strength NLP library for Named Entity Recognition. |
| **`colorama`** | Cross-platform colored terminal text. |
| **`ctypes`** | (Built-in) Used to interface with Windows Kernel for drive detection. |

## 5. Constraints & Rules (Detection Logic)

### File Constraints
- **Monitored Extensions**: The system ONLY checks text-based files:
    - `.txt`, `.csv`, `.log`, `.md`, `.json`, `.xml`
- **Ignored Directories**: System folders like `.git`, `.vscode`, `__pycache__`, `.venv`, and `src` are ignored to prevent loops and errors.
- **Performance**: Large files are read effectively, but extremely large logs might cause momentary pauses.

### Detection Rules (Triggers)
The system flags data as "Sensitive" if it matches:

**A. Strict Patterns (Regex)**
- **Email**: `anything@anything.anything` (e.g., `user@company.com`)
- **SSN**: US Social Security Format `xxx-xx-xxxx`
- **Credit Card**: Sequences of 13-16 digits.
- **Keywords**: "confidential", "private", "secret", "restricted" (Case insensitive).

**B. Smart Context (NLP)**
- **PERSON**: Names of people (e.g., "John Doe").
- **ORG**: Companies, Agencies (e.g., "Google", "FBI").
- **GPE**: Countries, Cities (e.g., "Paris", "China").
- **MONEY**: Monetary values (e.g., "$500", "1 million dollars").

## 6. How to Run & Use

### Installation
1.  Install Python 3.x.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    ```

### Running
Open a terminal and run:
```bash
python main.py
```

### Command Line Arguments
- `--external`: Enable USB monitoring immediately on startup.
- `--path "C:/Path/To/Folder"`: specific folder to monitor.
- `--no-user-dirs`: Disable default monitoring of Desktop, Documents, and Downloads.

### Interactive Menu Controls
Once running, you can use the menu to:
- **[1] Add Directory**: Type a path to start watching it.
- **[2] Remove Directory**: Stop watching a specific folder.
- **[4] Toggle USB Scanner**: Turn external drive detection ON/OFF.
- **[6] Start/Resume Monitoring**: Go to the active monitoring screen.
- **Ctrl+C**: While monitoring, press Ctrl+C to pause and return to the menu.
