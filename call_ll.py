import requests
import json
import time

url = "http://localhost:8080/generate"
payload = {"inputs": "Hello, how are you?"}

# Wait until the server is ready
for i in range(20):
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(json.dumps(response.json(), indent=2))
        break
    except requests.exceptions.RequestException as e:
        print(f"Attempt {i+1}: server not ready, retrying in 2 seconds...")
        time.sleep(2)
