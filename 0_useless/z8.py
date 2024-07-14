# # # txt = f"""
# # # Usage Instructions
# # # Inquire by artist name, genre, city, or specific time
# # #
# # # Example inputs:
# # # "Taylor Swift"
# # # "Rap"
# # # "Taipei"
# # # "Tomorrow"
# # # Specify multiple criteria simultaneously
# # #
# # # Example inputs:
# # # "Taylor Swift concerts in Taipei"
# # # "Post Malone, next month"
# # # "Hip-Hop, this week, and in Tainan city"
# # # Sample Queries
# # # Inquire about Jazz concerts in Taipei
# # #
# # # Query details:
# # # Keyword: Jazz
# # # City: Taipei
# # # Check if Post Malone has any concerts in Taipei this year
# # #
# # # Query details:
# # # Keyword: Post Malone
# # # Date: this year
# # # City: Taipei
# # # Get information on R&B festivals happening in Kaohsiung next month
# # #
# # # Query details:
# # # Keyword: R&B
# # # City: Kaohsiung
# # # Date: next month
# # # Find out which concerts are open for sale tomorrow
# # #
# # # Query details:
# # # Date: tomorrow
# # # """
# # # print(txt)
# #
# # # matched_tags = ['city']
# # # all_tags = ['keyword', 'date', 'city']
# # # further_search_tags = [tag for tag in all_tags if tag not in matched_tags]
# # # print(f"further_search_tags = {further_search_tags}")
# # # print(f"You can refine your search by specifying more details: {', '.join(further_search_tags)}")
# #
# # list1 = [1, 2, 3, 4]
# # list2 = [1, 3, 4, 5, 6]
# # list3 = [1, 6, 7, 8, 9]
# # list4 = [1, 9, 10, 11]
# #
# # # 使用集合操作取并集
# # union_set = set(list1) & set(list2) & set(list3) & set(list4)
# #
# # # 转换回列表
# # union_list = list(union_set)
# #
# # # 打印结果
# # print(f"The union of the four lists is: {union_list}")
# #
# from rank_bm25 import BM25Okapi
#
# import jieba
# import numpy as np
# import json, re
#
# def jieba_english_tokenize(words):
#     '''
#     1. "post", " ", "malone"
#     >> "post malone"
#     2. "austin", " ", "richard", " ", "post"
#     >> "austin richard post"
#     '''
#     pattern = r'^[a-zA-Z0-9]+$'
#     blank_space_indexes = []
#     for i in range(len(words) - 1):
#         if words[i] == ' ' and re.match(pattern, words[i - 1]) and re.match(pattern, words[i + 1]):
#             blank_space_indexes.append(i)
#     # print('空格有這些', blank_space_indexes)
#     # --- #
#     processed_indexes = []
#     english_words = []
#     for index in blank_space_indexes:
#         if index not in processed_indexes:
#             english_word = ''
#             if index + 2 not in blank_space_indexes:
#                 # 'post malone', 'taylor swift' 直接處理
#                 for i in range(index - 1, index + 2):
#                     english_word = english_word + words[i]
#                     processed_indexes.append(i)
#             else:
#                 # 'austin richard post', 'show me the money'
#                 start_index = index
#                 while index + 2 in blank_space_indexes:
#                     index = index + 2
#                 end_index = index
#                 for i in range(start_index - 1, end_index + 2):
#                     english_word = english_word + words[i]
#                     processed_indexes.append(i)
#             # print(english_word)
#             english_words.append(english_word)
#             # print(list(set(processed_indexes)))
#             # print('---')
#
#     words = [words[i] for i in range(len(words)) if i not in processed_indexes]
#     for english_word in english_words:
#         words.append(english_word)
#
#     return words
#
# print(jieba.lcut("Post Malone"))
# print(jieba_english_tokenize(jieba.lcut("Post Malone")))
with open('z8.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
lines = [line.replace('\n', '') for line in lines]
print("\\begin{itemize}")
for index, line in enumerate(lines):
    if index == 0:
        continue
    # elif index == 1:
    #     print(f"\item Participant {index + 1}: {line}")
    else:
        print(f"\t\item Participant {index}: {line}")

    if index == 15:
        break
print("\\end{itemize}")