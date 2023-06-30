import requests

def get_neko_img():
	resp = requests.get("https://nekos.best/api/v2/neko")
	data = resp.json()
	return (data["results"][0]["url"], data["results"][0]["artist_name"])

# gotten from https://nekos.best/
