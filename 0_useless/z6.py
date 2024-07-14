# # # from function_read_json import *
# # # from googletrans import Translator
# # # translator = Translator()
# # #
# # # data = read_json("concert_zh.json")
# # # # for i in range(len(data)):
# # # #     words = data[i]['tit'].split(' ')
# # # #     print(len(words))
# # # #     print(data[i]['tit'])
# # #
# # # for i in range(10):
# # #     txt = data[i]['tit']
# # #     translated_text = translator.translate(txt, src="zh-TW", dest="en").text
# # #     print(translated_text)
# # #     words = translated_text.split(' ')
# # #     print(len(words))
# # #     print('---')
# # import shutil
# # import time
# # from googletrans import Translator
# # import json
# # import re
# # # from function_read_json import *
# # #
# # # data = read_json("concert_zh.json")
# # # for i in range(len(data)):
# # #     if data[i]['tit'] == "":
# # #         print(i)
# # # # translator = Translator()
# # # # txt = '今天 I like you 明天'
# # # # translated_title = translator.translate(txt, src="zh-TW", dest="en").text
# # # # print(translated_title)
# #
# # import re
# # def a():
# #     for line in lines:
# #         print(line)
# # def get_prices_lines(lines):
# #     """ """
# #     """ 轉換 """
# #     # 轉換特殊數字
# #     lines = [re.sub(r"𝟬", "0", line) for line in lines]
# #     lines = [re.sub(r"𝟭", "1", line) for line in lines]
# #     lines = [re.sub(r"𝟮", "2", line) for line in lines]
# #     lines = [re.sub(r"𝟯", "3", line) for line in lines]
# #     lines = [re.sub(r"𝟰", "4", line) for line in lines]
# #     lines = [re.sub(r"𝟱", "5", line) for line in lines]
# #     lines = [re.sub(r"𝟲", "6", line) for line in lines]
# #     lines = [re.sub(r"𝟳", "7", line) for line in lines]
# #     lines = [re.sub(r"𝟴", "8", line) for line in lines]
# #     lines = [re.sub(r"𝟵", "9", line) for line in lines]
# #     # 大寫:
# #     lines = [re.sub(r"：", ':', line) for line in lines]
# #     # ~
# #     lines = [re.sub(r'至', '~', line) for line in lines]
# #     lines = [re.sub(r"～", '~', line) for line in lines]
# #     lines = [re.sub(r"-", '~', line) for line in lines]
# #     lines = [re.sub(r"－", '~', line) for line in lines]
# #     lines = [re.sub(r"–", '~', line) for line in lines]
# #     # 價格不要有,
# #     lines = [re.sub(r",(\d{3,})", r"\1", line) for line in lines]
# #     """ 轉換 """
# #
# #     """刪除內容"""
# #     # 空白行
# #     lines = [line.strip() for line in lines if line.strip()]
# #     # page_ticketplus中的內容 (不要括號)
# #     lines = [re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", line) for line in lines]
# #     #  
# #     lines = [re.sub(r" ", ' ', line) for line in lines]
# #     # 日期的年份
# #     lines = [re.sub(r"\d{4}\s*年", "", line) for line in lines]
# #     # \u200b
# #     lines = [re.sub(r'\u200b', '', line) for line in lines]
# #     # \u200d
# #     lines = [re.sub(r'\u200d', '', line) for line in lines]
# #     # \xa0
# #     lines = [re.sub(r'\xa0', '', line) for line in lines]
# #     # 不要入場
# #     lines = [re.sub(
# #         r"\d{2}:\d{2}\s?[入進][場站]|[入進]場\d{2}:\d{2}\s?|[入進]場.*\d{2}:\d{2}|\d{2}:\d{2}\s?open|open\d{2}:\d{2}\s?",
# #         "", line) for line in lines]
# #     # 贊助金額
# #     lines = [re.sub(r".*贊助[NT]?\$(\d+)", "", line) for line in lines]
# #     # 超過
# #     lines = [re.sub(r'超過.*\d{3,}|more than.*\d{3,}', '', line) for line in lines]
# #     # 單日上限
# #     lines = [re.sub(r'上限.*\d{3,}|spending limit.*\d{3,}', '', line) for line in lines]
# #     """ 與*擇一 """""
# #     # # 舞台部分視線遮蔽區域
# #     # lines = [line for line in lines if '舞台部分視線遮蔽區域' not in line]
# #     # # 人身安全起見
# #     # lines = [line for line in lines if '人身安全起見' not in line]
# #     # # 序號起始號
# #     # lines = [line for line in lines if '序號起始號' not in line]
# #     """ 與*擇一 """""
# #     # * (備註) (*與上面三個擇一其實就可以，這邊我們選擇*試試看)
# #     lines = [line for line in lines if '*' not in line]
# #     # 服務費
# #     lines = [line for line in lines if '服務費' not in line]
# #     # 舉例說明
# #     lines = [re.sub(r'.*舉例說明.*', '', line) for line in lines]
# #     # 退票
# #     lines = [re.sub(r'.*退票.*', '', line) for line in lines]
# #     # 票價每席
# #     lines = [re.sub(r'票價每席\d{3,}', '', line) for line in lines]
# #     # 不要加價購
# #     lines = [re.sub(r'\+.*?元|\+.*?\$\d{3,}', "", line) for line in lines]
# #     # @ (我想要把@台中、@台北這種的刪除)
# #     lines = [re.sub(r'@', '', line) for line in lines]
# #     # 特殊文字
# #     lines = [re.sub(r'[ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘʀꞯꞭꞫꞨꞤᴛᴜᴠᴡʏᴢ]', '', line) for line in lines]
# #     """刪除內容"""
# #
# #     """ 左右不要有空格 """
# #     # /
# #     lines = [re.sub(r"\s*/\s*", "/", line) for line in lines]
# #     # :
# #     lines = [re.sub(r"\s*:\s*", ':', line) for line in lines]
# #     # 價格的 $ 左右不要有空格
# #     lines = [re.sub(r"\s*\$\s*(\d{3,})", r'$\1', line) for line in lines]
# #     # 價格的 元 左右不要有空格
# #     lines = [re.sub(r"\s*(\d{3,})\s*元", r'\1元', line) for line in lines]
# #     """ 左右不要有空格 """
# #
# #     """ 左右留下一個空格 """
# #     # ~
# #     lines = [re.sub(r"\s*~\s*", " ~ ", line) for line in lines]
# #     # 兩個空格以上
# #     lines = [re.sub(r"\s{2,}", " ", line) for line in lines]
# #     """ 左右留下一個空格 """
# #
# #     # ''' 不要有逗號 ''' (保留)
# #     # lines = [re.sub(r"，", ' ', line) for line in lines]
# #
# #     return lines
# # lines = ['全年無休 瘋狂愛上\n', '無時無刻 點燃愛火加拿大高顏值暖男 elijah woods\n', 'elijah woods : ilu 24/7, 365 tour\xa0\n', '首度訪台 5月24日 clapper studio 炙熱開唱♦演出日期：2024/5/24 (五)\n', '♦演出時間：20:00 (實際演出時間以現場公告為準)\n', '♦演出地點：CLAPPER STUDIO\n', '♦票價：搖滾站席NT$ 1,800 (站席無序號，請依現場工作人員指示依序排隊入場)\xa0★限量VIP UPGRADE加價購，請見 https://bit.ly/ew_TW24_VIP (消費者必須持有一張「elijah woods : ilu 24/7, 365 tour」台北場有效入場票券方可進行加購，現場VIP報到及入場皆需出示演唱會票券及VIP UPGRADE加價購票券為入場憑證。且一組票券(演唱會入場票券+VIP UPGRADE加價購票券)僅限一人使用。)*人身安全起見，孕婦及身高未滿110公分或未滿7歲孩童，請勿購買站席票券，主辦方將有權謝絕入場。\n', '*本場演出僅限信用卡購票，並於演出前5日始開放取票。\n', '*請務必於演出日前關注主辦單位官方網站及臉書頁面，詳讀確認入場時間流程及相關規範，以免損害自身權益。🎫Live Nation Taiwan會員預售 : 2024/1/29 10AM – 2024/1/31 10AM\n', '(會員預購流程：http://bit.ly/lnpreCode)\n', '🎫售票時間：2024/01/31 12PM 拓元售票系統全面開賣\xa0*單筆訂單限購4張，可支援行動裝置購票。\n', '*各階段售票數量皆有限，售完為止。預購僅提供特有或優先購買之服務，敬請理解。\xa0\n', '*以上活動內容，主辦單位Live Nation Taiwan保留異動之權力。\xa0']
# #
# #
# # # 轉換特殊數字
# # lines = [re.sub(r"𝟬", "0", line) for line in lines]
# # lines = [re.sub(r"𝟭", "1", line) for line in lines]
# # lines = [re.sub(r"𝟮", "2", line) for line in lines]
# # lines = [re.sub(r"𝟯", "3", line) for line in lines]
# # lines = [re.sub(r"𝟰", "4", line) for line in lines]
# # lines = [re.sub(r"𝟱", "5", line) for line in lines]
# # lines = [re.sub(r"𝟲", "6", line) for line in lines]
# # lines = [re.sub(r"𝟳", "7", line) for line in lines]
# # lines = [re.sub(r"𝟴", "8", line) for line in lines]
# # lines = [re.sub(r"𝟵", "9", line) for line in lines]
# # # 大寫:
# # lines = [re.sub(r"：", ':', line) for line in lines]
# # # ~
# # lines = [re.sub(r'至', '~', line) for line in lines]
# # lines = [re.sub(r"～", '~', line) for line in lines]
# # lines = [re.sub(r"-", '~', line) for line in lines]
# # lines = [re.sub(r"－", '~', line) for line in lines]
# # lines = [re.sub(r"–", '~', line) for line in lines]
# # # 價格不要有,
# # lines = [re.sub(r",(\d{3,})", r"\1", line) for line in lines]
# # """ 轉換 """
# #
# # """刪除內容"""
# # # 空白行
# # lines = [line.strip() for line in lines if line.strip()]
# # # page_ticketplus中的內容 (不要括號)
# # lines = [re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", line) for line in lines]
# # #  
# # lines = [re.sub(r" ", ' ', line) for line in lines]
# # # 日期的年份
# # lines = [re.sub(r"\d{4}\s*年", "", line) for line in lines]
# # # \u200b
# # lines = [re.sub(r'\u200b', '', line) for line in lines]
# # # \u200d
# # lines = [re.sub(r'\u200d', '', line) for line in lines]
# # # \xa0
# # lines = [re.sub(r'\xa0', '', line) for line in lines]
# #
# # # 不要入場
# # lines = [re.sub(
# #     r"\d{2}:\d{2}\s?[入進][場站]|[入進]場\d{2}:\d{2}\s?|[入進]場.*\d{2}:\d{2}|\d{2}:\d{2}\s?open|open\d{2}:\d{2}\s?",
# #     "", line) for line in lines]
# # # 贊助金額
# # lines = [re.sub(r".*贊助[NT]?\$(\d+)", "", line) for line in lines]
# # # 超過
# # lines = [re.sub(r'超過.*\d{3,}|more than.*\d{3,}', '', line) for line in lines]
# # # 單日上限
# # lines = [re.sub(r'上限.*\d{3,}|spending limit.*\d{3,}', '', line) for line in lines]
# # a()
# # """ 與*擇一 """""
# # # # 舞台部分視線遮蔽區域
# # # lines = [line for line in lines if '舞台部分視線遮蔽區域' not in line]
# # # # 人身安全起見
# # # lines = [line for line in lines if '人身安全起見' not in line]
# # # # 序號起始號
# # # lines = [line for line in lines if '序號起始號' not in line]
# # """ 與*擇一 """""
# # # * (備註) (*與上面三個擇一其實就可以，這邊我們選擇*試試看)
# # lines = [line for line in lines if '*' not in line]
# #
# # # 服務費
# # lines = [line for line in lines if '服務費' not in line]
# #
# # # 舉例說明
# # lines = [re.sub(r'.*舉例說明.*', '', line) for line in lines]
# # # 退票
# # lines = [re.sub(r'.*退票.*', '', line) for line in lines]
# # # 票價每席
# # lines = [re.sub(r'票價每席\d{3,}', '', line) for line in lines]
# # # 不要加價購
# # lines = [re.sub(r'\+.*?元|\+.*?\$\d{3,}', "", line) for line in lines]
# # # @ (我想要把@台中、@台北這種的刪除)
# # lines = [re.sub(r'@', '', line) for line in lines]
# # # 特殊文字
# # lines = [re.sub(r'[ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘʀꞯꞭꞫꞨꞤᴛᴜᴠᴡʏᴢ]', '', line) for line in lines]
# # """刪除內容"""
# #
# # """ 左右不要有空格 """
# # # /
# # lines = [re.sub(r"\s*/\s*", "/", line) for line in lines]
# # # :
# # lines = [re.sub(r"\s*:\s*", ':', line) for line in lines]
# # # 價格的 $ 左右不要有空格
# # lines = [re.sub(r"\s*\$\s*(\d{3,})", r'$\1', line) for line in lines]
# # # 價格的 元 左右不要有空格
# # lines = [re.sub(r"\s*(\d{3,})\s*元", r'\1元', line) for line in lines]
# # """ 左右不要有空格 """
# #
# # """ 左右留下一個空格 """
# # # ~
# # lines = [re.sub(r"\s*~\s*", " ~ ", line) for line in lines]
# # # 兩個空格以上
# # lines = [re.sub(r"\s{2,}", " ", line) for line in lines]
# # """ 左右留下一個空格 """
# #
# # # ''' 不要有逗號 ''' (保留)
# # # lines = [re.sub(r"，", ' ', line) for line in lines]
# # # for line in lines:
# # #     print(line)
# # # for line in lines:
# # #
# # #     prices_lines = []
# # #     prices = []
# # #     # prcs = re.findall(r"\$\d{3,}|"
# # #     #                           r"\d{3,}元|"
# # #     #                           r"預售|"
# # #     #                           r"現場|"
# # #     #                           r"索票|"
# # #     #                           r"DOOR\s*\d{3,}|"
# # #     #                           r"票[:]?\d{3,}|"
# # #     #                           r"票\s*價|"
# # #     #                           r"NT", line)
# # #     contain_number = re.findall(r"\d{3,}", line)
# # #     print(contain_number)
# # #
# # #     # print(f"{prcs} / {contain_number}")
# # #     # # 如果有索票 就回傳免費
# # #     # if '索票' in prcs or '免費' in prcs:
# # #     #     print('0')
# # #     # # 如果這行有 關鍵字 & 有三位數以上的數字，那我就把他加進prices_lines
# # #     # contain_number = re.findall(r"\d{3,}", line)
# # #     # if prcs and contain_number:
# # #     #     prices_lines.append(line)
# from function_read_json import *
# import json
# from concert_translation import *
# # zh_en_cit("concert_en1.json")
# # zh_cities = ["台北", "新北", "桃園", "台中", "台南", "高雄", "基隆", "新竹", "苗栗", "彰化", "南投", "雲林",
# #              "嘉義", "屏東", "宜蘭", "花蓮", "台東", "金門", "澎湖", "連江"]
# # en_cities = ["Taipei", "New Taipei", "Taoyuan", "Taichung", "Tainan", "Kaohsiung", "Keelung", "Hsinchu", "Miaoli",
# #              "Changhua", "Nantou", "Yunlin", "Chiayi", "Pingtung", "Yilan", "Hualien", "Taitung", "Kinmen", "Penghu",
# #              "Lienchiang"]
# # data = read_json("concert_en1.json")
# # city_mapping = dict(zip(zh_cities, en_cities))
# # for i in range(len(data)):
# #     if 'cit' in data[i]:
# #         if 'cit' in data[i]:
# #             if data[i]['cit'] in city_mapping:
# #                 print(f"{data[i]['cit']} -> ", end='')
# #                 data[i]['cit'] = city_mapping[data[i]['cit']]
# #                 print(data[i]['cit'])
# #                 with open("concert_en1.json", 'w', encoding='utf-8') as f:
# #                     json.dump(data, f, indent=4, ensure_ascii=False)
# with open('user_preferred_language.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
# users = [line.split('|||')[0] for line in lines]
# print(users)
import os
from read_json_function import *
import re
from datetime import datetime


def get_latest_json_filename(directory):
    # 檢查目錄是否存在
    if not os.path.exists(directory):
        print(f"目錄 '{directory}' 不存在。")
        return None

    # 獲取目錄中的所有檔案名稱
    filenames = os.listdir(directory)

    # 過濾出所有的 .json 檔案
    json_files = [filename for filename in filenames if filename.endswith(".json")]

    # 如果沒有找到 .json 檔案，返回 None
    if not json_files:
        print("沒有找到任何 .json 檔案。")
        return None

    # 根據檔案的修改時間對 .json 檔案進行排序，最新的檔案在最後
    json_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))

    # 返回最新的 .json 檔案
    return json_files[-1]


def check_if_today(text):
    pattern = r"concert_(\d{1,2})_(\d{1,2})_(\d{1,2}).json"
    month_day = re.search(pattern, text)
    month = int(month_day.group(1))
    day = int(month_day.group(2))

    print(month, datetime.now().month)
    print(day, datetime.now().day)
    if month == datetime.now().month and day == datetime.now().day:
        return True
    else:
        return False


def get_daily_msg(language):
    new_file = get_latest_json_filename("new_concerts")
    plus_file = get_latest_json_filename("plus_concerts")

    if not (check_if_today(new_file) or check_if_today(plus_file)):
        if language == 'zh':
            formatted_str_list = ["今天沒有任何的資訊"]
        else:
            formatted_str_list = ["The is no information today."]

        print('no new file and no plus file')
        return formatted_str_list

    formatted_str_list = []

    if language == 'zh':
        zh_data = read_json("../concert_zh.json")

        if check_if_today(new_file):
            new_data = read_json(f"new_concerts/{new_file}")
            new_pins = [item['pin'] for item in new_data]
            new_pin_indexes = [index for index, item in enumerate(zh_data) if item.get('pin') in new_pins]

            formatted_str_list.append('新的演唱會資訊!')
            for index in new_pin_indexes:
                concert = zh_data[index]

                if concert['prc']:
                    sorted_prices = sorted(concert['prc'], reverse=True)
                    sorted_prices_str = ', '.join(map(str, sorted_prices))
                else:
                    sorted_prices_str = '-'
                concert_date_str = ', '.join(concert['pdt'])

                if concert['sdt']:
                    sale_date_str = ', '.join(concert['sdt'])
                else:
                    sale_date_str = '-'

                if concert['loc']:
                    location_str = ', '.join(concert['loc'])
                else:
                    location_str = '-'

                formatted_str = f"""
- {concert['tit']}
- 日期: {concert_date_str}
- 票價: {sorted_prices_str}
- 售票日期: {sale_date_str}
- 地點: {location_str}
{concert['url']}
                                        """
                formatted_str_list.append(formatted_str.strip())

        if check_if_today(plus_file):
            plus_data = read_json(f"plus_concerts/{plus_file}")
            plus_pins = [item['pin'] for item in plus_data]
            plus_pin_indexes = [index for index, item in enumerate(zh_data) if item.get('pin') in plus_pins]

            formatted_str_list.append('新的加場資訊!')
            for index in plus_pin_indexes:
                concert = zh_data[index]

                if concert['prc']:
                    sorted_prices = sorted(concert['prc'], reverse=True)
                    sorted_prices_str = ', '.join(map(str, sorted_prices))
                else:
                    sorted_prices_str = '-'
                concert_date_str = ', '.join(concert['pdt'])

                if concert['sdt']:
                    sale_date_str = ', '.join(concert['sdt'])
                else:
                    sale_date_str = '-'

                if concert['loc']:
                    location_str = ', '.join(concert['loc'])
                else:
                    location_str = '-'

                formatted_str = f"""
- {concert['tit']}
- 日期: {concert_date_str}
- 票價: {sorted_prices_str}
- 售票日期: {sale_date_str}
- 地點: {location_str}
{concert['url']}
                                                    """
                formatted_str_list.append(formatted_str.strip())

    if language == 'en':
        en_data = read_json("../concert_en.json")

        if check_if_today(new_file):
            new_data = read_json(f"new_concerts/{new_file}")
            new_pins = [item['pin'] for item in new_data]
            new_pin_indexes = [index for index, item in enumerate(en_data) if item.get('pin') in new_pins]

            formatted_str_list.append('New Concert Information!')
            for index in new_pin_indexes:
                concert = en_data[index]

                if concert['prc']:
                    sorted_prices = sorted(concert['prc'], reverse=True)
                    sorted_prices_str = ', '.join(map(str, sorted_prices))
                else:
                    sorted_prices_str = '-'
                concert_date_str = ', '.join(concert['pdt'])

                if concert['sdt']:
                    sale_date_str = ', '.join(concert['sdt'])
                else:
                    sale_date_str = '-'

                if concert['loc']:
                    location_str = ', '.join(concert['loc'])
                else:
                    location_str = '-'

                formatted_str = f"""
- {concert['tit']}
- Date: {concert_date_str}
- Price: {sorted_prices_str}
- Ticket Date: {sale_date_str}
- Location: {location_str}
{concert['url']}
"""
                formatted_str_list.append(formatted_str.strip())

        if check_if_today(plus_file):
            formatted_str_list.append('Additional Concert Announced!')
            plus_data = read_json(f"plus_concerts/{plus_file}")
            plus_pins = [item['pin'] for item in plus_data]
            plus_pin_indexes = [index for index, item in enumerate(en_data) if item.get('pin') in plus_pins]

            for index in plus_pin_indexes:
                concert = en_data[index]

                if concert['prc']:
                    sorted_prices = sorted(concert['prc'], reverse=True)
                    sorted_prices_str = ', '.join(map(str, sorted_prices))
                else:
                    sorted_prices_str = '-'
                concert_date_str = ', '.join(concert['pdt'])

                if concert['sdt']:
                    sale_date_str = ', '.join(concert['sdt'])
                else:
                    sale_date_str = '-'

                if concert['loc']:
                    location_str = ', '.join(concert['loc'])
                else:
                    location_str = '-'

                formatted_str = f"""
- {concert['tit']}
- Date: {concert_date_str}
- Price: {sorted_prices_str}
- Ticket Date: {sale_date_str}
- Location: {location_str}
{concert['url']}
"""
                formatted_str_list.append(formatted_str.strip())

    return formatted_str_list


#         if language == 'zh':
#             if check_if_today("new_concerts"):
#                 formatted_str_list = ['新的演唱會資訊!']
#                 for index in pin_indexes:
#                     concert = zh_data[index]
#
#                     if concert['prc']:
#                         sorted_prices = sorted(concert['prc'], reverse=True)
#                         sorted_prices_str = ', '.join(map(str, sorted_prices))
#                     else:
#                         sorted_prices_str = '-'
#                     concert_date_str = ', '.join(concert['pdt'])
#
#                     if concert['sdt']:
#                         sale_date_str = ', '.join(concert['sdt'])
#                     else:
#                         sale_date_str = '-'
#
#                     if concert['loc']:
#                         location_str = ', '.join(concert['loc'])
#                     else:
#                         location_str = '-'
#
#                     formatted_str = f"""
# - {concert['tit']}
# - 日期: {concert_date_str}
# - 票價: {sorted_prices_str}
# - 售票日期: {sale_date_str}
# - 地點: {location_str}
# {concert['url']}
# """
#                     formatted_str_list.append(formatted_str.strip())
#
#             if check_if_today("plus_concerts"):
#                 formatted_str_list = ['新的加場資訊!']
#                 for index in pin_indexes:
#                     concert = zh_data[index]
#
#                     if concert['prc']:
#                         sorted_prices = sorted(concert['prc'], reverse=True)
#                         sorted_prices_str = ', '.join(map(str, sorted_prices))
#                     else:
#                         sorted_prices_str = '-'
#                     concert_date_str = ', '.join(concert['pdt'])
#
#                     if concert['sdt']:
#                         sale_date_str = ', '.join(concert['sdt'])
#                     else:
#                         sale_date_str = '-'
#
#                     if concert['loc']:
#                         location_str = ', '.join(concert['loc'])
#                     else:
#                         location_str = '-'
#
#                     formatted_str = f"""
# - {concert['tit']}
# - 日期: {concert_date_str}
# - 票價: {sorted_prices_str}
# - 售票日期: {sale_date_str}
# - 地點: {location_str}
# {concert['url']}
# """
#                     formatted_str_list.append(formatted_str.strip())
#
#             if not check_if_today("new_concerts") and not check_if_today("plus_concerts"):
#                 formatted_str_list = ["今天沒有任何的資訊"]

#     if language == 'zh':
#         formatted_str_list = ['新的演唱會資訊!']
#         for index in pin_indexes:
#             concert = zh_data[index]
#
#             if concert['prc']:
#                 sorted_prices = sorted(concert['prc'], reverse=True)
#                 sorted_prices_str = ', '.join(map(str, sorted_prices))
#             else:
#                 sorted_prices_str = '-'
#             concert_date_str = ', '.join(concert['pdt'])
#
#             if concert['sdt']:
#                 sale_date_str = ', '.join(concert['sdt'])
#             else:
#                 sale_date_str = '-'
#
#             if concert['loc']:
#                 location_str = ', '.join(concert['loc'])
#             else:
#                 location_str = '-'
#
#             formatted_str = f"""
# - {concert['tit']}
# - 日期: {concert_date_str}
# - 票價: {sorted_prices_str}
# - 售票日期: {sale_date_str}
# - 地點: {location_str}
# {concert['url']}
# """
#             formatted_str_list.append(formatted_str.strip())

#     if language == 'en':
#         formatted_str_list = ['New concert information!']
#         for index in pin_indexes:
#             concert = en_data[index]
#
#             if concert['prc']:
#                 sorted_prices = sorted(concert['prc'], reverse=True)
#                 sorted_prices_str = ', '.join(map(str, sorted_prices))
#             else:
#                 sorted_prices_str = '-'
#             concert_date_str = ', '.join(concert['pdt'])
#
#             if concert['sdt']:
#                 sale_date_str = ', '.join(concert['sdt'])
#             else:
#                 sale_date_str = '-'
#
#             if concert['loc']:
#                 location_str = ', '.join(concert['loc'])
#             else:
#                 location_str = '-'
#
#             formatted_str = f"""
# - {concert['tit']}
# - 日期: {concert_date_str}
# - 票價: {sorted_prices_str}
# - 售票日期: {sale_date_str}
# - 地點: {location_str}
# {concert['url']}
# """
#             formatted_str_list.append(formatted_str.strip())
#
#     # daily_msg = '\n\n'.join(formatted_str_list)
#     # print(f"daily_msg = {daily_msg}")

# return formatted_str_list

msgs = get_daily_msg('en')
for msg in msgs:
    print(msg)
    print('---')

# latest_filename = get_latest_json_filename("new_concerts")
# print(latest_filename)
# pattern = r"new_concert_(\d{1,2})_(\d{1,2})_(\d{1,2}).json"
# md = re.search(pattern, latest_filename)
# month = int(md.group(1))
# day = int(md.group(2))
# print(month, datetime.now().month)
# print(day, datetime.now().day)
# if month == datetime.now().month and day == datetime.now().day:
#     print('oh ya')
# else:
#     print('oh no')
# latest_filename = get_latest_json_filename("plus_concerts")
# print(check_if_today(latest_filename))

""""""
# txt = "new_concert_3_20_16.json"
# pattern = r"new_concert_(\d{1,2})_(\d{1,2})_16.json"
# md = re.search(pattern, txt)
# month = md.group(1)
# day = md.group(2)
# print(month)
# print(day)
# if month == datetime.now().month and day == datetime.now().day:
#     print('oh ya')
