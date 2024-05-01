import json
import re

with open('singer_info.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
pattern = r"\((.*?)\)"
full_names = []
for i in range(len(data)):
    full_name = data[i]['singer_name']
    bracket_name = re.findall(pattern, full_name)
    # 裡面有括號
    if bracket_name:
        without_bracket_name = full_name[:full_name.index('(')].strip()
        full_names.append(without_bracket_name)
        full_names.append(bracket_name[0])
    # 裡面沒有括號，直接加進去
    else:
        full_names.append(full_name)

for name in full_names:
    print(f'      - {name}')
#     bracket_name = re.findall(pattern, data[i]['singer_name'])
#     if bracket_name:
#         bracket_names.append(bracket_name[0])
#     else:
#         name = data[i]['singer_name']
#         if '(' in name:
#             name = name[:name.index('(')].strip()
#             names.append(name)
#         else:
#             names.append(name)
#
# for bracket_name in bracket_names:
#     print(bracket_name)
# for name in names:
#     print(name)
