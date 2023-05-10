import requests
from pprint import pprint
from getpass import getpass

auth_endpoint = "http://localhost:8000/api/auth/"
username = input("Your username: ")
password = getpass("Your password: ")

auth_response = requests.post(auth_endpoint, json={"username": "admin", "password": password})
pprint(auth_response.json())
if auth_response.status_code == 200:
    token = auth_response.json()["token"]
    headers = {
        "Authorization": f'Bearer {token}'
    }

    endpoint = "http://localhost:8000/api/products/"

    get_response = requests.get(endpoint, headers=headers)
    pprint(get_response.json())
