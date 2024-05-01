import re


def contains_english_and_chinese(text):
    # 檢查是否包含英文
    english_pattern = re.compile(r'[a-zA-Z]')
    # 檢查是否包含中文
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')

    return bool(english_pattern.search(text)) and bool(chinese_pattern.search(text))


# 範例
# text = "hello 你好"
# result = contains_english_and_chinese(text)
# print("Contains both English and Chinese:", result)

import json
with open('singer_info.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
pattern = r"\((.*?)\)"
for i in range(len(data)):
    if contains_english_and_chinese(data[i]['singer_name']):
        brackets = re.findall(pattern, data[i]['singer_name'])
        if brackets:
            pass
        else:
            print(data[i]['singer_name'])