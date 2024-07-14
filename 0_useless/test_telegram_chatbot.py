import asyncio
import logging
from typing import Text

from typing import Final  # 引入Final類型，用於定義常量

from telegram import Update  # 從telegram模組引入Update類
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes  # 從telegram.ext模組引入多個類和模組

from rasa.core.agent import Agent
from rasa.shared.utils.cli import print_info, print_success
from rasa.shared.utils.io import json_to_string

import re

from get_city_date_indexes import en_dates_cities, zh_dates_cities

from get_keyword_indexes_zh import get_keyword_indexes, keyword_adjustment, get_language

zh_model = r"models\nlu-20240312-042044-vibrato-modern.tar.gz"
en_model = 'models/model_en.tar.gz'

agent_zh = Agent.load(zh_model)  # 載入中文模型
agent_en = Agent.load(en_model)  # 載入英文模型

zh_json = 'concert_data_old_zh.json'  # 中文演唱會資料
en_json = 'concert_data_old_en.json'  # 英文演唱會資料

# while True:
#     print(f'---\n請輸入')
#     user_input = input().lower()
#     language = get_language(user_input)
#     user_input, find_english_singer = keyword_adjustment(user_input)  # 修正歌手的名稱 # find_singer 不知道有沒有用上 先放著
#     print(f'經過 keyword adjustment之後 user input: {user_input}')
#     if language == 'zh':
#         dates_cities_indexes = zh_dates_cities(user_input, zh_json)
#         print(f'dates_cities_indexes = {dates_cities_indexes}')
#         # user_input 進入模型
#         # 判斷這個句子的intent以及有什麼keyword
#         result = asyncio.run(agent_zh.parse_message(user_input))
#         # intent - 售票時間
#         if result['intent']['name'] == 'query_ticket_time':
#             print('執行query_ticket_time')
#         # intent - keyword
#         elif result['intent']['name'] == 'query_keyword':
#             print('執行query_keyword')
#
#             keyword_indexes = None
#             for i in range(len(result['entities'])):
#                 if result['entities'][i]['entity'] == 'keyword':  # 找到的歌手
#                     keyword_indexes = []
#             if keyword_indexes is None:
#                 pass
#             else:  # 有找到keyword
#                 print('找到keyword')
#                 for i in range(len(result['entities'])):  # 先獲得keyword的全部位置
#                     print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
#                     if result['entities'][i]['entity'] == 'keyword':
#                         print(f"found keyword = {result['entities'][i]['value']}")
#                         print(f"found keyword indexes = {get_keyword_indexes(result['entities'][i]['value'], en_json)}")
#                         keyword_indexes.extend(get_keyword_indexes(result['entities'][i]['value'], zh_json))  # 只搜尋keyword
#                     else:
#                         print('不是keyword 跳過')
#
#             print('中文模型')
#             if dates_cities_indexes is None:
#                 if keyword_indexes is None:
#                     keyword_indexes = get_keyword_indexes(user_input, zh_json)  # 搜尋整個句子
#                     print(f'1 return keyword_indexes\n{keyword_indexes}')
#                 elif not keyword_indexes:
#                     print('2 return []')
#                 elif keyword_indexes:
#                     print(f'3 return keyword_indexes\n{keyword_indexes}')
#             elif not dates_cities_indexes:
#                 print('4 return []')
#             elif dates_cities_indexes:
#                 if keyword_indexes is None:
#                     print(f'5 return dates_cities_indexes\n{dates_cities_indexes}')
#                 elif not keyword_indexes:
#                     print('6 return []')
#                 elif keyword_indexes:
#                     print('7 return 兩者集合\n[...]')
#             #     if dates_cities is None:
#             #         print('句子裡面沒有日期或城市')
#             #         print('直接使用bm25搜尋這個句子')
#             #         keyword_indexes = get_keyword_indexes(user_input, zh_json)
#             #         print(f'keyword_indexes = {keyword_indexes}')
#             #     elif not dates_cities:
#             #         print('句子裡面有城市或日期，但是沒有匹配的資料')
#             #         print('return []')
#             #     elif dates_cities:  # 但是有日期
#             #         print('句子裡面有城市或日期，找到匹配城市或日期')
#             #         print('date_cities', dates_cities)
#             #
#
#
#             #
#             #     if keyword_indexes:
#             #         print('且匹配到keyword')
#             #         if dates_cities:
#             #             print('匹配到dates_cities')
#             #             print('取集合')
#             #         elif dates_cities is None:
#             #             print('句子當中沒有日期或是城市')
#             #             print('return keyword_indexes')
#             #         elif not dates_cities:
#             #             print('句子有日期或是城市 但是沒有匹配到')
#             #             print('return []')
#             #     else:
#             #         print('但是沒有匹配到keyword')
#             #         if dates_cities:
#             #             print('沒有keyword ')
#                 # if keyword_indexes and dates_cities:  # 有匹配到keyword 也有匹配到城市或日期 取集合
#                 #     print('有匹配到keyword 也有匹配到城市或日期 取集合')
#                 #     print('keyword_indexes', keyword_indexes)
#                 #     print('date_cities', dates_cities)
#                 #     print('取集合')
#                 # elif not keyword_indexes and dates_cities:  # 有keyword 但是沒有匹配到資料 但是有匹配到日期或城市
#                 #     print('有keyword 但是沒有匹配到資料 但是有匹配到日期或城市')
#                 #     print('return []')
#                 # elif keyword_indexes and dates_cities is None:  # 有keyword
#                 #     print('句子當中只有keyword 沒有日期或是城市')
#                 #     print(f'keyword_indexes = {keyword_indexes}')
#                 # elif keyword_indexes and not dates_cities:
#                 #     print('keyword有找到資料，但日期或城市沒有匹配的資料')
#                 #     print('return []')
#                 # else:
#                 #     print('我為什麼在這裡?')
#
#     elif language == 'en':
#         dates_cities_indexes = en_dates_cities(user_input, en_json)
#         print(f'dates_cities_indexes = {dates_cities_indexes}')
#         # user_input 進入模型
#         # 判斷這個句子的intent以及有什麼keyword
#         result = asyncio.run(agent_en.parse_message(user_input))
#         # intent - 售票時間
#         if result['intent']['name'] == 'query_ticket_time':
#             print('執行query_ticket_time')
#         # intent - keyword
#         elif result['intent']['name'] == 'query_keyword':
#             print('執行query_keyword')
#
#             keyword_indexes = None
#             for i in range(len(result['entities'])):
#                 if result['entities'][i]['entity'] == 'keyword':
#                     keyword_indexes = []
#             if keyword_indexes is None:
#                 pass
#             else:  # 有找到keyword
#                 print('找到keyword')
#                 for i in range(len(result['entities'])):  # 先獲得keyword的全部位置
#                     print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
#                     if result['entities'][i]['entity'] == 'keyword':
#                         print(f"found keyword = {result['entities'][i]['value']}")
#                         print(f"found keyword indexes = {get_keyword_indexes(result['entities'][i]['value'], en_json)}")
#                         keyword_indexes.extend(
#                             get_keyword_indexes(result['entities'][i]['value'], en_json))  # 只搜尋keyword
#                     else:
#                         print('不是keyword 跳過')
#
#             print('英文模型')
#             if dates_cities_indexes is None:
#                 if keyword_indexes is None:
#                     keyword_indexes = get_keyword_indexes(user_input, en_json)  # 搜尋整個句子
#                     print(f'1 return keyword_indexes\n{keyword_indexes}')
#                 elif not keyword_indexes:
#                     print('2 return []')
#                 elif keyword_indexes:
#                     print(f'3 return keyword_indexes\n{keyword_indexes}')
#             elif not dates_cities_indexes:
#                 print('4 return []')
#             elif dates_cities_indexes:
#                 if keyword_indexes is None:
#                     print(f'5 return dates_cities_indexes\n{dates_cities_indexes}')
#                 elif not keyword_indexes:
#                     print('6 return []')
#                 elif keyword_indexes:
#                     print('7 return 兩者集合\n[...]')
#         # 模型 判斷意圖
#         # result = asyncio.run(agent_en.parse_message(user_input))
#         # # 售票時間
#         # if result['intent']['name'] == 'query_ticket_time':
#         #     print('執行query_ticket_time')
#         # # keyword
#         # elif result['intent']['name'] == 'query_keyword':
#         #     print('執行query_keyword')
#         #     if len(result['entities']) == 0:
#         #         print('No Entities')
#         #     else:
#         #         keyword_indexes = []
#         #         for i in range(len(result['entities'])):
#         #             print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
#         #         if keyword_indexes:
#         #             print('keyword_indexes', keyword_indexes)
#         #             print('date_cities', dates_cities)
#         #         else:
#         #             print('搜尋了關鍵字 但是沒有找到')
#         # keyword_indexes = get_keyword_indexes(user_input, en_json)  # 獲取的keyword進行搜尋
#         # print(f'keyword indexes {keyword_indexes}')
#     # 中文 城市 時間
#     # 英文 城市 時間
#     # print('可以開始了')
#     # while True:
#     #     try:
#     #         user_input = input().lower()
#     #         chinese_pattern = re.compile(r'[\u4e00-\u9fa5]')
#     #         if bool(chinese_pattern.search(user_input)):
#     #             # 中文
#     #             dates_cities_indexes = zh_dates_cities(user_input, zh_json)
#     #             print('dates, city', dates_cities_indexes)
#     #
#     #             result = asyncio.run(agent_zh.parse_message(user_input))
#     #             # keyword_indexes = get_keyword_indexes(user_input, zh_json)
#     #             # print('keyword', keyword_indexes)
#     #         else:
#     #             # 英文
#     #             dates_cities_indexes = en_dates_cities(user_input, en_json)
#     #             print('dates, city', dates_cities_indexes)
#     #
#     #             result = asyncio.run(agent_en.parse_message(user_input))
#     #             for i in range(len(result['entities'])):
#     #                 if result['entities'][i]['entity'] == 'keyword':
#     #                     print(result['entities'][i]['value'])
#     #                 # print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
#     #             # keyword_indexes = get_keyword_indexes(user_input, en_json)
#     #             # print('keyword', keyword_indexes)
#     #
#     #         # print(result)
#     #         # print('city & dates', dates_cities_indexes)
#     #         # print('keyword', keyword_indexes)
#     #
#     #         print('---')
#     #     except:
#     #         print('輸入錯誤 可以麻煩你再輸入一次嗎')
#     #         continue
""" 註解版本 """
# 這個無限循環將一直執行，除非明確中斷或出現未處理的錯誤
while True:
    # 提示用戶輸入
    print(f'---\n請輸入')
    # 讀取用戶輸入並將其轉換為小寫以進行標準化
    user_input = input().lower()
    # 判斷用戶輸入的語言
    language = get_language(user_input)
    # 調整用戶輸入中的歌手名稱關鍵字；find_singer 的功能尚不清楚
    # user_input, find_english_singer = keyword_adjustment(user_input)
    # 輸出經過關鍵字調整後的用戶輸入
    print(f'經過 keyword adjustment之後 user input: {user_input}')

    # 根據語言分支處理
    if language == 'zh':
        # 處理中文輸入時的日期和城市索引
        dates_cities_indexes = zh_dates_cities(user_input, zh_json)
        print(f'dates_cities_indexes = {dates_cities_indexes}')

        # 異步運行中文語言模型來解析訊息
        result = asyncio.run(agent_zh.parse_message(user_input))
        # 處理“查詢售票時間”的意圖
        if result['intent']['name'] == 'query_ticket_time':
            print('執行query_ticket_time')
        # 處理“查詢關鍵字”的意圖
        elif result['intent']['name'] == 'query_keyword':
            print('執行query_keyword')
            # 初始化用於存儲關鍵字索引的變量
            keyword_indexes = None
            # 遍歷實體，尋找關鍵字
            for i in range(len(result['entities'])):
                if result['entities'][i]['entity'] == 'keyword':
                    keyword_indexes = []
            # 如果沒有找到關鍵字則繼續
            if keyword_indexes is None:
                pass
            else:  # 如果找到了關鍵字
                print('找到keyword')
                # 處理每一個找到的關鍵字
                for i in range(len(result['entities'])):
                    print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
                    if result['entities'][i]['entity'] == 'keyword':
                        print(f"found keyword = {result['entities'][i]['value']}")
                        print(f"found keyword indexes = {get_keyword_indexes(result['entities'][i]['value'], zh_json)}")
                        keyword_indexes.extend(get_keyword_indexes(result['entities'][i]['value'], zh_json))  # 只搜索關鍵字
                    else:
                        print('不是keyword 跳過')
            # 處理日期和城市索引
            if dates_cities_indexes is None:
                if keyword_indexes is None:
                    keyword_indexes = get_keyword_indexes(user_input, zh_json)  # 搜索整個句子
                    print(f'1 return keyword_indexes\n{keyword_indexes}')
                elif not keyword_indexes:
                    print('2 return []')
                elif keyword_indexes:
                    print(f'3 return keyword_indexes\n{keyword_indexes}')
            elif not dates_cities_indexes:
                print('4 return []')
            elif dates_cities_indexes:
                if keyword_indexes is None:
                    print(f'5 return dates_cities_indexes\n{dates_cities_indexes}')
                elif not keyword_indexes:
                    print('6 return []')
                elif keyword_indexes:
                    print('7 return 兩者集合\n[...]')

    elif language == 'en':
        # 處理英文輸入時的日期和城市索引
        dates_cities_indexes = en_dates_cities(user_input, en_json)
        print(f'dates_cities_indexes = {dates_cities_indexes}')
        # 異步運行英文語言模型來解析訊息
        result = asyncio.run(agent_en.parse_message(user_input))
        # 處理“查詢售票時間”的意圖
        if result['intent']['name'] == 'query_ticket_time':
            print('執行query_ticket_time')
        # 處理“查詢關鍵字”的意圖
        elif result['intent']['name'] == 'query_keyword':
            print('執行query_keyword')
            # 初始化用於存儲關鍵字索引的變量
            keyword_indexes = None
            # 遍歷實體，尋找關鍵字
            for i in range(len(result['entities'])):
                if result['entities'][i]['entity'] == 'keyword':
                    keyword_indexes = []
            # 如果沒有找到關鍵字則繼續
            if keyword_indexes is None:
                pass
            else:  # 如果找到了關鍵字
                print('找到keyword')
                # 處理每一個找到的關鍵字
                for i in range(len(result['entities'])):
                    print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
                    if result['entities'][i]['entity'] == 'keyword':
                        print(f"found keyword = {result['entities'][i]['value']}")
                        print(f"found keyword indexes = {get_keyword_indexes(result['entities'][i]['value'], en_json)}")
                        keyword_indexes.extend(
                            get_keyword_indexes(result['entities'][i]['value'], en_json))  # 只搜索關鍵字
                    else:
                        print('不是keyword 跳過')
            # 處理日期和城市索引
            if dates_cities_indexes is None:
                if keyword_indexes is None:
                    keyword_indexes = get_keyword_indexes(user_input, en_json)  # 搜索整個句子
                    print(f'1 return keyword_indexes\n{keyword_indexes}')
                elif not keyword_indexes:
                    print('2 return []')
                elif keyword_indexes:
                    print(f'3 return keyword_indexes\n{keyword_indexes}')
            elif not dates_cities_indexes:
                print('4 return []')
            elif dates_cities_indexes:
                if keyword_indexes is None:
                    print(f'5 return dates_cities_indexes\n{dates_cities_indexes}')
                elif not keyword_indexes:
                    print('6 return []')
                elif keyword_indexes:
                    print('7 return 兩者集合\n[...]')
