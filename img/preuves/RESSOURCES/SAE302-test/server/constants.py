"""
Configuration constants for the Client-Server application.
"""
import os

# Network Constants
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 52300
BUFFER_SIZE = 1024
ENCODING_FORMAT = "utf-8"
TERMINATION_MSG = "q"

# File System Constants
# Uses relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")