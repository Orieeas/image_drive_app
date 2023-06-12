import requests
import base64

url = "http://localhost:8000/records"

headers = {
    "Content-Type": "application/json"
}
# Загрузка аудиофайла в байтах
with open("shinshilla-31200.wav", "rb") as f:
    audio_bytes = f.read()


data = {
    "user_id": "d317836b-c190-44b5-aaf5-7feadb8472c5",
    "token": "2ad6df50-776b-4850-8b31-1365d7ab0a78",
    "audio": base64.b64encode(audio_bytes).decode('utf-8')
}

response = requests.post(url, json=data, headers=headers)

# Обработка ответа
if response.status_code == 200:
    result = response.json()
    print("Record URL:", result.get("url"))
else:
    print("Error:", response.text)