import pandas as pd
import numpy as np

class BreakoutStrategy:
    def __init__(self, symbol, mt5_client):
        self.symbol = symbol
        self.mt5_client = mt5_client
        self.max_orders = 10
        self.active_orders = []  # Keep track of orders placed
        self.sma_period = 40

    def calculate_indicators(self, df):
        """
        Calculate technical indicators:
          - 40-period SMA
          - Example: RSI, MACD, Bollinger Bands, etc.
        """
        # Calculate SMA
        df['sma_40'] = df['close'].rolling(window=self.sma_period).mean()

        # Placeholder for additional indicators:
        # df['rsi'] = compute_rsi(df['close'])
        # df['macd'] = compute_macd(df['close'])
        # df['boll_upper'], df['boll_lower'] = compute_bollinger_bands(df['close'])

        return df

    def determine_levels(self, df, timeframe='M5'):
        """
        Determine support and resistance levels:
         - Resistance: Highest high over the last 3 hours (i.e. 36 5-min bars)
         - Support: Lowest low over the last trading day (can vary based on market)
        """
        resistance = df['high'].tail(36).max()  # last 3 hours of data on a M5 chart
        support = df['low'].tail(288).min()       # approx. one trading day (assuming 5min bars over ~24 hrs, adjust as needed)
        return support, resistance

    def generate_signal(self, df):
        """
        Use the following logic:
         1. If the last candle closes above resistance and above the SMA -> BUY signal.
         2. If the last candle closes below support and below the SMA -> SELL signal.
         3. Include conditions for order reversal if needed.
        """
        df = self.calculate_indicators(df)
        support, resistance = self.determine_levels(df)
        last = df.iloc[-1]
        signal = None

        # Buy Condition
        if last['close'] > resistance and last['close'] > last['sma_40']:
            signal = 'BUY'
        # Sell Condition
        elif last['close'] < support and last['close'] < last['sma_40']:
            signal = 'SELL'
        return signal, support, resistance

    def execute_strategy(self, df):
        """
        Check signals and send orders if conditions are met.
        Note: For paper trading, you might simulate the order execution.
        """
        signal, support, resistance = self.generate_signal(df)
        if signal:
            print(f"Signal for {self.symbol}: {signal} (Support: {support}, Resistance: {resistance})")
            # Here you would check if active orders exist,
            # manage risk/reward, and possibly reverse orders.
            # For example, if signal changes from BUY to SELL, close the current position.
            # Also, enforce a max of 10 orders per symbol.
            # Then, call mt5_client.send_order() with appropriate parameters.
        else:
            print("No clear signal.")