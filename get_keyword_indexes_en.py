import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from rank_bm25 import BM25Okapi

nltk.download('punkt')
nltk.download('stopwords')

# 從文件讀取演唱會數據
with open('concert_data_old_en.json', 'r', encoding='utf-8') as file:
    concerts = json.load(file)

# 構建文檔
documents = [concert["tit"] + " " + concert["int"] for concert in concerts]


# 預處理函數，進行分詞和去除停用詞
def preprocess(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text.lower())
    filtered_text = [word for word in word_tokens if word not in stop_words and word.isalpha()]
    return filtered_text


# 預處理所有文檔
texts = [preprocess(doc) for doc in documents]

# 使用BM25Okapi建立索引
bm25 = BM25Okapi(texts)


# 查詢函數
# def search(query):
#     query_processed = preprocess(query)
#     scores = bm25.get_scores(query_processed)
#     ranked_scores = sorted(((score, idx) for idx, score in enumerate(scores)), reverse=True, key=lambda x: x[0])
#     print(ranked_scores)
#     # return [(documents[idx], score) for score, idx in ranked_scores[:10]]  # 返回前三個最高得分的文檔
#     return [(documents[idx].split("///")[0], score) for score, idx in ranked_scores[:10]]  # 返回前十個最高得分的文檔

def search(query):
    query_processed = preprocess(query)
    scores = bm25.get_scores(query_processed)
    ranked_scores = sorted(((score, idx) for idx, score in enumerate(scores)), reverse=True, key=lambda x: x[0])
    # Filter out documents with a score of 0
    # return [(documents[idx].split("///")[0], score) for score, idx in ranked_scores[:10] if score > 0]
    results = [(idx, score) for score, idx in ranked_scores[:10] if score > 0]
    indexes = []
    for result in results:
        indexes.append(result[0])
    return indexes


# 測試查詢
query = "super robot"
indexes = search(query)
for index in indexes:
    print(concerts[index]['tit'])
