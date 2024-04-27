# with open('japanese_sorted_waiting.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
# with open('korean_sorted_waiting.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
# with open('chinese_sorted_waiting.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
# print(lines)
# if lines == []:
#     print('yes')
# else:
#     print('no')

with open('western_sorted.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    number = line.count('(')
    if number > 1:
        print(line)