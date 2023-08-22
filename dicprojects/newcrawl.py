import requests
from bs4 import BeautifulSoup
from kiwipiepy import Kiwi

search = "민법"

wiki_url = "https://ko.wikipedia.org/w/index.php?search=" + search + "&title=특수:검색&profile=advanced&fulltext=1&ns0=1"
headers = {'Content-Type': 'application/json'}
response = requests.get(wiki_url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    page_title = soup.select_one('span.mw-page-title-main')
    search = page_title.text
    url = "https://ko.wikipedia.org/w/api.php?action=parse&parse&page=" + search + "&prop=wikitext&formatversion=2&format=json"
    response = requests.get(url, headers=headers)