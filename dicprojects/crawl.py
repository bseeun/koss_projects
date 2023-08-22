import requests
from bs4 import BeautifulSoup
from kiwipiepy import Kiwi

# Wikipedia content crawling
def getWikiData(search):
    wiki_url = "https://ko.wikipedia.org/wiki/" + search
    headers = {'Content-Type': 'application/json'}
    response = requests.get(wiki_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        page_title = soup.select_one('span.mw-page-title-main')
        search = page_title.text
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
def make_word(result, text_data):
    cosine_list = []
    made_words = []
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
                cosine_list.append(form)
                temp_word += form
                
            elif temp_word == "":
                temp_word = form

            bef_loc = start + length
            form_num += 1
            bef_tag = 'NN'

        # 관형격 조사일 때 ex)신의성실의 원칙
        elif tag == 'JKG' and bef_tag == "NN":
            cosine_list.append(form)
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

# 키워드와 관련된 유사도 높은 결과 단어 추출
def getWord(text):
    content, url, text_data, text_wikitext, text = tokenizing(text)
    made_words = make_word(content, text_data)
    made_words_set = set(made_words)
    final_words_list = list(made_words_set)
    similar_word = []
    result = {}
    return result

result = getWord("한국사")
