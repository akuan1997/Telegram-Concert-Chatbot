# # from playwright.sync_api import sync_playwright, Playwright
# # from playwright.sync_api import expect, Page
# #
# # with sync_playwright() as p:
# #     browser = p.chromium.launch(headless=False)
# #     context = browser.new_context()
# #     page = context.new_page()
# #     page.set_default_timeout(3000)
# #     not_exists = []
# #     exists = []
# #     problems = []
# #     numbers = [
# #         "5487",
# #         "5489",
# #         "5491",
# #         "5493",
# #         "5495",
# #         "5497",
# #         "5499",
# #         "5501",
# #         "5503",
# #         "5505",
# #         "5507",
# #         "5512",
# #         "5518",
# #         "5521",
# #         "5537",
# #         "5586",
# #         "5606",
# #         "5610",
# #         "5662",
# #         "5733",
# #         "5735",
# #         "5737",
# #         "5739",
# #         "5742"
# #     ]
# #     # for number in numbers:
# #     for i in range(6062, 6327):
# #         url = f"https://concertinfo.site/?p={i}-2"
# #         page.goto(url)
# #         try:
# #             page.wait_for_selector(".page-title")
# #             if '找不到' in page.title():
# #                 not_exists.append(i)
# #             else:
# #                 exists.append(i)
# #             print(f"not_exists = {not_exists}")
# #             print(f"exists = {exists}")
# #             print(f"problems = {problems}")
# #             print('---')
# #         except:
# #             problems.append(i)
# #             print(f"not_exists = {not_exists}")
# #             print(f"exists = {exists}")
# #             print(f"problems = {problems}")
# #             print('---')
# #             continue
# import asyncio
# import logging
# from typing import Text
#
# from rasa.core.agent import Agent
# from rasa.shared.utils.cli import print_info, print_success
# from rasa.shared.utils.io import json_to_string
#
# from fuzzywuzzy import fuzz
# import yaml
# import re
#
# def keyword_adjustment_optimized(user_input):
#     with open('data/keyword.yml', 'r', encoding='utf-8') as f:
#         data = yaml.safe_load(f)
#
#     names = data['nlu'][0]['examples'].replace('- ', '').split('\n')
#     # names_without_space = [name.replace(' ', '') for name in names]
#
#     # 創建名字的小寫版本set以提高查找效率
#     names_set = {name.lower() for name in names}
#
#     # 提取用戶輸入中的英文字詞並轉成小寫
#     english_words = re.findall(r'[A-Za-z0-9]+', user_input.lower())
#     print(f"english_words = {english_words}")
#
#     # 基本匹配檢查
#     for word in english_words:
#         if word in names_set:
#             return user_input, True  # 如果找到精確匹配，直接返回
#
#     # 如果基本匹配未找到，進行模糊匹配
#     for word in english_words:
#         for name in names:
#             if fuzz.partial_ratio(word, name.lower()) > 80:
#                 user_input = user_input.replace(word, name)
#                 return user_input, True
#
#     return user_input, False  # 如果都沒找到匹配，返回原輸入
#
# a, b = keyword_adjustment_optimized("is post malone going to have a concert?")
# print(a)
# print(b)
# from get_keyword_indexes_en import *
import time
import os

""" 0513 00:43 """
# def get_latest_json_filename(directory):
#     # 檢查目錄是否存在
#     if not os.path.exists(directory):
#         print(f"目錄 '{directory}' 不存在。")
#         return None
#
#     # 獲取目錄中的所有檔案名稱
#     filenames = os.listdir(directory)
#
#     # 過濾出所有的 .json 檔案
#     json_files = [filename for filename in filenames if filename.endswith(".json")]
#
#     # 如果沒有找到 .json 檔案，返回 None
#     if not json_files:
#         print("沒有找到任何 .json 檔案。")
#         return None
#
#     # 根據檔案的修改時間對 .json 檔案進行排序，最新的檔案在最後
#     json_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
#
#     # 返回最新的 .json 檔案
#     return json_files[-1]
#
#
# while True:
#     time.sleep(3)
#     old_json = get_latest_json_filename(r"C:\Users\pfii1\akuan\git-repos\2024_Concert_Chatbot\concert_jsons")
#     print(f"old_json = {old_json}")

""""""
# directory = r"C:\Users\pfii1\akuan\git-repos\2024_Concert_Chatbot\concert_jsons"
# # 獲取目錄中的所有檔案名稱
# filenames = os.listdir(directory)
#
# # 過濾出所有的 .json 檔案
# json_files = [filename for filename in filenames if filename.endswith(".json")]
# json_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
# for file in json_files:
#     print(f"\"concert_jsons/{file}\",")
""""""
from function_read_json import *

# json_list = [
#     "concert_jsons/concert_3_14_23.json",
#     "concert_jsons/concert_3_17_16.json",
#     "concert_jsons/concert_3_17_19.json",
#     "concert_jsons/concert_3_18_13.json",
#     "concert_jsons/concert_3_20_16.json",
#     "concert_jsons/concert_3_22_0.json",
#     "concert_jsons/concert_3_23_14.json",
#     "concert_jsons/concert_3_24_8.json",
#     "concert_jsons/concert_3_25_0.json",
#     "concert_jsons/concert_3_25_17.json",
#     "concert_jsons/concert_3_26_0.json",
#     "concert_jsons/concert_3_27_3.json",
#     "concert_jsons/concert_3_29_0.json",
#     "concert_jsons/concert_3_30_13.json",
#     "concert_jsons/concert_3_30_20.json",
#     "concert_jsons/concert_3_31_14.json",
#     "concert_jsons/concert_3_31_18.json",
#     "concert_jsons/concert_4_2_0.json",
#     "concert_jsons/concert_4_3_10.json",
#     "concert_jsons/concert_4_3_22.json",
#     "concert_jsons/concert_4_4_14.json",
#     "concert_jsons/concert_4_4_3.json",
#     "concert_jsons/concert_4_5_16.json",
#     "concert_jsons/concert_4_7_17.json",
#     "concert_jsons/concert_4_15_1.json",
#     "concert_jsons/concert_5_2_14.json",
#     "concert_jsons/concert_5_4_20.json",
#     "concert_jsons/concert_5_7_1.json",
#     "concert_jsons/concert_5_7_21.json",
#     "concert_jsons/concert_5_9_14.json",
#     "concert_jsons/concert_5_10_11.json",
#     "concert_jsons/concert_5_11_23.json",
#     "concert_jsons/concert_5_12_11.json",
#     "concert_jsons/concert_5_12_21.json"
# ]

import re
from get_concert_new_old import *


def create_pin(url, txt):
    if '~' not in txt:
        pattern = r'\d{4}/(\d{1,2})/(\d{1,2}) (\d{1,2}):\d{1,2}'
        match = re.search(pattern, txt)
        month = match.group(1)
        day = match.group(2)
        hour = match.group(3)
        # print(f"month = {month}")
        # print(f"day = {day}")
        # print(f"hour = {hour}")
        pin = f"{url}_{month}_{day}_{hour}"
        # print(f"pin = {pin}")
        return pin
    else:
        pattern = r'\d{4}/(\d{2})/(\d{2}).*?~.*?\d{4}/(\d{2})/(\d{2})'
        match = re.search(pattern, txt)
        month1 = match.group(1)
        day1 = match.group(2)
        month2 = match.group(3)
        day2 = match.group(4)
        # print(f"month1 = {month1}")
        # print(f"day1 = {day1}")
        # print(f"month2 = {month2}")
        # print(f"day2 = {day2}")
        pin = f"{url}_{month1}_{day1}_{month2}_{day2}"
        # print(f"pin = {pin}")
        return pin

        # print(json_list[-1])
        # data = read_json(json_list[-1])
        # print(len(data))
        # for i in range(len(data)):
        #     # if data[i]['web'] == 'KKTIX':
        #     #
        #     if not data[i]['pdt']:
        #         print(data[i]['tit'])
        #         print(data[i]['web'])
        #     else:
        #         print(data[i]['web'])
        #         print(data[i]['pin'])
        # print(data[i]['pdt'])
        # if len(data[i]['pdt']) > 1:
        #     print(data[i]['tit'])
        # pin = create_pin(data[i]['pdt'][0])
        # print(f"pin = {pin}")
        # if '~' not in data[i]['pdt'][0]:
        #     pattern = r'\d{4}/(\d{1,2})/(\d{1,2}) (\d{1,2}):\d{1,2}'
        #     match = re.search(pattern, data[i]['pdt'][0])
        #     month = match.group(1)
        #     day = match.group(2)
        #     hour = match.group(3)
        #     print(f"month = {month}")
        #     print(f"day = {day}")
        #     print(f"hour = {hour}")
        #     print(f"{data[i]['url']}_{month}_{day}_{hour}")
        # else:
        #     print(data[i]['pdt'])
        #     pattern = r'\d{4}/(\d{2})/(\d{2}).*?~.*?\d{4}/(\d{2})/(\d{2})'
        #     match = re.search(pattern, data[i]['pdt'][0])
        #     month1 = match.group(1)
        #     day1 = match.group(2)
        #     month2 = match.group(3)
        #     day2 = match.group(4)
        #     print(f"month1 = {month1}")
        #     print(f"day1 = {day1}")
        #     print(f"month2 = {month2}")
        #     print(f"day2 = {day2}")
        #     print(f"{data[i]['url']}_{month1}_{day1}_{month2}_{day2}")
        print('---')
        # print(data[i]['tit'])
        # print(data[i]['pdt'])
        # print(data[i]['url'])
        # pass
        # else:
        #     print(data[i]['pdt'])


def testing_for_large(start_index, json_filename, mode):
    # print(f"len(json_list) = {len(json_list)}")
    # for i in range(len(json_list) - 1):
    for i in range(start_index, start_index + 1):
        current_index = i
        print(f"current_index = {current_index}")
        old_json = json_list[current_index]
        new_json = json_list[current_index + 1]

        print(f"old_json: {json_list[current_index]}\nnew_json: {json_list[current_index + 1]}\n---")

        with open(old_json, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        with open(new_json, 'r', encoding='utf-8') as f:
            new_data = json.load(f)
        with open(json_filename, 'r', encoding='utf-8') as f:
            all_data = json.load(f)

        pins_new = [entry['pin'] for entry in new_data]
        pins_old = [entry['pin'] for entry in old_data]

        new_but_old_pins = [pin for pin in pins_new if pin not in pins_old]
        old_but_new_pins = [pin for pin in pins_old if pin not in pins_new]

        print(f'current_index = {current_index}')
        print(f'len(new_data) = {len(new_data)}')
        print(f'len(old_data) = {len(old_data)}')
        print(f'len(all_data) = {len(all_data)}')
        print(f'len(new_but_old_pins) = {len(new_but_old_pins)}')
        print(f'len(old_but_new_pins) = {len(old_but_new_pins)}')

        # 新宣布的演唱會資訊、可以刪除的演唱會資訊、資訊有更動的演唱會資訊
        new_data_filtered, plus_concerts, all_data = get_new_delete_compare_concerts(new_but_old_pins, old_but_new_pins,
                                                                                     new_data, old_data, all_data)

        print(f"len(new_data_filtered) = {len(new_data_filtered)}")
        print(f"len(plus_concerts) = {len(plus_concerts)}")
        for j in range(len(plus_concerts)):
            print(plus_concerts[j]['tit'])
            print(plus_concerts[j]['url'])
        print(f'運算結束 -> len(all_data) = {len(all_data)}')

        # json_in_order(json_filename)

        # 寫進json裡面
        if mode == 1:  # 0 not write, 1 write (for testing)
            with open(json_filename, "w", encoding="utf-8") as f:
                json.dump(all_data, f, indent=4, ensure_ascii=False)
                print('寫入成功')
        elif mode == 0:
            print('設定為未寫入')

        print(f"new_data_filtered = {new_data_filtered}")
        if new_data_filtered:
            with open('new_concerts/test.json', 'w', encoding='utf-8') as f:
                json.dump(new_data_filtered, f, ensure_ascii=False, indent=4)
                print('寫入成功')

        print(f"plus_concerts = {plus_concerts}")
        if plus_concerts:
            with open('plus_concerts/test.json', 'w', encoding='utf-8') as f:
                json.dump(new_data_filtered, f, ensure_ascii=False, indent=4)
                print('寫入成功')

        print(f"current_index = {current_index}")
        print(f"len(all_data) = {len(all_data)}")
        print('----------------------------- Next ----------------------------------------------')


def price_in_order(json_filename):
    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

        for i in range(len(data)):
            data[i]['prc'] = sorted(data[i]['prc'], reverse=True)
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)


json_list = [
    "concert_jsons/concert_3_14_23.json",
    "concert_jsons/concert_3_17_16.json",
    "concert_jsons/concert_3_17_19.json",
    "concert_jsons/concert_3_18_13.json",
    "concert_jsons/concert_3_20_16.json",
    "concert_jsons/concert_3_22_0.json",
    "concert_jsons/concert_3_23_14.json",
    "concert_jsons/concert_3_24_8.json",
    "concert_jsons/concert_3_25_0.json",
    "concert_jsons/concert_3_25_17.json",
    "concert_jsons/concert_3_26_0.json",
    "concert_jsons/concert_3_27_3.json",
    "concert_jsons/concert_3_29_0.json",
    "concert_jsons/concert_3_30_13.json",
    "concert_jsons/concert_3_30_20.json",
    "concert_jsons/concert_3_31_14.json",
    "concert_jsons/concert_3_31_18.json",
    "concert_jsons/concert_4_2_0.json",
    "concert_jsons/concert_4_3_10.json",
    "concert_jsons/concert_4_3_22.json",
    "concert_jsons/concert_4_4_3.json",
    "concert_jsons/concert_4_4_14.json",
    "concert_jsons/concert_4_5_16.json",
    "concert_jsons/concert_4_7_17.json",
    "concert_jsons/concert_4_15_1.json",
    "concert_jsons/concert_5_2_14.json",
    "concert_jsons/concert_5_4_20.json",
    "concert_jsons/concert_5_7_1.json",
    "concert_jsons/concert_5_7_21.json",
    "concert_jsons/concert_5_9_14.json",
    "concert_jsons/concert_5_10_11.json",
    "concert_jsons/concert_5_11_23.json",
    "concert_jsons/concert_5_12_11.json",
    "concert_jsons/concert_5_12_21.json",
    "concert_jsons/concert_5_13_14.json",
    "concert_jsons/concert_5_13_15.json",
    "concert_jsons/concert_5_13_17.json",
    "concert_jsons/concert_5_13_18.json",
    "concert_jsons/concert_5_13_19.json",

]
""" 刪除沒有pdt的資料 """
# for i in range(len(json_list)):
#     data = read_json(json_list[i])
#     print(f"{len(data)} -> ", end='')
#     data = [item for item in data if item['pdt']]
#     print(f"{len(data)}")
#     with open(json_list[i], 'w', encoding='utf-8') as f:
#         json.dump(data, f, indent=4, ensure_ascii=False)
#     print('---')

""" 根據url還有pdt重新寫入pin"""
# print(json_list[0])
# data = read_json(json_list[0])
# for json_file in json_list:
#     print(json_file)
#     data = read_json(json_file)
#     for i in range(len(data)):
#         if data[i]['web'] == 'KKTIX':
#             data[i]['pin'] = data[i]['url']
#         else:
#             data[i]['pin'] = create_pin(data[i]['url'], data[i]['pdt'][0])
#             print(data[i]['pin'])
#         with open(json_file, 'w', encoding='utf-8') as f:
#             json.dump(data, f, indent=4, ensure_ascii=False)

""" 檢查pin有沒有重複的"""
# for json_file in json_list:
#     data = read_json(json_file)
#     for i in range(len(data)):
#        for j in range(i + 1, len(data)):
#            if data[i]['pin'] == data[j]['pin']:
#                print(data[i]['tit'])

""" 新舊對比 """
# shutil.copy(json_list[0], "concert_zh.json")  # test
# data = read_json("concert_zh.json")
# print(len(data))
# for i in range(len(json_list) - 1):
#     testing_for_large(i, "concert_zh.json", 0)
testing_for_large(37, "concert_zh.json", 0)
""" 顯示一下url以及pin """
# for i in range(len(json_list)):
#     data = read_json(json_list[i])
#     for j in range(len(data)):
#         print(data[j]['url'])
#         print(data[j]['pin'])
#         print('---')
#     print('---------------------------------')

""""""
data = read_json("concert_zh.json")
print(len(data))
# print(json_list[-1])
# data = read_json(json_list[-1])
# print(len(data))
# for i in range(len(data)):
#     for j in range(i + 1, len(data)):
#         if data[i]['url'] == data[j]['url']:
#                 print(f"{data[i]['tit']}")
#                 print(f"{data[j]['tit']}")
#                 print(f"{data[i]['pdt']} / {data[j]['pdt']}")
#                 print(f"{data[j]['web']}")
#                 print(data[i]['url'])
#                 print('---')
""""""
# for json_file in json_list:
#     print(json_file)
#     data = read_json(json_file)
#     for i in range(len(data)):
#         print(f"{data[i]['pdt']}")
# for j in range(i + 1, len(data)):
#     if data[i]['url'] == data[j]['url']:
#         print(json_file)
#         print(f"{data[i]['tit']}")
#         print(f"{data[j]['tit']}")
#         print(f"{data[i]['pdt']} / {data[j]['pdt']}")
#         print(f"{data[j]['web']}")
#         print(data[i]['url'])
#         print('---')
""""""
# if data[i]['web'] == 'KKTIX':
#     if data[i]['url'] == data[j]['url']:
#         pass
#         # print(json_file)
#         # print(f"{data[i]['tit']}")
#         # print(f"{data[j]['tit']}")
#         # print(f"{data[i]['pdt']} / {data[j]['pdt']}")
#         # print(data[i]['url'])
#         # print('---')
# else:
#     if data[i]['url'] == data[j]['url']:
#         print(json_file)
#         print(f"{data[i]['tit']}")
#         print(f"{data[j]['tit']}")
#         print(f"{data[i]['pdt']} / {data[j]['pdt']}")
#         print(f"{data[j]['web']}")
#         print(data[i]['url'])
#         print('---')
#     print('------------------------------')
""""""

print('--------------------')
""""""
# if not data[i]['pdt'] or len(data[i]['pdt']) != 1:
#     print(json_file)
#     print(data[i]['tit'])
#     print(data[i]['pdt'])
#     print(data[i]['url'])
#     print('---')

# if data[i]['pdt']:
#     print(data[i]['tit'])
#     print(data[i]['pdt'])
#     print(data[i]['url'])
#     print('---')
# if data[i]['pdt']:
#     print(data[i]['tit'])
#     print(data[i]['pdt'])
#     print(data[i]['url'])
#     print('---')


# data = read_json(json_list[0])
# for i in range(len(data)):
#     if not data[i]['pdt']:
#         print(data[i]['tit'])
#         print(data[i]['url'])
#         print('---')
#     print('--------------------')
# data = read_json(json_list[0])
# for i in range(len(data)):
#     # print(data[i]['pdt'])
#     if len(data[i]['pdt']) != 1:
#         print(data[i]['tit'])
