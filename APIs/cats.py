import json
import requests

def get_cat_url():
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    json_data = json.loads(response.text)
    url = json_data[0]['url']
    return url

# gotten from https://thecatapi.com/