import pygame
import requests
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from collections import deque
from datetime import datetime, timedelta
import time  # Import the time module

# Coinbase API endpoint for Bitcoin price
current_price_url = 'https://api.coinbase.com/v2/prices/spot?currency=USD'
historical_price_url = 'https://api.coinbase.com/v2/prices/spot?currency=USD&date'

# Set up Pygame
pygame.init()
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Bitcoin Price Chart')

# Initialize empty lists to store price data
timestamps = deque(maxlen=60)  # Keep the last 60 timestamps (1-hour history)
prices = deque(maxlen=60)      # Corresponding Bitcoin prices

# Function to fetch Bitcoin price from Coinbase API
def get_bitcoin_price(url):
    response = requests.get(url)
    data = response.json()
    if 'data' in data and 'amount' in data['data']:
        return float(data['data']['amount'])
    else:
        print("Error: Unable to fetch Bitcoin price.")
        return None

# Set up timing for updates
update_interval = timedelta(minutes=1)  # Update every 1 minute
last_update_time = datetime.now() - update_interval

# Fetch historical price as of 1 hour ago
historical_time = datetime.now() - timedelta(hours=1)
historical_price_url += f'={historical_time.isoformat()}'
historical_price = get_bitcoin_price(historical_price_url)

# If historical price is available, add it to the data
if historical_price is not None:
    timestamps.append(historical_time.strftime('%H:%M'))
    prices.append(historical_price)

# Function to format Y-axis labels with $ symbol
def format_price_ticks(value, _):
    return f'${value:.2f}'

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = datetime.now()
    
    # Check if it's time to update the data
    if current_time - last_update_time >= update_interval:
        # Fetch Bitcoin price and update data
        bitcoin_price = get_bitcoin_price(current_price_url)
        if bitcoin_price is not None:
            timestamps.append(current_time.strftime('%H:%M'))
            prices.append(bitcoin_price)
            last_update_time = current_time

    # Plot Bitcoin price as a line chart
    plt.clf()  # Clear the previous plot
    plt.plot(timestamps, prices, marker='o', label='Price')
    plt.xlabel('Time')
    plt.ylabel('Bitcoin Price')
    plt.title('Bitcoin Price Chart')
    plt.grid(True)
    plt.legend()
    
    # Format the Y-axis labels with $
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_price_ticks))

    # Save the chart as an image and display it using Pygame
    plt.savefig('bitcoin_price_chart.png')
    chart = pygame.image.load('bitcoin_price_chart.png')
    screen.blit(chart, (0, 0))
    pygame.display.update()

    # Wait for 5 seconds before the next update
    time.sleep(5)

pygame.quit()