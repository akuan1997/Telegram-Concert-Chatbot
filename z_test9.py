from concert_new_old1 import *

new_json = 'concert_3_17_16.json'
old_json = 'concert_3_14_23.json'

with open(new_json, 'r', encoding='utf-8') as f:
    new_data = json.load(f)

with open(old_json, 'r', encoding='utf-8') as f:
    old_data = json.load(f)

with open('concert_zh.json', 'r', encoding='utf-8') as f:
    all_data = json.load(f)

print(f'len(new_data) = {len(new_data)}')
print(f'len(old_data) = {len(old_data)}')
print(f'len(all_data) = {len(all_data)}')

pins_new = [entry['pin'] for entry in new_data]
pins_old = [entry['pin'] for entry in old_data]

new_but_old_pins = [pin for pin in pins_new if pin not in pins_old]
old_but_new_pins = [pin for pin in pins_old if pin not in pins_new]

print(f'len(pins_new) = {len(new_but_old_pins)}')
print(f'len(pins_old) = {len(old_but_new_pins)}')

# 1. 新增新的演唱會資訊
# show_new_but_old(new_but_old_pins)
# new_concerts(new_but_old_pins, new_data, all_data)
# 2. 移除那些演唱會無法獲得的演唱會資訊
# show_old_but_new(old_but_new_pins)
# old_concert_delete(old_but_new_pins, all_data)
# # ! 3. 寫進concert.json裡面
# 4. 比較內文
check_each_info(new_data, old_data, all_data)

# with open('concert_zh.json', "w", encoding="utf-8") as f:
#     json.dump(all_data, f, indent=4, ensure_ascii=False)