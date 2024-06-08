import json
import re
from datetime import datetime, time
import shutil  # test
from concert_rest_api import *
import os


def find_unique_part(str1, str2):
    set1 = set(str1.splitlines())
    set2 = set(str2.splitlines())
    return "\n".join(set2 - set1)


def extract_earliest_date(date_list):
    """
    Extract the earliest date from a list of date strings,
    handling both single dates and date ranges.
    """
    # Set a far future date as the initial minimum
    min_date = datetime(9999, 12, 31, 23, 59)
    for date_str in date_list:
        # Split the date range into start and end dates, if applicable
        dates = date_str.split(' ~ ')
        for date in dates:
            # Strip time if present and convert to datetime for comparison
            date_only = date.split(' ')[0]
            date_obj = datetime.strptime(date_only, '%Y/%m/%d')
            if date_obj < min_date:
                min_date = date_obj
    return min_date


def json_in_order(json_filename):
    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Sort the data by the earliest date found in the 'pdt' field
    sorted_data = sorted(data, key=lambda x: extract_earliest_date(x['pdt']))

    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=4)


# Function to display new concert data that is not in old data
def show_new_but_old(new_but_old_pins, new_data):
    print('\n--- new but old ---\n')
    for pin in new_but_old_pins:
        for i in range(len(new_data)):
            if new_data[i]['pin'] == pin:  # Check if the pin from new data matches the pin from the list
                print(new_data[i]['tit'])  # Print the title of the concert
                print(new_data[i]['url'])  # Print the URL of the concert
                print(new_data[i]['pin'])  # Print the PIN of the concert
    print('\n--- new but old ---\n')


# Function to display old concert data that is not in new data
def show_old_but_new(old_but_new_pins, old_data):
    print(f'in function, len(old_but_new_pins) = {len(old_but_new_pins)}')
    print('\n--- old but new ---\n')
    for pin in old_but_new_pins:
        for i in range(len(old_data)):
            if old_data[i]['pin'] == pin:  # Check if the pin from old data matches the pin from the list
                print(old_data[i]['tit'])  # Print the title of the concert
                print(old_data[i]['url'])  # Print the URL of the concert
                print(old_data[i]['pin'])  # Print the PIN of the concert
    print('\n--- old but new ---\n')


# Function to find the index of a concert in all_data using its pin
def get_pin_index_in_all_data(pin, all_data):
    index = -1  # Default index
    for i in range(len(all_data)):
        if all_data[i]['pin'] == pin:
            index = i  # Update index if pin is found
            break
    return index


# Function to check and update concert information between new and old data sets
def check_each_info(new_data, old_data, all_data):
    change_pins = []
    plus_concerts = []
    # Iterate over each item in new_data
    for i in range(len(new_data)):
        # Iterate over each item in old_data
        for j in range(len(old_data)):
            # Check if the current items in new_data and old_data have the same 'pin' value
            if new_data[i]['pin'] == old_data[j]['pin']:

                pin = old_data[j]['pin']  # Retrieve the 'pin' code, which is the same in both new and old data
                pin_index_in_all_data = get_pin_index_in_all_data(pin,
                                                                  all_data)  # Find the index of this 'pin' in all_data

                # # Special case handling for KKTIX platform
                # if new_data[i]['web'] == 'KKTIX':
                #     # If the 'int' field is different in new and old data, check further
                #     if new_data[i]['int'] != old_data[j]['int']:
                #         unique_part = find_unique_part(old_data[j]['int'], new_data[i]['int'])
                #         if '加場' in unique_part or '加開' in unique_part or '釋票' in unique_part or '清票' in unique_part:
                #             # print('kktix通知使用者')
                #
                #         # If new data indicates an added show and old data doesn't, notify the user
                #         if ('加場' in new_data[i]['int'] or '加開' in new_data[i]['int'] or '清票' in new_data[i][
                #             'int'] or '釋票' in new_data[i]['int']) and '加場' not in old_data[j][
                #             'int']:
                #             # print(f"new_data[i]['tit'] = {new_data[i]['tit']}")
                #             # print('KKTIX，加場，通知使用者')
                #             # print(new_data[i]['pin'])
                # else:
                # replace "\n \n" or "\n\n" to "\n"
                new_data[i]['int'] = re.sub(r'\s*\n+\s*', '\n', new_data[i]['int'])
                old_data[j]['int'] = re.sub(r'\s*\n+\s*', '\n', old_data[j]['int'])

                ''''''

                # For other platforms, check and # print changes in 'sdt', 'prc', 'pdt', and 'loc'
                if new_data[i]['sdt'] != old_data[j]['sdt']:
                    revise = True
                    if len(new_data[i]['sdt']) > len(old_data[j]['sdt']):
                        # print(f"{new_data[i]['tit']}")
                        # print(f"新增sdt / {old_data[j]['sdt']} -> {new_data[i]['sdt']}\n{new_data[i]['url']}\n---")
                        all_data[pin_index_in_all_data]['sdt'] = new_data[i]['sdt']
                        # to do, website
                        change_pins.append(new_data[i]['pin'])
                    elif len(new_data[i]['sdt']) == len(old_data[j]['sdt']):
                        # print(f"{new_data[i]['tit']}")
                        for k in range(len(new_data[i]['sdt'])):
                            if new_data[i]['sdt'][k] == '':
                                revise = False
                                break
                        if revise:
                            # print(
                            #     f"相同數量的sdt / {old_data[j]['sdt']} -> {new_data[i]['sdt']}\n準備修改all_data\nurl: {new_data[i]['url']}\npin: {new_data[i]['pin']}\n---")
                            all_data[pin_index_in_all_data]['sdt'] = new_data[i]['sdt']
                            # to do, website
                            change_pins.append(new_data[i]['pin'])
                        # else:
                        # print(
                        #     f"相同數量的sdt，但是出現空白 / {old_data[j]['sdt']} -> {new_data[i]['sdt']}\n不修改all_data\nurl: {new_data[i]['url']}\npin: {new_data[i]['pin']}\n---")
                    # else:
                    # print(f"{new_data[i]['tit']}")
                    # print(
                    #     f"sdt減少 / {old_data[j]['sdt']} -> {new_data[i]['sdt']}\n不修改all_data\nurl: {new_data[i]['url']}\npin: {new_data[i]['pin']}\n---")

                if new_data[i]['pdt'] != old_data[j]['pdt']:
                    revise = True
                    if len(new_data[i]['pdt']) > len(old_data[j]['pdt']):
                        # print(f"{new_data[i]['tit']}")
                        # print(f"新增pdt / {old_data[j]['pdt']} -> {new_data[i]['pdt']}\n{new_data[i]['url']}\n---")
                        all_data[pin_index_in_all_data]['pdt'] = new_data[i]['pdt']
                        # to do, website
                        change_pins.append(new_data[i]['pin'])
                    elif len(new_data[i]['pdt']) == len(old_data[j]['pdt']):
                        # print(f"{new_data[i]['tit']}")
                        for k in range(len(new_data[i]['pdt'])):
                            if new_data[i]['pdt'][k] == '':
                                revise = False
                                break
                        if revise:
                            # print(
                            #     f"相同數量的pdt / {old_data[j]['pdt']} -> {new_data[i]['pdt']}\n準備修改all_data\nurl: {new_data[i]['url']}\npin: {new_data[i]['pin']}\n---")
                            all_data[pin_index_in_all_data]['pdt'] = new_data[i]['pdt']
                            # to do, website
                            change_pins.append(new_data[i]['pin'])
                        # else:
                        # print(
                        #     f"相同數量的pdt，但是出現空白 / {old_data[j]['pdt']} -> {new_data[i]['pdt']}\n不修改all_data\nurl: {new_data[i]['url']}\npin: {new_data[i]['pin']}\n---")
                    # else:
                    # print(f"{new_data[i]['tit']}")
                    # print(
                    #     f"pdt減少 / {old_data[j]['pdt']} -> {new_data[i]['pdt']}\n不修改all_data\nurl: {new_data[i]['url']}\npin: {new_data[i]['pin']}\n---")

                if new_data[i]['loc'] != old_data[j]['loc']:
                    revise = True
                    if len(new_data[i]['loc']) > len(old_data[j]['loc']):
                        # print(f"{new_data[i]['tit']}")
                        # print(f"新增loc / {old_data[j]['loc']} -> {new_data[i]['loc']}\n{new_data[i]['url']}\n---")
                        all_data[pin_index_in_all_data]['loc'] = new_data[i]['loc']
                        # to do, website
                        change_pins.append(new_data[i]['pin'])
                    elif len(new_data[i]['loc']) == len(old_data[j]['loc']):
                        # print(f"{new_data[i]['tit']}")
                        for k in range(len(new_data[i]['loc'])):
                            if new_data[i]['loc'][k] == '':
                                revise = False
                                break
                        if revise:
                            # print(
                            #     f"相同數量的loc / {old_data[j]['loc']} -> {new_data[i]['loc']}\n準備修改all_data\nurl: {new_data[i]['url']}\npin: {new_data[i]['pin']}\n---")
                            all_data[pin_index_in_all_data]['loc'] = new_data[i]['loc']
                            # to do, website
                            change_pins.append(new_data[i]['pin'])
                        # else:
                        # print(
                        #     f"相同數量的loc，但是出現空白 / {old_data[j]['loc']} -> {new_data[i]['loc']}\n不修改all_data\nurl: {new_data[i]['url']}\npin: {new_data[i]['pin']}\n---")
                    # else:
                    # print(f"{new_data[i]['tit']}")
                    # print(
                    #     f"loc減少 / {old_data[j]['loc']} -> {new_data[i]['loc']}\n不修改all_data\nurl: {new_data[i]['url']}\npin: {new_data[i]['pin']}\n---")

                ''''''

                if new_data[i]['prc'] != old_data[j]['prc']:
                    if len(new_data[i]['prc']) > len(old_data[j]['prc']):
                        # print(f"{new_data[i]['tit']}")
                        # print(f"新增prc / {old_data[j]['prc']} -> {new_data[i]['prc']}\n{new_data[i]['url']}\n---")
                        all_data[pin_index_in_all_data]['prc'] = new_data[i]['prc']
                        # to do, website
                        change_pins.append(new_data[i]['pin'])
                    # elif len(new_data[i]['prc']) == len(old_data[j]['prc']):
                    # print(f"{new_data[i]['tit']}")
                    # print(
                    #     f"prc持平 / {old_data[j]['prc']} -> {new_data[i]['prc']}\n不修改all_data\nurl: {new_data[i]['url']}\npin: {new_data[i]['pin']}\n---")
                    # else:
                    # print(f"{new_data[i]['tit']}")
                    # print(
                    #     f"prc減少 / {old_data[j]['prc']} -> {new_data[i]['prc']}\n不修改all_data\nurl: {new_data[i]['url']}\npin: {new_data[i]['pin']}\n---")
                ''''''

                # Check 'int' field again for changes other than KKTIX
                if new_data[i]['int'] != old_data[j]['int']:
                    # print(new_data[i]['tit'])
                    # # print('old /', repr(old_data[j]['int']))  # test
                    # # print('new /', repr(new_data[i]['int']))  # test
                    unique_part = find_unique_part(old_data[j]['int'], new_data[i]['int'])
                    # # print(f'unique_part = {repr(unique_part)}')
                    if '加場' in unique_part or '加開' in unique_part or '釋票' in unique_part or '清票' in unique_part:
                        # print('重要資訊！通知使用者')
                        plus_concerts.append(new_data[i])
                        all_data[pin_index_in_all_data]['int'] = new_data[i]['int']
                        # print(new_data[i]['url'])
                        # to do, website
                        change_pins.append(new_data[i]['pin'])
                    else:
                        # print('沒有加場、加開、釋票、清票資訊')
                        if len(new_data[i]['int']) != 0 and len(new_data[i]['int']) > len(old_data[j]['int']):
                            # print('新內文 > 舊內文\n準備修改all_data當中的內文')
                            all_data[pin_index_in_all_data]['int'] = new_data[i]['int']  # Update 'int' in all_data
                            # to do, website
                            change_pins.append(new_data[i]['pin'])
                        # else:
                        # print(f'新內文 < 舊內文\n不修改all_data當中的內文')
                    # print('---')
                    # # print(f'{new_data[i]["web"]} int 不同')
                    # if len(new_data[i]['int']) > len(old_data[j]['int']):
                    #     # print('新增了一些文字，修改')
                    #     # print('old /', repr(old_data[j]['int']))
                    #     # print('new /', repr(new_data[i]['int']))
                    #     all_data[pin_index_in_all_data]['int'] = new_data[i]['int']  # Update 'int' in all_data
                    #     # print(f"all_data[pin_index_in_all_data]['int'] = {repr(all_data[pin_index_in_all_data]['int'])}")
                    #     if '加場' in new_data[i]['int'] or '加開' in new_data[i]['int']:
                    #         # print('而且是有關於加場的，通知使用者')
                    #         # print('---')
                    #     else:
                    #         # print('但不是有關於加場 / 加開方面的資訊')
                    #         # print('---')
                    # else:
                    #     # print('新資料減少了一些文字，不需要更改all_data')
                    #     # print('old /', repr(old_data[j]['int']))
                    #     # print('new /', repr(new_data[i]['int']))
                    #     # print('---')

                # Potential code to write the updated all_data to a JSON file
                # with open('concert_zh.json', 'w', encoding='utf-8') as file:
                #     json.dump(all_data, file, indent=4, ensure_ascii=False)
    """"""
    # with open('concert_pin_postid.txt', 'r', encoding='utf-8') as f:
    #     lines = f.readlines()
    # for pin in change_pins:
    #     for i in range(len(all_data)):
    #         if all_data[i]['pin'] == pin:  # 這個pin在all_data的第i個位置
    #             for line in lines:
    #                 line_pin = line.split('|||')[1].replace('\n', '')
    #                 if pin == line_pin:
    #                     post_id = line.split('|||')[0]
    #                     update_post_content(post_id, all_data[i])
    """"""
    # print(f"len(change_pins) = {len(change_pins)}")
    # print(f"change_pins = {change_pins}")

    return plus_concerts, all_data


# Function to add new concerts to all_data
def new_concert_add(new_but_old_pins, new_data, all_data):
    print('-------------------------------------------------------------------------------------------------------')
    print(f'all_data ({len(all_data)}) + new_but_old_pins ({len(new_but_old_pins)}) = ', end='')
    new_data_filtered = [data for data in new_data if data['pin'] in new_but_old_pins]  # Filter new concerts by pin
    all_data.extend(new_data_filtered)  # Add new concerts to all_data
    print(f'all_data ({len(all_data)})')

    # 記得不要使用pin，而是直接使用data
    # print(f"len(new_data_filtered) = {len(new_data_filtered)}")
    # print('-------------------------------------------------------------------------------------------------------')
    """"""
    # for i in range(len(new_data_filtered)):
    #     post_concert(new_data_filtered[i])
    """"""
    return new_data_filtered, all_data


# Function to remove concerts from all_data that are no longer active
def old_concert_delete(old_but_new_pins, old_data, all_data):
    print('-------------------------------------------------------------------------------------------------------')
    print(f'all_data ({len(all_data)}) - old_but_new_pins ({len(old_but_new_pins)}) = ', end='')
    # print(f'len(delete_pins) = {len(old_but_new_pins)}')
    # print(f'len(all_data) = {len(all_data)}')
    all_data_filtered = [data for data in all_data if
                         data['pin'] not in old_but_new_pins]  # Filter out deleted concerts
    all_data.clear()  # Clear existing data
    all_data.extend(all_data_filtered)  # Update all_data with filtered list
    print(f'all_data ({len(all_data)})')
    """ test """
    # for i in range(len(old_data)):
    #     for pin in old_but_new_pins:
    #         if old_data[i]['pin'] == pin:
    #             print(old_data[i]['tit'])
    """ test """
    print('-------------------------------------------------------------------------------------------------------')
    # print(f"old_but_new_pins = {old_but_new_pins}")
    """"""
    # with open('concert_pin_postid.txt', 'r', encoding='utf-8') as f:
    #     lines = f.readlines()
    # new_lines = []
    # for line in lines:
    #     line_pin = line.split('|||')[1].strip()  # 使用strip()來移除尾部的換行符和其他空白
    #     post_id = line.split('|||')[0]
    #     if line_pin not in old_but_new_pins:
    #         new_lines.append(line)
    #     else:
    #         delete_article(post_id)  # 假設 delete_article 是一個正確定義且可用來刪除文章的函數
    # with open('concert_pin_postid.txt', 'w', encoding='utf-8') as f:
    #     f.writelines(new_lines)
    """"""
    return all_data


def get_new_delete_compare_concerts(new_but_old_pins, old_but_new_pins, new_data, old_data, all_data):
    # 1. 新增新的演唱會資訊
    # show_new_but_old(new_but_old_pins, new_data)
    new_data_filtered, all_data = new_concert_add(new_but_old_pins, new_data, all_data)
    # 2. 移除那些演唱會無法獲得的演唱會資訊
    # show_old_but_new(old_but_new_pins, old_data)
    all_data = old_concert_delete(old_but_new_pins, old_data, all_data)
    # 3. 比較內文
    plus_concerts, all_data = check_each_info(new_data, old_data, all_data)
    return new_data_filtered, plus_concerts, all_data


def testing_for_whole():
    # json_list = [
    #     "concert_jsons/concert_3_14_23.json",
    #     "concert_jsons/concert_3_17_16.json",
    #     "concert_jsons/concert_3_17_19.json",
    #     "concert_jsons/concert_3_18_13.json",
    #     "concert_jsons/concert_3_20_16.json",
    #     "concert_jsons/concert_3_22_0.json",
    #     "concert_jsons/concert_3_23_14.json",
    #     "concert_jsons/concert_3_24_8.json",
    #     "concert_jsons/concert_3_25_0.json",
    #     "concert_jsons/concert_3_25_17.json",
    #     "concert_jsons/concert_3_26_0.json",
    #     "concert_jsons/concert_3_27_3.json",
    #     "concert_jsons/concert_3_29_0.json",
    #     "concert_jsons/concert_3_30_13.json",
    #     "concert_jsons/concert_3_30_20.json",
    #     "concert_jsons/concert_3_31_14.json",
    #     "concert_jsons/concert_3_31_18.json",
    #     "concert_jsons/concert_4_15_1.json",
    #     "concert_jsons/concert_4_2_0.json",
    #     "concert_jsons/concert_4_3_10.json",
    #     "concert_jsons/concert_4_3_22.json",
    #     "concert_jsons/concert_4_4_14.json",
    #     "concert_jsons/concert_4_4_3.json",
    #     "concert_jsons/concert_4_5_16.json",
    #     "concert_jsons/concert_4_7_17.json",
    #     "concert_jsons/concert_5_2_14.json",
    #     "concert_jsons/concert_5_4_20.json",
    #     "concert_jsons/concert_5_7_1.json",
    #     "concert_jsons/concert_5_7_21.json",
    #     "concert_jsons/concert_5_8_16.json",
    #     "concert_5_8_20.json"
    # ]
    print(f"len(json_list) = {len(json_list)}")

    for i in range(1, len(json_list) - 1):
        # for i in range(start_index, start_index + 1):
        current_index = i
        # print(f"current_index = {current_index}")
        old_json = json_list[current_index]
        new_json = json_list[current_index + 1]

        print(f"old_json: {json_list[current_index]}\nnew_json: {json_list[current_index + 1]}")

        with open(old_json, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        with open(new_json, 'r', encoding='utf-8') as f:
            new_data = json.load(f)
        with open('concert_zh.json', 'r', encoding='utf-8') as f:
            all_data = json.load(f)

        pins_new = [entry['pin'] for entry in new_data]
        pins_old = [entry['pin'] for entry in old_data]

        new_but_old_pins = [pin for pin in pins_new if pin not in pins_old]
        old_but_new_pins = [pin for pin in pins_old if pin not in pins_new]

        # print(f'current_index = {current_index}')
        print(f'len(new_data) = {len(new_data)}')
        print(f'len(old_data) = {len(old_data)}')
        print(f'len(all_data) = {len(all_data)}')
        print(f'len(new_but_old_pins) = {len(new_but_old_pins)}')
        print(f'len(old_but_new_pins) = {len(old_but_new_pins)}')

        # 新宣布的演唱會資訊、可以刪除的演唱會資訊、資訊有更動的演唱會資訊
        new_data_filtered, plus_concerts, all_data = get_new_delete_compare_concerts(new_but_old_pins, old_but_new_pins,
                                                                                     new_data, old_data, all_data)
        print(f"len(new_data_filtered) = {len(new_data_filtered)}")
        print(f"len(plus_concerts) = {len(plus_concerts)}")
        for i in range(len(plus_concerts)):
            print(plus_concerts[i]['tit'])
            print(plus_concerts[i]['url'])
        # print(f'運算結束 -> len(all_data) = {len(all_data)}')
        # 寫進json裡面
        write_json = 1  # 0 not write, 1 write (for testing)
        if write_json == 1:
            with open('concert_zh.json', "w", encoding="utf-8") as f:
                json.dump(all_data, f, indent=4, ensure_ascii=False)
                # print('寫入成功')
        # else:
        # print('設定為未寫入')
        # print(f"current_index = {current_index}")

    json_in_order('concert_zh.json')


def testing_for_small(start_index):
    json_list = [
        "test1.json",
        "test2.json",
        "test3.json"
    ]
    print(f"len(json_list) = {len(json_list)}")

    # for i in range(len(json_list) - 1):
    for i in range(start_index, start_index + 1):
        current_index = i
        # print(f"current_index = {current_index}")
        old_json = json_list[current_index]
        new_json = json_list[current_index + 1]

        # shutil.copy(old_json, 'concert_zh.json')  # test

        print(f"old_json: {json_list[current_index]}\nnew_json: {json_list[current_index + 1]}")

        with open(old_json, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        with open(new_json, 'r', encoding='utf-8') as f:
            new_data = json.load(f)
        with open('concert_zh.json', 'r', encoding='utf-8') as f:
            all_data = json.load(f)

        pins_new = [entry['pin'] for entry in new_data]
        pins_old = [entry['pin'] for entry in old_data]

        new_but_old_pins = [pin for pin in pins_new if pin not in pins_old]
        old_but_new_pins = [pin for pin in pins_old if pin not in pins_new]

        # print(f'current_index = {current_index}')
        print(f'len(new_data) = {len(new_data)}')
        print(f'len(old_data) = {len(old_data)}')
        print(f'len(all_data) = {len(all_data)}')
        print(f'len(new_but_old_pins) = {len(new_but_old_pins)}')
        print(f'len(old_but_new_pins) = {len(old_but_new_pins)}')

        # 新宣布的演唱會資訊、可以刪除的演唱會資訊、資訊有更動的演唱會資訊
        new_data_filtered, plus_concerts, all_data = get_new_delete_compare_concerts(new_but_old_pins, old_but_new_pins,
                                                                                     new_data, old_data, all_data)
        # print(f"len(new_data_filtered) = {len(new_data_filtered)}")
        # print(f"len(plus_concerts) = {len(plus_concerts)}")
        for i in range(len(plus_concerts)):
            print(plus_concerts[i]['tit'])
            print(plus_concerts[i]['url'])
        # print(f'運算結束 -> len(all_data) = {len(all_data)}')
        # 寫進json裡面
        write_json = 0  # 0 not write, 1 write (for testing)
        if write_json == 1:
            with open('concert_zh.json', "w", encoding="utf-8") as f:
                json.dump(all_data, f, indent=4, ensure_ascii=False)
                # print('寫入成功')
        # else:
        #     print('設定為未寫入')
        # print(f"current_index = {current_index}")

    json_in_order('concert_zh.json')


def os_show_file_title(folder_path):
    json_filenames = []
    # 使用os模块列出文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            # print(filename.replace('.mhtml', ''))
            json_filenames.append(f"{folder_path}/{filename}")
    return json_filenames


def data_comparison(start_index, json_filename, mode):
    # print(f"len(json_list) = {len(json_list)}")
    # json_list = os_show_file_title("concert_jsons")

    # for i in range(len(json_list) - 1):
    for i in range(start_index, start_index + 1):
        current_index = i
        # print(f"current_index = {current_index}")
        old_json = json_list[current_index]
        new_json = json_list[current_index + 1]

        print(f"old_json: {json_list[current_index]}\nnew_json: {json_list[current_index + 1]}")

        with open(old_json, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        with open(new_json, 'r', encoding='utf-8') as f:
            new_data = json.load(f)
        with open(json_filename, 'r', encoding='utf-8') as f:
            all_data = json.load(f)

        pins_new = [entry['pin'] for entry in new_data]
        pins_old = [entry['pin'] for entry in old_data]

        new_but_old_pins = [pin for pin in pins_new if pin not in pins_old]
        old_but_new_pins = [pin for pin in pins_old if pin not in pins_new]

        # print(f'current_index = {current_index}')
        print(f'len(new_data) = {len(new_data)}')
        print(f'len(old_data) = {len(old_data)}')
        print(f'len(all_data) = {len(all_data)}')
        print(f'len(new_but_old_pins) = {len(new_but_old_pins)}')
        print(f'len(old_but_new_pins) = {len(old_but_new_pins)}')

        # 新宣布的演唱會資訊、可以刪除的演唱會資訊、資訊有更動的演唱會資訊
        new_data_filtered, plus_concerts, all_data = get_new_delete_compare_concerts(new_but_old_pins, old_but_new_pins,
                                                                                     new_data, old_data, all_data)
        # print(f"len(new_data_filtered) = {len(new_data_filtered)}")
        # print(f"len(plus_concerts) = {len(plus_concerts)}")
        # for j in range(len(plus_concerts)):
        #     print(plus_concerts[j]['tit'])
        #     print(plus_concerts[j]['url'])
        # print(f'運算結束 -> len(all_data) = {len(all_data)}')

        json_in_order(json_filename)

        # 寫進json裡面
        if mode == 1:  # 0 not write, 1 write (for testing)
            with open(json_filename, "w", encoding="utf-8") as f:
                json.dump(all_data, f, indent=4, ensure_ascii=False)
                # print('寫入成功')
        # elif mode == 0:
        #     print('設定為未寫入')
        # print(f"current_index = {current_index}")

        # print(f"len(all_data) = {len(all_data)}")


# to do, index 0的所有演唱會要先post
def initialize():
    with open('concert_jsons/concert_3_14_23.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for i in range(len(data)):
        print(f"{i + 1}/{len(data)}")
        post_concert(data[i])


def delete_post(start_index, end_index):
    # with open('concert_pin_postid.txt', 'w', encoding='utf-8') as f:
    #     f.write('')

    for i in range(start_index, end_index):
        try:
            print(i)
            delete_article(i)
        except Exception as e:
            print(e)
            continue
    print('結束')


def check_duplicate():
    with open('concert_pin_postid.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    pins = [line.split('|||')[1].replace('\n', '') for line in lines]
    for i in range(len(pins)):
        for j in range(i + 1, len(pins)):
            if pins[i] == pins[j]:
                print(pins[i])


def for_testing():
    while True:
        answer = input('是否執行get_concert_new_old.py?\n')
        if answer == "y":
            """"""
            # for i in range(len(json_list) - 1):
            #     testing_for_large(i, "concert_zh.json", 1)
            """"""
            # data = read_json("concert_zh.json")
            # print(len(data))
            # data = read_json("singer_info.json")
            # print(len(data))
            """"""
            # data = read_json("concert_zh.json")
            # for i in range(len(data)):
            #     post_concert(data[i])
            """"""
            # delete_post(10978, 11079)

            # initialize()

            # check_duplicate()
            # print(len(json_list))
            # with open('concert_zh.json', 'r', encoding='utf-8') as f:
            #     data = json.load(f)
            break


# for_testing()
# delete_post(10738, 11222)
# data = read_json("concert_zh.json")
# post_concert(data[0])
# for i in range(1, len(data)):
#     post_concert(data[i])

# json_list = os_show_file_title("concert_jsons")
# for each_json in json_list:
#     print(each_json)

json_list = ["concert_jsons/concert_3_14_23.json", "concert_jsons/concert_3_17_16.json", "concert_jsons/concert_3_17_19.json",
             "concert_jsons/concert_3_18_13.json", "concert_jsons/concert_3_20_16.json", "concert_jsons/concert_3_22_0.json",
             "concert_jsons/concert_3_23_14.json", "concert_jsons/concert_3_24_8.json", "concert_jsons/concert_3_25_0.json",
             "concert_jsons/concert_3_25_17.json", "concert_jsons/concert_3_26_0.json", "concert_jsons/concert_3_27_3.json",
             "concert_jsons/concert_3_29_0.json", "concert_jsons/concert_3_30_13.json", "concert_jsons/concert_3_30_20.json",
             "concert_jsons/concert_3_31_14.json", "concert_jsons/concert_3_31_18.json", "concert_jsons/concert_4_2_0.json",
             "concert_jsons/concert_4_3_10.json", "concert_jsons/concert_4_3_22.json", "concert_jsons/concert_4_4_14.json",
             "concert_jsons/concert_4_4_3.json", "concert_jsons/concert_4_5_16.json", "concert_jsons/concert_4_7_17.json",
             "concert_jsons/concert_4_15_1.json", "concert_jsons/concert_5_2_14.json", "concert_jsons/concert_5_4_20.json",
             "concert_jsons/concert_5_7_1.json", "concert_jsons/concert_5_7_21.json", "concert_jsons/concert_5_9_14.json",
             "concert_jsons/concert_5_10_11.json", "concert_jsons/concert_5_11_23.json", "concert_jsons/concert_5_12_11.json",
             "concert_jsons/concert_5_12_21.json", "concert_jsons/concert_5_13_14.json", "concert_jsons/concert_5_13_15.json",
             "concert_jsons/concert_5_13_17.json", "concert_jsons/concert_5_13_18.json", "concert_jsons/concert_5_13_19.json",
             "concert_jsons/concert_5_14_17.json", "concert_jsons/concert_5_14_4.json", "concert_jsons/concert_5_15_1.json",
             "concert_jsons/concert_5_15_19.json", "concert_jsons/concert_5_16_20.json", "concert_jsons/concert_5_21_20.json",
             "concert_jsons/concert_5_22_20.json", "concert_jsons/concert_5_23_20.json", "concert_jsons/concert_5_28_20.json",
             "concert_jsons/concert_5_29_20.json", "concert_jsons/concert_6_4_23.json", ]
shutil.copy(json_list[0], "concert_zh1.json") # for testing and validation
for i in range(len(json_list)-1):
    data_comparison(i, "concert_zh1.json", 1)
