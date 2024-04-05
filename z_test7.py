# with open('concert_pin_postid.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#
# print(lines)
#
# with open('concert_pin_postid.txt', 'a', encoding='utf-8') as f:
#     f.write('hello\n')
from y_example_read_json import *
import json

# from get_concert_info import *

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
             "concert_4_3_22.json",
             "concert_4_4_3.json",
             "concert_4_4_14.json"
             ]

a = ['350', '123']
print(a)
for index, price in enumerate(a):
    if isinstance(price, str):
        try:
            a[index] = int(price)
        except:
            pass
print(a)

for i in range(len(json_list)):
    data = read_json(json_list[i])
    for j in range(len(data)):
        for index, price in enumerate(data[j]['prc']):
            if isinstance(price, str):
                print(data[j]['prc'])
                try:
                    data[j]['prc'][index] = int(price)
                except:
                    pass
                print(data[j]['prc'])




# ''' 刪除不必要的kktix資訊 '''
# data = read_json(json_list[i])
# delete_titles = ["【免費索票體驗】KKTIX 虛擬活動票務系統，搭配外部串流平台",
#                  "【免費索票體驗】KKTIX Live，一站式售票、觀賞活動超流暢",
#                  "【免費體驗】KKTIX Live，外部售票系統，輸入兌換碼馬上開播"]
# new_data = [item for item in data if item['tit'] not in delete_titles]
# with open(json_list[i], 'w', encoding='utf-8') as f:
#     json.dump(new_data, f, indent=4, ensure_ascii=False)

# ''' 根據地址填上城市 '''
# get_city_from_stadium(json_list[i])

# ''' 根據日期排序 '''
# json_in_order(json_list[i])
