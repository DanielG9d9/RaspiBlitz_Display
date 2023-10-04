import pygame
import requests
import json

# Coinbase API endpoint for Bitcoin price
url = 'https://api.coinbase.com/v2/prices/spot?currency=USD'

# Set up Pygame
pygame.init()
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Bitcoin Price')

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
    bitcoin_price = get_bitcoin_price()

    # Display Bitcoin price on the screen
    font = pygame.font.Font(None, 36)
    text = font.render(f'Bitcoin Price: ${bitcoin_price}', True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(text, (10, 10))
    pygame.display.update()

pygame.quit()
