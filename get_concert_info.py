import json
import os
import threading
import shutil
import re
from googletrans import Translator
import era, indievox, kktix, livenation, ticketplus
from get_data_from_text import sort_datetime

# import sys
# sys.path.append(r"C:\Users\pfii1\akuan\git-repos\2024_Concert_Chatbot\web_scraping")
# from web_scraping import era, indievox, kktix, livenation, ticketplus

json_new = ['era_new.json',
            'indievox_new.json',
            'kktix_new.json',
            'livenation_new.json',
            'ticketplus_new.json']

thread_era = threading.Thread(target=era.get_era)
thread_indievox = threading.Thread(target=indievox.get_indievox)
thread_kktix = threading.Thread(target=kktix.get_kktix)
thread_livenation = threading.Thread(target=livenation.get_livenation)
threading_ticketplus = threading.Thread(target=ticketplus.get_ticketplus)


def threads_start():
    thread_era.start()
    thread_indievox.start()
    thread_kktix.start()
    thread_livenation.start()
    threading_ticketplus.start()


def threads_join():
    thread_era.join()
    thread_indievox.join()
    thread_kktix.join()
    thread_livenation.join()
    threading_ticketplus.join()
    print('All Threads Finished!')


def threads_integration():
    merged_data = []
    for json_file in json_new:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            merged_data.extend(data)
    with open('concert_data_new_zh.json', 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)


def load_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return json.load(file)


def compare_concerts(new_concert, old_concerts):
    for old_concert in old_concerts:
        if new_concert['url'] == old_concert['url']:
            return old_concert
    return None


def new_concerts():
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


def delete_files():
    # 1. 刪除kktix那三個不需要的資料
    with open('concert_data_new_zh.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    delete_titles = ["【免費索票體驗】KKTIX 虛擬活動票務系統，搭配外部串流平台",
                     "【免費索票體驗】KKTIX Live，一站式售票、觀賞活動超流暢",
                     "【免費體驗】KKTIX Live，外部售票系統，輸入兌換碼馬上開播"]

    new_data = [item for item in data if item['tit'] not in delete_titles]

    with open('concert_data_new_zh.json', 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)
    print('Successfully Deleted!')


def json_new_to_old():
    with open('concert_data_old_zh.json', 'r', encoding='utf-8') as old_file:
        old_data = json.load(old_file)

    with open('concert_data_new_zh.json', 'r', encoding='utf-8') as new_file:
        new_data = json.load(new_file)

    with open('concert_data_old_zh.json', 'w', encoding='utf-8') as old_file:
        json.dump(new_data, old_file, indent=4, ensure_ascii=False)

    with open('concert_data_old_en.json', 'r', encoding='utf-8') as old_file:
        old_data = json.load(old_file)

    with open('concert_data_new_en.json', 'r', encoding='utf-8') as new_file:
        new_data = json.load(new_file)

    with open('concert_data_old_en.json', 'w', encoding='utf-8') as old_file:
        json.dump(new_data, old_file, indent=4, ensure_ascii=False)


def each_concert_number():
    with open('era_new.json', 'r', encoding='utf-8') as f:
        era_data = json.load(f)
    with open('indievox_new.json', 'r', encoding='utf-8') as f:
        indievox_data = json.load(f)
    with open('kktix_new.json', 'r', encoding='utf-8') as f:
        kktix_data = json.load(f)
    with open('livenation_new.json', 'r', encoding='utf-8') as f:
        livenation_data = json.load(f)
    with open('ticketplus_new.json', 'r', encoding='utf-8') as f:
        ticketplus_data = json.load(f)
    print(f'era\t\t\t\t{len(era_data)}')
    print(f'indievox\t\t{len(indievox_data)}')
    print(f'kktixt\t\t\t{len(kktix_data)}')
    print(f'Live nation\t\t{len(livenation_data)}')
    print(f'ticketplus\t\t{len(ticketplus_data)}')
    with open('concert_data_new_zh.json', 'r', encoding='utf-8') as f:
        concert_data = json.load(f)
    print(f'concert data\t{len(concert_data)}')


def zh_en():
    # Copying the original file to a new file for translated content
    shutil.copy('concert_data_new_zh.json', 'concert_data_new_en.json')

    translator = Translator()

    # Open the copied file for reading and translation
    with open('concert_data_new_en.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i in range(len(data)):
        print(f'current progress {i}/{len(data)}')

        # Check if 'int' field is not None or empty
        if data[i]['int']:
            try:
                # 使用正則表達式移除非中文字符
                data[i]['int'] = re.sub(r'[^\u4e00-\u9fa5]+', '', data[i]['int'])
                # Translate the text and update the 'int' field
                translated_text = translator.translate(data[i]['int'], src="zh-TW", dest="en").text
                data[i]['int'] = translated_text
                print('Successful')
            except Exception as e:
                print(f'Error translating: {e}')
                print('Skipping this entry')
        else:
            print('None or empty, skip')

        print('------------------------------------')

    # Write the translated data back to the file
    with open('concert_data_new_en.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def reset_failure_log():
    with open('failure_log.txt', 'w', encoding='utf-8') as f:
        f.write('')


def get_latest_concert_info():
    # reset_failure_log()
    # threads_start()
    # threads_join()
    # threads_integration()
    # each_concert_number() # 驗算用
    # delete_files()
    # zh_en()
    new_concerts()
    # json_new_to_old()


get_latest_concert_info()
