import json
import re
import yaml
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
from rank_bm25 import BM25Okapi
import os

nltk.download('punkt')
nltk.download('stopwords')


def get_latest_json_filename(directory):
    # 檢查目錄是否存在
    if not os.path.exists(directory):
        print(f"目錄 '{directory}' 不存在。")
        return None

    # 獲取目錄中的所有檔案名稱
    filenames = os.listdir(directory)

    # 過濾出所有的 .json 檔案
    json_files = [filename for filename in filenames if filename.endswith(".json")]

    # 如果沒有找到 .json 檔案，返回 None
    if not json_files:
        print("沒有找到任何 .json 檔案。")
        return None

    # 根據檔案的修改時間對 .json 檔案進行排序，最新的檔案在最後
    json_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))

    # 返回最新的 .json 檔案
    return json_files[-1]


def preprocess(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = tokenizer.tokenize(text.lower())
    # print(f"word_tokens = {word_tokens}")
    # 更新過濾條件，確保在歌手名單中的詞不會因包含停用詞而被過濾
    filtered_text = [word for word in word_tokens if word in singers or
                     (word not in stop_words and all(char.isalpha() or char.isspace() for char in word))]
    # print(f"filtered_text = {filtered_text}")
    return filtered_text


def get_keyword_indexes_en(user_input, json_filename):
    global using_json, documents, texts
    print(f'正在使用的json: {using_json}')
    latest_json = get_latest_json_filename(directory_path)

    if using_json != latest_json:
        print(f'使用的json產生變化: {using_json} -> {latest_json}')
        # 從文件讀取演唱會數據
        with open(f"en_concert_jsons/{latest_json}", 'r', encoding='utf-8') as file:
            concerts = json.load(file)

        # 構建文檔
        documents = [concert["tit"] + " " + concert["int"] for concert in concerts]

        # 預處理所有文檔 (每次都會卡在這裡)
        texts = [preprocess(doc) for doc in documents]

        using_json = latest_json
        print(f'Using json now: {latest_json}')

    # 使用BM25Okapi建立索引
    bm25 = BM25Okapi(texts)
    query_processed = preprocess(user_input)
    scores = bm25.get_scores(query_processed)
    ranked_scores = sorted(((score, idx) for idx, score in enumerate(scores)), reverse=True, key=lambda x: x[0])
    results = [(idx, score) for score, idx in ranked_scores[:10] if score > 0]
    indexes = [result[0] for result in results]
    return indexes


# print('ready')
# while True:
#     user_input = input()
#     preprocess(user_input)
# preprocess("Justin Bieber.")
# preprocess("post malone.")
# preprocess("the weekend.")
# preprocess("I would like to know the place of post malone's concert")
# 讀取 YAML 文件中的歌手名單
with open('../data/keyword.yml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
    singers = data['nlu'][0]['examples'].replace('- ', '').split('\n')
    singers = [singer.lower() for singer in singers]

# 建立正則表達式：對每個名稱進行轉義，防止特殊字符造成問題
escaped_singers = [re.escape(singer) for singer in singers]
pattern = '|'.join(escaped_singers) + r'|\w+'
# 創建一個 tokenizer
tokenizer = RegexpTokenizer(pattern)

directory_path = r"C:\Users\pfii1\akuan\git-repos\2024_Concert_Chatbot\en_concert_jsons"
# 獲取目錄中的所有檔案名稱
filenames = os.listdir(directory_path)
# 過濾出所有的 .json 檔案
json_files = [filename for filename in filenames if filename.endswith(".json")]
# 根據檔案的修改時間對 .json 檔案進行排序，最新的檔案在最後
json_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory_path, x)))
using_json = json_files[-1]

# 從文件讀取演唱會數據
with open("../concert_data_json/concert_en.json", 'r', encoding='utf-8') as file:
    concerts = json.load(file)

# 構建文檔
documents = [concert["tit"] + " " + concert["int"] for concert in concerts]

# 預處理所有文檔 (每次都會卡在這裡)
texts = [preprocess(doc) for doc in documents]
