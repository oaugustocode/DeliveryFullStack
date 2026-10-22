import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiZXhwIjoxNzkzMjgzOTE5fQ.1Idn5VGXXE5MmJWfXcEKHIfaBY2tv2ZxIEZ7bqyRFv4 "
}


requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(requisicao)
print(requisicao.json)