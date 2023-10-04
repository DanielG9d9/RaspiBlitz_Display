import pygame
import requests
import json
import matplotlib.pyplot as plt
from collections import deque

# Coinbase API endpoint for Bitcoin price
url = 'https://api.coinbase.com/v2/prices/spot?currency=USD'

# Set up Pygame
pygame.init()
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Bitcoin Price Chart')

# Initialize empty lists to store price data
timestamps = []
prices = []
max_data_points = 50  # Adjust this based on how many data points you want to display

# Function to fetch Bitcoin price from Coinbase API
def get_bitcoin_price():
    response = requests.get(url)
    data = response.json()
    return data['data']['amount']

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fetch Bitcoin price
    bitcoin_price = float(get_bitcoin_price())
    
    # Append data to lists
    timestamps.append(len(timestamps) + 1)
    prices.append(bitcoin_price)
    
    # Trim data to maximum number of data points
    if len(timestamps) > max_data_points:
        timestamps.pop(0)
        prices.pop(0)

    # Plot Bitcoin price as a line chart
    plt.clf()  # Clear the previous plot
    plt.plot(timestamps, prices, marker='o')
    plt.xlabel('Time')
    plt.ylabel('Bitcoin Price (USD)')
    plt.title('Bitcoin Price Chart')
    plt.grid(True)

    # Save the chart as an image and display it using Pygame
    plt.savefig('bitcoin_price_chart.png')
    chart = pygame.image.load('bitcoin_price_chart.png')
    screen.blit(chart, (0, 0))
    pygame.display.update()

pygame.quit()