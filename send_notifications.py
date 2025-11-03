import requests
import time
import random

API_URL = "http://127.0.0.1:8000/api/notifications/send/"

def send_notification():
    messages = [
        "🚀 Server is running smoothly",
        "⚡ Realtime update from backend",
        "🔥 Django Channels works perfectly",
        "💬 This message is sent via REST + WS",
        "🧠 Data sync in progress...",
        "✅ All systems operational"
    ]

    while True:
        msg = random.choice(messages)
        response = requests.post(API_URL, json={"message": msg})
        print(f"Sent: {msg} | Status: {response.status_code}")
        time.sleep(3)  # wait 3 seconds between messages

if __name__ == "__main__":
    print("Starting continuous notification sender...")
    try:
        send_notification()
    except KeyboardInterrupt:
        print("\nStopped by user.")
