from datetime import datetime
from y_example_read_json import read_json

new_all = read_json('concert_data_new_zh.json')
old_all = read_json('concert_data_old_zh.json')

era = read_json('website_jsons/era.json')
indievox = read_json('website_jsons/indievox.json')
kktix = read_json('website_jsons/kktix.json')
livenation = read_json('website_jsons/livenation.json')
ticketplus = read_json('website_jsons/ticketplus.json')

ab = read_json('concert_jsons/concert_3_14_23.json')


# kktix1 = read_json('kktix1.json')
# kktix2 = read_json('kktix2.json')
# kktix3 = read_json('kktix3.json')

# for i in range(len(kktix1)):
#     if kktix1[i]['pin'][-1] != '0':
#         print(kktix1[i]['url'])
#         print(kktix1[i]['pin'])
# for i in range(len(kktix2)):
#     if kktix1[i]['pin'][-1] != '0':
#         print(kktix1[i]['url'])
#         print(kktix1[i]['pin'])
# for i in range(len(kktix3)):
#     if kktix1[i]['pin'][-1] != '0':
#         print(kktix1[i]['url'])
#         print(kktix1[i]['pin'])

# print(ab[i]['pin'])

def check_sdt(data):
    for i in range(len(data)):
        print(i, data[i]['sdt'])
        # print(data[i]['url'])


def check_pdt(data):
    for i in range(len(data)):
        print(data[i]['pdt'])


def check_loc(data):
    for i in range(len(data)):
        print(data[i]['loc'])


def check_prc(data):
    for i in range(len(data)):
        print(data[i]['prc'])


def check_all_sdt():
    check_sdt(era)
    check_sdt(indievox)
    check_sdt(kktix)
    check_sdt(livenation)
    check_sdt(ticketplus)


def check_all_pdt():
    check_pdt(era)
    check_pdt(indievox)
    check_pdt(kktix)
    check_pdt(livenation)
    check_pdt(ticketplus)


def check_all_loc():
    check_loc(era)
    check_loc(indievox)
    check_loc(kktix)
    check_loc(livenation)
    check_loc(ticketplus)


def check_all_prc():
    check_prc(era)
    check_prc(indievox)
    check_prc(kktix)
    check_prc(livenation)
    check_prc(ticketplus)


def check_all_cit(data):
    for i in range(len(data)):
        print(data[i]['cit'], data[i]['loc'])


# check_all_sdt()
# check_all_pdt()
# check_all_loc()
# check_all_prc()
# check_all_cit(old_all)
# check_all_sdt()
for i in range(len(old_all)):
    print(old_all[i]['tit'])
#     print(i, old_all[i]['sdt'])