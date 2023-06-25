'''import requests

params = {
    "id": "65d1e1e4-17f6-4b77-8ef0-647c785a894a",
    "user": "d317836b-c190-44b5-aaf5-7feadb8472c5"
}

response = requests.get("http://localhost:8000/image", params=params)

with open("image.jpg", "wb") as image_file:
    image_file.write(response.content)
'''


###

'''import tempfile
import requests
from fastapi.responses import FileResponse



import tempfile
import requests
from fastapi.responses import FileResponse

params = {
    "id": "65d1e1e4-17f6-4b77-8ef0-647c785a894a",
    "user": "d317836b-c190-44b5-aaf5-7feadb8472c5"
}

response = requests.get("http://localhost:8000/image", params=params)

with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
    temp_file.write(response.content)
    temp_file.flush()
    temp_file.seek(0)

    response = FileResponse(temp_file, media_type="image/jpeg")

    with open("image.jpg", "wb") as image_file:
        for chunk in response.iter_content(chunk_size=1024 * 8):
            image_file.write(chunk)
            
        '''

###

import requests
from PIL import Image
import io
from PIL import Image

url = "http://localhost:8000/image"
params = {"id": "59aecbaf-104f-4b0d-890e-c810c52cacb7",
    "user": "d317836b-c190-44b5-aaf5-7feadb8472c5"}
response = requests.get(url, params=params)

if response.status_code == 200:
    # Обработка полученного изображения

    imag = response.content
    #imag = str(imag)
    #print(imag)
    # ...
    print(type(imag),'1')

    import base64
    # Замените <ваш_объект_bytes> на объект bytes, который вы хотите преобразовать в изображение
    img_mode='RGB'
    img_size=(400,300)
    decoded = base64.b64decode(imag)

    # Создаем объект Image из байтового представления
    img = Image.frombytes("RGB", (400,300), decoded)

    # Проверяем, что изображение успешно создано
    img.show()

    # Сохраняем новое изображение в файл
    with open("new_image6.jpg", "wb") as f:
        img.save(f)
    # Используйте библиотеку io, чтобы создать файлоподобный объект из объекта bytes


    # Откройте изображение с помощью библиотеки Pillow и сохраните его в текущей директории

elif response.status_code == 404:
    print("Изображение не найдено")
else:
    print("Ошибка при выполнении запроса")