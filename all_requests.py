from create_user import create_user
from post_image import post_image
from get_image import get_image

#put ur name into create user, for example:
print(create_user('John'))
#put ur user_id,token,image_name, for example:
print(post_image('e53254f4-0de6-45a7-b929-d8a88f75ca29', 'fbe56649-125e-4a76-94e3-e6fb13f5392e','sample-birch-400x300.jpg'))
#put ur url to file and user_id, for example:
print(get_image('http://localhost:8000/image?id=c489938d-fa5c-4ff2-ae8b-cb48335aacb7&user=d317836b-c190-44b5-aaf5-7feadb8472c5','d317836b-c190-44b5-aaf5-7feadb8472c5'))
