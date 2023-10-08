import requests
import datetime
import plotly.graph_objs as go
import pandas as pd

# Define the Coinbase Pro API endpoints
base_url = 'https://api.pro.coinbase.com'
bitcoin_product_id = 'BTC-USD'
ethereum_product_id = 'ETH-USD'

# Set the time interval for historical data (24 hours)
end_time = datetime.datetime.now()
start_time = end_time - datetime.timedelta(days=1)

# Convert start and end times to ISO 8601 format
start_iso = start_time.isoformat()
end_iso = end_time.isoformat()

# Define the URL for historical Bitcoin data
bitcoin_url = f'{base_url}/products/{bitcoin_product_id}/candles'
params = {
    'start': start_iso,
    'end': end_iso,
    'granularity': 3600,  # 1-hour intervals
}
response_bitcoin = requests.get(bitcoin_url, params=params)
data_bitcoin = response_bitcoin.json()

# Define the URL for historical Ethereum data
ethereum_url = f'{base_url}/products/{ethereum_product_id}/candles'
response_ethereum = requests.get(ethereum_url, params=params)
data_ethereum = response_ethereum.json()

# Extract timestamps and closing prices
timestamps_bitcoin = [entry[0] for entry in data_bitcoin]
timestamps_ethereum = [entry[0] for entry in data_ethereum]
bitcoin_prices = [entry[4] for entry in data_bitcoin]
ethereum_prices = [entry[4] for entry in data_ethereum]

# Convert timestamps to datetime objects
timestamps_bitcoin = [datetime.datetime.utcfromtimestamp(ts) for ts in timestamps_bitcoin]
timestamps_ethereum = [datetime.datetime.utcfromtimestamp(ts) for ts in timestamps_ethereum]

# Combine timestamps and prices into a DataFrame
bitcoin_data = pd.DataFrame({'timestamp': timestamps_bitcoin, 'open': bitcoin_prices, 'close': bitcoin_prices, 'high': bitcoin_prices, 'low': bitcoin_prices})
bitcoin_data.set_index('timestamp', inplace=True)

# Create a candlestick chart for Bitcoin prices
fig = go.Figure(data=[go.Candlestick(x=bitcoin_data.index,
                open=bitcoin_data['open'],
                high=bitcoin_data['high'],
                low=bitcoin_data['low'],
                close=bitcoin_data['close'])])

# Add Ethereum prices as a line plot
fig.add_trace(go.Scatter(x=timestamps_ethereum, y=ethereum_prices, mode='lines', name='Ethereum', line=dict(color='blue')))

# Customize the layout
fig.update_layout(title='Bitcoin Candlestick Chart (Last 24 Hours)',
                  yaxis_title='Price (USD)')

# Save the plot as an image (e.g., PNG)
fig.write_image('crypto_candlestick.png')

# Optionally, you can display the plot in an interactive window
# fig.show()