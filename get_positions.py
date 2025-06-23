### Get all open positions in Alpaca account using Alpaca API.

import pandas as pd
from datetime import datetime, timezone, timedelta
import pytz
from alpaca.trading.client import TradingClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv("/Users/jerzy/Develop/Python/.env")
# Trade keys
TRADE_KEY = os.getenv("TRADE_KEY")
TRADE_SECRET = os.getenv("TRADE_SECRET")

trading_client = TradingClient(TRADE_KEY, TRADE_SECRET)

        
# Get all open positions
portfolio = trading_client.get_all_positions()
# print(type(portfolio))  # Check if it's a list or object
# print(portfolio)  # Print the portfolio to see its contents
for position in portfolio:
    print(f"Symbol: {position.symbol}, Qty: {position.qty}, Side: {position.side}, Unreal_PnL: {position.unrealized_pl}")
#     # Define the request parameters
# Extract 'qty' as an integer from the first position
#qty = int(portfolio[0]['qty'])

#print(qty)  # Output: -2

# Access the first position's quantity
position = portfolio[0]  # Get the first position
qty = int(position.qty)  # ✅ Use dot notation instead of brackets
# print(qty)  # Output: -2    

if ( qty < 0  ):
    print(f"Your first position is a short position of {qty} shares of {position.symbol}, with an unrealized PnL of: {position.unrealized_pl}")
else:
    print(f"Your first position is a long position of {qty} shares of {position.symbol}, with an unrealized PnL of: {position.unrealized_pl}")

# Convert orders to data frame
position_frame = pd.DataFrame(position)
position_frame.shape
# print(position_frame)

# Get current NY time
ny_timezone = pytz.timezone("America/New_York")
current_time = datetime.now(ny_timezone)
file_name = "/Users/jerzy/Develop/MachineTrader/Internship_Summer_2025/data/positions_" + current_time.strftime("%Y%m%d") + ".csv"
position_frame.to_csv(file_name, index=False)
print("Finished getting _frame and saved to positions.csv")

