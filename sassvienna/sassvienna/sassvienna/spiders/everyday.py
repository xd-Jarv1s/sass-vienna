import requests
import json
from datetime import datetime

# Define your Telegram bot token and channel ID
TOKEN = '7162097876:AAE27cvUGt6tUzuX3NI9VoNnoUsbNYYnBUM'
CHANNEL_ID = '-1002278281776'  # Use '@channelusername' or '-1001234567890'


# Function to send a message to Telegram
def send_telegram_message(message):
    print(f"Sending message to Telegram:\n{message}")
    response = requests.post(
        f'https://api.telegram.org/bot{TOKEN}/sendMessage',
        data={'chat_id': CHANNEL_ID, 'text': message, 'parse_mode': 'Markdown'}
    )
    print(f"Telegram response: {response.status_code} - {response.json()}")
    return response.json()


# Load events from the JSON file
def load_events_from_file():
    try:
        with open('sass_events.json', 'r', encoding='utf-8') as file:
            events = json.load(file)
            print(f"Loaded {len(events)} events from the file.")
            return events
    except FileNotFoundError:
        print("Error: The file 'sass_events.json' does not exist.")
        return []
    except json.JSONDecodeError:
        print("Error parsing the JSON file.")
        return []


# Get today's date in the format 'dd. Mmm'
today_date = datetime.now().strftime('%d. %b')
print(f"Today's date: {today_date}.")

# Load events from the file
events = load_events_from_file()

# Process each event and send the message to Telegram if the date matches today's date
for event in events:
    event_date = event.get('start_date', 'Unknown date')

    # Check if the event's date matches today's date
    if event_date == today_date:
        title = event.get('title', 'Unknown title')
        start_time = event.get('start_time', 'Unknown start time')
        end_time = event.get('end_time', 'Unknown end time')
        lineup = event.get('lineup', 'Unknown lineup')
        link = event.get('link', 'No link available')
        location = event.get('location', 'SASS Music Club')

        # Prepare the message
        message = (
            f"📅 *Event*: {title}\n"
            f"🗓 *Date*: {event.get('day', 'Unknown day')}, {event_date}\n"
            f"⏰ *Time*: {start_time} - {end_time}\n"
            f"🎤 *Lineup*: {lineup}\n"
            f"📍 *Location*: Sass\n"
            f"🔗 {link}"
        )


        # Print the message to the console
        print(f"Prepared message for event '{title}':\n{message}\n")

        # Send the message to Telegram
        response = send_telegram_message(message)
        if response.get('ok'):
            message_id = response['result']['message_id']
            print(f"Message successfully sent. Message ID: {message_id}")
        else:
            print(f"Error sending message. Response: {response}")
    else:
        print(f"Event '{event.get('title', 'Unknown title')}' is not scheduled for today. Skipping.")
