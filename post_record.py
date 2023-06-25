from PIL import Image
import base64
import requests

import requests
import base64

# Открываем изображение
with open("sample-birch-400x300.jpg", "rb") as f:
    img = Image.open(f)
    # Преобразуем изображение в байтовое представление
    img_bytes = img.tobytes()

# Кодируем байтовое представление в формат base64
encoded = base64.b64encode(img_bytes)
encoded = encoded.decode("utf-8")
print(type(encoded))
'''print(type(encoded))
# Декодируем обратно в байтовый формат
decoded = base64.b64decode(encoded)

# Создаем новый объект изображения на основе декодированных байтов
new_img = Image.frombytes(img.mode, img.size, decoded)

# Сохраняем новое изображение в файл
with open("new_image.jpg", "wb") as f:
    new_img.save(f)'''



data = {
    'user_id': 'd317836b-c190-44b5-aaf5-7feadb8472c5','token':'2ad6df50-776b-4850-8b31-1365d7ab0a78',
    "image": encoded,
    "base_url": "http://localhost:8000"
}

response = requests.post("http://localhost:8000/images", json=data)

