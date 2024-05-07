# import json
# import re
#
# with open('singer_info.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
# pattern = r"\((.*?)\)"
# full_names = []
# for i in range(len(data)):
#     full_name = data[i]['singer_name']
#     bracket_name = re.findall(pattern, full_name)
#     # 裡面有括號
#     if bracket_name:
#         without_bracket_name = full_name[:full_name.index('(')].strip()
#         full_names.append(without_bracket_name)
#         full_names.append(bracket_name[0])
#     # 裡面沒有括號，直接加進去
#     else:
#         full_names.append(full_name)
#
# for name in full_names:
#     chinese_name = re.findall(r'[\u4e00-\u9fff]', name)
#     if chinese_name:
#         pass
#     else:
#         print(f'      - {name}')
# #     bracket_name = re.findall(pattern, data[i]['singer_name'])
# #     if bracket_name:
# #         bracket_names.append(bracket_name[0])
# #     else:
# #         name = data[i]['singer_name']
# #         if '(' in name:
# #             name = name[:name.index('(')].strip()
# #             names.append(name)
# #         else:
# #             names.append(name)
# #
# # for bracket_name in bracket_names:
# #     print(bracket_name)
# # for name in names:
# #     print(name)
# # user_status = {}
# # user_id = "12345"
# # current_status = "active"
# # user_status[user_id] = current_status
# # print(user_status)

import json
from y_example_read_json import *

data = read_json("singer_info.json")
print(len(data))
# print(data[9])
# for i in range(len(data)):
#
#     if '\"' in data[i]['tit']:
#         print(i, data[i]['tit'])

# print(data[289]['tit'])
# if data[289]['tit']:
#     print('yes')
# else:
#     print('no')
