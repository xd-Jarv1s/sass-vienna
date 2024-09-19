import json
import requests
from datetime import datetime

# Define your Telegram bot token and chat ID
TOKEN = '7162097876:AAE27cvUGt6tUzuX3NI9VoNnoUsbNYYnBUM'
CHAT_ID = '-1002325845465'

# Function to send a message to Telegram
def send_telegram_message(message):
    print(f"Sending message to Telegram:\n{message}")
    response = requests.post(
        f'https://api.telegram.org/bot{TOKEN}/sendMessage',
        data={'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
    )
    print(f"Telegram response: {response.status_code} - {response.json()}")
    return response.json()

# Function to delete a message from Telegram
def delete_telegram_message(message_id):
    print(f"Deleting message with ID: {message_id}")
    response = requests.post(
        f'https://api.telegram.org/bot{TOKEN}/deleteMessage',
        data={'chat_id': CHAT_ID, 'message_id': message_id}
    )
    return response.json()

# Load the events from the JSON file
try:
    with open('sass_events.json', 'r') as file:
        data = json.load(file)
        print(f"Loaded {len(data)} events from the file sass_events.json.")
except FileNotFoundError:
    print("Error: The file 'sass_events.json' does not exist.")
    data = []

# Process each event and send the message to Telegram
for event in data:
    start_date = event.get('start_date', 'Unknown date')
    event_day = event.get('day', 'Unknown day')
    event_id = event.get('title', 'Unknown title')  # Use title as identifier for simplicity

    print(f"Processing event: {event_id} (date: {start_date}, day: {event_day})")

    # Prepare the message
    start_time = event.get('start_time', 'Unknown start time')
    end_time = event.get('end_time', 'Unknown end time')
    title = event.get('title', 'Unknown title')
    subline = event.get('subline', '')
    lineup = event.get('lineup', 'Unknown lineup')
    link = event.get('link', 'No link available')

    message = (
        f"📅 *Event*: {title}\n"
        f"🗓 *Date*: {event_day}, {start_date}\n"
        f"⏰ *Time*: {start_time} - {end_time}\n"
        f"🎤 *Lineup*: {lineup}\n"
        f"📍 *Location*: SASS Music Club\n"
        f"🔗 {link}"
    )

    if subline:
        message += f"\n🔖 *Subline*: {subline}"

    # Print the message to the console
    print(f"Prepared message for event '{event_id}':\n{message}\n")

    # Send the message to Telegram
    response = send_telegram_message(message)
    if response.get('ok'):
        message_id = response['result']['message_id']
        print(f"Message successfully sent. Message ID: {message_id}")
    else:
        print(f"Error sending message. Response: {response}")

# Function to remove outdated messages (to be implemented based on your requirements)
def remove_outdated_messages():
    # Example: Remove messages older than 1 day
    print("Removing outdated messages...")
    pass  # Implement your own logic here
