import requests


pk = input('Input pk of the product: ')
endpoint = f"http://localhost:8000/api/products/{pk}/update/"

data = {
    'title': 'Hello World my update',
    'price': 129.99
}

get_response = requests.put(endpoint, json=data)
# print(get_response.headers)
print(get_response.json())