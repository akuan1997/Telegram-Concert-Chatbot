import json
import os
import threading
from web_scraping import era, indievox, kktix, livenation, ticketplus

json_new = ['era_new.json,'
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
    with open('concert_data_new.json', 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)


def new_concerts():
    with open('concert_data_new.json', 'r', encoding='utf-8') as f:
        new_data = json.load(f)
    with open('concert_data_old.json', 'r', encoding='utf-8') as f:
        current_data = json.load(f)

    added_data = []
    for new_item in new_data:
        found = False


def delete_files():
    # 1. 刪除kktix那三個不需要的資料
    with open('concert_data_new.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    delete_titles = ["【免費索票體驗】KKTIX 虛擬活動票務系統，搭配外部串流平台",
                     "【免費索票體驗】KKTIX Live，一站式售票、觀賞活動超流暢",
                     "【免費體驗】KKTIX Live，外部售票系統，輸入兌換碼馬上開播"]

    new_data = [item for item in data if item['tit'] not in delete_titles]

    with open('concert_data_new.json', 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)


def json_new_to_old():
    with open('concert_data_old.json', 'r', encoding='utf-8') as old_file:
        old_data = json.load(old_file)

    with open('concert_data_new.json', 'r', encoding='utf-8') as new_file:
        new_data = json.load(new_file)

    with open('concert_data_old.json', 'w', encoding='utf-8') as old_file:
        json.dump(new_data, old_file, indent=4, ensure_ascii=False)


def zh_en():
    pass


def get_latest_concert_info():
    threads_start()
    threads_join()
    # threads_integration()
    # delete_files()
    # new_concerts()
    # json_new_to_old()
