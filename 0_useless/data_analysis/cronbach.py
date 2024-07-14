import pandas as pd
from scipy.stats import pearsonr

# Load the data from the uploaded CSV file
file_path = 'data.csv'

# Attempt to load the CSV with different encoding to handle the UnicodeDecodeError
try:
    df = pd.read_csv(file_path, encoding='utf-8-sig')
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding='latin1')

# Rename columns to readable names
df.columns = [
    'ID', 'Like_Chatbot', 'Like_Website', 'Future_Use_Chatbot', 'Future_Use_Website',
    'Recommend_Chatbot', 'Recommend_Website'
]

# Check the updated dataframe
print(df.head())

# Calculate the correlation matrix
correlation_matrix = df[
    ['Like_Chatbot', 'Like_Website', 'Future_Use_Chatbot', 'Future_Use_Website']
].corr()

# Define the function to calculate Cronbach's alpha
def cronbach_alpha(df):
    item_corr_sum = correlation_matrix.values.sum()
    num_items = len(correlation_matrix)
    alpha = num_items / (num_items - 1) * (1 - item_corr_sum / (num_items ** 2))
    return alpha

# Calculate Cronbach's alpha
cronbach_alpha_value = cronbach_alpha(
    df[['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9']]
)
print(f'Cronbach\'s alpha: {cronbach_alpha_value}')
