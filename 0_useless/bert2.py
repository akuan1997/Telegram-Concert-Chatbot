from transformers import BertTokenizer, BertModel
import torch
import numpy as np
import json

# 加载 'bert-base-chinese' 模型和分词器
model_name = 'bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)


# 文本编码函数
def encode_text(text):
    encoded_input = tokenizer(text, return_tensors='pt', max_length=512, truncation=True)
    with torch.no_grad():
        model_output = model(**encoded_input)
    return model_output.last_hidden_state[0, 0, :].numpy()


# 计算向量间余弦相似度的函数
def cosine_similarity(vec_a, vec_b):
    return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))


# 根据用户输入查找相似的演唱会信息的函数
def find_similar_concerts(user_input, concert_data, top_n=5):
    user_input_encoded = encode_text(user_input)
    similarity_scores = []

    for concert in concert_data:
        concert_title = concert['tit']
        concert_title_encoded = encode_text(concert_title)
        similarity = cosine_similarity(user_input_encoded, concert_title_encoded)
        similarity_scores.append((concert, similarity))

    # 根据相似度排序并返回前 top_n 个结果
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    return similarity_scores[:top_n]


# 测试功能
test_input = "怕胖團"  # 这里输入歌手或乐团的名字
with open('0_useless/concert_data_s.json', 'r', encoding='utf-8') as f:
    concert_data = json.load(f)
similar_concerts = find_similar_concerts(test_input, concert_data, top_n=5)

for concert, similarity in similar_concerts:
    print(f"相似度: {similarity}, 演唱会: {concert['tit']}")
