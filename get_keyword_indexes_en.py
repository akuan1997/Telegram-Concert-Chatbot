import json
import re
import yaml
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
from rank_bm25 import BM25Okapi

nltk.download('punkt')
nltk.download('stopwords')

# 讀取 YAML 文件中的歌手名單
with open('data/keyword.yml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
    singers = data['nlu'][0]['examples'].replace('- ', '').split('\n')
    singers = [singer.lower() for singer in singers]

# 建立正則表達式：對每個名稱進行轉義，防止特殊字符造成問題
escaped_singers = [re.escape(singer) for singer in singers]
pattern = '|'.join(escaped_singers) + r'|\w+'

# 創建一個 tokenizer
tokenizer = RegexpTokenizer(pattern)

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
    # 從文件讀取演唱會數據
    with open(json_filename, 'r', encoding='utf-8') as file:
        concerts = json.load(file)

    # 構建文檔
    documents = [concert["tit"] + " " + concert["int"] for concert in concerts]

    # 預處理所有文檔
    texts = [preprocess(doc) for doc in documents]

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
