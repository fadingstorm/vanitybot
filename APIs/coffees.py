import requests

def get_coffee_img():
	resp = requests.get("https://coffee.alexflipnote.dev/random.json")
	data = resp.json()
	return (data["file"])

# gotten from https://coffee.alexflipnote.dev/
