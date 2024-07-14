from get_concert_new_old import *

json_list = ["concert_3_14_23.json",
             "concert_3_17_16.json",
             "concert_3_17_19.json",
             "concert_3_18_13.json",
             "concert_3_20_16.json",
             "concert_3_22_0.json",
             "concert_3_23_14.json",
             "concert_3_24_8.json",
             "concert_3_25_0.json",
             "concert_3_25_17.json",
             "concert_3_26_0.json",
             "concert_3_27_3.json",
             "concert_3_29_0.json",
             "concert_3_30_13.json",
             "concert_3_30_20.json",
             "concert_3_31_14.json",
             "concert_3_31_18.json",
             "concert_4_2_0.json",
             "concert_4_3_10.json",
             "concert_4_4_3.json",
             "concert_4_4_14.json"]

# for current_index in range(16):
current_index = 0
write_json = 0  # 0 not write, 1 write (for testing)
old_json = json_list[current_index]
new_json = json_list[current_index + 1]

print(f"{json_list[current_index]} + {json_list[current_index + 1]}")

with open(new_json, 'r', encoding='utf-8') as f:
    new_data = json.load(f)

with open(old_json, 'r', encoding='utf-8') as f:
    old_data = json.load(f)

with open('../concert_zh.json', 'r', encoding='utf-8') as f:
    all_data = json.load(f)

with open('concert_zh1.json', "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=4, ensure_ascii=False)

pins_new = [entry['pin'] for entry in new_data]
pins_old = [entry['pin'] for entry in old_data]

new_but_old_pins = [pin for pin in pins_new if pin not in pins_old]
old_but_new_pins = [pin for pin in pins_old if pin not in pins_new]

''' test '''
print(f'len(new_data) = {len(new_data)}')
print(f'len(old_data) = {len(old_data)}')
print(f'len(all_data) = {len(all_data)}')
# pins_all = [entry['pin'] for entry in all_data]
# test_pins = [pin for pin in old_but_new_pins if pin in pins_all]
# test_pins1 = [pin for pin in pins_all if pin in old_but_new_pins]
# print(len(test_pins))
# print(len(test_pins1))
# for pin in old_but_new_pins:
#     print(pin)
print(f'len(new_but_old_pins) = {len(new_but_old_pins)}')
print(f'len(old_but_new_pins) = {len(old_but_new_pins)}')
''' test '''

all_data = get_new_delete_compare_concerts(all_data)
# 4. 寫進json裡面
if write_json == 1:
    with open('../concert_zh.json', "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)

# '''test'''
# print(f'len(new_data) = {len(new_data)}')
# print(f'len(old_data) = {len(old_data)}')
print(f'current_index = {current_index}')
print(f"{json_list[current_index]} + {json_list[current_index + 1]}")
print(f'len(all_data) = {len(all_data)}')
# '''test'''
