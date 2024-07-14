# id = "7043645741"
# with open("user_preferred_language.txt", 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#
# for line in lines:
#     if id in line:
#         print(line[line.index('|||') + 3:line.index('|||') + 5])
#
#
# # lines = [line.replace('\n', '').split('|||')[0] for line in lines]
# #
# # if "7043645741" in lines:
# #     print('eyu')
#
# def get_language(id, lines):
#     for line in lines:
#         if id in line:
#             return line[line.index('|||') + 3:line.index('|||') + 5]
with open('z_test11.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
lines = [line.replace('\n', '').split('. ')[1] for line in lines]
for line in lines:
    print(line)