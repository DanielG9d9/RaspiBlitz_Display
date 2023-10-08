import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.ticker as ticker
import datetime
import matplotlib.dates as mdates  # Import the mdates module

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


# Create a new figure and axis
fig, ax1 = plt.subplots()

# Convert timestamps to matplotlib date format using mdates.date2num
timestamps_bitcoin_matplotlib = mdates.date2num(timestamps_bitcoin)
timestamps_ethereum_matplotlib = mdates.date2num(timestamps_ethereum)

# Plot Bitcoin prices as a line chart on the left axis in orange
ax1.plot_date(timestamps_bitcoin_matplotlib, bitcoin_prices, '-o', label='Bitcoin', color='orange')
ax1.set_xlabel('Time (24 Hour Format)')
ax1.set_ylabel('Bitcoin Price (USD)', color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('$%d'))

# Use FuncFormatter to add commas to Y1 axis
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '${:,.0f}'.format(x)))

# Create a secondary axis for Ethereum prices in blue
ax2 = ax1.twinx()
ax2.plot_date(timestamps_ethereum_matplotlib, ethereum_prices, '-o', label='Ethereum', color='blue')
ax2.set_ylabel('Ether Price (USD)', color='black')
ax2.tick_params(axis='y', labelcolor='black')
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('$%d'))

# Use FuncFormatter to add commas to Y2 axis
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '${:,.0f}'.format(x)))

# Combine the legends from both axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines = lines1 + lines2
labels = labels1 + labels2
ax1.legend(lines, labels, loc='upper center')

# Set the title
plt.title('Bitcoin and Ether Prices (Last 24 Hours)')

# Create timestamps every 6 hours
interval = 3  # hours
timestamps_x = []
for i in range(0, len(timestamps_bitcoin), interval):
    timestamps_x.append(timestamps_bitcoin[i])

# Convert timestamps for X-axis to matplotlib date format using mdates.date2num
timestamps_x_matplotlib = mdates.date2num(timestamps_x)

# Set the major locator and formatter for the X-axis
ax1.xaxis.set_major_locator(mticker.FixedLocator(timestamps_x_matplotlib))
ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: mdates.num2date(x).strftime('%H:%M')))

# Rotate x-axis labels for better visibility
plt.xticks(rotation=45)

# Save the plot as an image (e.g., PNG)
plt.tight_layout()
plt.savefig('crypto_prices.png')

# Optionally, you can close the plot to release resources
plt.close()