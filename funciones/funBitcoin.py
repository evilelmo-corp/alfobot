import requests
from bs4 import BeautifulSoup

def bitcoin():
    url = "https://markets.businessinsider.com/currencies/btc-eur"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    bitcoin_value = 'NaN'
    bitcoin_value = soup.find("span", class_ = "price-section__current-value").text
    #if not bitcoin_value: bitcoin_value = 'NaN'
    msg=f'El bitcoin está ahora a {bitcoin_value}€. A qué estás esperando?'
    return msg

    #await message.channel.send(f'El bitcoin está ahora a {bitcoin_value}€. A qué estás esperando?')