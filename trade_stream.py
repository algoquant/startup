# Strategy to trade a single stock using the streaming real-time stock price bars from the Alpaca API
# The strategy is based on the difference between the stock's closing price and its VWAP.
# If the close price is significantly below the VWAP, it sells the stock.
# If the close price is significantly above the VWAP, it buys the stock.

# This is only to illustrate how to use the streaming real-time data using the Alpaca websocket. 
# This is only for illustration purposes, and not a real trading strategy.

from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import LimitOrderRequest, MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.live.stock import StockDataStream
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

# Data client for historical stock data
data_client = StockDataStream(DATA_KEY, DATA_SECRET)
# Create the SDK trading client
trading_client = TradingClient(TRADE_KEY, TRADE_SECRET)

# Define the trading parameters
symbol = "SPY"
qty = 1  # Number of shares
type = "market"
# type = "limit"
# side = OrderSide.BUY  # Set to BUY or SELL as needed
# Adjustment to the limit price to make it below the ask or above the bid
delta = 0.1
threshold = 0.05  # Threshold for price difference to trigger a trade


# Define callbacks
# async def handle_quote(quote):
#     print(f"Quote: {quote}")

# async def handle_trade(trade):
#     print(f"Trade: {trade}")

async def trade_bars(bar):
    print(f"Bar price: {bar}")
    # print(f"Symbol: {bar.symbol}, Open: {bar.open}, High: {bar.high}, Low: {bar.low}, Close: {bar.close}, Volume: {bar.volume}, Trade_count: {bar.trade_count}, VWAP: {bar.vwap}")
    close = bar.close
    vwap = bar.vwap
    timestamp = bar.timestamp.astimezone(ZoneInfo("America/New_York"))
    date_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Time: {date_time}, Symbol: {bar.symbol}, Close: {close}, VWAP: {vwap}")
    if close < (vwap - threshold):
        side = OrderSide.SELL
        # Define the order parameters based on the order type
        if type == "market":
            # Submit market order
            print(f"Submitting a {type} {side} order for {qty} shares of {symbol}")
            order_params = MarketOrderRequest(
                symbol = symbol,
                qty = qty,
                side = side,
                type = type,
                time_in_force = TimeInForce.DAY
            )
        elif type == "limit":
            # Submit a limit order to sell at the current bid price plus a small adjustment
            limit_price = round(close + delta, 2)
            print(f"Submitting a {type} {side} order for {qty} shares of {symbol} at {limit_price}")
            # Submit limit order
            order_params = LimitOrderRequest(
                symbol = symbol,
                qty = qty,
                side = side,
                type = type,
                time_in_force = TimeInForce.DAY,
                limit_price = limit_price
            )
        # Submit the order
        trading_client.submit_order(order_params)
    elif close > (vwap + threshold):
        side = OrderSide.BUY
        # Define the order parameters based on the order type
        if type == "market":
            # Submit market order
            print(f"Submitting a {type} {side} order for {qty} shares of {symbol}")
            order_params = MarketOrderRequest(
                symbol = symbol,
                qty = qty,
                side = side,
                type = type,
                time_in_force = TimeInForce.DAY
            )
        elif type == "limit":
            # Submit a limit order to buy at the current ask price minus a small adjustment
            limit_price = round(close - delta, 2)
            print(f"Submitting a {side} limit order for {qty} shares of {symbol} at {limit_price}")
            # Submit limit order
            order_params = LimitOrderRequest(
                symbol = symbol,
                qty = qty,
                side = side,
                type = type,
                time_in_force = TimeInForce.DAY,
                limit_price = limit_price
            )
        # Submit the order
        trading_client.submit_order(order_params)
    else:
        print(f"No trade executed for {symbol} at {close} - no significant price change from VWAP {vwap}")
    print("Done\n")


# Subscribe to updates
# data_client.subscribe_quotes(handle_quote, symbol)
# data_client.subscribe_trades(handle_trade, symbol)
data_client.subscribe_bars(trade_bars, symbol)

# Run the stream
data_client.run()

