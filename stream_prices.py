# Streaming real-time stock prices (quotes, trades, bars)
# https://wire.insiderfinance.io/alpaca-algorithmic-trading-api-in-python-part-1-getting-started-with-paper-trading-efbff8992836

from alpaca.data.live.stock import StockDataStream
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv("/Users/jerzy/Develop/Python/.env")
# Get API keys from environment
# Data keys
DATA_KEY = os.getenv("DATA_KEY")
DATA_SECRET = os.getenv("DATA_SECRET")

# Data client for historical stock data
data_client = StockDataStream(DATA_KEY, DATA_SECRET)

# Define the trading symbol
symbol = "SPY"

# Define callbacks
async def handle_quote(quote):
    print(f"Quote: {quote}")

async def handle_trade(trade):
    print(f"Trade: {trade}")

async def handle_bar(bar):
    print(f"Bar: {bar}")
    print(f"Symbol: {bar.symbol}, Open: {bar.open}, High: {bar.high}, Low: {bar.low}, Close: {bar.close}, Volume: {bar.volume}, Trade_count: {bar.trade_count}, VWAP: {bar.vwap}")
    
# Subscribe to updates
# data_client.subscribe_quotes(handle_quote, symbol)
# data_client.subscribe_trades(handle_trade, symbol)
data_client.subscribe_bars(handle_bar, symbol)

# Run the stream
data_client.run()

