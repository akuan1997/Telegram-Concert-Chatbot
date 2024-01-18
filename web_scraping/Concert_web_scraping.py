import json
import os
import threading

json_new = ['era_new.json,'
            'indievox_new.json',
            'kktix_new.json',
            'livenation_new.json',
            'ticketplus_new.json']

thread_era = threading.Thread(target=get_era)
thread_indievox = threading.Thread(target=get_indievox)
thread_kktix = threading.Thread(target=get_kktix)
thread_livenation = threading.Thread(target=get_livenation)
threading_ticketplus = threading.Thread(target=get_tixcraft)


def launch_threads():
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
    print('All Threads Finished')


def json_integration():
    merged_data = []
    for json_file in json_new:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            merged_data.extend(data)
    with open('concert_data_new.json', 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)
