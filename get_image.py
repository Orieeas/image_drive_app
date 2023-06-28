import base64
import requests
from PIL import Image
import ast
import random


def get_image(urrl,user_id):
    url = "http://localhost:8000/image"
    params = {"url": urrl,
        "user": user_id}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        # Обработка полученного изображения

        imag = response.json()
        img_mode = imag['img_mode']
        img_size = (imag['img_size'])
        img_size = ast.literal_eval(img_size)
        imag = imag['file']
        decoded = base64.b64decode(imag)
        img = Image.frombytes(img_mode, img_size, decoded)
        name=str("new_image_")+str(random.randint(1,100000))+str(".jpg")
        with open((name), "wb") as f:
            img.save(f)
        return (f"Congratulation! New image {f.name} added")
    elif response.status_code == 404:
        raise Exception(f'Image have not found')
    else:
        raise Exception(f'Error')