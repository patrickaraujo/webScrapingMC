import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

regex = re.compile(r'<[^>]+>')
def remove_html(string):
    return regex.sub('', string)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def requestSite(site):
    domain = urlparse(site).netloc
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    response = s.get(site)
    print(response.status_code)
    print("\nHeader\n")
    print(response.headers)

    #print("\nContent\n")
    conteudo = response.content
    #print(conteudo)
    #print(type(conteudo))

    site = BeautifulSoup(conteudo, 'html.parser')

    #print(site.prettify())
    gameTitle = site.find_all('td', attrs={'class': 'clamp-summary-wrap'})
    print("Quantidade de títulos:\t", len(gameTitle))
    gameList = [[]]
    for x in gameTitle:
        #print(x.prettify())
        #print(type(x))
        titulo = x.find('a', attrs={'class': 'title'})

        titTemp = str(titulo)
        ult = titTemp.rfind("><h3>")
        fim = titTemp.rfind("</h3>")

        title = (str(titulo)[ult+5:(-(len(titTemp)-fim))])
        print(title)
        link = domain+(titTemp[23:(-(len(titTemp)-ult+1))])
        data = x.find('div', attrs={'class': 'clamp-details'})
        notaMC = x.find('div', attrs={'class': 'metascore_w large game positive'})
        notaUser = x.find('div', attrs={'class': 'metascore_w user large game mixed'})
        plataforma = x.find('span', attrs={'class': 'data'})
        sinopse = x.find('div', attrs={'class': 'summary'})
        summary = (remove_html((str(sinopse))[21:-6])).strip()
        platf = (remove_html(str(plataforma))).strip()
        notaMCConv = str(notaMC)
        notaUsuario = (remove_html(str(notaUser))).strip()
        if(notaMCConv!="None"):
            notaMCConv = notaMCConv[45:-6]

        date = ""

        for num, t in enumerate(data):
            if(num==3):
                texto = str(t)
                x = texto.rfind("<span>")
                date = texto[(x+6):-7]
        gameList.append([title, platf, notaMCConv, notaUsuario, summary, link, date])
    df = pd.DataFrame(gameList, columns=['Titles', 'Platform', 'RatingMC', 'UserRating', 'Summary', 'Link', 'Release'])
    print(df)
    df = df.drop(index=0)

    print(df)
    df.to_json(r'NewReleasesIOS.json')