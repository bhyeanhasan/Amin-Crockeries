import requests
import json

url = 'http://127.0.0.1:8000/api/'
data = {
    'name': 'abdur',
    'res': 45,
    'tag': 'pitol'
}
json_data = json.dumps(data)
r = requests.post(url, data=json_data)
python_data = r.json()
print(python_data)
