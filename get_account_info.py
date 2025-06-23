# Download account information from Alpaca using the Alpaca Trade API.

import pandas as pd
from datetime import datetime, timezone, timedelta
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv("/Users/jerzy/Develop/Python/.env")
# Trade keys
TRADE_KEY = os.getenv("TRADE_KEY")
TRADE_SECRET = os.getenv("TRADE_SECRET")

# Create API object
BASE_URL = "https://paper-api.alpaca.markets"
trade_api = tradeapi.REST(TRADE_KEY, TRADE_SECRET, BASE_URL, api_version="v2")

# Get account information
account = trade_api.get_account()

# Print account info
print("Account ID:", account.id)
print("Status:", account.status)
print("Equity:", account.equity)
print("Buying Power:", account.buying_power)
print("Cash:", account.cash)
print("Portfolio Value:", account.portfolio_value)

# Convert account object to dictionary, then to DataFrame
account_frame = pd.DataFrame([account._raw])
account_frame.shape

# Save account info to CSV
current_time = datetime.now()
file_name = "/Users/jerzy/Develop/MachineTrader/Internship_Summer_2025/data/account_info_" + current_time.strftime("%Y%m%d") + ".csv"
account_frame.to_csv(file_name, index=False)


