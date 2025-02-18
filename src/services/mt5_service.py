import MetaTrader5 as mt5
import yaml
import os
import pandas as pd
from datetime import datetime

class MT5Client:
    def __init__(self, config_path='config/mt5_config.json'):
        self.config = self._load_config(config_path)
        self.connected = False

    def _load_config(self, config_path):
        import json
        with open(config_path, 'r') as file:
            return json.load(file)

    def connect(self):
        # Use the provided terminal path and credentials
        # terminal_path = self.config.get('terminal_path') # No terminal path in config
        # if terminal_path:
        #     # Set the terminal path (for Windows, you can set it via mt5.initialize)
        #     os.environ["PATH"] += os.pathsep + os.path.dirname(terminal_path)
        login = self.config['account'].get('number')
        password = self.config['account'].get('password')
        server = self.config['account'].get('server')

        # Initialize connection (adjust parameters as needed)
        if not mt5.initialize(login=login, password=password, server=server):
            print("MT5 initialization failed, error code =", mt5.last_error())
            return False
        self.connected = True
        print("Connected to MT5")
        return True

    def disconnect(self):
        mt5.shutdown()
        self.connected = False

    def get_data(self, symbol, timeframe, n=100):
        """
        Retrieve the latest n bars for a given symbol and timeframe.
        For a 5-minute chart, use mt5.TIMEFRAME_M5.
        """
        if not self.connected:
            raise Exception("Not connected to MT5")
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n)
        if rates is None:
            raise Exception("Failed to retrieve rates: " + str(mt5.last_error()))
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    def send_order(self, symbol, order_type, volume, price, slippage=10):
        """
        Executes a trade. For paper trading, you can simulate the trade here.
        """
        if not self.connected:
            raise Exception("Not connected to MT5")
        # For a demo, you might want to simulate instead of sending a real order.
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "slippage": slippage,
            "magic": 123456,  # unique identifier for your EA
            "comment": "paper trade",
            "type_time": mt5.ORDER_TIME_GTC,  # good till canceled
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        print("Order send result:", result)
        return result
