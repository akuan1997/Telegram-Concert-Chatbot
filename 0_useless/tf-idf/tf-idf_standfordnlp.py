import stanfordnlp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

# Initialize Stanford NLP for Chinese language
# stanfordnlp.download('zh')  # Download Chinese models
nlp = stanfordnlp.Pipeline(lang='zh')

user_input = "怕胖團"


# Function to tokenize text using Stanford NLP
def tokenize_with_stanfordnlp(text):
    doc = nlp(text)
    tokens = [word.text for sent in doc.sentences for word in sent.words]
    return ' '.join(tokens)


# Your concert data processing
with open('concert_data.json', 'r', encoding='utf-8') as file:
    concert_data = json.load(file)

# Tokenize and process documents
documents = [tokenize_with_stanfordnlp(concert["tit"] + " " + concert["int"]) for concert in concert_data]

# TF-IDF Vectorization
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

# Process user input with tokenization and vectorization
user_input_tokenized = tokenize_with_stanfordnlp(user_input)
user_input_tfidf = vectorizer.transform([user_input_tokenized])

# Calculate cosine similarity
cosine_similarities = cosine_similarity(user_input_tfidf, tfidf_matrix)

# Identify the concert with the highest similarity score
most_similar_concert_index = np.argmax(cosine_similarities)
most_similar_concert = concert_data[most_similar_concert_index]

# Output the result
print(f"The most similar concert to your input is: {most_similar_concert['tit']}")

# Remember to handle exceptions and errors in real applications.
