# import os
#
#
# def get_filenames(directory):
#     # 檢查目錄是否存在
#     if not os.path.exists(directory):
#         print(f"目錄 '{directory}' 不存在。")
#         return
#
#     # 獲取目錄中的所有檔案名稱
#     filenames = os.listdir(directory)
#
#     filenames = [filename for filename in filenames if ".json" in filename]
#
#     # 顯示所有檔案名稱
#     for filename in filenames:
#         print(filename)
#
#
# def get_new_old_json(directory):
#     # 檢查目錄是否存在
#     if not os.path.exists(directory):
#         print(f"目錄 '{directory}' 不存在。")
#         return
#
#     # 獲取目錄中的所有檔案名稱
#     filenames = os.listdir(directory)
#
#     filenames = [filename for filename in filenames if ".json" in filename]
#
#     new_json = filenames[-1]
#     old_json = filenames[-2]
#
#     return new_json, old_json
#
#
# # 輸入要查看的目錄路徑
# directory_path = r"C:\Users\pfii1\akuan\git-repos\2024_Concert_Chatbot\concert_jsons"
# # get_filenames(directory_path)
# from nltk.tokenize import word_tokenize
# from nltk.tokenize import RegexpTokenizer
#
# tokenizer = RegexpTokenizer(r'\w+|[^\w\s]+')
#
# text = "post malone"
# word_tokens = word_tokenize(text.lower())
# print(word_tokens)
""""""
# import yaml
# with open('data/keyword.yml', 'r', encoding='utf-8') as f:
#     data = yaml.safe_load(f)
#     singers = data['nlu'][0]['examples'].replace('- ', '').split('\n')
# for i, singer in enumerate(singers):
#     if len(singer) <= 2:
#         print(i + 5, singer)
""""""


def success_msg(txt):
    # print(f"\033[32m{txt}\033[0m\033[1m")  # 白色，但是變成粗體字
    print(f"\033[32m{txt}\033[0m")  # 绿色文本，重置所有格式


def hello():
    global x
    x = x + 1


x = 1
success_msg(x)

y = 2
print(y)

from read_json_function import *

data = read_json("concert_zh.json")
success_msg(len(data))


def metoo():
    print('nothing to lose')


import pyautogui

# 获取当前鼠标位置
current_mouse_position = pyautogui.position()
print(f"当前鼠标位置： {current_mouse_position}")

import random

data = read_json("concert_zh.json")
random_integers = sorted([random.randint(0, len(data) - 1) for _ in range(10)])
print(random_integers)


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

        if language == 'zh':
            formatted_str = f"""
- {concert['tit']}
- 日期: {concert_date_str}
- 票價: {sorted_prices_str}
- 售票日期: {sale_date_str}
- {concert['url']}
            """
        elif language == 'en':
            formatted_str = f"""
- {concert['tit']}
- Date: {concert_date_str}
- Ticket Price: {sorted_prices_str}
- Sale Date: {sale_date_str}
- {concert['url']}
            """

        formatted_str_list.append(formatted_str.strip())

    print(formatted_str_list)
    return formatted_str_list


messages = show_concert_info(random_integers, 'zh')
for msg in messages:
    print(msg)
