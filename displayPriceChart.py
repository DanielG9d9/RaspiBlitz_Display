import schedule
import time
import webbrowser

# Function to display the image in a web browser
def display_image():
    # Open the image generated by getPriceChart.py in a web browser
    webbrowser.open('file://C:/dev/repository/RaspiBlitz_Display/crypto_prices.png', new=2)

# Schedule the function to run every 15 minutes
schedule.every(15).minutes.do(display_image)

# Run the schedule loop
while True:
    schedule.run_pending()
    time.sleep(1)  # Sleep for 1 second to avoid high CPU usage