from rank_bm25 import BM25Okapi
import jieba
import numpy as np
import json

jieba.load_userdict('user_defined_lastfm.txt')

user_input = "音樂祭"

# 使用jieba進行中文分詞
def chinese_tokenizer(text):
    return jieba.lcut(text)

# 你的演唱會資料
with open('../concert_data.json', 'r', encoding='utf-8') as file:
    concert_data = json.load(file)

# 使用'tit'和'int'欄位，並為'tit'增加權重
documents = [chinese_tokenizer(concert["tit"] + " " + concert["int"]) for concert in concert_data]

# 創建BM25模型
bm25 = BM25Okapi(documents)

# 處理輸入
user_tokens = chinese_tokenizer(user_input)

# 計算BM25分數
scores = bm25.get_scores(user_tokens)

# 找到最相似的幾個演唱會
sorted_indices = np.argsort(scores)[::-1]  # 從高到低排序
how_many_results = 200
top_concerts = []
for i in sorted_indices:
    if scores[i] > 0:
        top_concerts.append((concert_data[i]['tit'], scores[i]))
    if len(top_concerts) == how_many_results:
        break

# 打印最相似的演唱會
if top_concerts:
    for idx, (title, score) in enumerate(top_concerts):
        print(f"{idx + 1}. {title} (相似度: {score:.2f})")
        for i in range(len(concert_data)):
            if concert_data[i]['tit'] == title:
                print(concert_data[i]['url'])
else:
    print("沒有找到匹配的演唱會。")
