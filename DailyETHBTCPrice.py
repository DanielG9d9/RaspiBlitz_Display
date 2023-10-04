import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.ticker import FuncFormatter

# Coinbase Pro API endpoints for daily Bitcoin and Ethereum price data
btc_api_url = 'https://api.pro.coinbase.com/products/BTC-USD/candles'
eth_api_url = 'https://api.pro.coinbase.com/products/ETH-USD/candles'
params = {
    'granularity': 86400,  # 1 day in seconds
    'start': '',           # Will be set to 7 days ago
    'end': '',             # Will be set to now
}

# Function to fetch historical price data
def get_historical_prices(api_url):
    # Calculate the start time (7 days ago from now)
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)

    # Format the timestamps
    params['start'] = start_time.isoformat()
    params['end'] = end_time.isoformat()

    # Fetch historical price data
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = json.loads(response.text)
        timestamps = [datetime.utcfromtimestamp(entry[0]).strftime('%Y-%m-%d') for entry in data]  # Format as YYYY-MM-DD
        prices = [entry[4] for entry in data]
        return timestamps, prices
    else:
        print(f"Error: Unable to fetch historical price data from {api_url}.")
        return None, None

# Function to format Y-axis labels with $ and commas
def format_y_axis(value, _):
    return '${:,.0f}'.format(value)

# Main function to plot historical weekly price movement for Bitcoin and Ethereum
def plot_price_movement(btc_timestamps, btc_prices, eth_timestamps, eth_prices):
    if btc_timestamps is not None and btc_prices is not None and eth_timestamps is not None and eth_prices is not None:
        fig, ax1 = plt.subplots()

        # Create a secondary Y-axis for Ethereum price
        ax2 = ax1.twinx()

        ax1.plot(btc_timestamps, btc_prices, marker='o', label='Bitcoin Price', color='orange')
        ax2.plot(eth_timestamps, eth_prices, marker='o', label='Ethereum Price', color='blue')
        
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Bitcoin Price (USD)', color='orange')
        ax2.set_ylabel('Ethereum Price (USD)', color='blue')
        
        ax1.set_title('Bitcoin and Ethereum Price Movement (Past Week)')
        
        ax1.grid(True)
        
        # Apply the custom Y-axis label formatting to both axes
        ax1.yaxis.set_major_formatter(FuncFormatter(format_y_axis))
        ax2.yaxis.set_major_formatter(FuncFormatter(format_y_axis))
        
        # Combine legends from both axes
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper left')
        
        plt.xticks(rotation=45)
        
        plt.tight_layout()

        # Save the plot as an image file
        plt.savefig('crypto_weekly_price_movement.png')

        # Display the saved plot using a file viewer
        print("Weekly crypto price movement chart saved as 'crypto_weekly_price_movement.png'.")

# Fetch historical price data for Bitcoin and Ethereum and plot it
btc_timestamps, btc_prices = get_historical_prices(btc_api_url)
eth_timestamps, eth_prices = get_historical_prices(eth_api_url)
plot_price_movement(btc_timestamps, btc_prices, eth_timestamps, eth_prices)