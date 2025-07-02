### Cancel the open trade orders, using the Alpaca SDK.
# https://alpaca.markets/sdks/python/trading.html

import pandas as pd
from datetime import date, datetime
from zoneinfo import ZoneInfo
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus
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
# Get order_id of first open order
# order_id = "31077c7b-67f8-4b25-a38b-0889023b2cb1"
# order_id = orders[0].id
# print("order_id: " + order_id)
# Cancel the order using the order_id
# trade_api.cancel_order(order_id)

# Cancel all open orders
canceled_orders = trading_client.cancel_orders()
# len(canceled_orders)
# Convert the list to a data frame
canceled_orders = pd.DataFrame([order.model_dump() for order in canceled_orders])

# Save canceled orders to CSV file
time_ny = datetime.now(ZoneInfo("America/New_York"))
date_today = time_ny.strftime("%Y%m%d")
filename = "/Users/jerzy/Develop/MachineTrader/Internship_Summer_2025/data/canceled_orders_" + date_today + ".csv"
# Append to CSV (write header only if file does not exist)
canceled_orders.to_csv(filename, mode="a", header=not os.path.exists(filename), index=False)
print("Finished cancelling orders and saved to canceled_orders.csv")


'''
# Old code
# This code to cancel a single order doesn't work: trading_client.cancel_orders(order_id)
# Cancel all open orders in a loop
if (len(orders) > 0):
    # Create empty data frame of cancelled orders
    canceled_orders = pd.DataFrame(columns=["date", "timestamp", "order_id"])
    # Cancel all open orders in a loop
    for order in orders:
        order_id = str(order.id)
        trading_client.cancel_orders(order_id)
        date_now = datetime.now()
        time_stamp = date_now.timestamp()
        canceled_orders.loc[len(canceled_orders)] = [date_now, time_stamp, order_id]
        print(f"Cancelled order {order_id} at {date_now}")
    # Save cancelled orders to CSV file
    # date_today = time.localtime()
    # filename = "/Users/jerzy/Develop/Python/canceled_orders_" + time.strftime("%Y%m%d", date_today) + ".csv"
    date_today = datetime.now()
    date_today = date_today.strftime("%Y%m%d")
    filename = "/Users/jerzy/Develop/MachineTrader/Internship_Summer_2025/data/canceled_orders_" + date_today + ".csv"
    canceled_orders.to_csv(filename, index=False)
    print("Finished cancelling orders and saved to canceled_orders.csv")
else:
    print("No open orders found. Exiting script.")


### Alternative way to cancel an order using requests and the Alpaca endpoint
### Example of how to cancel an order using requests and the Alpaca endpoint
# import requests
# # Get account details
# account = trade_api.get_account()
# # print("account: " + account)
# # Extract the account ID
# account_id = account.id
# # print("account_id: " + account_id)

# url = "https://paper-api.alpaca.markets/v2/orders/" + order_id
# # url = "https://paper-api.alpaca.markets/v2/orders/" + account_id + "/orders/" + order_id
# print("url: " + url)
# response = requests.delete(url)

# # # headers = {"accept": "application/json"}
# # # response = requests.delete(url, headers=headers)

# print(response)
# # print(response.status_code)
# # print(response.text)

'''
