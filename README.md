# Trading Project

## Overview
This project implements a trading system that integrates with MetaTrader 5 (MT5) and utilizes reinforcement learning for trade execution. The system is designed to analyze market data, execute trades based on a support and resistance strategy, and continuously improve its trading logic through machine learning.

## Project Structure
```
trading_project
├── src
│   ├── services
│   │   ├── mt5_client.py          # Handles MT5 connection and data retrieval
│   │   └── training_service.py     # Manages interaction with the RL model
│   └── strategies
│       └── support_resistance_strategy.py  # Implements trading logic
├── config
│   └── mt5_config.json            # MT5 connection credentials
├── data
│   └── logs
│       └── trading.log             # Logs trading activities
├── R1-V
│   ├── ... (cloned R1-V repository content)
├── Dockerfile                       # Docker image configuration
├── requirements.txt                 # Python package dependencies
└── README.md                        # Project documentation
```

## Setup Instructions
1. **Clone the Repository**
   Clone the R1-V repository to access the reinforcement learning framework:
   ```
   git clone https://github.com/Deep-Agent/R1-V.git
   ```

2. **Install Dependencies**
   Install the required Python packages using pip:
   ```
   pip install -r requirements.txt
   ```

3. **Configure MT5 Connection**
   Update the `config/mt5_config.json` file with your MT5 account credentials:
   ```json
   {
       "account": "YOUR_ACCOUNT_NUMBER",
       "password": "YOUR_PASSWORD",
       "server": "YOUR_SERVER"
   }
   ```

4. **Run the Application**
   Use the following command to start the trading system:
   ```
   python src/services/training_service.py
   ```

## Trading Strategy
The trading strategy is based on dynamic support and resistance levels on a 5-minute chart. The system identifies key levels and executes trades based on candle closes in relation to these levels and a 40-period Simple Moving Average (SMA). The strategy includes:
- **Resistance Breakout**: Buy when the price breaks above resistance and closes above the SMA.
- **Support Breakdown**: Sell when the price breaks below support and closes below the SMA.
- **Order Management**: Up to 10 simultaneous orders, with conditions for taking profits and managing reversals.

## Logging
All trading activities, including executed trades and errors, are logged in `data/logs/trading.log` for monitoring and analysis.

## Reinforcement Learning Integration
The project leverages the R1-V framework to train a reinforcement learning model that learns from trading experiences and improves decision-making over time.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.