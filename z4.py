import asyncio
import logging
from typing import Text

from rasa.core.agent import Agent
from rasa.shared.utils.cli import print_info, print_success
from rasa.shared.utils.io import json_to_string

from fuzzywuzzy import fuzz
import yaml
import re

from get_keyword_indexes_en import *
from get_keyword_indexes_zh import *
from get_city_date_indexes import *

from function_read_json import *

# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize, RegexpTokenizer
# from rank_bm25 import BM25Okapi
#
#
# def preprocess(text):
#     # 讀取 YAML 文件中的歌手名單
#     with open('data/keyword.yml', 'r', encoding='utf-8') as f:
#         data = yaml.safe_load(f)
#         singers = data['nlu'][0]['examples'].replace('- ', '').split('\n')
#         singers = [singer.lower() for singer in singers]
#
#     # 建立正則表達式：對每個名稱進行轉義，防止特殊字符造成問題
#     escaped_singers = [re.escape(singer) for singer in singers]
#     pattern = '|'.join(escaped_singers) + r'|\w+'
#
#     # 創建一個 tokenizer
#     tokenizer = RegexpTokenizer(pattern)
#
#     stop_words = set(stopwords.words('english'))
#     word_tokens = tokenizer.tokenize(text.lower())
#     # print(f"word_tokens = {word_tokens}")
#     # 更新過濾條件，確保在歌手名單中的詞不會因包含停用詞而被過濾
#     filtered_text = [word for word in word_tokens if word in singers or
#                      (word not in stop_words and all(char.isalpha() or char.isspace() for char in word))]
#     # print(f"filtered_text = {filtered_text}")
#     return filtered_text
#
#
# def get_keyword_indexes_en(user_input, json_filename):
#     # 從文件讀取演唱會數據
#     with open(json_filename, 'r', encoding='utf-8') as file:
#         concerts = json.load(file)
#
#     # 構建文檔
#     documents = [concert["tit"] + " " + concert["int"] for concert in concerts]
#
#     # 預處理所有文檔
#     texts = [preprocess(doc) for doc in documents]
#
#     # 使用BM25Okapi建立索引
#     bm25 = BM25Okapi(texts)
#
#     query_processed = preprocess(user_input)
#     scores = bm25.get_scores(query_processed)
#     ranked_scores = sorted(((score, idx) for idx, score in enumerate(scores)), reverse=True, key=lambda x: x[0])
#     results = [(idx, score) for score, idx in ranked_scores[:10] if score > 0]
#     indexes = [result[0] for result in results]
#     return indexes


# from z_test6 import *
def keyword_adjustment_optimized(user_input):
    with open('data/keyword.yml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    names = data['nlu'][0]['examples'].replace('- ', '').split('\n')
    # names_without_space = [name.replace(' ', '') for name in names]

    # 創建名字的小寫版本set以提高查找效率
    names_set = {name.lower() for name in names}

    # 提取用戶輸入中的英文字詞並轉成小寫
    english_words = re.findall(r'[A-Za-z0-9]+', user_input.lower())
    print(f"中文模型裡面的english_words = {english_words}")

    # 基本匹配檢查
    for word in english_words:
        if word in names_set:
            return user_input, True  # 如果找到精確匹配，直接返回

    # 如果基本匹配未找到，進行模糊匹配
    for word in english_words:
        for name in names:
            if fuzz.partial_ratio(word, name.lower()) > 80:
                user_input = user_input.replace(word, name)
                return user_input, True

    return user_input, False  # 如果都沒找到匹配，返回原輸入


def get_zh_indexes(user_input, json_filename):
    print(f"原本的輸入: {user_input}")
    user_input, find_singer = keyword_adjustment_optimized(user_input)
    print(f"經過方程式後的輸入: {user_input}")
    result = asyncio.run(zh_agent.parse_message(user_input))
    print('zh', result)
    print(f'find singer?', find_singer)  # from function
    print(f"intent: {result['intent']['name']}")
    print(f"score: {result['intent']['confidence']}")
    if result['intent']['confidence'] > 0.6:
        print('信心程度大於六成')
    print('--')

    if len(result['entities']) == 0:
        """
        鄭伊健 (Ekin Cheng) 名字必須分開
        """
        print('No Entities')
    else:
        if result['intent']['name'] == "query_ticket_time":
            ticket_time_indexes = zh_get_ticket_time(user_input, json_filename)

            found_keyword = False
            keyword_indexes = []

            for i in range(len(result['entities'])):
                if result['entities'][i]['value']:
                    print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
                    if result['entities'][i]['entity'] == 'keyword':
                        found_keyword = True
                        keyword_index = get_keyword_indexes_zh(result['entities'][i]['value'], json_filename)
                        print(f"keyword_index = {keyword_index}")
                        keyword_indexes.extend(keyword_index)

            if found_keyword and ticket_time_indexes:
                print('取集合')
                print(f"ticket_time_indexes = {ticket_time_indexes}")
                print(f"keyword_indexes = {keyword_indexes}")
                print('取集合')
                intersection = [item for item in keyword_indexes if item in ticket_time_indexes]
                print(f"intersection = {intersection}")
                return intersection
            elif not found_keyword and ticket_time_indexes:
                print('直接搜尋售票時間')
                print(f"ticket_time_indexes = {ticket_time_indexes}")
                return ticket_time_indexes
            elif found_keyword and not ticket_time_indexes:
                print('直接搜尋keyword')
                print(f"keyword_indexes = {keyword_indexes}")
                return keyword_indexes
            else:
                print('直接回傳找不到')
                return []

        elif result['intent']['name'] == "query_keyword":
            found_datetime_city = False
            found_keyword = False
            keyword_indexes = []
            for i in range(len(result['entities'])):
                if result['entities'][i]['value']:
                    print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")

                    if result['entities'][i]['entity'] == 'datetime' or result['entities'][i]['entity'] == 'city':
                        found_datetime_city = True
                        print(f"found_datetime_city = {found_datetime_city}")

                    if result['entities'][i]['entity'] == 'keyword':
                        found_keyword = True
                        keyword_index = get_keyword_indexes_zh(result['entities'][i]['value'], json_filename)
                        print(f"keyword_index = {keyword_index}")
                        keyword_indexes.extend(keyword_index)

            if found_keyword and found_datetime_city:
                print('取集合')
                print(f"keyword_indexes = {keyword_indexes}")
                dates_cities_indexes = zh_dates_cities(user_input, json_filename)
                print(f"dates_cities_indexes = {dates_cities_indexes}")
                print('取集合')
                intersection = [item for item in keyword_indexes if item in dates_cities_indexes]
                print(f"intersection = {intersection}")
                return intersection
            elif not found_keyword and found_datetime_city:
                print('只搜尋日期')
                dates_cities_indexes = zh_dates_cities(user_input, json_filename)
                print(f"dates_cities_indexes = {dates_cities_indexes}")
                return dates_cities_indexes
            elif found_keyword and not found_datetime_city:
                print('只搜尋關鍵字')
                print(f"keyword_indexes = {keyword_indexes}")
                return keyword_indexes
            else:
                print('找不到關鍵字，也找不到日期，那就直接搜尋keyword_indexes')
                keyword_index = get_keyword_indexes_zh(user_input, json_filename)
                print(f"keyword_index = {keyword_index}")
                return keyword_index


async def get_en_indexes(user_input, json_filename):
    with open('en_data/keyword.yml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    names = data['nlu'][0]['examples'].replace('- ', '').split('\n')
    names = [name.replace(' ', '') for name in names]

    print_success("NLU model loaded. Type a message and press enter to parse it.")
    message = user_input.lower()
    print(f'ori msg: {message}')

    result = en_agent.parse_message(message)

    print(f"intent: {result['intent']['name']}")
    print(f"score: {result['intent']['confidence']}")
    if result['intent']['confidence'] > 0.6:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('--')
    if len(result['entities']) == 0:
        print('No Entities')
    else:
        if result['intent']['name'] == "query_ticket_time":
            ticket_time_indexes = en_get_ticket_time(user_input, json_filename)
            print(f"ticket_time_indexes = {ticket_time_indexes}")
            return ticket_time_indexes
        elif result['intent']['name'] == "query_keyword":
            keywords = []
            found_datetime = False

            for i in range(len(result['entities'])):
                if result['entities'][i]['entity'] == 'datetime':
                    found_datetime = True
                elif result['entities'][i]['entity'] == 'keyword':
                    keywords.append(result['entities'][i]['value'])

            if keywords:
                keyword = max(keywords, key=len)

                found_keyword = False
                for j, name in enumerate(names):
                    if name.lower() == keyword.lower():
                        keyword = names[j]
                        found_keyword = True
                        break

                if not found_keyword:
                    print('沒有在keyword.yml當中找到keyword')
                    keyword = keyword.title()
                else:
                    print('有在keyword.yml當中找到keyword')

                print(f"keyword = {keyword}")
                if found_datetime:
                    print('有keyword，也有datetime，取集合')
                    en_dates_cities_indexes = en_dates_cities(user_input, json_filename)
                    print(f"en_dates_cities_indexes = {en_dates_cities_indexes}")
                    get_keyword_indexes_en_indexes = get_keyword_indexes_en(keyword, json_filename)
                    print(f"get_keyword_indexes_en_indexes = {get_keyword_indexes_en_indexes}")
                    intersection = [item for item in get_keyword_indexes_en_indexes if item in en_dates_cities_indexes]
                    print(f"intersection = {intersection}")
                    return intersection
                else:
                    print('有keyword，但是沒有datetime，直接顯示keyword indexes')
                    get_keyword_indexes_en_indexes = get_keyword_indexes_en(keyword, json_filename)
                    print(f"get_keyword_indexes_en_indexes = {get_keyword_indexes_en_indexes}")
                    return get_keyword_indexes_en_indexes
            else:
                print('沒有keyword')
                if found_datetime:
                    en_dates_cities_indexes = en_dates_cities(user_input, json_filename)
                    print(f"en_dates_cities_indexes = {en_dates_cities_indexes}")
                    return en_dates_cities_indexes
                else:
                    print('沒有keyword，也沒有日期，直接把user_input拿去keyword搜尋')
                    get_keyword_indexes_en_indexes = get_keyword_indexes_en(user_input, json_filename)
                    print(f"get_keyword_indexes_en_indexes = {get_keyword_indexes_en_indexes}")
                    return get_keyword_indexes_en_indexes


# def get_en_indexes(user_input, json_filename):
#     print(f"原本的輸入: {user_input}")
#     user_input, find_singer = keyword_adjustment_optimized(user_input)
#     print(f"經過方程式後的輸入: {user_input}")
#     result = asyncio.run(en_agent.parse_message(user_input))
#     print(result)
#
#     print(f'find singer?', find_singer)  # from function
#     print(f"intent: {result['intent']['name']}")
#     print(f"score: {result['intent']['confidence']}")
#     if result['intent']['confidence'] > 0.6:
#         print('信心程度大於六成')
#     print('--')
#     if len(result['entities']) == 0:
#         """
#         鄭伊健 (Ekin Cheng) 名字必須分開
#         """
#         print('No Entities')
#     else:
#         found_datetime_city = False
#         keyword_indexes = []
#         for i in range(len(result['entities'])):
#             if result['entities'][i]['value']:
#                 print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
#
#                 if result['entities'][i]['entity'] == 'datetime' or result['entities'][i]['entity'] == 'city':
#                     found_datetime_city = True
#                     print(f"found_datetime_city = {found_datetime_city}")
#
#                 if result['entities'][i]['entity'] == 'keyword':
#                     keyword_index = get_keyword_indexes_en(result['entities'][i]['value'], json_filename)
#                     print(f"keyword_index = {keyword_index}")
#                     keyword_indexes.extend(keyword_index)
#
#         if keyword_indexes and found_datetime_city:
#             print('取集合')
#             print(f"keyword_indexes = {keyword_indexes}")
#             dates_cities_indexes = en_dates_cities(user_input, json_filename)
#             print(f"dates_cities_indexes = {dates_cities_indexes}")
#             intersection = [item for item in keyword_indexes if item in dates_cities_indexes]
#             print(f"intersection = {intersection}")
#             return intersection
#         elif not keyword_indexes and found_datetime_city:
#             print('只搜尋日期')
#             dates_cities_indexes = en_dates_cities(user_input, json_filename)
#             print(f"dates_cities_indexes = {dates_cities_indexes}")
#             return dates_cities_indexes
#         elif keyword_indexes and not found_datetime_city:
#             print('只搜尋關鍵字')
#             print(f"keyword_indexes = {keyword_indexes}")
#             return keyword_indexes
#         else:
#             print('直接回傳找不到')
#             return []


# def get_indexes(user_input, json_filename):
#     print(f"原本的輸入: {user_input}")
#     if "zh" in json_filename:
#         user_input, find_singer = keyword_adjustment_optimized(user_input)
#         print(f"經過方程式後的輸入: {user_input}")
#         result = asyncio.run(zh_agent.parse_message(user_input))
#         print('zh', result)
#         print(f'find singer?', find_singer)  # from function
#         print(f"intent: {result['intent']['name']}")
#         print(f"score: {result['intent']['confidence']}")
#         if result['intent']['confidence'] > 0.6:
#             print('信心程度大於六成')
#         print('--')
#     elif "en" in json_filename:
#         result = asyncio.run(en_agent.parse_message(user_input))
#         print('en', result)
#
#     # user_input, find_singer = keyword_adjustment_optimized(user_input)
#     # print(f"經過方程式後的輸入: {user_input}")
#     # if "zh" in json_filename:
#     #     result = asyncio.run(zh_agent.parse_message(user_input))
#     # elif "en" in json_filename:
#     #     result = asyncio.run(en_agent.parse_message(user_input))
#     # print(result)
#     #
#     # print(f'find singer?', find_singer)  # from function
#     # print(f"intent: {result['intent']['name']}")
#     # print(f"score: {result['intent']['confidence']}")
#     # if result['intent']['confidence'] > 0.6:
#     #     print('信心程度大於六成')
#     # print('--')
#     if len(result['entities']) == 0:
#         """
#         鄭伊健 (Ekin Cheng) 名字必須分開
#         """
#         print('No Entities')
#     else:
#         found_datetime_city = False
#         found_keyword = False
#         keyword_indexes = []
#         for i in range(len(result['entities'])):
#             if result['entities'][i]['value']:
#                 print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
#
#                 if result['entities'][i]['entity'] == 'datetime' or result['entities'][i]['entity'] == 'city':
#                     found_datetime_city = True
#                     print(f"found_datetime_city = {found_datetime_city}")
#
#                 if result['entities'][i]['entity'] == 'keyword':
#                     found_keyword = True
#                     if "zh" in json_filename:
#                         keyword_index = get_keyword_indexes_zh(result['entities'][i]['value'], json_filename)
#                     elif "en" in json_filename:
#                         keyword_index = get_keyword_indexes_en(result['entities'][i]['value'], json_filename)
#                     print(f"keyword_index = {keyword_index}")
#                     keyword_indexes.extend(keyword_index)
#
#         if found_keyword and found_datetime_city:
#             print('取集合')
#             print(f"keyword_indexes = {keyword_indexes}")
#             if "zh" in json_filename:
#                 dates_cities_indexes = zh_dates_cities(user_input, json_filename)
#             elif "en" in json_filename:
#                 dates_cities_indexes = en_dates_cities(user_input, json_filename)
#             print(f"dates_cities_indexes = {dates_cities_indexes}")
#             intersection = [item for item in keyword_indexes if item in dates_cities_indexes]
#             print(f"intersection = {intersection}")
#             return intersection
#         elif not found_keyword and found_datetime_city:
#             print('只搜尋日期')
#             if "zh" in json_filename:
#                 dates_cities_indexes = zh_dates_cities(user_input, json_filename)
#             elif "en" in json_filename:
#                 dates_cities_indexes = en_dates_cities(user_input, json_filename)
#             print(f"dates_cities_indexes = {dates_cities_indexes}")
#             return dates_cities_indexes
#         elif found_keyword and not found_datetime_city:
#             print('只搜尋關鍵字')
#             print(f"keyword_indexes = {keyword_indexes}")
#             return keyword_indexes
#         else:
#             print('直接回傳找不到')
#             return []

""" zh config """
zh_model_path = r'models\nlu-20240501-165733-frayed-acre.tar.gz'  # zh model
zh_agent = Agent.load(zh_model_path)
zh_json = "concert_zh.json"

""" en config """
en_model_path = r'en_models\nlu-20240511-033142-brilliant-set.tar.gz'
en_agent = Agent.load(en_model_path)
en_json = "concert_en.json"

"""
獲得時間 en_dates_cities
獲得keyword get_keyword_indexes_en
獲得售票時間 en_get_ticket_time
"""


def show_concert_info(indexes, language):
    if not indexes:
        return [
            "對不起，我沒有找到相關的演唱會資訊。" if language == 'zh' else "Sorry, I couldn't find any relevant concert information."]

    formatted_str_list = []
    if language == 'zh':
        data = read_json("concert_zh.json")
        print('zh', len(data))
    elif language == 'en':
        data = read_json("concert_en.json")
        print('en', len(data))

    for index in indexes:
        if index >= len(data):
            print(f"索引 {index} 超出範圍，最大索引值應該小於 {len(data)}")
            continue

        concert = data[index]

        if concert['prc']:
            sorted_prices = sorted(concert['prc'], reverse=True)
            sorted_prices_str = ', '.join(map(str, sorted_prices))
        else:
            sorted_prices_str = '-'
        concert_date_str = ', '.join(concert['pdt'])

        if concert['sdt']:
            sale_date_str = ', '.join(concert['sdt'])
        else:
            sale_date_str = '-'

        if concert['loc']:
            location_str = ', '.join(concert['loc'])
        else:
            location_str = '-'

        if language == 'zh':
            formatted_str = f"""
- {concert['tit']}
- 日期: {concert_date_str}
- 票價: {sorted_prices_str}
- 售票日期: {sale_date_str}
- 地點: {location_str}
{concert['url']}
            """
        elif language == 'en':
            formatted_str = f"""
- {concert['tit']}
- Date: {concert_date_str}
- Ticket Price: {sorted_prices_str}
- Sale Date: {sale_date_str}
- Location: {sale_date_str}
{concert['url']}
            """

        formatted_str_list.append(formatted_str.strip())

    return formatted_str_list

current_language = 'en'
print('載入完成')
while True:
    user_input = input("請輸入: ")
    if user_input.lower() == 'zh' or user_input.lower() == 'en':
        current_language = user_input.lower()  # 更新當前語言為用戶輸入的值
        print(f"切換語言為 {current_language}")
    else:
        if current_language == 'zh':
            found_indexes = get_zh_indexes(user_input, zh_json)
            print(f"found_indexes = {found_indexes}")
            messages = show_concert_info(found_indexes, "zh")
            for msg in messages:
                print(msg)
                print('---')
        elif current_language == 'en':
            found_indexes = get_en_indexes(user_input, en_json)
            print(f"found_indexes = {found_indexes}")
            messages = show_concert_info(found_indexes, "en")
            for msg in messages:
                print(msg)
                print('---')
    print('-----------------------------------------------')


    """"""
    # found_indexes = get_en_indexes(user_input, en_json)  # 根據json檔案決定語言
    # print(f"found_indexes = {found_indexes}")
    # data = read_json("concert_en.json")
    # print("en_dates_cities")
    # en_dates_cities_indexes = en_dates_cities(user_input, en_json)
    # print(f"en_dates_cities_indexes = {en_dates_cities_indexes}")
    # if en_dates_cities_indexes:
    #     for index in en_dates_cities_indexes:
    #         print(data[index]['tit'])
    # print('---')
    # print("get_keyword_indexes_en")
    # get_keyword_indexes_en_indexes = get_keyword_indexes_en(user_input, en_json)
    # print(f"get_keyword_indexes_en_indexes = {get_keyword_indexes_en_indexes}")
    # if get_keyword_indexes_en_indexes:
    #     for index in get_keyword_indexes_en_indexes:
    #         print(data[index]['tit'])
    # print('---')
    # print("en_get_ticket_time")
    # en_get_ticket_time_indexes = en_get_ticket_time(user_input, en_json)
    # print(f"en_get_ticket_time_indexes = {en_get_ticket_time_indexes}")
    # if en_get_ticket_time_indexes:
    #     for index in en_get_ticket_time_indexes:
    #         print(data[index]['tit'])

    # print(f"原本的輸入: {user_input}")
    # user_input, find_singer = keyword_adjustment_optimized(user_input)
    # print(f"經過方程式後的輸入: {user_input}")
    # result = asyncio.run(zh_agent.parse_message(user_input))
    # print(result)
    #
    # print(f'find singer?', find_singer)  # from function
    # print(f"intent: {result['intent']['name']}")
    # print(f"score: {result['intent']['confidence']}")
    # if result['intent']['confidence'] > 0.6:
    #     print('信心程度大於六成')
    # print('--')
    # if len(result['entities']) == 0:
    #     """
    #     鄭伊健 (Ekin Cheng) 名字必須分開
    #     """
    #     print('No Entities')
    # else:
    #     found_datetime_city = False
    #     keyword_indexes = []
    #     for i in range(len(result['entities'])):
    #         if result['entities'][i]['value']:
    #             print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
    #
    #             if result['entities'][i]['entity'] == 'datetime' or result['entities'][i]['entity'] == 'city':
    #                 found_datetime_city = True
    #                 print(f"found_datetime_city = {found_datetime_city}")
    #
    #             if result['entities'][i]['entity'] == 'keyword':
    #                 keyword_index = get_keyword_indexes(result['entities'][i]['value'], zh_json)
    #                 print(f"keyword_index = {keyword_index}")
    #                 keyword_indexes.extend(keyword_index)
    #
    #     if keyword_indexes and found_datetime_city:
    #         print('取集合')
    #         print(f"keyword_indexes = {keyword_indexes}")
    #         dates_cities_indexes = zh_dates_cities(user_input, zh_json)
    #         print(f"dates_cities_indexes = {dates_cities_indexes}")
    #         intersection = [item for item in keyword_indexes if item in dates_cities_indexes]
    #         print(f"intersection = {intersection}")
    #     elif not keyword_indexes and found_datetime_city:
    #         print('只搜尋日期')
    #         dates_cities_indexes = zh_dates_cities(user_input, zh_json)
    #         print(f"dates_cities_indexes = {dates_cities_indexes}")
    #     elif keyword_indexes and not found_datetime_city:
    #         print('只搜尋關鍵字')
    #         print(f"keyword_indexes = {keyword_indexes}")
    #     else:
    #         print('直接回傳找不到')
