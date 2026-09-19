import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_telegram_message(message):
    """Sends a message to Telegram."""
    
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Replace with your bot token
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Replace with your chat ID
    
    print(f"Sending message to Telegram: {TELEGRAM_BOT_TOKEN}")
    print(f"Chat ID: {TELEGRAM_CHAT_ID}")

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        print("✅ Telegram message sent!")
    else:
        print(f"❌ Failed to send Telegram message: {response.text}") 
        
if __name__ == "__main__":
    send_telegram_message("Hello, world!")