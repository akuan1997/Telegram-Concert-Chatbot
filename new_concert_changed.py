import json


def load_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return json.load(file)


def compare_concerts(new_concert, old_concerts):
    for old_concert in old_concerts:
        if new_concert['url'] == old_concert['url']:
            return old_concert
    return None


def find_changes(new_concert, old_concert):
    changes = []
    for field in ['sdt', 'prc', 'pdt', 'int']:
        if new_concert[field] != old_concert[field]:
            print(new_concert['tit'])
            print(new_concert[field])
            print(old_concert[field])
            # print(new_concert['url'])
            # print(old_concert['url'])
            print('--------------')
            changes.append(field)
    return changes


# 加载数据
old_concerts = load_data('concert_data_old_zh.json')
new_concerts = load_data('concert_data_new_zh.json')

new_concert_list = []
changed_concert_list = []

# 比较数据
for new_concert in new_concerts:
    matched_concert = compare_concerts(new_concert, old_concerts)
    if matched_concert is None:
        new_concert_list.append(new_concert)
    else:
        changes = find_changes(new_concert, matched_concert)
        if changes:
            changed_concert_list.append((new_concert, changes))

# 打印结果
print("新的演唱会信息:")
for concert in new_concert_list:
    print(concert['tit'])
    if not concert['sdt']:
        print(f"售票時間:\t已開放售票")
    else:
        print(f"售票時間:\t{concert['sdt']}")
    print(f"票   價:\t{concert['prc']}")
    print(f"表演時間:\t{concert['pdt']}")
    print(f"地   點:\t{concert['loc']}")
    print(f"售票網站:\t{concert['web']}")
    print(f"網   址:\t{concert['url']}")

print("\n发生变化的演唱会信息:")
for concert, changes in changed_concert_list:
    print(f"{concert} - 变化的部分: {changes}")
