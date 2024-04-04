# with open('concert_pin_postid.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#
# print(lines)
#
# with open('concert_pin_postid.txt', 'a', encoding='utf-8') as f:
#     f.write('hello\n')
from y_example_read_json import *
import json
from get_concert_info import *

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
             "concert_4_3_22.json"]

for i in range(len(json_list)):
    # json_in_order(json_list[i])
    get_city_from_stadium(json_list[i])
    # data = read_json(json_list[i])
    # for j in range(len(data)):
    #     print(data[j]['pdt'])
    # print('----------------------------')