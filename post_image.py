from PIL import Image
import requests
import base64


def post_image(user_id,token,image_name):
    with open(image_name, "rb") as f:
        img = Image.open(f)
        img_bytes = img.tobytes()
    encoded = base64.b64encode(img_bytes)
    encoded = encoded.decode("utf-8")
    data = {
        'user_id': user_id,'token':token,
        "image": encoded,
        "base_url": "http://localhost:8000",
        "img_mode": img.mode,
        "img_size": str(img.size)
    }
    response = requests.post("http://localhost:8000/images", json=data)
    if response.status_code == 200:
        print(response.json())
    else:
        raise Exception(f'Failed to add image: {response.text}')
