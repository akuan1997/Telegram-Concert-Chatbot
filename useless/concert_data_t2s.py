# import opencc
# converter = opencc.OpenCC('s2twp.json')
# a = converter.convert('汉字')  # 漢字
# print(a)
#
# converter = opencc.OpenCC('t2s.json')
# a = converter.convert('漢字')  # 汉字
# print(a)

import json
import opencc
converter = opencc.OpenCC('t2s.json')

with open('concert_data_s.json', 'w', encoding='utf-8') as file:
    file.write('')

# 打開'concert_data.json'並讀取資料
with open('../concert_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 複製資料到'concert_data_s.json'
with open('concert_data_s.json', 'w', encoding='utf-8') as file:
    # json.dump(data, file, ensure_ascii=False, indent=2)
    json.dump(data, file, indent=4, ensure_ascii=False)

with open('concert_data_s.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for i in range(len(data)):
    data[i]['tit'] = converter.convert(data[i]['tit'])
    data[i]['int'] = converter.convert(data[i]['int'])

    with open('concert_data_s.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# # 將'concert_data_s.json'中的繁體字轉換成簡體字
# cc = OpenCC('t2s')
# with open('concert_data_s.json', 'r', encoding='utf-8') as file:
#     simplified_data = json.load(file)
#     simplified_data = cc.convert(simplified_data)
#
# # 覆寫'concert_data_s.json'，以保存簡體字版本的資料
# with open('concert_data_s.json', 'w', encoding='utf-8') as file:
#     json.dump(simplified_data, file, ensure_ascii=False, indent=2)
