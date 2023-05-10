import requests


pk = input('Input pk of the product: ')
endpoint = f"http://localhost:8000/api/products/{pk}/"

get_response = requests.get(endpoint, json={'title': 'Hello world'})
# print(get_response.headers)
print(get_response.json())
