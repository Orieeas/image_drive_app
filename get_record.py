import requests
# Скачивание файла аудиозаписи
def download_audio(id, user):
    url = f'http://localhost:8000/record/?id={id}&user={user}'
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError('Failed to download audio')
    return response.content

# Скачивание файла аудиозаписи
user={'id':'','some_id':''}
audio_content = download_audio(id='some_id', user=user['id'])
with open('audio.mp3', 'wb') as f:
    f.write(audio_content)