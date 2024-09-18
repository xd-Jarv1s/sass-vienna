import json
import requests
from datetime import datetime

# Define your Telegram bot token and chat ID
TOKEN = '7162097876:AAE27cvUGt6tUzuX3NI9VoNnoUsbNYYnBUM'
CHAT_ID = '-1002325845465'

# List to keep track of already sent events
sent_events = {}

# Define the days of the week
day_of_week = datetime.today().weekday()
day_names = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
today_day_name = day_names[day_of_week]

print(f"Today is {today_day_name}, {datetime.today().strftime('%A, %d. %B %Y')}.")

# Function to check if the event was already sent
def was_event_sent(event_id):
    result = event_id in sent_events
    print(f"Checking if the event '{event_id}' has already been sent: {'Yes' if result else 'No'}.")
    return result

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

# Get the current date
today = datetime.today().strftime('%d. %b')
print(f"Today's date: {today}")

# Process each event and check if it's for today
for event in data:
    start_date = event.get('start_date', 'Unknown date')
    event_day = event.get('day', 'Unknown day')
    event_id = event.get('title', 'Unknown title')  # Use title as identifier for simplicity

    print(f"Processing event: {event_id} (date: {start_date}, day: {event_day})")

    # Check if the event is today and on the correct day of the week
    if start_date == today and event_day == today_day_name:
        print(f"Event '{event_id}' is scheduled for today ({today_day_name}, {today}).")

        # Check if the event was already sent
        if was_event_sent(event_id):
            print(f"Event '{event_id}' has already been sent. Skipping.")
            continue

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
            f"🔗 [More Info]({link})"
        )

        if subline:
            message += f"\n🔖 *Subline*: {subline}"

        # Print the message to the console
        print(f"Prepared message for event '{event_id}':\n{message}\n")

        # Send the message to Telegram
        response = send_telegram_message(message)
        if response.get('ok'):
            message_id = response['result']['message_id']
            print(f"Message sent successfully. Message ID: {message_id}")
            # Add the event and message ID to the sent_events dictionary
            sent_events[event_id] = message_id
        else:
            print(f"Error sending message. Response: {response}")

    else:
        print(f"Event '{event.get('title', 'Unknown title')}' is not scheduled for today. Skipping.")

# Function to remove outdated messages (to be implemented based on your requirements)
def remove_outdated_messages():
    # Example: Remove messages older than 1 day
    print("Removing outdated messages...")
    pass  # Implement your own logic here
