# from fuzzywuzzy import fuzz
# import json
# import re
#
#
# # with open('concert_data_old_zh.json', 'r', encoding='utf-8') as f:
# #     data = json.load(f)
# #
# # count = 0
# # for i in range(len(data)):
# #     if data[i]['cit'] == '台北':
# #         print(data[i]['tit'])
# #         count = count + 1
# # print(count)
#
# def results_compare(txt1, txt2):
#     with open(txt1, 'r', encoding='utf-8') as f:
#         data1 = f.readlines()
#
#     leftovers = []
#
#     for i in range(len(data1)):
#         found = False
#         title = data1[i]
#         print('title', title)
#         # ---
#         with open(txt2, 'r', encoding='utf-8') as f:
#             data2 = f.readlines()
#
#         for j in range(len(data2)):
#             if title == data2[j]:
#                 print(data2[j])
#
#                 del data2[j]
#
#                 with open(txt2, 'w', encoding='utf-8') as f:
#                     for data_piece in data2:
#                         f.write(data_piece)
#
#                 found = True
#
#                 break
#
#         if found:
#             print('刪除')
#         else:
#             leftovers.append(i)
#         print('---')
#
#     for leftover in leftovers:
#         print(data1[leftover])
#
# results_compare('z_test6.txt', 'z_test7.txt')
#
# # for i in range(len(data)):
# #     start_found = False
# #     end_found = False
# #     if len(data[i]['pdt']) == 1:
# #         if '~' in data[i]['pdt'][0]:
# #             title = data[i]['tit']
# #             print(title)
# #             print(data[i]['pdt'][0])
# #             dates = re.findall(r"\d{4}/\d{1,2}/\d{1,2}", data[i]['pdt'][0])
# #             start_date = dates[0]
# #             end_date = dates[1]
# #             for j in range(len(data)):
# #                 if not i == j:
# #                     if title == data[j]['tit']:
# #                         if len(data[j]['pdt']) == 1:
# #                             if start_date in data[j]['pdt'][0]:
# #                                 start_found = True
# #                             if end_date in data[j]['pdt'][0]:
# #                                 end_found = True
# #             print('start', start_found)
# #             print('end', end_found)
# #             if start_found and end_found:
# #                 print('found both')
# #
# #             print('---')
import jieba

jieba.load_userdict('user_dict.txt')

user_input = "(G)I-DLE"


# 使用jieba進行中文分詞
def chinese_tokenizer(text):
    if ' ' in text:
        if len(text.split(' ')) == 2:
            return [text]
    else:
        return jieba.lcut(text)

print(chinese_tokenizer(user_input))