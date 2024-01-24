import json
import os

json_new = ['era.json',
            'ibon_new.json',
            'indievox.json',
            'kktix_new.json',
            'livenation.json',
            'ticketplus.json']


def integrate_json():
    # 完成之後先合併，輸出'concert_data_new_zh.json'
    merged_data = []
    for json_file in json_new:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            merged_data.extend(data)

    # 定義 concert_data.json 的相對路徑
    file_path = os.path.join('../..', '0_useless/concert_data.json')

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)

def number_of_each_data():
    with open('../era.json', 'r', encoding='utf-8') as f:
        era_data = json.load(f)
    with open('../0_useless/ibon_new.json', 'r', encoding='utf-8') as f:
        ibon_data = json.load(f)
    with open('../indievox.json', 'r', encoding='utf-8') as f:
        indievox_data = json.load(f)
    with open('../kktix_new.json', 'r', encoding='utf-8') as f:
        kktix_data = json.load(f)
    with open('../livenation.json', 'r', encoding='utf-8') as f:
        livenation_data = json.load(f)
    with open('../ticketplus.json', 'r', encoding='utf-8') as f:
        ticketplus_data = json.load(f)
    with open('concert_data.json', 'r', encoding='utf-8') as f:
        concert_data = json.load(f)

    print('era\t\t\t', len(era_data))
    print('ibon\t\t', len(ibon_data))
    print('indievox\t', len(indievox_data))
    print('kktix\t\t', len(kktix_data))
    print('livenation\t', len(livenation_data))
    print('ticketplus\t', len(ticketplus_data))
    print('concert\t\t', len(concert_data))


integrate_json()
# number_of_each_data()
# with open('concert_data.json', 'r', encoding='utf-8') as f:
#     concert_data = json.load(f)
# for i in range(len(concert_data)):
#     print(concert_data[i]['int'])
