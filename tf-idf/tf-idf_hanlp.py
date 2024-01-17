from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import hanlp

user_input = "怕胖團"  # User input

# Initialize HanLP tokenizer
hanlp_tokenizer = hanlp.load('PKU_NAME_MERGED_SIX_MONTHS_CONVSEG')


def hanlp_tokenize(text):
    # Using HanLP for tokenization
    return hanlp_tokenizer(text)


# Load your concert data
with open('concert_data.json', 'r', encoding='utf-8') as file:
    concert_data = json.load(file)

# Use 'tit' and 'int' fields, and add weight to 'tit'
# documents = [concert["tit"] * 2 + " " + concert["int"] for concert in concert_data]
documents = [concert["tit"] + " " + concert["int"] for concert in concert_data]

# Create a TF-IDF vectorizer, using HanLP for Chinese segmentation
vectorizer = TfidfVectorizer(tokenizer=hanlp_tokenize, token_pattern=None)

# Convert documents into TF-IDF representation
tfidf_matrix = vectorizer.fit_transform(documents)

# 1. Input Processing
user_vector = vectorizer.transform([user_input])

# 2. Similarity Calculation
similarity_scores = cosine_similarity(user_vector, tfidf_matrix)

''' Find the most similar concert '''

# 3. Find the most similar concert
most_similar_index = np.argmax(similarity_scores)
most_similar_score = similarity_scores[0, most_similar_index]

''' Find several most similar concerts '''

# 3. Sort and find the most similar concerts
sorted_indices = np.argsort(similarity_scores[0])[::-1]  # Sort from high to low

how_many_results = 10
top_concerts = []
for i in sorted_indices:
    if similarity_scores[0, i] > 0:  # Check if similarity is greater than 0
        top_concerts.append((concert_data[i]['tit'], similarity_scores[0, i]))
    if len(top_concerts) == how_many_results:  # Only need the top 3
        break

# Print the most similar concerts
if top_concerts:
    for idx, (title, score) in enumerate(top_concerts):
        print(f"{idx + 1}. {title} (相似度: {score:.2f})")
else:
    print("No matching concert found.")
