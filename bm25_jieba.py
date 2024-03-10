from rank_bm25 import BM25Okapi
import jieba
import numpy as np
import json
import re

jieba.load_userdict('user_dict.txt')


def jieba_english_tokenize(words):
    pattern = r'^[a-zA-Z0-9]+$'
    blank_space_indexes = []
    for i in range(len(words) - 1):
        if words[i] == ' ' and re.match(pattern, words[i - 1]) and re.match(pattern, words[i + 1]):
            blank_space_indexes.append(i)
    # print('空格有這些', blank_space_indexes)
    # --- #
    processed_indexes = []
    english_words = []
    for index in blank_space_indexes:
        if index not in processed_indexes:
            english_word = ''
            if index + 2 not in blank_space_indexes:
                # 'post malone', 'taylor swift' 直接處理
                for i in range(index - 1, index + 2):
                    english_word = english_word + words[i]
                    processed_indexes.append(i)
            else:
                # 'austin richard post', 'show me the money'
                start_index = index
                while index + 2 in blank_space_indexes:
                    index = index + 2
                end_index = index
                for i in range(start_index - 1, end_index + 2):
                    english_word = english_word + words[i]
                    processed_indexes.append(i)
            # print(english_word)
            english_words.append(english_word)
            # print(list(set(processed_indexes)))
            # print('---')

    words = [words[i] for i in range(len(words)) if i not in processed_indexes]
    for english_word in english_words:
        words.append(english_word)

    return words


# 使用jieba進行中文分詞
def chinese_tokenizer(text):
    return jieba_english_tokenize(jieba.lcut(text))


# # 你的演唱會資料
# with open('concert_data_old_zh.json', 'r', encoding='utf-8') as file:
#     concert_data = json.load(file)
#
# documents = [chinese_tokenizer(concert["tit"] + " " + concert["int"]) for concert in concert_data]  # ori
# for i, document in enumerate(documents):
#     for j, element in enumerate(document):
#         document[j] = document[j].lower()
#
# # documents = [chinese_tokenizer(concert["tit"] + " " + concert['cit'] + " " + concert["int"]) for concert in concert_data] # test
# # documents = [chinese_tokenizer(concert['tit'] + " " + concert['cit']) for concert in concert_data] # test
#
# # 創建BM25模型
# bm25 = BM25Okapi(documents)
#
# # # 測試
# # k1 = 1.5
# # b = 0.5
# # bm25 = BM25Okapi(documents, k1=k1, b=b)
#
# # 處理輸入
# user_tokens = chinese_tokenizer(user_input)
# user_tokens = [token.lower() for token in user_tokens]
#
# # 計算BM25分數
# scores = bm25.get_scores(user_tokens)
#
# # 找到最相似的幾個演唱會
# sorted_indices = np.argsort(scores)[::-1]  # 從高到低排序
# how_many_results = 200
# top_concerts = []
# for i in sorted_indices:
#     if scores[i] > 0:
#         top_concerts.append((concert_data[i]['tit'], scores[i]))
#     if len(top_concerts) == how_many_results:
#         break
#
# matched_indexes = []
# for i in range(len(concert_data)):
#     for j, (title, score) in enumerate(top_concerts):
#         if concert_data[i]['tit'] == title:
#             print(concert_data[i]['tit'])
#             if i not in matched_indexes:
#                 matched_indexes.append(i)
# print('--- 結束 ---')
# print(matched_indexes)


#             if i not in matched_indexes:
#                 matched_indexes.append(i)
#             # print(f'index = {i}')
#             # print(f'{concert_data[i]["tit"]}')

# print(matched_indexes)
# for i in range(len(matched_indexes)):
#     print(concert_data[i]['tit'])

# # 打印最相似的演唱會
# if top_concerts:
#     print('abc', top_concerts)
#     for idx, (title, score) in enumerate(top_concerts):
#         print(f"{idx + 1}. {title} (相似度: {score:.2f})")
#         for i in range(len(concert_data)):
#             if concert_data[i]['tit'] == title:
#                 print(concert_data[i]['url'])
# else:
#     print("沒有找到匹配的演唱會。")

# zh_cities = ["台北", "新北", "桃園", "台中", "台南", "高雄", "基隆", "新竹", "苗栗", "彰化", "南投", "雲林",
#              "嘉義", "屏東", "宜蘭", "花蓮", "台東", "金門", "澎湖", "連江"]

def get_keyword_indexes(text, json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    documents = [chinese_tokenizer(concert["tit"] + " " + concert["int"]) for concert in data]  # ori
    for i, document in enumerate(documents):
        for j, element in enumerate(document):
            document[j] = document[j].lower()

    bm25 = BM25Okapi(documents)

    # 處理輸入
    user_tokens = chinese_tokenizer(text)
    user_tokens = [token.lower() for token in user_tokens]

    # 計算BM25分數
    scores = bm25.get_scores(user_tokens)

    # 找到最相似的幾個演唱會
    sorted_indices = np.argsort(scores)[::-1]  # 從高到低排序
    how_many_results = 15
    top_concerts = []
    for i in sorted_indices:
        if scores[i] > 0:
            top_concerts.append((data[i]['tit'], scores[i]))
        if len(top_concerts) == how_many_results:
            break
    if top_concerts:
        matched_indexes = []
        for i in range(len(data)):
            for j, (title, score) in enumerate(top_concerts):
                if data[i]['tit'] == title:
                    # print(data[i]['tit'])
                    if i not in matched_indexes:
                        matched_indexes.append(i)
        # print('--- 結束 ---')
        print(matched_indexes)

        return matched_indexes
    else:
        return None

search_word = 'jp saxe'
matched_indexes = get_keyword_indexes(search_word, 'concert_data_old_zh.json')
if matched_indexes is not None:
    with open('concert_data_old_zh.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for index in matched_indexes:
        print(data[index]['tit'])
        print(data[index]['url'])
else:
    print('沒有找到')
