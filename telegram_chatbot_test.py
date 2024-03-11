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

from get_keyword_indexes import get_keyword_indexes, keyword_adjustment, get_language

zh_model = r"models\nlu-20240312-042044-vibrato-modern.tar.gz"
en_model = 'models/model_en.tar.gz'

agent_zh = Agent.load(zh_model)  # 載入中文模型
# agent_en = Agent.load(en_model)  # 載入英文模型

zh_json = 'concert_data_old_zh.json'  # 中文演唱會資料
en_json = 'concert_data_old_en.json'  # 英文演唱會資料

print('可以開始了')
while True:
    user_input = input().lower()
    language = get_language(user_input)
    user_input, find_english_singer = keyword_adjustment(user_input)  # 修正歌手的名稱 # find_singer 不知道有沒有用上 先放著
    print(f'經過 keyword adjustment之後 user input: {user_input}')
    if language == 'zh':
        print('中文模型')
        dates_cities = zh_dates_cities(user_input, zh_json)
        print(dates_cities)
        # user_input 進入模型
        # 判斷這個句子的intent以及有什麼keyword
        result = asyncio.run(agent_zh.parse_message(user_input))
        # intent - 售票時間
        if result['intent']['name'] == 'query_ticket_time':
            print('執行query_ticket_time')
        # intent - keyword
        elif result['intent']['name'] == 'query_keyword':
            print('執行query_keyword')
            if len(result['entities']) == 0:  # 沒有找到keyword
                print('句子裡面沒有keyword')
                if dates_cities is None:
                    print('句子裡面沒有日期或城市')
                    print('直接使用bm25搜尋這個句子')
                    keyword_indexes = get_keyword_indexes(user_input, zh_json)
                    print(f'keyword_indexes = {keyword_indexes}')
                elif not dates_cities:
                    print('句子裡面有城市或日期，但是沒有匹配的資料')
                    print('return []')
                elif dates_cities:  # 但是有日期
                    print('句子裡面有城市或日期，找到匹配城市或日期')
                    print('date_cities', dates_cities)

            else:  # 有找到keyword
                print('找到keyword')
                keyword_indexes = []
                for i in range(len(result['entities'])):  # 先獲得keyword的全部位置
                    print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
                    keyword_indexes.extend(get_keyword_indexes(result['entities'][i]['value'], zh_json))

                if keyword_indexes and dates_cities:  # 有keyword位置 也有dc的位置 取集合
                    print('keyword有找到資料，日期或城市也有找到資料')
                    print('keyword_indexes', keyword_indexes)
                    print('date_cities', dates_cities)
                    print('取集合')
                elif keyword_indexes and dates_cities is None:
                    print('句子當中只有keyword 沒有日期或是城市')
                    print(f'keyword_indexes = {keyword_indexes}')
                elif keyword_indexes and not dates_cities:
                    print('keyword有找到資料，但日期或城市沒有匹配的資料')
                    print('return []')

    elif language == 'en':
        print('英文模型')
        dates_cities = en_dates_cities(user_input, zh_json)
        # 模型 判斷意圖
        # result = asyncio.run(agent_en.parse_message(user_input))
        # # 售票時間
        # if result['intent']['name'] == 'query_ticket_time':
        #     print('執行query_ticket_time')
        # # keyword
        # elif result['intent']['name'] == 'query_keyword':
        #     print('執行query_keyword')
        #     if len(result['entities']) == 0:
        #         print('No Entities')
        #     else:
        #         keyword_indexes = []
        #         for i in range(len(result['entities'])):
        #             print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
        #         if keyword_indexes:
        #             print('keyword_indexes', keyword_indexes)
        #             print('date_cities', dates_cities)
        #         else:
        #             print('搜尋了關鍵字 但是沒有找到')
        # keyword_indexes = get_keyword_indexes(user_input, en_json)  # 獲取的keyword進行搜尋
        # print(f'keyword indexes {keyword_indexes}')
    # 中文 城市 時間
    # 英文 城市 時間
    # print('可以開始了')
    # while True:
    #     try:
    #         user_input = input().lower()
    #         chinese_pattern = re.compile(r'[\u4e00-\u9fa5]')
    #         if bool(chinese_pattern.search(user_input)):
    #             # 中文
    #             dates_cities_indexes = zh_dates_cities(user_input, zh_json)
    #             print('dates, city', dates_cities_indexes)
    #
    #             result = asyncio.run(agent_zh.parse_message(user_input))
    #             # keyword_indexes = get_keyword_indexes(user_input, zh_json)
    #             # print('keyword', keyword_indexes)
    #         else:
    #             # 英文
    #             dates_cities_indexes = en_dates_cities(user_input, en_json)
    #             print('dates, city', dates_cities_indexes)
    #
    #             result = asyncio.run(agent_en.parse_message(user_input))
    #             for i in range(len(result['entities'])):
    #                 if result['entities'][i]['entity'] == 'keyword':
    #                     print(result['entities'][i]['value'])
    #                 # print(f"{result['entities'][i]['entity']}: {result['entities'][i]['value']}")
    #             # keyword_indexes = get_keyword_indexes(user_input, en_json)
    #             # print('keyword', keyword_indexes)
    #
    #         # print(result)
    #         # print('city & dates', dates_cities_indexes)
    #         # print('keyword', keyword_indexes)
    #
    #         print('---')
    #     except:
    #         print('輸入錯誤 可以麻煩你再輸入一次嗎')
    #         continue
