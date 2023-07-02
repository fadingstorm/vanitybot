import html
import requests

def decode_html_entities(text):
    decoded_text = html.unescape(text)
    return decoded_text

def get_trivia():
    resp = requests.get("https://opentdb.com/api.php?amount=1")
    raw = resp.json()
    data = raw['results'][0]
    data['category'] = decode_html_entities(data['category'])
    data['difficulty'] = decode_html_entities(data['difficulty'])
    data['question'] = decode_html_entities(data['question'])
    data['correct_answer'] = decode_html_entities(data['correct_answer'])
    data['incorrect_answers'] = [decode_html_entities(answer) for answer in data['incorrect_answers']]
    return data

#print(get_trivia())

# gotten from https://opentdb.com/api_config.php
