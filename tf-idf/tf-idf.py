from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

# 你的演唱會資料
with open('../web_scraping/era.json', 'r', encoding='utf-8') as file:
    concert_data = json.load(file)

# 提取標題、時間、地點的文字信息
# documents = [" ".join([concert["tit"], " ".join(concert["pdt"]), " ".join(concert["loc"])]) for concert in concert_data]

# 使用'int'欄位
# documents = [concert["int"] for concert in concert_data]
# 使用 'tit'欄位 以及 'int'欄位
documents = [concert["tit"] + " " + concert["int"] for concert in concert_data]

# 使用'tit'和'int'欄位
# documents = [concert["tit"] + " " + concert["int"] for concert in concert_data]

# 創建TF-IDF向量器
vectorizer = TfidfVectorizer()

# 轉換文檔為TF-IDF表示
tfidf_matrix = vectorizer.fit_transform(documents)

# 打印特徵名稱
print("Features:\n", vectorizer.get_feature_names_out())

# 打印TF-IDF矩陣
print("TF-IDF Matrix:\n", tfidf_matrix.toarray())

# 1. 輸入處理
user_input = "山川豐"
user_vector = vectorizer.transform([user_input])

# 2. 相似性計算
similarity_scores = cosine_similarity(user_vector, tfidf_matrix)

# 3. 找到最相似的演唱會
most_similar_index = np.argmax(similarity_scores)
most_similar_score = similarity_scores[0, most_similar_index]
most_similar_concert = concert_data[most_similar_index]

# 4. 提取票價
ticket_prices = most_similar_concert["prc"]

# 打印結果
print("最相似的演唱會:", most_similar_concert["tit"])
print(f'數值: {most_similar_score}')
print("票價:", ticket_prices)
