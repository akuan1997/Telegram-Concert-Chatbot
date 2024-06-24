import re
from datetime import datetime, timedelta

# 定义时间单位和对应的秒数
time_units = {
    'second': 1,
    'seconds': 1,
    'sec': 1,
    'secs': 1,
    'minute': 60,
    'minutes': 60,
    'min': 60,
    'mins': 60,
    'hour': 3600,
    'hours': 3600,
    'day': 86400,
    'days': 86400,
    'week': 604800,
    'weeks': 604800,
    'month': 2592000,
    'months': 2592000,
}


def convert_time_to_seconds(sentence):
    # 使用正则表达式提取时间
    pattern = r'(\d+)\s*(seconds?|secs?|minutes?|mins?|hours?|days?|weeks?|months?)'
    matches = re.findall(pattern, sentence, re.IGNORECASE)

    total_seconds = 0
    for match in matches:
        value = int(match[0])
        unit = match[1].lower()
        total_seconds += value * time_units[unit]

    return total_seconds


# date_time_str = "2024/6/10 12:00"
# # 示例句子
# # 将字符串转换为datetime对象
# date_time = datetime.strptime(date_time_str, "%Y/%m/%d %H:%M")
# print(date_time)
# # sentence = "1 day and 2 hours and 30 minutes."
# sentence = "5 secs"
# total_seconds = convert_time_to_seconds(sentence)
# new_date_time = date_time - timedelta(seconds=total_seconds)
# print(new_date_time)
# # print(f"The total time in seconds is: {total_seconds}")
#
# now = datetime.now()
# print(now)
# new_date_time = now + timedelta(seconds=5)
# print(new_date_time)
# print(new_date_time.hour)


def format_seconds(seconds):
    units = [
        ('year', 60 * 60 * 24 * 365),
        ('month', 60 * 60 * 24 * 30),
        ('week', 60 * 60 * 24 * 7),
        ('day', 60 * 60 * 24),
        ('hour', 60 * 60),
        ('minute', 60),
        ('second', 1),
    ]

    result = []
    for name, count in units:
        value = seconds // count
        if value:
            seconds -= value * count
            unit_name = name if value == 1 else name + 's'
            result.append(f"{value} {unit_name}")

    return ', '.join(result) if result else "0 seconds"


# # 示例用法
# print(format_seconds(60))  # 1 minute
# print(format_seconds(75))  # 1 minute 15 seconds
# print(format_seconds(3662))  # 1 hour 1 minute 2 seconds
# print(format_seconds(90061))  # 1 day 1 hour 1 minute 1 second

""""""
time_units_zh = {
    '秒': 1,
    '秒鐘': 1,
    '分': 60,
    '分鐘': 60,
    '小時': 3600,
    '天': 86400,
    '周': 604800,
    '週': 604800,
    '月': 2592000,
}


def chinese_to_arabic(chinese_number):
    chinese_numerals = {
        '零': 0,
        '一': 1,
        '二': 2,
        '三': 3,
        '四': 4,
        '五': 5,
        '六': 6,
        '七': 7,
        '八': 8,
        '九': 9,
        '十': 10,
    }

    num = 0
    if '十' in chinese_number:
        parts = chinese_number.split('十')
        if parts[0] == '':
            num += 10
        else:
            num += chinese_numerals[parts[0]] * 10
        if len(parts) > 1 and parts[1] != '':
            num += chinese_numerals[parts[1]]
    else:
        num = chinese_numerals[chinese_number]

    return num


def extract_number(time_string):
    pattern = r'(\d+|[\u4e00-\u9fff]+)\s*(秒鐘?|分鐘?|小時|天|周|週|月)'
    matches = re.findall(pattern, time_string)

    total_seconds = 0
    for match in matches:
        number, unit = match
        if number.isdigit():
            value = int(number)
        else:
            value = chinese_to_arabic(number)
        total_seconds += value * time_units_zh[unit]

    return total_seconds


def convert_time_to_seconds_zh(sentence):
    return extract_number(sentence)


date_time_str = "2024/6/10 12:00"
# 将字符串转换为datetime对象
date_time = datetime.strptime(date_time_str, "%Y/%m/%d %H:%M")
print(date_time)
# 示例句子
sentence = "五十分鐘"
total_seconds = convert_time_to_seconds_zh(sentence)
new_date_time = date_time - timedelta(seconds=total_seconds)
print(new_date_time)


def format_seconds_zh(seconds):
    units = [
        ('年', 60 * 60 * 24 * 365),
        ('月', 60 * 60 * 24 * 30),
        ('周', 60 * 60 * 24 * 7),
        ('天', 60 * 60 * 24),
        ('小時', 60 * 60),
        ('分鐘', 60),
        ('秒', 1),
    ]

    result = []
    for name, count in units:
        value = seconds // count
        if value:
            seconds -= value * count
            result.append(f"{value} {name}")

    return ', '.join(result) if result else "0 秒"


# 示例用法
print(format_seconds_zh(60))  # 1 minute
print(format_seconds_zh(75))  # 1 minute 15 seconds
print(format_seconds_zh(3662))  # 1 hour 1 minute 2 seconds
print(format_seconds_zh(90061))  # 1 day 1 hour 1 minute 1 second
