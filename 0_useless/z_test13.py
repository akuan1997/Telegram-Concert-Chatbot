# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from fuzzywuzzy import process
#
# nltk.download('punkt')
# nltk.download('stopwords')
#
# # 模擬一些範例文章
# articles = {
#     "Article 1": "Live concert of Coldplay happening in New York next month.",
#     "Article 2": "Eminem's surprise performance shocks fans at LA gala.",
#     "Article 3": "Classical music evening with compositions from Beethoven and Mozart."
# }
#
#
# # 預處理函數，進行分詞和去除停用詞
# def preprocess(text):
#     stop_words = set(stopwords.words('english'))
#     word_tokens = word_tokenize(text)
#     filtered_text = [word for word in word_tokens if word.lower() not in stop_words]
#     return " ".join(filtered_text)
#
#
# # 預處理所有文章
# preprocessed_articles = {key: preprocess(value) for key, value in articles.items()}
#
#
# # 搜索函數，根據關鍵字返回最匹配的文章
# def search_articles(query):
#     query_processed = preprocess(query)
#     results = process.extract(query_processed, preprocessed_articles, limit=10)
#     return results
#
#
# # 測試搜索功能
# search_query = "classical music concert"
# search_results = search_articles(search_query)
#
# print(search_results)
# print(len(search_results))
# print(type(search_results))
# for result in search_results:
#     print(result)
#     print('---')
import shutil
from googletrans import Translator
import json
import re

zh_cities = ["台北", "新北", "桃園", "台中", "台南", "高雄", "基隆", "新竹", "苗栗", "彰化", "南投", "雲林",
             "嘉義", "屏東", "宜蘭", "花蓮", "台東", "金門", "澎湖", "連江"]
en_cities = ["Taipei", "New Taipei", "Taoyuan", "Taichung", "Tainan", "Kaohsiung", "Keelung", "Hsinchu", "Miaoli",
             "Changhua", "Nantou", "Yunlin", "Chiayi", "Pingtung", "Yilan", "Hualien", "Taitung", "Kinmen", "Penghu",
             "Lienchiang"]


def zh_en(zh_json, en_json):
    city_mapping = dict(zip(zh_cities, en_cities))
    # Copying the original file to a new file for translated content
    shutil.copy(zh_json, en_json)

    translator = Translator()

    # Open the copied file for reading and translation
    with open(en_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(len(data))
    for i in range(len(data)):
        print(f'current progress {i + 1}/{len(data)}')

    #     if data[i]['tit']:
    #         try:
    #             translated_text = translator.translate(data[i]['tit'], src="zh-TW", dest="en").text
    #             data[i]['tit'] = translated_text
    #             print('Title Successful')
    #         except Exception as e:
    #             print(f'Title Error translating: {e}')
    #             # print(data[i]['tit'])
    #             # print(data[i]['int'])
    #             print('Skipping this entry')
    #     else:
    #         print('title empty')
    #
        # Check if 'int' field is not None or empty
        if data[i]['int']:
            try:
                # 使用正則表達式移除非中文字符
                data[i]['int'] = re.sub(r'[^\u4e00-\u9fa5]+', '', data[i]['int'])
                # Translate the text and update the 'int' field
                translated_text = translator.translate(data[i]['int'], src="zh-TW", dest="en").text
                data[i]['int'] = translated_text
                print('Content Successful')
            except Exception as e:
                print(f'Inner Text Error translating: {e}')
                # print(data[i]['tit'])
                # print(data[i]['int'])
                print('Skipping this entry')
        else:
            print('inner text empty')

        if 'cit' in data[i]:
            if data[i]['cit'] in city_mapping:
                data[i]['cit'] = city_mapping[data[i]['cit']]
                print(data[i]['cit'])

                # with open('concert_test.json', 'w', encoding='utf-8') as f:
                #     json.dump(data, f, indent=4, ensure_ascii=False)

        print('------------------------------------')

    # Write the translated data back to the file
    # with open(en_json, 'w', encoding='utf-8') as f:
    #     json.dump(data, f, indent=4, ensure_ascii=False)


def zh_en1(zh_json, en_json):
    city_mapping = dict(zip(zh_cities, en_cities))
    shutil.copy(zh_json, en_json)
    translator = Translator()
    with open(en_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        print(f'current progress {data.index(item) + 1}/{len(data)}')

        # Translate title if not empty
        if item.get('tit'):
            try:
                item['tit'] = translator.translate(item['tit'], src="zh-TW", dest="en").text
                print('Title Successful')
            except Exception as e:
                print(f'Error translating title: {e}')

        # Translate introduction if not empty
        if item.get('int'):
            try:
                item['int'] = translator.translate(item['int'], src="zh-TW", dest="en").text
                print('Content Successful')
            except Exception as e:
                print(f'Error translating content: {e}')

        # Map city names
        if item.get('cit') and item['cit'] in city_mapping:
            item['cit'] = city_mapping[item['cit']]
            print(item['cit'])

        print('------------------------------------')

    with open(en_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def zh_en_origin(zh_json, en_json):
    city_mapping = dict(zip(zh_cities, en_cities))
    # Copying the original file to a new file for translated content
    shutil.copy(zh_json, en_json)

    translator = Translator()

    # Open the copied file for reading and translation
    with open(en_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i in range(len(data)):
        print(f'current progress {i + 1}/{len(data)}')

        # Check if 'int' field is not None or empty
        if data[i]['int']:
            try:
                # 使用正則表達式移除非中文字符
                data[i]['int'] = re.sub(r'[^\u4e00-\u9fa5]+', '', data[i]['int'])
                # Translate the text and update the 'int' field
                translated_text = translator.translate(data[i]['int'], src="zh-TW", dest="en").text
                data[i]['int'] = translated_text
                print('Successful')
            except Exception as e:
                print(f'Error translating: {e}')
                print('Skipping this entry')
        else:
            print('None or empty, skip')

        if 'cit' in data[i]:
            if data[i]['cit'] in city_mapping:
                data[i]['cit'] = city_mapping[data[i]['cit']]
                print(data[i]['cit'])

                # with open('concert_test.json', 'w', encoding='utf-8') as f:
                #     json.dump(data, f, indent=4, ensure_ascii=False)

        print('------------------------------------')

    # Write the translated data back to the file
    with open(en_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


zh_en('concert_5_4_20.json', 'concert_data_old_en.json')
