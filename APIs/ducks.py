import requests

def get_duck_img():
	resp = requests.get("https://random-d.uk/api/quack")
	data = resp.json()
	return (data["url"], data["message"])

# gotten from https://random-d.uk/api