# script.py
import requests

token = "7342084415:AAFYrhb2Rm_hYWKfTbcwZlZ_zaM_M6McWTw"
key = "getUpdates"
url = f"https://api.telegram.org/bot{token}/{key}"
response = requests.get(url, timeout=30)
print(response.json())

