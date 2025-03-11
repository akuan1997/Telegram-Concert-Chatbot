from datetime import datetime
from read_json_function import read_json

new_all = read_json('concert_data_new_zh.json')
old_all = read_json('concert_data_old_zh.json')

era = read_json('../concert_data_json/website_jsons/era.json')
indievox = read_json('../concert_data_json/website_jsons/indievox.json')
kktix = read_json('../concert_data_json/website_jsons/kktix.json')
livenation = read_json('../concert_data_json/website_jsons/livenation.json')
ticketplus = read_json('../concert_data_json/website_jsons/ticketplus.json')

ab = read_json('../concert_data_json/concert_jsons/concert_3_14_23.json')


# kktix1 = read_json('kktix1.json')
# kktix2 = read_json('kktix2.json')
# kktix3 = read_json('kktix3.json')

# for i in range(len(kktix1)):
#     if kktix1[i]['pin'][-1] != '0':
#         print(kktix1[i]['url'])
#         print(kktix1[i]['pin'])
# for i in range(len(kktix2)):
#     if kktix1[i]['pin'][-1] != '0':
#         print(kktix1[i]['url'])
#         print(kktix1[i]['pin'])
# for i in range(len(kktix3)):
#     if kktix1[i]['pin'][-1] != '0':
#         print(kktix1[i]['url'])
#         print(kktix1[i]['pin'])

# print(ab[i]['pin'])

def check_sdt(data):
    for i in range(len(data)):
        print(i, data[i]['sdt'])
        # print(data[i]['url'])


def check_pdt(data):
    for i in range(len(data)):
        print(data[i]['pdt'])


def check_loc(data):
    for i in range(len(data)):
        print(data[i]['loc'])


def check_prc(data):
    for i in range(len(data)):
        print(data[i]['prc'])


def check_all_sdt():
    check_sdt(era)
    check_sdt(indievox)
    check_sdt(kktix)
    check_sdt(livenation)
    check_sdt(ticketplus)


def check_all_pdt():
    check_pdt(era)
    check_pdt(indievox)
    check_pdt(kktix)
    check_pdt(livenation)
    check_pdt(ticketplus)


def check_all_loc():
    check_loc(era)
    check_loc(indievox)
    check_loc(kktix)
    check_loc(livenation)
    check_loc(ticketplus)


def check_all_prc():
    check_prc(era)
    check_prc(indievox)
    check_prc(kktix)
    check_prc(livenation)
    check_prc(ticketplus)


def check_all_cit(data):
    for i in range(len(data)):
        print(data[i]['cit'], data[i]['loc'])


# check_all_sdt()
# check_all_pdt()
# check_all_loc()
# check_all_prc()
# check_all_cit(old_all)
# check_all_sdt()
# for i in range(len(old_all)):
#     print(old_all[i]['tit'])
#     print(i, old_all[i]['sdt'])
# for i in range(len(old_all)):
#     for j in range(i + 1, len(old_all)):
#         if old_all[i]['pin'] == old_all[j]['pin']:
#             print('yes')
# data = read_json("concert_5_9_14.json")
from googletrans import Translator
import json, re
# Copying the original file to a new file for translated content

translator = Translator()

with open("concert_zh1.json", 'r', encoding='utf-8') as f:
    data = json.load(f)
index = 231
# print(data[index]['tit'])
translated_title = translator.translate(data[index]['tit'], src="zh-TW", dest="en").text
print(f"translated_title = {translated_title}")
# print(data[index]['int'])
translated_int = translator.translate(data[index]['int'], src="zh-TW", dest="en").text
print(f"translated_int = {translated_int}")
# for i in range(len(data)):
#     if data[i]['int']:
#         try:
#             # 使用正則表達式移除非中文字符
#             data[i]['int'] = re.sub(r'[^\u4e00-\u9fa5]+', '', data[i]['int'])
#             # Translate the text and update the 'int' field
#             translated_text = translator.translate(data[i]['int'], src="zh-TW", dest="en").text
#             data[i]['int'] = translated_text
#             print('Content Successful')
#         except Exception as e:
#             print(f'Inner Text Error translating: {e}')
#             # print(data[i]['tit'])
#             # print(data[i]['int'])
#             print('Skipping this entry')
#     else:
#         print('inner text empty')

print('------------------------------------')


# data = read_json("concert_zh1.json")
# print(len(data))
# for i in range(len(data)):
#     if "2025國際沈文程日" in data[i]['tit']:
#         print(data[i]['tit'])
#         print(data[i]['pdt'])
