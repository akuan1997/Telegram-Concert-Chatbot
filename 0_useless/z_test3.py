import json
import yaml
import re

def load_keywords(path):
    with open(path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    examples_text = data['nlu'][0]['examples']
    keywords = [line.replace('- ', '').strip() for line in examples_text.split('\n') if line.strip() != '']
    return keywords


def improved_match(keyword, text):
    pattern = r'\b' + re.escape(keyword) + r'(?=\W|$)'  # (?=\W|$) 斷言關鍵詞後是非字母數字字符或字符串末尾
    if re.search(pattern, text, re.IGNORECASE):
        return True
    return False


with open('concert_4_15_1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

keywords = load_keywords('../data/keyword.yml')

for i in range(len(data)):
    for keyword in keywords:
        if improved_match(keyword, data[i]['tit']):
            print(f'{keyword}///{data[i]["tit"]}')
            print('---')

# for index, keyword in enumerate(keywords):
#     if keyword == '':
#         print(index)

# for i in range(len(data)):
#     for keyword in keywords:
#         if keyword in data[i]['tit']:
#             print(f'{keyword}///{data[i]["tit"]}')
#             # print(keyword, '|||', data[i]['tit'])
#             print('---')
    # best_match, score = find_best_match(data[i]['tit'], keywords)
    # print(f"User input: {data[i]['tit']}")
    # print(f"Did you mean: {best_match} (score: {score})\n")
