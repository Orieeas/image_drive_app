import requests


def create_user(name):
    url = 'http://localhost:8000/users'
    data = {'name': name}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Failed to create user: {response.text}')
