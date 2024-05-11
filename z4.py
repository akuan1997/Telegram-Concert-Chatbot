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

from y_example_read_json import *

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
    print(f"english_words = {english_words}")

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
                print('直接回傳找不到')
                return []


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

def get_en_indexes(user_input, json_filename):
    pass
zh_model_path = r'models\nlu-20240501-165733-frayed-acre.tar.gz'  # zh model
zh_agent = Agent.load(zh_model_path)
en_model_path = r'models\nlu-20240505-013208-fixed-itinerary.tar.gz'
en_agent = Agent.load(en_model_path)
zh_json = "concert_zh.json"
en_json = "concert_en.json"
print('載入完成')
"""
獲得時間 en_dates_cities
獲得keyword get_keyword_indexes_en
獲得售票時間 en_get_ticket_time
"""
while True:
    user_input = input("請輸入: ")
    # found_indexes = get_zh_indexes(user_input, zh_json)  # 根據json檔案決定語言
    # print(f"found_indexes = {found_indexes}")
    # found_indexes = get_en_indexes(user_input, en_json)  # 根據json檔案決定語言
    # print(f"found_indexes = {found_indexes}")
    data = read_json("concert_en.json")
    print("en_dates_cities")
    en_dates_cities_indexes = en_dates_cities(user_input, en_json)
    print(f"en_dates_cities_indexes = {en_dates_cities_indexes}")
    if en_dates_cities_indexes:
        for index in en_dates_cities_indexes:
            print(data[index]['tit'])
    print('---')
    print("get_keyword_indexes_en")
    get_keyword_indexes_en_indexes = get_keyword_indexes_en(user_input, en_json)
    print(f"get_keyword_indexes_en_indexes = {get_keyword_indexes_en_indexes}")
    if get_keyword_indexes_en_indexes:
        for index in get_keyword_indexes_en_indexes:
            print(data[index]['tit'])
    print('---')
    print("en_get_ticket_time")
    en_get_ticket_time_indexes = en_get_ticket_time(user_input, en_json)
    print(f"en_get_ticket_time_indexes = {en_get_ticket_time_indexes}")
    if en_get_ticket_time_indexes:
        for index in en_get_ticket_time_indexes:
            print(data[index]['tit'])
    print('-----------------------------------------------')
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

