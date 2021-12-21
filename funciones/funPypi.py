import requests
from bs4 import BeautifulSoup

def pypi(lista_tokens):

    for search in lista_tokens:
        try:
            url = "https://pypi.org/project/{}/".format(search)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            pip = soup.find(class_ = "banner").find(class_="package-header__pip-instructions").find(id="pip-command").text
            return (pip)
        except:
            pass