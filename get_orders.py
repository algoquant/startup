# Retrieve the open trade orders, using the Alpaca SDK.
# https://alpaca.markets/sdks/python/trading.html

import pandas as pd
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderSide, QueryOrderStatus
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv("/Users/jerzy/Develop/Python/.env")
# Trade keys
TRADE_KEY = os.getenv("TRADE_KEY")
TRADE_SECRET = os.getenv("TRADE_SECRET")

# Create the SDK trading client
trading_client = TradingClient(TRADE_KEY, TRADE_SECRET)

# Get all open orders
orders = trading_client.get_orders(filter=GetOrdersRequest(status=QueryOrderStatus.OPEN))
# Get all closed orders
# orders = trading_client.get_orders(filter=GetOrdersRequest(status=QueryOrderStatus.CLOSED))
# Get all buy orders for SPY and AAPL
# request_params = GetOrdersRequest(
#                     status=QueryOrderStatus.ALL,
#                     side=OrderSide.BUY,
#                     symbols=["SPY", "AAPL"],
#                  )
# orders = trading_client.get_orders(filter=request_params)

# Print the IDs and the client IDs of the orders
for order in orders:
    print("Order ID: " + str(order.id))
    print("Client order ID: " + order.client_order_id)


# Convert orders to data frame
orders_frame = pd.DataFrame([order.model_dump() for order in orders])
orders_frame.shape

# Save orders data frame to CSV file
time_ny = datetime.now(ZoneInfo("America/New_York"))
date_today = time_ny.strftime("%Y%m%d")
filename = "/Users/jerzy/Develop/MachineTrader/Internship_Summer_2025/data/orders_" + date_today + ".csv"
orders_frame.to_csv(filename, index=False)
print("Finished getting orders and saved to orders.csv")



''' 

##########
# Alternative way to fetch orders using requests

import requests

headers = {
    "APCA-API-KEY-ID": TRADE_KEY,
    "APCA-API-SECRET-KEY": TRADE_SECRET
}

BASE_URL = "https://paper-api.alpaca.markets"  # Use "https://api.alpaca.markets" for live trading

# Fetch orders
response = requests.get(f"{BASE_URL}/v2/orders?status=all", headers=headers)
print(f"Fetching orders from {BASE_URL}/v2/orders")

if response.status_code == 200:
    orders = response.json()
    
    # Convert to DataFrame
    orders_frame = pd.DataFrame(orders)

    # Display the first few rows
    # print(orders_frame)
    print(orders_frame.head())

    # Optionally save to CSV
    orders_frame.to_csv("/Users/jerzy/Develop/Python/alpaca_orders.csv", index=False)
else:
    print(f"Error: {response.status_code}, {response.text}")

# Save DataFrame to CSV
orders_frame.to_csv("/Users/jerzy/Develop/Python/paper3_orders.csv", index=False)

''' 

