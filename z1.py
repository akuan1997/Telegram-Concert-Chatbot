# with open('concert_pin_postid.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#
# pin = "https://ticketplus.com.tw/activity/8455304be5b4ffef154340fd40d9dfa71"
# for index, line in enumerate(lines):
#     line_pin = line.split('|||')[1].replace('\n', '')
#     if pin == line_pin:
#         lines.pop(index)
#
# with open('concert_pin_postid1.txt', 'w', encoding='utf-8') as f:
#     f.writelines(lines)
#
# print(lines)
# print(len(lines))
import json
from y_example_read_json import *
json_list = [
    "concert_jsons/concert_3_14_23.json",
    "concert_jsons/concert_3_17_16.json",
    "concert_jsons/concert_3_17_19.json",
    "concert_jsons/concert_3_18_13.json",
    "concert_jsons/concert_3_20_16.json",
    "concert_jsons/concert_3_22_0.json",
    "concert_jsons/concert_3_23_14.json",
    "concert_jsons/concert_3_24_8.json",
    "concert_jsons/concert_3_25_0.json",
    "concert_jsons/concert_3_25_17.json",
    "concert_jsons/concert_3_26_0.json",
    "concert_jsons/concert_3_27_3.json",
    "concert_jsons/concert_3_29_0.json",
    "concert_jsons/concert_3_30_13.json",
    "concert_jsons/concert_3_30_20.json",
    "concert_jsons/concert_3_31_14.json",
    "concert_jsons/concert_3_31_18.json",
    "concert_jsons/concert_4_15_1.json",
    "concert_jsons/concert_4_2_0.json",
    "concert_jsons/concert_4_3_10.json",
    "concert_jsons/concert_4_3_22.json",
    "concert_jsons/concert_4_4_14.json",
    "concert_jsons/concert_4_4_3.json",
    "concert_jsons/concert_4_5_16.json",
    "concert_jsons/concert_4_7_17.json",
    "concert_jsons/concert_5_2_14.json",
    "concert_jsons/concert_5_4_20.json",
    "concert_jsons/concert_5_7_1.json",
    "concert_jsons/concert_5_7_21.json",
    "concert_jsons/concert_5_8_16.json",
]

for i in range(len(json_list)):
    data = read_json(json_list[i])
    for j in range(len(data)):
        if data[j]['tit'] == '':
            print(data[j]['web'])
            print(data[j]['url'])
    print('-----------------------------------------')