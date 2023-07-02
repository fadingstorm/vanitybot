# this stuff is ALL taken from https://waifu.pics/docs

import requests

def get_the_img(what):
	resp = requests.get(f"https://api.waifu.pics/sfw/{what}")
	data = resp.json()
	return (data['url'])