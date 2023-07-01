from bs4 import BeautifulSoup
import requests
import random

def get_anime_news():
    html_text = requests.get('https://myanimelist.net/news').text
    soup = BeautifulSoup(html_text, 'lxml')
    all_news = soup.find_all('div', class_='news-unit-right')
    
    num = random.randint(0, len(all_news) - 1)
    names = []
    descs = []
    links = []
    for news in all_news:
        name = news.find('a').text
        desc = news.find('div', class_="text").text
        link = news.find('a')['href']
        names.append(name)
        descs.append(desc.strip())
        links.append(link)
    return (names[num], descs[num], links[num])

#print(get_anime_news())