Repository with startup Python scripts.
The Python scripts demonstrate how to use the Alpaca API for trading stocks.
The scripts include utility functions for handling streaming real-time stock prices via the websockets, calculating EMA prices, submitting trade orders, processing trade confirmations, and handling exceptions.

+ utils.py  
Utility functions for data processing, calculating EMA prices, submitting trades, and managing orders.

+ stream_ticks_ema.py  
Calculates the volume weighted EMA prices and variance from the streaming real-time tick stock prices from the Alpaca websocket.
Saves the tick prices to a CSV file and plots the EMA prices with Bollinger Bands.

+ stream_ticks2bars.py  
Aggregates the streaming real-time stock price ticks from the Alpaca websocket into 1-second bar prices.
Calculates the volume weighted EMA prices and variance from the streaming real-time tick stock prices.
Saves the bar prices to a CSV file and plots the EMA prices with Bollinger Bands.

+ submit_order.py  
Submits a trade order using the Alpaca SDK, and later submits a request to confirm the order.

+ submit_callback.py  
Submits a trade order using the Alpaca SDK, and waits for a confirmation via the WebSocket.

+ stream_confirmations.py  
Receives streaming trade confirmations for submitted orders via the WebSocket.

+ strat_bollinger_bars_vwap.py  
Strategy trades a single stock using the streaming real-time stock price bars from the Alpaca API.

