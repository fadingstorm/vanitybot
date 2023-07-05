import requests

def get_dadjoke():
	resp = requests.get("https://icanhazdadjoke.com/slack")
	data = resp.json()
	return (data["attachments"][0]["fallback"])

# https://icanhazdadjoke.com/api