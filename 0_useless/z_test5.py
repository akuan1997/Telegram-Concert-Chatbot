import json
from read_json_function import *
from datetime import datetime

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
             "concert_4_4_14.json",
             "concert_4_5_16.json"]


# delete_past_ticketing_time('concert_zh.json')
# data = read_json('concert_zh.json')
# for i in range(len(data)):
#     if data[i]['sdt']:
#         print(data[i]['sdt'])
def print_list_str(lst):
    lst_str = ''
    if len(lst) == 1 and lst[0] != '':
        lst_str = lst[0]
    elif len(lst) > 1:
        for i in range(len(lst)):
            lst_str += str(lst[i]) + ' / '
        lst_str = lst_str[:-3]
    else:
        lst_str = '-'

    return lst_str
    # print(lst)
    # print(len(lst))
    # for i in range(len(lst)):
    #     lst_str += lst[i] + ' / '
    # print(lst_str)
    # if lst_str == '':
    #     lst_str = '-'
    #     print('in function', lst_str)
    # else:
    #     print('in function', lst_str)
    #     lst_str = lst_str[:-3]
    #
    # return lst_str


data = read_json(json_list[0])
for i in range(len(data)):
    sdt = ''
    prc = ''
    pdt = ''
    loc = ''
    print('售票時間\t:', print_list_str(data[i]['sdt']))
    print('價格\t\t:', print_list_str(data[i]['prc']))
    print('表演時間\t:', print_list_str(data[i]['pdt']))
    print('地點\t\t:', print_list_str(data[i]['loc']))
    print('售票網站\t:', data[i]['web'])
    print('售票網址\t:', data[i]['url'])
    print('---')

# for i in range(len(json_list)):
#     data = read_json(json_list[i])
#     for j in range(len(data)):
#         if len(data[j]['sdt']) > 1:
#             print(data[j]['sdt'])
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
