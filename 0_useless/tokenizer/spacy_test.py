import spacy
from spacy.tokens import Doc

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


# Define a function to load user-defined terms from a file
def load_user_terms(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            term = line.strip()  # Remove any leading/trailing whitespace
            if term:  # Check if the term is not empty
                # Add the term as a special case to the tokenizer
                nlp.tokenizer.add_special_case(term, [{spacy.symbols.ORTH: term}])


# Path to the user dictionary file
user_dict_path = "user_dict.txt"

# Load the user-defined terms into spaCy
load_user_terms(user_dict_path)

# Example text to test if the custom terms are recognized
test_text = "tarlor swift"

# Process the text with spaCy
doc = nlp(test_text)

# Print out tokens to verify custom terms are tokenized correctly
print([token.text for token in doc])
