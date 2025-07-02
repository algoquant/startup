### Submit trade orders using the Alpaca SDK.
# https://docs.alpaca.markets/docs/working-with-orders
# https://wire.insiderfinance.io/alpaca-algorithmic-trading-api-in-python-part-1-getting-started-with-paper-trading-efbff8992836
# https://alpaca.markets/sdks/python/trading.html

import time
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockQuotesRequest, StockLatestQuoteRequest, StockBarsRequest
from alpaca.data.enums import DataFeed
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import LimitOrderRequest, MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv("/Users/jerzy/Develop/Python/.env")
# Data keys
DATA_KEY = os.getenv("DATA_KEY")
DATA_SECRET = os.getenv("DATA_SECRET")
# Trade keys
TRADE_KEY = os.getenv("TRADE_KEY")
TRADE_SECRET = os.getenv("TRADE_SECRET")

# Create the SDK trading client
trading_client = TradingClient(TRADE_KEY, TRADE_SECRET)

# Define the trading parameters
symbol = "SPY"
qty = 1  # Example quantity, adjust as needed
# type = "market"
type = "limit"
side = OrderSide.BUY  # Set to BUY or SELL as needed
# side = OrderSide.SELL
# Adjustment to the limit price to make it below the ask or above the bid
delta = 0.5


# Define the order parameters based on the order type
if type == "market":
    # Submit market order
    order_params = MarketOrderRequest(
        symbol = symbol,
        qty = qty,
        side = side,
        type = type,
        time_in_force = TimeInForce.DAY
    ) # end order_params
    print(f"Submitting a {type} {side} order for {qty} shares of {symbol}")
elif type == "limit":
    # Submit limit order
    # Create the SDK data client for live and historical stock data
    data_client = StockHistoricalDataClient(DATA_KEY, DATA_SECRET)
    # Create the request parameters for live stock prices - SIP for comprehensive data, or IEX for free data.
    quote_params = StockLatestQuoteRequest(symbol_or_symbols=symbol, feed=DataFeed.SIP)
    # Get the latest quotes - as a dictionary
    latest_quotes = data_client.get_stock_latest_quote(quote_params)
    # Get the price quote
    price_quotes = latest_quotes[symbol]
    # Get the latest bid/ask prices
    ask_price = price_quotes.ask_price
    bid_price = price_quotes.bid_price
    print(f"Latest quotes for {symbol}: Ask = {price_quotes.ask_price}, Bid = {price_quotes.bid_price}")
    if side == OrderSide.BUY:
        # Submit a limit order to buy at the current ask price minus a small adjustment
        limit_price = round(ask_price - delta, 2)
    elif side == OrderSide.SELL:
        # Submit a limit order to sell at the current bid price plus a small adjustment
        limit_price = round(bid_price + delta, 2)
    order_params = LimitOrderRequest(
        symbol = symbol,
        qty = qty,
        side = side,
        type = type,
        limit_price = limit_price,
        extended_hours = True,
        time_in_force = TimeInForce.DAY
    ) # end order_params
    print(f"Submitting a {type} {side} order for {qty} shares of {symbol} at {limit_price}")


### Submit the trade order
# Create filename with date, to save submitted orders to CSV file
time_ny = datetime.now(ZoneInfo("America/New_York"))
date_today = time_ny.strftime("%Y%m%d")
time_ny = time_ny.strftime("%Y-%m-%d %H:%M:%S")
filename = f"/Users/jerzy/Develop/MachineTrader/Internship_Summer_2025/data/submitted_orders_{date_today}.csv"
try:
    response = trading_client.submit_order(order_data=order_params)
    # Remember the order ID for reference
    order_id = response.id
    print(f"Submitted {side} order for {qty} shares of {symbol} with the order-id: {order_id}")
    # Check the order status after waiting for 10 seconds
    print("Waiting 10 seconds for the order to be processed...")
    time.sleep(10)
    order_status = trading_client.get_order_by_id(order_id)
    print(f"Order status: {order_status.status}")
    ### Append the submitted orders to a CSV file
    # After submitting the order and getting the response object
    order_dict = response.model_dump()  # or response._raw for some SDKs
    order_df = pd.DataFrame([order_dict])
    # Append to CSV (write header only if file does not exist)
    order_df.to_csv(filename, mode="a", header=not os.path.exists(filename), index=False)
    print(f"Order appended to {filename}")
except Exception as e:
    # Convert error to string and save to CSV
    error_df = pd.DataFrame([{"timestamp: ": time_ny, "symbol: ": symbol, "side: ": side, "error: ": str(e)}])
    error_df.to_csv(filename, mode="a", header=not os.path.exists(filename), index=False)
    print(f"Trade rejected: {e}")


