import requests
from bs4 import BeautifulSoup
import time
from kiwipiepy import Kiwi

# 연관검색어 추출하기
def get_search_results(search_query, made_words):
    nownum = 2000
    search_url = "https://ko.wikipedia.org/w/index.php?search=" + search_query + "&title=특수:검색&profile=default&fulltext=1&ns0=1&offset=0&limit=2000"
    # limit이 몇 개씩 단어 보여주는지 알려주는거 offset이 시작번호 0으로 하면 처음부터 
    # 순서 1: 먼저 방문, 한 100개정도 먼저 보여줘 그리고 몇갠지 찾아 그리고 그 숫자 끝날때까지 한 2000개? 씩 한 페이지에 보여주고 단어 크롤링하기
    
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")

    res_num = soup.find('div', class_ = "results-info")
    totalnum = int(res_num['data-mw-num-results-total'])
    
    results = soup.find_all('div', class_='mw-search-result-heading')

    search_results = []

    for div in results:
        title_tag = div.find('a', attrs={'title': True})
        if title_tag:
            title = title_tag['title']
            search_results.append(title)
            made_words.append(title)
            content, url, text_data, text_wikitext, text = tokenizing(title)
            make_word(content, text_data, made_words)

    while(nownum < totalnum) :
        nownum = str(nownum) #str
        search_url = "https://ko.wikipedia.org/w/index.php?search=" + search_query + "&title=특수:검색&profile=default&fulltext=1&ns0=1&offset=" + nownum + "&limit=4000"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, "html.parser")

        results = soup.find_all('div', class_='mw-search-result-heading')

        for div in results:
            title_tag = div.find('a', attrs={'title': True})
            if title_tag:
                title = title_tag['title']
                search_results.append(title)
                made_words.append(title)
                content, url, text_data, text_wikitext, text = tokenizing(title)
                make_word(content, text_data, made_words)

        nownum = int(nownum) #int
        nownum += 4000

    return search_results, content, url, text_data, text_wikitext, text

# Wikipedia content crawling
def getWikiData(search):
    wiki_url = "https://ko.wikipedia.org/wiki/" + search
    headers = {'Content-Type': 'application/json'}
    url = "https://ko.wikipedia.org/w/api.php?action=parse&parse&page=" + search + "&prop=wikitext&formatversion=2&format=json"
    response = requests.get(url, headers=headers)
    return response.json(), wiki_url, search

# Tokenization of the synopsis
def tokenizing(text):
    text_data, url, text = getWikiData(text)
    kiwi = Kiwi()
    kiwi.prepare()
    index = text_data['parse']['wikitext'].find("== 각주 ==")
    if(index != -1):
          text_data['parse']['wikitext'] = text_data['parse']['wikitext'][:index]
    text_wikitext = text_data['parse']['wikitext']
    result = kiwi.tokenize(text_wikitext)
    return result, url, text_data, text_wikitext, text

# Extracting words and their cosine similarity values
def make_word(result, text_data, made_words):
    temp_word = ""
    bef_tag = ""
    bef_loc = 0
    form_num = 0

    for form, tag, start, length in result:
        # Nouns
        if tag in ['NNP', 'NNG']:
            # 명사 여러 개가 띄어쓰기 없이 나왔을 때 한 단어로 취급, 후에 바꿔도 됨(모든 명사 구분하는 걸로)
            if bef_tag == 'NN' and bef_loc == start:
                temp_word += form
            # 띄어쓰기 후에 들어오는 명사
            elif bef_tag == 'NN' and bef_loc != start:
                made_words.append(temp_word)
                temp_word = form
                form_num = 0
                
            # 관형격 조사 다음에 들어오는 명사
            elif bef_tag == 'JKG' or bef_tag == 'XSN':
                temp_word += form
                
            elif temp_word == "":
                temp_word = form

            bef_loc = start + length
            form_num += 1
            bef_tag = 'NN'

        # 관형격 조사일 때 ex)신의성실의 원칙
        elif tag == 'JKG' and bef_tag == "NN":
            temp_word += form + " "
            bef_tag = 'JKG'
            form_num += 1

        # ~적 (e.g., 안정적, 감각적)
        elif tag == 'XSN' and bef_tag == "NN":
            temp_word += form + " "
            bef_tag = 'XSN'
            form_num += 1
        
        else:
            if bef_tag == 'NN' and len(temp_word) > 1:
                made_words.append(temp_word)

            temp_word = ""
            bef_tag = ""
            bef_loc = 0
            form_num = 0

    return made_words

# 키워드와 관련된 유사도 높은 결과 단어 추출, 시작하는 부분 get_search_results함수 호출
def getWord(text): 
    made_words = []
    get_search_results(text, made_words)
    made_words_set = set(made_words)

    return made_words_set


start = time.time()
result = getWord("염화나트륨")
finish = time.time()
howlong = finish - start

print(result)
print(len(result))
print(howlong)