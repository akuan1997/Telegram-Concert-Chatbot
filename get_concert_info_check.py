from datetime import datetime
from example_read_json import read_json

new_all = read_json('concert_data_new_zh.json')
old_all = read_json('concert_data_old_zh.json')

era = read_json('concert_json_files/era.json')
indievox = read_json('concert_json_files/indievox.json')
kktix = read_json('concert_json_files/kktix.json')
livenation = read_json('concert_json_files/livenation.json')
ticketplus = read_json('concert_json_files/ticketplus.json')


def check_sdt(data):
    for i in range(len(data)):
        print(data[i]['sdt'])


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
check_all_pdt()
# check_all_loc()
# check_all_prc()
# check_all_cit(old_all)
