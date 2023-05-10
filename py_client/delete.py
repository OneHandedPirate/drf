import requests


pk = int(input('Input pk of the product you what to delete: '))
endpoint = f"http://localhost:8000/api/products/{pk}/delete/"

get_response = requests.delete(endpoint)
print(get_response.status_code)
