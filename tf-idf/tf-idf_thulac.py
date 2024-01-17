from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import thulac
import sys
import io


# 使用 THULAC 進行分詞的函數
def thulac_tokenize(text):
    # 暫時重定向標準輸出
    original_stdout = sys.stdout
    sys.stdout = io.StringIO()

    # 初始化 THULAC，這一步將不會輸出到標準輸出
    thu = thulac.thulac(seg_only=True)

    # 恢復標準輸出
    sys.stdout = original_stdout

    return thu.cut(text, text=True)


user_input = "怕胖團"

# 讀取演唱會資料
with open('concert_data.json', 'r', encoding='utf-8') as file:
    concert_data = json.load(file)

# 使用 THULAC 進行分詞
documents = [thulac_tokenize(concert["tit"] + " " + concert["int"]) for concert in concert_data]

# 初始化 TF-IDF 向量化器，使用自定義的分詞函數
vectorizer = TfidfVectorizer(tokenizer=thulac_tokenize)
X = vectorizer.fit_transform(documents)

# 計算與用戶輸入的餘弦相似度
user_input_vector = vectorizer.transform([user_input])
cosine_similarities = cosine_similarity(user_input_vector, X).flatten()

# 找出最相似的演唱會
most_similar_concert_index = np.argmax(cosine_similarities)
most_similar_concert = concert_data[most_similar_concert_index]

print("最相似的演唱會是:", most_similar_concert["tit"])
