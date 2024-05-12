import json

with open('0_useless/concert_data_new_zh.json', 'r', encoding='utf-8') as f:
    new_data = json.load(f)

with open('0_useless/concert_data_old_zh.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

with open('concert_zh.json', 'r', encoding='utf-8') as f:
    all_data = json.load(f)

# def check_pin(new_data_pin, old_data):
#     found = False
#     index = -1
#     for i in range(len(old_data)):
#         if new_data_pin == old_data[i]['pin']:
#             index = i
#             break
#     return index


print(f'len(new_data) = {len(new_data)}')
print(f'len(old_data) = {len(old_data)}')


def show_new_but_old(new_but_old):
    print('\n--- new but old ---\n')
    for pin in new_but_old:
        for i in range(len(new_data)):
            if new_data[i]['pin'] == pin:
                print(new_data[i]['tit'])
                print(new_data[i]['url'])
    print('\n--- new but old ---\n')


def show_old_but_new(old_but_new):
    print('\n--- old but new ---\n')
    for pin in old_but_new:
        for i in range(len(old_data)):
            if old_data[i]['pin'] == pin:
                print(old_data[i]['tit'])
                print(old_data[i]['url'])
    print('\n--- old but new ---\n')


''' 底下這些functions應該用不到 '''
# def show_new_but_all(new_but_all):
#     print('--- new but all ---')
#     for pin in new_but_all:
#         for i in range(len(new_data)):
#             if new_data[i]['pin'] == pin:
#                 print(new_data[i]['tit'])
#                 print(new_data[i]['url'])
#     print('--- new but all ---')
#
#
# def show_all_but_new(all_but_new):
#     print('--- all but new ---')
#     for pin in all_but_new:
#         for i in range(len(all_data)):
#             if all_data[i]['pin'] == pin:
#                 print(all_data[i]['tit'])
#                 print(all_data[i]['url'])
#     print('--- all but new ---')
#
#
# def show_old_but_all(old_but_all):
#     print('--- old but all ---')
#     for pin in old_but_all:
#         for i in range(len(old_data)):
#             if old_data[i]['pin'] == pin:
#                 print(old_data[i]['tit'])
#                 print(old_data[i]['url'])
#     print('--- old but all ---')
#
#
# def show_all_but_old(all_but_old):
#     print('--- all but old ---')
#     for pin in all_but_old:
#         for i in range(len(all_data)):
#             if all_data[i]['pin'] == pin:
#                 print(all_data[i]['tit'])
#                 print(all_data[i]['url'])
#     print('--- all but old  ---')

''' 底下這個function暫時用不到 '''


# def get_new_pins_delete_pins(new_data, old_data):
#     pins_new = [entry['pin'] for entry in new_data]
#     pins_old = [entry['pin'] for entry in old_data]
#
#     new_pins = [pin for pin in pins_new if pin not in pins_old]  # 新公布的活動
#     # for pin in new_pins:
#     #     print(pin)
#     # print(len(new_pins))
#
#     delete_pins = [pin for pin in pins_old if pin not in pins_new]  # 可以刪掉的活動
#     # for pin in delete_pins:
#     #     print(pin)
#     # print(len(delete_pins))
#
#     return new_pins, delete_pins

def old_concert_delete(delete_pins, all_data):
    print(f'len(delete_pins) = {len(delete_pins)}')
    print(f'len(all_data) = {len(all_data)}')

    # 刪除相應的活動
    all_data_filtered = [data for data in all_data if data['pin'] not in delete_pins]

    # 更新 all_data
    all_data.clear()
    all_data.extend(all_data_filtered)
    print(f'len(all_data) = {len(all_data)}')

    # with open('concert_zh.json', 'w', encoding='utf-8') as file:
    #     json.dump(all_data, file, indent=4, ensure_ascii=False)


# ''' 暫時用不到 '''
def get_pin_index_in_all_data(pin, all_data):
    index = -1
    for i in range(len(all_data)):
        if all_data[i]['pin'] == pin:
            index = i
            break
    return index


def check_each_info(new_data, old_data, all_data):
    for i in range(len(new_data)):
        for j in range(len(old_data)):
            if new_data[i]['pin'] == old_data[j]['pin']:  # 如果為同一筆資料
                pin = old_data[j]['pin']  # 獲得pin碼 (new old 一樣)
                pin_index_in_all_data = get_pin_index_in_all_data(pin, all_data)  # 這個pin碼在all_data的哪一個位置?
                # print(f'pin = {pin}')
                # print(f'pin_index_in_all_data = {pin_index_in_all_data}')

                # kktix在演唱會公布的時候能獲得到完整的資訊
                # 但是當售票結束或是活動結束後就會無法獲得資訊
                # 因此只比較int
                if new_data[i]['web'] == 'KKTIX':
                    if new_data[i]['int'] != old_data[j]['int']:
                        if ('加場' in new_data[i]['int'] or '加開' in new_data[i]['int']) and '加場' not in old_data[j][
                            'int'] and '加場' not in old_data[j]['int']:
                            print('通知使用者')
                            print(f"new_data[i]['tit'] = {new_data[i]['tit']}")
                            # print(f"new_data[i]['int'] = {new_data[i]['int']}")
                            print('------------------------------------------')
                            # print(f"old_data[j]['int'] = {old_data[j]['int']}")
                            print(new_data[i]['url'])
                            print(new_data[i]['pin'])
                            all_data[pin_index_in_all_data]['int'] = new_data[i]['int']
                else:
                    if new_data[i]['sdt'] != old_data[j]['sdt']:
                        print('sdt 不同')
                        print(f"old_data[j]['tit'] = {old_data[j]['tit']}")
                        print(f"new_data[i]['sdt'] = {new_data[i]['sdt']}")
                        print(f"old_data[j]['sdt'] = {old_data[j]['sdt']}")
                        print(f"web = {new_data[i]['web']}")
                        print(f"url = {new_data[i]['url']}")
                        all_data[pin_index_in_all_data]['sdt'] = new_data[i]['sdt']
                        print(all_data[pin_index_in_all_data]['sdt'])
                    if new_data[i]['prc'] != old_data[j]['prc']:
                        print('prc 不同')
                        print(f"old_data[j]['tit'] = {old_data[j]['tit']}")
                        print(f"new_data[i]['prc'] = {new_data[i]['prc']}")
                        print(f"old_data[j]['prc'] = {old_data[j]['prc']}")
                        print(f"web = {new_data[i]['web']}")
                        print(f"url = {new_data[i]['url']}")
                        all_data[pin_index_in_all_data]['prc'] = new_data[i]['prc']
                        print(all_data[pin_index_in_all_data]['prc'])
                    if new_data[i]['pdt'] != old_data[j]['pdt']:
                        print('pdt 不同')
                        print(f"old_data[j]['tit'] = {old_data[j]['tit']}")
                        print(f"new_data[i]['pdt'] = {new_data[i]['pdt']}")
                        print(f"old_data[j]['pdt'] = {old_data[j]['pdt']}")
                        print(f"web = {new_data[i]['web']}")
                        print(f"url = {new_data[i]['url']}")
                        all_data[pin_index_in_all_data]['pdt'] = new_data[i]['pdt']
                        print(all_data[pin_index_in_all_data]['pdt'])
                    if new_data[i]['loc'] != old_data[j]['loc']:
                        print("loc 不同")
                        print(f"old_data[j]['tit'] = {old_data[j]['tit']}")
                        print(f"new_data[i]['loc'] = {new_data[i]['loc']}")
                        print(f"old_data[j]['loc'] = {old_data[j]['loc']}")
                        print(f"web = {new_data[i]['web']}")
                        print(f"url = {new_data[i]['url']}")
                        all_data[pin_index_in_all_data]['loc'] = new_data[i]['loc']
                        print(all_data[pin_index_in_all_data]['loc'])
                    if new_data[i]['int'] != old_data[j]['int']:
                        if ('加場' in new_data[i]['int'] or '加開' in new_data[i]['int']) and (
                                '加場' not in old_data[i]['int'] or '加場' not in old_data[i]['int']):
                            print(f"new_data[i]['web'] = {new_data[i]['web']}")
                            print(f'{new_data[i]["url"]}')
                            print(f"new_data[i]['int'] = {new_data[i]['int']}")
                            print('------------------------------------------')
                            print(f"old_data[j]['int'] = {old_data[j]['int']}")
                            print('------------------------------------------')
                            print(f'{new_data[i]["web"]} int 不同')
                            if '加場' in new_data[i]['int'] or '加開' in new_data[i]['int']:
                                print('通知使用者')
                                all_data[pin_index_in_all_data]['int'] = new_data[i]['int']
                                print(new_data[i]['tit'])
                                print(new_data[i]['url'])
                            all_data[pin_index_in_all_data]['int'] = new_data[i]['int']

                # with open('concert_zh.json', 'w', encoding='utf-8') as file:
                #     json.dump(all_data, file, indent=4, ensure_ascii=False)


def new_concerts(new_pins, new_data, all_data):
    # new_pin_indexes = []
    # for new_pin in new_pins:
    #     for i in range(len(new_data)):
    #         if new_data[i]['pin'] == new_pin:
    #             new_pin_indexes.append(i)
    # print(f'new_pin_indexes = {new_pin_indexes}')
    # print(f'len(all_data) = {len(all_data)}')
    # for new_pin_index in new_pin_indexes:
    #     all_data.append(new_data[new_pin_index])

    new_data_filtered = [data for data in new_data if data['pin'] in new_pins]
    print(f'len(all_data) = {len(all_data)}')
    all_data.extend(new_data_filtered)

    ''' 記得測試完成之後要打開 '''
    # with open('concert_zh.json', 'w', encoding='utf-8') as file:
    #     json.dump(all_data, file, indent=4, ensure_ascii=False)

    print(f'len(all_data) = {len(all_data)}')


def check_concerts():
    pins_new = [entry['pin'] for entry in new_data]
    pins_old = [entry['pin'] for entry in old_data]
    # pins_all = [entry['pin'] for entry in all_data]

    # new 有 old 沒有
    new_but_old_pins = [pin for pin in pins_new if pin not in pins_old]  # 新公布的活動

    # new 沒有 old 有
    old_but_new_pins = [pin for pin in pins_old if pin not in pins_new]  # 可以刪掉的活動

    show_new_but_old(new_but_old_pins)  # all_data新增
    new_concerts(new_but_old_pins, new_data, all_data)
    show_old_but_new(old_but_new_pins)  # all_data刪除
    old_concert_delete(old_but_new_pins, all_data)
    check_each_info(new_data, old_data, all_data)
    # 兩者做比較

    ''' 底下這些註解應該都用不到了 '''
    # # new 有 all 沒有
    # new_but_all = [pin for pin in pins_new if pin not in pins_all]
    # show_new_but_all(new_but_all)
    # # new 沒有 all 有
    # all_but_new = [pin for pin in pins_all if pin not in pins_new]
    # show_all_but_new(all_but_new)
    # # old 有 all 沒有
    # old_but_all = [pin for pin in pins_old if pin not in pins_all]
    # show_old_but_all(old_but_all)
    # # old 沒有 all 有
    # all_but_old = [pin for pin in pins_all if pin not in pins_old]
    # show_all_but_old(all_but_old)


# # 1. 獲得新演唱會資料以及那些資料是可以刪除的
# new_pins, delete_pins = get_new_pins_delete_pins(new_data, old_data)
# print(f'new_pins = {new_pins}')
# print(f'delete_pins = {delete_pins}')
# # 2. 在all_data中刪除那些裡面沒用的data
# old_concert_delete(all_data, delete_pins)
# # 3. 開始比對new_data & old_data
# compare_new_old(new_data, old_data, all_data)
# # last. 新的pin 不對 這個可以最後處理
# new_concerts(new_pins, new_data, all_data)
#
#
# print(len(new_data))
# print(len(old_data))
# check_concerts()
# # with open('era.json', 'r', encoding='utf-8') as f:
# #     test_data = json.load(f)
# #
# # for i in range(len(test_data)):
# #     print(test_data[i]['tit'])
# #     print(test_data[i]['int'])
# #     print('-------------------------')
#
# # for i in range(len(new_data)):
# #     if new_data[i]['pin'] == 'https://chillin.kktix.cc/events/wheeinconcert04210':
# #         # if '加場' in new_data[i]['int'] or '加開' in new_data[i]['int']:
# #         #     print('yes')
# #         print(new_data[i]['int'])
# # print('-------------------------')
# # for i in range(len(old_data)):
# #     if old_data[i]['pin'] == 'https://chillin.kktix.cc/events/wheeinconcert04210':
# #         # if '加場' in old_data[i]['int'] or '加開' in old_data[i]['int']:
# #             # print('yes')
# #         print(old_data[i]['int'])
#
# # a = "加開 abc"
# # b = "加開 abcdf"
# # if a != b:
# #     print('yes')
# #     if '加場' in a or '加開' in a and '加場' not in b and '加開' not in b:
