from get_city_date_indexes import *

# with open('z_test12.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#
# lines = [line.replace('\n', '') for line in lines if '-' not in line]
# test_words = [
#     '四月',
#
#     # '明年以前 搶票',
#     # '下個月初以及四月中',  # 錯誤
#     # '下個月初還有五月中',  # 錯誤
#     # '下個月初、四月底',  # 錯誤
#     # '下個月',
#     # '下個月初',
#     # '四月初',
#     # '四月中',
#     # '下週日以及下周六',
#     # '下下周以及下周',
#     # '下周六以及下周日',
#     # '下下周二',
#     # "下下周二我想要去健身房運動",
#     # '明年三月十一號晚上八點',
#     # '明年三月十一號',
#     # '明年三月',
#     # '三月十一號晚上八點',
#     # '三月十一號',
#     # '三月',
#     # # '十一號晚上八點',  # 錯誤
#     # # '十一號',  # 錯誤
#     # '晚上八點',
#     # '2024-10-5 20:00',
#     # '九月的晚上和十月的下午',
#     # '九月晚上和十月下午',
#     # '十月和十一月的下午',
#     # '十一月和十二月 晚上八點之後',
#     # '十一月和十二月的晚上八點之後',
#     # '十一月八號晚上九點到十一點之間',
#     # '十一月八號 晚上九點到十一點之間',
#     # '下禮拜一',
#     # '明年三月和五月',
#     # '明年三月到五月之間',
#     # '今年八月和九月',
#     # '今年 八月 九月 十月'
# ]
#
# for line in lines:
#     zh_get_ticket_time(line)
#     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

''''''
with open('z_test11.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
lines = [line.replace('\n', '') for line in lines if '-' not in line]
for line in lines:
    en_get_dates(line)
    # ticket_indexes = en_get_ticket_time(line, 'concert_data_old_zh.json')
    print(f'ticket_indexes = {ticket_indexes}')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
