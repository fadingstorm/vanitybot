from bs4 import BeautifulSoup
import requests

def get_stock(ticker):
    html_text = requests.get('https://money.cnn.com/quote/quote.html?symb=' + ticker.upper()).text
    soup = BeautifulSoup(html_text, 'lxml')
    if ('Symbol not found' in soup.text) or (' vs ' in soup.text):
        return False
    else:
        fullname = soup.find('h1').text
        subname = soup.find('span', class_='wsod_smallSubHeading').text
        name = fullname.replace(subname, '').strip()
        price = soup.find('span', streamformat='ToHundredth').text
        changes = soup.find('td', class_='wsod_change')
        dataaaaa = changes.find_all('span', class_='posData')
        if len(dataaaaa) != 0:
            data = changes.find_all('span', class_='posData')
            changePrice = data[0].text
            changePercent = data[1].text
        else:
            data = changes.find_all('span', class_='negData')
            changePrice = data[0].text
            changePercent = data[1].text           
        return (name, price, changePrice, changePercent)

#print(get_stock(input()))