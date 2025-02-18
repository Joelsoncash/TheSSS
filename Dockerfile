# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install MetaTrader5 - Force reinstall and no cache
RUN pip install --no-cache-dir --force-reinstall MetaTrader5==5.0.13

# Copy the rest of the application code
COPY . .

# Set environment variables if necessary (e.g., PYTHONUNBUFFERED)
ENV PYTHONUNBUFFERED=1

# Run the main application
CMD ["python", "src/main.py"]

import sys

class MT5Client:
    def __init__(self, terminal_path=None):
        if terminal_path:
            self.terminal_path = terminal_path
        else:
            # Choose the executable path based on platform
            if sys.platform.startswith('win'):
                # Windows default path
                self.terminal_path = r"C:\Program Files\MetaTrader 5\terminal64.exe"
            else:
                # MacOS – assuming you've installed MT5 via Wine or an app bundle
                self.terminal_path = "/Applications/MetaTrader 5.app/Contents/MacOS/MetaTrader 5"
        self.connected = False

    def initialize_connection(self):
        import MetaTrader5 as mt5
        if not mt5.initialize(self.terminal_path):
            print("Failed to initialize MT5 connection")
            self.connected = False
        else:
            self.connected = True
            print("MT5 connection established")
