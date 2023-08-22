def make_word(result):
    cosine_list = []
    made_words = []
    temp_word = ""
    bef_tag = ""
    bef_loc = 0
    form_num = 0
    cnt_dict = {}
    cosine = {}
    for form, tag, start, length in result:

        # Nouns (일반명사, 고유명사)
        if tag in ['NNP', 'NNG']:

            # 명사 여러 개가 띄어쓰기 없이 나왔을 때 한 단어로 취급
            if bef_tag == 'NN' and bef_loc == start:
                temp_word += form

            # 띄어쓰기 후에 들어오는 명사
            elif bef_tag == 'NN' and bef_loc != start:
                if temp_word in cnt_dict:
                    cnt_dict[temp_word] += 1
                else:
                    cnt_dict[temp_word] = 1
                made_words.append(temp_word)
                temp_word = form
                form_num = 0 # 밑에서 1 더해서 일단 초기화
                
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
            cosine_list.append(temp_word)
            temp_word += form + " "
            bef_tag = 'JKG'
            form_num += 1

        # ~적 ex)안정적 공급
        elif tag == 'XSN' and bef_tag == "NN":
            cosine_list.append(temp_word)
            temp_word += form + " "
            bef_tag = 'XSN'
            form_num += 1
        
        # 그 외의 태그 등장시 만들어진 단어 append
        else:
            if bef_tag == 'NN' and len(temp_word) > 1:
                if temp_word in cnt_dict:
                    cnt_dict[temp_word] += 1
                else:
                    cnt_dict[temp_word] = 1
                made_words.append(temp_word)
                # for token in cosine_list:
                #     if token in ko_model.wv.key_to_index:
                #         cosine_sim = cosine_similarity([ko_model.wv[text_data['parse']['title']]], [ko_model.wv[token]])
                #         if cosine_sum < cosine_sim:
                #             cosine_sum = cosine_sim
                #             cosine[temp_word] = cosine_sum

            cosine_list = []
            cosine_sum = 0
            temp_word = ""
            bef_tag = ""
            bef_loc = 0
            form_num = 0

    return cosine, made_words, cnt_dict

make_word()