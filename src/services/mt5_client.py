class MT5Client:
    def __init__(self, terminal_path):
        self.terminal_path = terminal_path
        self.connected = False

    def initialize_connection(self):
        import MetaTrader5 as mt5
        if not mt5.initialize(self.terminal_path):
            print("Failed to initialize MT5 connection")
            self.connected = False
        else:
            self.connected = True
            print("MT5 connection established")

    def get_ohlc_data(self, symbol, timeframe, num_bars):
        if not self.connected:
            print("MT5 client is not connected")
            return None
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)
        return rates

    def get_tick_data(self, symbol):
        if not self.connected:
            print("MT5 client is not connected")
            return None
        tick = mt5.symbol_info_tick(symbol)
        return tick

    def execute_trade(self, symbol, action, volume, price=None):
        if not self.connected:
            print("MT5 client is not connected")
            return None
        order_type = mt5.ORDER_BUY if action == 'buy' else mt5.ORDER_SELL
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price if price else mt5.symbol_info_tick(symbol).ask,
            "sl": 0,
            "tp": 0,
            "deviation": 10,
            "magic": 0,
            "comment": "Trade executed by MT5Client",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        return result

    def close_connection(self):
        import MetaTrader5 as mt5
        mt5.shutdown()
        self.connected = False
        print("MT5 connection closed")