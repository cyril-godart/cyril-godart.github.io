# Multi-Format Communicating Search Engine (SAE32)

A clean, robust client-server application designed to perform advanced searches across various document formats. This project features a multi-threaded server architecture and includes both a simple Graphical User Interface (GUI) and a Command-Line Interface (CLI).

---

## 🚀 Features

### Core Search Capabilities
- **Multi-Format Support:** 
  - **Plain Text & HTML:** Full-text indexing with line-number reporting.
  - **Excel (XLSX/XLS):** Identifies specific sheets and cell coordinates (e.g., `Sheet1 | A1`).
  - **PDF:** Extracts text and identifies the specific page number of each match.
- **Advanced Logic Engine:** 
  - **Boolean Operators:** Supports `AND` and `OR` logic for refined results.
  - **Regex Search:** Full Regular Expression support for complex pattern matching.
  - **Proximity Search:** Automatically detects terms located within a distance of 50 characters.
- **Filtering:** Restrict searches to specific categories (TXT, HTML, PDF, or XLSX).

### Networking & Interfaces
- **Multi-Threaded Server:** Capable of handling several clients simultaneously using Python's `threading` and `socket` modules.
- **GUI mode:** A simplified Tkinter interface.
- **CLI mode:** A fast interactive terminal interface.

---

## 🛠️ Architecture

The project is organized into four main modules to ensure clarity and PEP-8 compliance:

- **`server.py`**: The central hub that listens for connections and delegates search tasks to independent threads.
- **`search_tool.py`**: The core logic engine responsible for parsing files and executing matching algorithms (Regex, Boolean, etc.).
- **`client_gui.py`**: The frontend application managing the graphical interface.
- **`client_cli.py`**: The frontend application for the terminal.

---

## 📦 Installation

1.  **Clone the repository** to your local machine.
2.  **Install dependencies** via the provided `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
    *Dependencies include: `openpyxl` (Excel) and `pypdf` (PDF).*
3.  **Prepare Documents**: Place the files you wish to search in the `documents/` folder.

---

## 🚦 Usage

### 1. Start the Server
Run the server first to listen for incoming search requests:
```bash
python server.py
```

---

### 2. Connect and Search

#### Graphical Interface (GUI)
Launch the graphical interface in a separate terminal:
```bash
python client_gui.py
```
1. Verify the IP (`127.0.0.1`) and Port (`65432`) match the server configuration.
2. Click **Connect** to establish the socket interaction.
3. Enter your query. You can use simple keywords, ` AND ` or ` OR `, or check **Regex**.
4. Select the extensions you want to scan.
5. Click **Search**.
6. Double-click a result in the list to open the source file automatically.

#### Command-Line Interface (CLI)
Alternatively, you can use the CLI client:
```bash
python client_cli.py
```
1. Follow the interactive prompts to enter your query.
2. Enter the extensions you want to scan separated by spaces (or press Enter for all).
3. The results will be neatly printed to the terminal.

---

## ⚖️ Technical Compliance

| Requirement | Implementation Detail |
| :--- | :--- |
| **Client-Server Interaction** | Full client-to-server communication using JSON payloads. |
| **Simultaneous Clients** | Server uses `threading` to handle handling multiple connections. |
| **Document Categories** | User can toggle specific formats in the clients. |
| **TXT/HTML Management** | Full text parsing with line-by-line reporting (standard library `html.parser`). |
| **Excel (XLSX) Management** | Uses `openpyxl` to find cell coordinates and sheet names. |
| **PDF Management** | Uses `pypdf` to extract text and identify page numbers. |
| **Advanced Search** | Logic implemented to handle multi-word logical operators (`AND`/`OR`) and Regex. |
| **Code Quality** | Written in English, PEP-8 compliant, using docstrings and constants, separated into functions. |