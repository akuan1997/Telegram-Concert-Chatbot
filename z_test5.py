import json
from y_example_read_json import *

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


# data = read_json(json_list[0])
# for i in range(len(data)):
#     sdt = ''
#     prc = ''
#     pdt = ''
#     loc = ''
#
#     print('售票時間', data[i]['sdt'])
#     print('價格', data[i]['prc'])
#     print('表演時間', data[i]['pdt'])
#     print('地點', data[i]['loc'])
#     print('售票網站', data[i]['web'])
#     for j in range(len(data[i]['web'])):
#         pass
#     print('售票網址', data[i]['url'])
#     print('---')


for i in range(len(json_list)):
    data = read_json(json_list[i])
    for j in range(len(data)):
        if len(data[j]['sdt']) > 1:
            print(data[j]['sdt'])
        # data[j]['prc'] = sorted(data[j]['prc'], reverse=True)
        # print(data[j]['prc'])
        # print(data[j]['pin'])
        # with open(json_list[i], 'w', encoding='utf-8') as f:
        #     json.dump(data, f, indent=4, ensure_ascii=False)
    print('---------------------------------------')

# for i in range(len(json_list)):
#     data = read_json(json_list[i])
#     for j in range(len(data)):
#         # data[j]['prc'] = sorted(data[j]['prc'], reverse=True)
#         print(data[j]['prc'])
#         # with open(json_list[i], 'w', encoding='utf-8') as f:
#         #     json.dump(data, f, indent=4, ensure_ascii=False)

# for j in range(len(data)):
#     data[j]['prc'] = sorted(data[j]['prc'], reverse=True)
#     print(data[j]['prc'])
# # print(sorted_data)
#
# for j in range(len(data)):
#     data[j]['prc'] = sorted(data[j]['prc'], reverse=True)
#     print(data[j]['prc'])
# print('----------------------------------------------------')
# with open(json_list[i], 'w', encoding='utf-8') as f:
#     json.dump(data, f, indent=4, ensure_ascii=False)
