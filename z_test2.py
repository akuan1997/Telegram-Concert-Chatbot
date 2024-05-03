from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import yaml
import json

def load_keywords(path):
    with open(path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    examples_text = data['nlu'][0]['examples']
    keywords = [line.replace('- ', '').strip() for line in examples_text.split('\n') if line.strip() != '']
    return keywords


def find_best_match(input_text, keywords):
    input_text = input_text.lower()
    best_match = None
    highest_score = 0

    # 使用 token_sort_ratio 來改善多詞匹配
    for keyword in keywords:
        score = fuzz.token_sort_ratio(input_text, keyword.lower())
        if score > highest_score:
            highest_score = score
            best_match = keyword

    return best_match, highest_score


# 載入歌手名稱
keywords = load_keywords('data/keyword.yml')

# 測試用例
test_cases = [
    '我想要知道post malone的演唱會',
    '我想要知道taylor swift的演唱會',
    '我想要知道Taylor Swift的演唱會',
    '我想要知道tayolr Swift的演唱會',
    '我想要知道iu的演唱會',
    '我想要知道akmu的演唱會',
    '我想要知道鄭恩地的演唱會資訊，你可以跟我說嗎?',
    '最近五月天會開演唱會嗎?',
    '最近池俊寬的演唱會資訊',
    'tien duu',
    '請告訴我anderson malone演唱會資訊',
    '林俊傑 演唱會',
    '請告訴我有關於林俊傑的演唱會',
    '你知道張學友最近的演唱會資訊嗎?',
    '我想要知道台北接下來五月的演唱會資訊',
    '台北 演唱會 三月'
]


for test in test_cases:
    best_match, score = find_best_match(test, keywords)
    print(f"User input: {test}")
    print(f"Did you mean: {best_match} (score: {score})\n")
