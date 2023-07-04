import requests
from bs4 import BeautifulSoup

def get_lipsum(number, length):
    text = ''
    resp = requests.get(f"https://loripsum.net/api/{number}/{length}/headers")
    soup = BeautifulSoup(resp.content, 'lxml')
    title = soup.find('h1').text
    data = soup.find_all('p')
    for p in data:
        data[data.index(p)] = p.text.strip()
    for paragraph in data:
        text += (paragraph + '\n\n')
    return (title, text.strip())