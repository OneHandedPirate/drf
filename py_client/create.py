import requests


endpoint = "http://localhost:8000/api/products/"

title = input('Input title: ')
content = input('Input content: ')
price = input('Input price: ')

get_response = requests.post(endpoint, json={'title': title, 'content': content, 'price': price})
print(get_response.json())
