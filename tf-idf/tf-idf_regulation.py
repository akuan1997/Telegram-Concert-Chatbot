from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

user_input = "怕胖團" # 應該要擺在# 1. 輸入處理下面一行的 但是為了方便我擺在這邊

# 你的演唱會資料
with open('concert_data.json', 'r', encoding='utf-8') as file:
    concert_data = json.load(file)

# 使用'tit'和'int'欄位，並為'tit'增加權重
# documents = [concert["tit"] * 2 + " " + concert["int"] for concert in concert_data]
documents = [concert["tit"] + " " + concert["int"] for concert in concert_data]

# 創建TF-IDF向量器，使用中文分詞
vectorizer = TfidfVectorizer(token_pattern=r'(?u)\b\w+\b')

# 轉換文檔為TF-IDF表示
tfidf_matrix = vectorizer.fit_transform(documents)

# 1. 輸入處理
user_vector = vectorizer.transform([user_input])

# 2. 相似性計算
similarity_scores = cosine_similarity(user_vector, tfidf_matrix)

''' 找到最相似的演唱會 '''

# 3. 找到最相似的演唱會
most_similar_index = np.argmax(similarity_scores)
most_similar_score = similarity_scores[0, most_similar_index]

# # 檢查是否有足夠高的相似度分數
# if most_similar_score < 0.1:  # 可以根據需要調整閾值
#     print("沒有找到匹配的演唱會。")
#     print(f'score {most_similar_score}')
# else:
#     most_similar_concert = concert_data[most_similar_index]
#
#     # 打印結果
#     print("最相似的演唱會:", most_similar_concert["tit"])
#     print(f'score {most_similar_score}')

# 打印結果
# most_similar_concert = concert_data[most_similar_index]
# print("最相似的演唱會:", most_similar_concert["tit"])
# print(f'score {most_similar_score}')

''' 找到最相似的演唱會 '''

''' 找到最相似的幾個演唱會 '''

# 3. 排序並找到最相似的演唱會
sorted_indices = np.argsort(similarity_scores[0])[::-1]  # 從高到低排序

how_many_results = 10
top_concerts = []
for i in sorted_indices:
    if similarity_scores[0, i] > 0:  # 檢查相似度是否大於0
        top_concerts.append((concert_data[i]['tit'], similarity_scores[0, i]))
    if len(top_concerts) == how_many_results:  # 只需要前3個
        break

# 打印最相似的演唱會
if top_concerts:
    for idx, (title, score) in enumerate(top_concerts):
        print(f"{idx + 1}. {title} (相似度: {score:.2f})")

    # 使用者選擇
    # user_choice = int(input("請選擇你感興趣的演唱會編號: "))
    # selected_concert = top_concerts[user_choice - 1][0]
    #
    # print(f"您選擇的演唱會是: {selected_concert}")
else:
    print("沒有找到匹配的演唱會。")

''' 找到最相似的幾個演唱會 '''
