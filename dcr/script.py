# script.py
import requests

token = "YOUR_BOT_TOKEN"
key = "getUpdates"
url = f"https://api.telegram.org/bot{token}/{key}"
response = requests.get(url, timeout=30)
print(response.json())

