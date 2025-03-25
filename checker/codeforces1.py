import requests


url = "https://codeforces.com/api/user.info?handles=pascal65536"
# Запрос информации о пользователе
response = requests.get(url)
data = response.json()
print(data)

if data["status"] == "OK":
    user = data["result"][0]
    print(f"Handle: {user['handle']}, Rating: {user['rating']}")
else:
    print("Ошибка при запросе данных")