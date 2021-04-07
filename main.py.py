import requests
from bs4 import BeautifulSoup
import json

page = requests.get("https://www.animesvision.com.br/all-series")

def get_anime_list(pag):
    try:
        page = requests.get("https://www.animesvision.com.br/all-series?page="+ str(pag))
        print("https://www.animesvision.com.br/all-series?page="+ str(pag))
        soup = BeautifulSoup(page.text, 'html.parser')
        mydivs = soup.find_all("a", {"class": "thumb"})
        return mydivs
    except:
        print('erro ao obter episodios da pagina {} '.format(pag))

def get_anime_infos(anime):
    try:
        page = requests.get("https://www.animesvision.com.br"+ anime['href'])
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup
    
    except:
        print('erro ao obter informações do anime {} '.format())
        
def obtain_list_of_episodes(anime_soup):        
    atags = anime_soup.find_all("a", {"class": "btn btn-sm btn-go2"})
    episodes_pages = []
    
    for a in atags:
        if "/download" in a['onclick']:
            episodes_pages.append(a['onclick'].replace("window.open('", '').replace("')", '').replace("', '_blank", ''))

    return episodes_pages
            

def insert_anime(anime, infos):
    try:
        response = requests.post('http://localhost:8080/v1/anime', json={
            'ANIME_NAME': anime['title'],
            'ANIME_NUM_EPISODES': int(anime.contents[1].text.replace(' ep(s)', '')),
            'ANIME_THUMBNAILS': anime.contents[5]['src'],
            'ANIME_URL': "https://www.animesvision.com.br"+ anime['href'],
            'ANIME_DESCRIPTION': description[0].text,
            'ANIME_IMAGE': '',
            'ANIME_LANGUAGE': informations[5].text,
            'ANIME_STATUS': informations[6].text,
        })
        
        return response
    
    except:
        print('erro ao tentar cadastrar o anime')    

for pag in range(123):
    animes = get_anime_list(pag)
    for anime in animes:
        infos = get_anime_infos(anime)
        episodes = obtain_list_of_episodes(infos)
        response = insert_anime(anime, infos)
        print(json.loads(response.text).get('ANIME_ID'))
        






