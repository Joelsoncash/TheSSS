import time
import MetaTrader5 as mt5
from src.services.mt5_service import MT5Client
from src.strategies.breakout_strategy import BreakoutStrategy
from src.services.rl_trader import RLTrader

def main():
    symbol = "EURUSD"  # Change to your desired symbol
    timeframe = mt5.TIMEFRAME_M5  # 5-minute bars

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
            rl_trader.train()
            # 4. Sleep until the next 5-min bar (or a smaller interval if you need more frequent updates)
            time.sleep(60)  # Check every minute (adjust as needed)
    except KeyboardInterrupt:
        print("Terminating trading session.")
    finally:
        mt5_client.disconnect()

if __name__ == "__main__":
    main()