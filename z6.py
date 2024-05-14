# from function_read_json import *
# from googletrans import Translator
# translator = Translator()
#
# data = read_json("concert_zh.json")
# # for i in range(len(data)):
# #     words = data[i]['tit'].split(' ')
# #     print(len(words))
# #     print(data[i]['tit'])
#
# for i in range(10):
#     txt = data[i]['tit']
#     translated_text = translator.translate(txt, src="zh-TW", dest="en").text
#     print(translated_text)
#     words = translated_text.split(' ')
#     print(len(words))
#     print('---')
import shutil
import time
from googletrans import Translator
import json
import re
from function_read_json import *

data = read_json("concert_zh.json")
for i in range(len(data)):
    if data[i]['tit'] == "":
        print(i)
# translator = Translator()
# txt = '今天 I like you 明天'
# translated_title = translator.translate(txt, src="zh-TW", dest="en").text
# print(translated_title)
