import json
from get_data_from_text import sort_datetime

def load_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return json.load(file)


def compare_concerts(new_concert, old_concerts):
    for old_concert in old_concerts:
        if new_concert['url'] == old_concert['url']:
            return old_concert
    return None


# 加载数据
old_concerts = load_data('concert_data_old_zh.json')
new_concerts = load_data('concert_data_new_zh.json')

new_concert_list = []

# 比较数据
for new_concert in new_concerts:
    matched_concert = compare_concerts(new_concert, old_concerts)
    if matched_concert is None:
        new_concert_list.append(new_concert)

# 打印结果
print("新的演唱会信息:")
for concert in new_concert_list:
    print(concert['tit'])

    # -------------------------------------
    # 表演時間
    # -------------------------------------

    # 创建两个空列表来存储表演时间信息
    performance_datetimes = []
    performance_datetimes_until = []

    # 遍历concert['pdt']中的每个表演时间
    for pdt in concert['pdt']:
        # 检查表演时间中是否包含'~'，如果包含，则将其添加到另一个列表中
        if '~' in pdt:
            performance_datetimes_until.append(pdt)
        else:
            # 否则，将其添加到第一个列表中
            performance_datetimes.append(pdt)

    # 对表演时间进行排序
    performance_datetimes = sort_datetime(performance_datetimes)

    # 创建空字符串来存储表演时间的字符串表示形式
    performance_datetime_str = ''
    performance_datetime_until_str = ''

    # 将排序后的表演时间转换为字符串
    for i, performance_datetime in enumerate(performance_datetimes):
        performance_datetime_str += performance_datetime
        if i < len(performance_datetimes) - 1:
            performance_datetime_str += ', '

    # 如果同时存在performance_datetimes和performance_datetimes_until
    if performance_datetimes and performance_datetimes_until:
        # 将performance_datetimes_until中的时间添加到字符串中
        for i, performance_datetime in enumerate(performance_datetimes_until):
            performance_datetime_until_str += f'({performance_datetime})'
            if i < len(performance_datetimes_until) - 1:
                performance_datetime_until_str += ', '
        # 合并performance_datetime_str和performance_datetime_until_str，用换行符分隔
        performance_datetime_str = performance_datetime_str + '\n' + performance_datetime_until_str
    # 如果只有performance_datetimes_until
    elif not performance_datetimes and performance_datetimes_until:
        # 直接将performance_datetimes_until中的时间赋值给performance_datetime_str
        for i, performance_datetime in enumerate(performance_datetimes_until):
            performance_datetime_until_str += f'{performance_datetime}'
            if i < len(performance_datetimes_until) - 1:
                performance_datetime_until_str += ', '
        performance_datetime_str = performance_datetime_until_str

    if performance_datetimes or performance_datetimes_until:
        print(f"表演時間\tPerformance Time:\t{performance_datetime_str}")
    else:
        print(f"表演時間\tPerformance Time:\t-")
    # -------------------------------------
    # 票價
    # -------------------------------------

    prices = []
    for price in concert['prc']:
        prices.append(price)
    price_str = ''
    prices = sorted(list(set(prices)), reverse=True)
    for i, price in enumerate(prices):
        price_str += str(price)
        if i < len(prices) - 1:
            price_str += ', '
    if not prices:
        print(f"票價\t\tPrices:\t\t\t\t-")
    else:
        print(f"票價\t\tPrices:\t\t\t\t{price_str}")

    # -------------------------------------
    # 地點
    # -------------------------------------

    locations = []
    for location in concert['loc']:
        locations.append(location)
    location_str = ''
    for i, location in enumerate(locations):
        location_str += location
        if i < len(locations) - 1:
            location_str += ', '
    if locations:
        print(f"地點\t\tLocations:\t\t\t{location_str}")
    else:
        print(f"地點\t\tLocations:\t\t\t\t-")

    # -------------------------------------
    # 售票時間
    # -------------------------------------

    sell_datetimes = []
    for sdt in concert['sdt']:
        sell_datetimes.append(sdt)
    sell_datetimes = sort_datetime(sell_datetimes)
    sell_datetime_str = ''
    for i, sell_datetime in enumerate(sell_datetimes):
        sell_datetime_str += sell_datetime
        if i < len(sell_datetimes) - 1:
            sell_datetime_str += ', '

    if not concert['sdt']:
        print(f"售票時間\tTicketing Time:\t\t售票中 Available")
    else:
        print(f"售票時間\tTicketing Time:\t{concert['sdt']}")

    # -------------------------------------
    # 售票網站
    # -------------------------------------

    print(f"售票網站\tTicketing Website:\t{concert['web']}")

    # -------------------------------------
    # 網址
    # -------------------------------------

    print(f"網址\t\tURL: {concert['url']}")
    print()