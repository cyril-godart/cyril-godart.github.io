# Multi-Format File Searcher (SAE3.02)

This project is a Client-Server application developed in **Python 3**. 
The server searches for a specific keyword sent by the client across multiple file formats located in the `server/data` directory.

## Supported Formats
The application currently supports searching in:
- Text files (`.txt`)
- HTML files (`.html`) - Treated as text
- PDF files (`.pdf`)
- Excel files (`.xlsx`)

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

1. Clone the repository or download the files.
2. Install the required dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt