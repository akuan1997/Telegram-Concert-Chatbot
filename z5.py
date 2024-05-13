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
x = 1
print(x)


def hello():
    global x
    x = x + 1


y = 2
print(y)

from read_json_function import *
data = read_json("concert_zh.json")
print(len(data))


def metoo():
    print('nothing to lose')

import pyautogui

# 获取当前鼠标位置
current_mouse_position = pyautogui.position()
print("当前鼠标位置：", current_mouse_position)