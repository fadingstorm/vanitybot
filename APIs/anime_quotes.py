import requests

def get_anime_quote():
	resp = requests.get("https://animechan.xyz/api/random")
	data = resp.json()
	return (data["character"], data["quote"], data["anime"])

# gotten from https://animechan.xyz/docs#random-quote