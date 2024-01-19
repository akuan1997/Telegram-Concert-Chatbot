import json
import os
import threading
import shutil
import re
from googletrans import Translator
import era, indievox, kktix, livenation, ticketplus

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
        if not concert['sdt']:
            print(f"售票時間:\t已開放售票")
        else:
            print(f"售票時間:\t{concert['sdt']}")
        print(f"票   價:\t{concert['prc']}")
        print(f"表演時間:\t{concert['pdt']}")
        print(f"地   點:\t{concert['loc']}")
        print(f"售票網站:\t{concert['web']}")
        print(f"網   址:\t{concert['url']}")


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
