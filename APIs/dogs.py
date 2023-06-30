import json
import requests

def get_dog_url():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    json_data = json.loads(response.text)
    url = json_data["message"]
    return url

# gotten from https://dog.ceo/dog-api/