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
from y_example_read_json import *

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
json_list = [
    "testing_concert_jsons/concert_3_14_23.json",
    "testing_concert_jsons/concert_3_17_16.json",
    "testing_concert_jsons/concert_3_17_19.json",
    "testing_concert_jsons/concert_3_18_13.json",
    "testing_concert_jsons/concert_3_20_16.json",
    "testing_concert_jsons/concert_3_22_0.json",
    "testing_concert_jsons/concert_3_23_14.json",
    "testing_concert_jsons/concert_3_24_8.json",
    "testing_concert_jsons/concert_3_25_0.json",
    "testing_concert_jsons/concert_3_25_17.json",
    "testing_concert_jsons/concert_3_26_0.json",
    "testing_concert_jsons/concert_3_27_3.json",
    "testing_concert_jsons/concert_3_29_0.json",
    "testing_concert_jsons/concert_3_30_13.json",
    "testing_concert_jsons/concert_3_30_20.json",
    "testing_concert_jsons/concert_3_31_14.json",
    "testing_concert_jsons/concert_3_31_18.json",
    "testing_concert_jsons/concert_4_2_0.json",
    "testing_concert_jsons/concert_4_3_10.json",
    "testing_concert_jsons/concert_4_3_22.json",
    "testing_concert_jsons/concert_4_4_14.json",
    "testing_concert_jsons/concert_4_4_3.json",
    "testing_concert_jsons/concert_4_5_16.json",
    "testing_concert_jsons/concert_4_7_17.json",
    "testing_concert_jsons/concert_4_15_1.json",
    "testing_concert_jsons/concert_5_2_14.json",
    "testing_concert_jsons/concert_5_4_20.json",
    "testing_concert_jsons/concert_5_7_1.json",
    "testing_concert_jsons/concert_5_7_21.json",
    "testing_concert_jsons/concert_5_9_14.json",
    "testing_concert_jsons/concert_5_10_11.json",
    "testing_concert_jsons/concert_5_11_23.json",
    "testing_concert_jsons/concert_5_12_11.json",
    "testing_concert_jsons/concert_5_12_21.json",
    "testing_concert_jsons/concert_5_13_14.json",
    "testing_concert_jsons/concert_5_13_15.json",
    "testing_concert_jsons/concert_5_13_17.json",
    "testing_concert_jsons/concert_5_13_18.json",
    "testing_concert_jsons/concert_5_13_19.json",

]
""""""
for i in range(len(json_list)):
    data = read_json(json_list[i])
    print(f"{len(data)} -> ", end='')
    data = [item for item in data if item['tit'] != '']
    print(f"{len(data)}")
    with open(json_list[i], 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print('---')
""""""
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
import re


def create_pin(txt):
    if '~' not in data[i]['pdt'][0]:
        pattern = r'\d{4}/(\d{1,2})/(\d{1,2}) (\d{1,2}):\d{1,2}'
        match = re.search(pattern, txt)
        month = match.group(1)
        day = match.group(2)
        hour = match.group(3)
        # print(f"month = {month}")
        # print(f"day = {day}")
        # print(f"hour = {hour}")
        pin = f"{data[i]['url']}_{month}_{day}_{hour}"
        # print(f"pin = {pin}")
        return pin
    else:
        print(data[i]['pdt'])
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
        pin = f"{data[i]['url']}_{month1}_{day1}_{month2}_{day2}"
        # print(f"pin = {pin}")
        return pin


print(json_list[-1])
data = read_json(json_list[-1])
print(len(data))
for i in range(len(data)):
    # if data[i]['web'] == 'KKTIX':
    #
    if not data[i]['pdt']:
        print(data[i]['tit'])
        print(data[i]['web'])
    else:
        print(data[i]['web'])
        print(data[i]['pin'])
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
