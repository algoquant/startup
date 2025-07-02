# Get streaming trade updates
# The TradingStream websocket client streams order updates. 
# When an order is submitted, filled, cancelled, etc, you will receive a response on the client.
# Run this script in a terminal to listen for trade updates, 
# and then submit an order in another terminal to see the updates.
# https://alpaca.markets/sdks/python/trading.html

from alpaca.trading.stream import TradingStream
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv("/Users/jerzy/Develop/Python/.env")
# Trade keys
TRADE_KEY = os.getenv("TRADE_KEY")
TRADE_SECRET = os.getenv("TRADE_SECRET")

trading_stream = TradingStream(TRADE_KEY, TRADE_SECRET)

async def update_handler(data):
    # trade updates will arrive in our async handler
    print(data)

# subscribe to trade updates and supply the handler as a parameter
trading_stream.subscribe_trade_updates(update_handler)

# start our websocket streaming
trading_stream.run()

