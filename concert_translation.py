import shutil
import time
from googletrans import Translator
import json
import re

zh_cities = ["台北", "新北", "桃園", "台中", "台南", "高雄", "基隆", "新竹", "苗栗", "彰化", "南投", "雲林",
             "嘉義", "屏東", "宜蘭", "花蓮", "台東", "金門", "澎湖", "連江"]
en_cities = ["Taipei", "New Taipei", "Taoyuan", "Taichung", "Tainan", "Kaohsiung", "Keelung", "Hsinchu", "Miaoli",
             "Changhua", "Nantou", "Yunlin", "Chiayi", "Pingtung", "Yilan", "Hualien", "Taitung", "Kinmen", "Penghu",
             "Lienchiang"]

from function_read_json import *

city_mapping = dict(zip(zh_cities, en_cities))


def zh_en(zh_json, en_json):
    # Copying the original file to a new file for translated content
    shutil.copy(zh_json, en_json)

    translator = Translator()

    # Open the copied file for reading and translation
    with open(en_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i in range(len(data)):
        print(f'current progress {i + 1}/{len(data)}')

        """ title """
        print("ori:", data[i]['tit'])
        try:
            translated_title = translator.translate(data[i]['tit'], src="zh-TW", dest="en").text
            data[i]['tit'] = translated_title
            print('title text successful')
        except Exception as e:
            print(e)
            with open('trans_error.txt', 'a', encoding='utf-8') as f:
                f.write(f"{i}|||title\n")
        print("aft:", data[i]['tit'])

        """ inner text """
        try:
            if data[i]['int'] != '':
                data[i]['int'] = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9 ,。．、？！；：「」（）《》“”‘’]+', '', data[i]['int'])
                translated_inner_text = translator.translate(data[i]['int'], src="zh-TW", dest="en").text
                data[i]['int'] = translated_inner_text
                print('inner text successful')
        except Exception as e:
            print(e)
            with open('trans_error.txt', 'a', encoding='utf-8') as f:
                f.write(f"{i}|||inner text\n")

        """ city """
        if 'cit' in data[i]:
            if 'cit' in data[i]:
                if data[i]['cit'] in city_mapping:
                    print(f"{data[i]['cit']} -> ", end='')
                    data[i]['cit'] = city_mapping[data[i]['cit']]
                    print(data[i]['cit'])
                    # with open(en_json, 'w', encoding='utf-8') as f:
                    #     json.dump(data, f, indent=4, ensure_ascii=False)

        print('------------------------------------')

        time.sleep(3)

    with open(en_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def zh_en_cit(en_json):
    data = read_json(en_json)
    city_mapping = dict(zip(zh_cities, en_cities))
    for i in range(len(data)):
        if 'cit' in data[i]:
            if 'cit' in data[i]:
                if data[i]['cit'] in city_mapping:
                    print(f"{data[i]['cit']} -> ", end='')
                    data[i]['cit'] = city_mapping[data[i]['cit']]
                    print(data[i]['cit'])
                    with open(en_json, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
# def zh_en(zh_json, en_json):
#     city_mapping = dict(zip(zh_cities, en_cities))
#     # Copying the original file to a new file for translated content
#     shutil.copy(zh_json, en_json)
#
#     translator = Translator()
#
#     # Open the copied file for reading and translation
#     with open(en_json, 'r', encoding='utf-8') as f:
#         data = json.load(f)
#
#     for i in range(len(data)):
#         print(f'current progress {i + 1}/{len(data)}')
#
#         if data[i]['tit']:
#             ori_title = data[i]['tit']
#             try:
#                 translated_title = translator.translate(data[i]['tit'], src="zh-TW", dest="en").text
#                 data[i]['tit'] = translated_title
#             except Exception as e:
#                 data[i]['tit'] = ori_title
#                 print(f'Error translating title: {e}')
#                 print('Skipping this entry')
#
#         # Check if 'int' field is not None or empty
#         if data[i]['int']:
#             try:
#                 # 使用正則表達式移除非中文字符
#                 data[i]['int'] = re.sub(r'[^\u4e00-\u9fa5]+', '', data[i]['int'])
#                 # Translate the text and update the 'int' field
#                 translated_text = translator.translate(data[i]['int'], src="zh-TW", dest="en").text
#                 data[i]['int'] = translated_text
#                 print('Successful')
#             except Exception as e:
#                 print(f'Error translating inner text: {e}')
#                 print('Skipping this entry')
#         else:
#             print('None or empty, skip')
#
#         if 'cit' in data[i]:
#             if data[i]['cit'] in city_mapping:
#                 data[i]['cit'] = city_mapping[data[i]['cit']]
#                 print(data[i]['cit'])
#
#         print('------------------------------------')
#
#         time.sleep(3)
#
#     # Write the translated data back to the file
#     with open(en_json, 'w', encoding='utf-8') as f:
#         json.dump(data, f, indent=4, ensure_ascii=False)


# def zh_en(zh_json, en_json):
#     city_mapping = dict(zip(zh_cities, en_cities))
#     # Copying the original file to a new file for translated content
#     shutil.copy(zh_json, en_json)
#
#     translator = Translator()
#
#     # Open the copied file for reading and translation
#     with open(en_json, 'r', encoding='utf-8') as f:
#         data = json.load(f)
#
#     for i in range(len(data)):
#         print(f'current progress {i + 1}/{len(data)}')
#
#         print("ori:", data[i]['tit'])
#         try:
#             translated_title = translator.translate(data[i]['tit'], src="zh-TW", dest="en").text
#             data[i]['tit'] = translated_title
#             print('title text successful')
#         except Exception as e:
#             print(e)
#             time.sleep(3)
#             try:
#                 translated_title = translator.translate(data[i]['tit'], src="zh-TW", dest="en").text
#                 data[i]['tit'] = translated_title
#                 print('title text successful')
#             except Exception as e:
#                 with open('trans_error.txt', 'a', encoding='utf-8') as f:
#                     f.write(f"{i}|||title\n")
#
#         print("aft:", data[i]['tit'])
#         try:
#             if data[i]['int'] != '':
#                 data[i]['int'] = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9 ,。．、？！；：「」（）《》“”‘’]+', '', data[i]['int'])
#                 translated_inner_text = translator.translate(data[i]['int'], src="zh-TW", dest="en").text
#                 data[i]['int'] = translated_inner_text
#                 print('inner text successful')
#         except Exception as e:
#             print(e)
#             time.sleep(3)
#             try:
#                 translated_inner_text = translator.translate(data[i]['int'], src="zh-TW", dest="en").text
#                 data[i]['int'] = translated_inner_text
#                 print('inner text successful')
#             except Exception as e:
#                 with open('trans_error.txt', 'a', encoding='utf-8') as f:
#                     f.write(f"{i}|||inner text\n")
#
#         if 'cit' in data[i]:
#             if data[i]['cit'] in city_mapping:
#                 data[i]['cit'] = city_mapping[data[i]['cit']]
#                 print(data[i]['cit'])
#
#         print('------------------------------------')
#
#         time.sleep(3)
#
#     # Write the translated data back to the file
#     with open(en_json, 'w', encoding='utf-8') as f:
#         json.dump(data, f, indent=4, ensure_ascii=False)