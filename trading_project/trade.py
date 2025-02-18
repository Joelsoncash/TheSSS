class Trade:
    def __init__(self, symbol, order_type, volume, price):
        self.symbol = symbol
        self.order_type = order_type
        self.volume = volume
        self.price = price

    def __repr__(self):
        return f"Trade(symbol={self.symbol}, order_type={self.order_type}, volume={self.volume}, price={self.price})"

# Initialize MT5 connection
mt5_client = MT5Client()
if not mt5_client.connect():
    return

# Initialize strategy
strategy = BreakoutStrategy(symbol, mt5_client)

# Initialize RL agent
rl_trader = RLTrader(mt5_client, symbol, timeframe)
rl_trader.initialize_trainer()

try:
    while True:
        # 1. Get the latest data from MT5
        df = mt5_client.get_data(symbol, timeframe, n=300)  # Get enough data for indicator calc
        # 2. Run the strategy to check for signals and execute orders
        strategy.execute_strategy(df)
        # 3. Let the RL agent observe, decide, and (paper) trade