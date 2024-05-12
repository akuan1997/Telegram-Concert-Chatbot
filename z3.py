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
from get_keyword_indexes_en import *
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




