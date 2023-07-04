import requests
from bs4 import BeautifulSoup, Comment

# makes sure that each page of the embed has at least 300 chars but not over 1024
def split_string(string):
    MAX_LENGTH = 1024
    MIN_LENGTH = 300
    strings = []

    while len(string) > MAX_LENGTH:
        split_index = string.rfind("\n\n", 0, MAX_LENGTH - MIN_LENGTH)
        if split_index == -1:
            split_index = MAX_LENGTH
        strings.append(string[:split_index].strip())
        string = string[split_index:]

    if len(string) >= MIN_LENGTH:
        strings.append(string.strip())

    return strings

def get_lyrics(song):
    resp = requests.get(f"https://search.azlyrics.com/search.php?q={song.replace(' ', '+')}&x=7d80b8046a326010acb95d114747e7a5da342259ee906b770a92cfa9ab1fb545").text
    soup = BeautifulSoup(resp, 'lxml')
    if "Sorry, your search returned" in soup.text:
        return "Sorry, I couldn\'t find that song!"
        print('lol')
    else:
        panel = soup.find('div', class_='panel')
        info = panel.find('td', class_='text-left visitedlyr').text.replace('1. ', '').split(' - ')
        name = info[0].replace('"', '').strip()
        artist = info[1].strip()
        
        newlink = panel.find('td', class_='text-left visitedlyr').find('a')['href']
        resp = requests.get(newlink).text
        soup = BeautifulSoup(resp, 'lxml')
        
        # this finds the very specific html comment and finds the parent div
        where = soup.find_all(string=lambda string:isinstance(string, Comment))[13].find_parent('div')
        lyrics = split_string(where.text)

        pic = "https://www.azlyrics.com" + soup.find('img', class_='album-image')['src']
        
        
        return (name, artist, lyrics, pic)