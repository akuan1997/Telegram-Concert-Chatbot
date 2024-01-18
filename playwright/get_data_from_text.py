import re
from datetime import datetime, timedelta, time
from collections import Counter


# 把中文的時間替換成統一的格式
def chi_am_pm(match):
    # print(match)
    hour = int(match.group(1))
    # print(hour)
    minute = match.group(2) if match.group(2) else "00"
    # print(minute)
    if hour < 12:
        hour += 12
    return f"{hour}:{minute}"


# 把英文的時間替換成統一的格式
def eng_am_pm(match):
    hour = int(match.group(1))
    minute = match.group(2) if match.group(2) else "00"
    am_pm = match.group(3)

    if am_pm.lower() == "pm" and hour < 12:
        hour += 12

    return f"{hour}:{minute}"


# 對只有日期的時間加上年分
def add_year(match):
    # \d{4}/\d{1,2}/\d{1,2}
    # \d{1,2}/\d{1,2}"
    date = match.group()
    # 如果是mm/dd (為什麼<6，因為mm/dd最多也只有五個character)
    if len(date) < 6:
        # print('addadd', date)  # test
        month = date.split('/')[0]
        day = date.split('/')[1]
        try:
            # 試著把他變成datetime_obj，如果不行，代表他不是一個日期
            # new_date = '2023/' + month + '/' + day
            # new_date = f'{datetime.now().year}/{month}/{day}'
            if month > datetime.now().month:
                new_date = f'{datetime.now().year}/{month}/{day}'
            else:
                new_date = f'{datetime.now().year + 1}/{month}/{day}'
            datetime.strptime(new_date, "%Y/%m/%d")
            # 如果成功了就回傳
            return new_date
        except:
            return date
    # 已經是yyyy/mm/dd
    else:
        # 直接回傳
        return date


# # (check)
# def add_year(match):
#     # \d{4}/\d{1,2}/\d{1,2}
#     # \d{1,2}/\d{1,2}"
#     date = match.group()
#     # 如果是mm/dd (為什麼<6，因為mm/dd最多也只有五個character)
#     if len(date) < 6:
#         # sudo code
#         """
#         1. 爬蟲月份 >= 現在，都直接加上今年的年份
#         2. 爬蟲月份 <  現在
#         2024/1/14, 2023/10/31
#         前面三個月，後面六個月
#         """
#         month = date.split('/')[0]
#         day = date.split('/')[1]
#         try:
#             if month >= datetime.now().month:
#                 new_date = f'{datetime.now().year}/{month}/{day}'
#                 return new_date
#             # else:
#
#         except:
#             return date
#         # print('addadd', date)
#         # month = date.split('/')[0]
#         # day = date.split('/')[1]
#         # try:
#         #     # 試著把他變成datetime_obj，如果不行，代表他不是一個日期
#         #     # new_date = '2023/' + month + '/' + day
#         #     new_date = f'{datetime.now().year}/{month}/{day}'
#         #     datetime.strptime(new_date, "%Y/%m/%d")
#         #     # 如果成功了就回傳
#         #     return new_date
#         # except:
#         #     return date
#     # 已經是yyyy/mm/dd
#     else:
#         # 直接回傳
#         return date


# 獲得整理過後的票價文本

# 獲得整理過後的票價文本
def get_prices_lines(lines):
    """ """
    """ 轉換 """
    # 轉換特殊數字
    lines = [re.sub(r"𝟬", "0", line) for line in lines]
    lines = [re.sub(r"𝟭", "1", line) for line in lines]
    lines = [re.sub(r"𝟮", "2", line) for line in lines]
    lines = [re.sub(r"𝟯", "3", line) for line in lines]
    lines = [re.sub(r"𝟰", "4", line) for line in lines]
    lines = [re.sub(r"𝟱", "5", line) for line in lines]
    lines = [re.sub(r"𝟲", "6", line) for line in lines]
    lines = [re.sub(r"𝟳", "7", line) for line in lines]
    lines = [re.sub(r"𝟴", "8", line) for line in lines]
    lines = [re.sub(r"𝟵", "9", line) for line in lines]
    # 大寫:
    lines = [re.sub(r"：", ':', line) for line in lines]
    # ~
    lines = [re.sub(r'至', '~', line) for line in lines]
    lines = [re.sub(r"～", '~', line) for line in lines]
    lines = [re.sub(r"-", '~', line) for line in lines]
    lines = [re.sub(r"－", '~', line) for line in lines]
    lines = [re.sub(r"–", '~', line) for line in lines]
    # 價格不要有,
    lines = [re.sub(r",(\d{3,})", r"\1", line) for line in lines]
    """ 轉換 """

    """刪除內容"""
    # 空白行
    lines = [line.strip() for line in lines if line.strip()]
    # page_ticketplus中的內容 (不要括號)
    lines = [re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", line) for line in lines]
    #  
    lines = [re.sub(r" ", ' ', line) for line in lines]
    # 日期的年份
    lines = [re.sub(r"\d{4}\s*年", "", line) for line in lines]
    # \u200b
    lines = [re.sub(r'\u200b', '', line) for line in lines]
    # \u200d
    lines = [re.sub(r'\u200d', '', line) for line in lines]
    # \xa0
    lines = [re.sub(r'\xa0', '', line) for line in lines]
    # 不要入場
    lines = [re.sub(
        r"\d{2}:\d{2}\s?[入進][場站]|[入進]場\d{2}:\d{2}\s?|[入進]場.*\d{2}:\d{2}|\d{2}:\d{2}\s?open|open\d{2}:\d{2}\s?",
        "", line) for line in lines]
    # 贊助金額
    lines = [re.sub(r".*贊助[NT]?\$(\d+)", "", line) for line in lines]
    # 超過
    lines = [re.sub(r'超過.*\d{3,}|more than.*\d{3,}', '', line) for line in lines]
    # 單日上限
    lines = [re.sub(r'上限.*\d{3,}|spending limit.*\d{3,}', '', line) for line in lines]
    """ 與*擇一 """""
    # # 舞台部分視線遮蔽區域
    # lines = [line for line in lines if '舞台部分視線遮蔽區域' not in line]
    # # 人身安全起見
    # lines = [line for line in lines if '人身安全起見' not in line]
    # # 序號起始號
    # lines = [line for line in lines if '序號起始號' not in line]
    """ 與*擇一 """""
    # * (備註) (*與上面三個擇一其實就可以，這邊我們選擇*試試看)
    lines = [line for line in lines if '*' not in line]
    # 服務費
    lines = [line for line in lines if '服務費' not in line]
    # 舉例說明
    lines = [re.sub(r'.*舉例說明.*', '', line) for line in lines]
    # 退票
    lines = [re.sub(r'.*退票.*', '', line) for line in lines]
    # 票價每席
    lines = [re.sub(r'票價每席\d{3,}', '', line) for line in lines]
    # 不要加價購
    lines = [re.sub(r'\+.*?元|\+.*?\$\d{3,}', "", line) for line in lines]
    # @ (我想要把@台中、@台北這種的刪除)
    lines = [re.sub(r'@', '', line) for line in lines]
    # 特殊文字
    lines = [re.sub(r'[ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘʀꞯꞭꞫꞨꞤᴛᴜᴠᴡʏᴢ]', '', line) for line in lines]
    """刪除內容"""

    """ 左右不要有空格 """
    # /
    lines = [re.sub(r"\s*/\s*", "/", line) for line in lines]
    # :
    lines = [re.sub(r"\s*:\s*", ':', line) for line in lines]
    # 價格的 $ 左右不要有空格
    lines = [re.sub(r"\s*\$\s*(\d{3,})", r'$\1', line) for line in lines]
    # 價格的 元 左右不要有空格
    lines = [re.sub(r"\s*(\d{3,})\s*元", r'\1元', line) for line in lines]
    """ 左右不要有空格 """

    """ 左右留下一個空格 """
    # ~
    lines = [re.sub(r"\s*~\s*", " ~ ", line) for line in lines]
    # 兩個空格以上
    lines = [re.sub(r"\s{2,}", " ", line) for line in lines]
    """ 左右留下一個空格 """

    # ''' 不要有逗號 ''' (保留)
    # lines = [re.sub(r"，", ' ', line) for line in lines]

    return lines


# 獲得票價
def get_prices(lines):
    lines = get_prices_lines(lines)
    prices_lines = []
    prices = []
    for line in lines:
        # 關鍵字
        prcs = re.findall(r"\$\d{3,}|"
                          r"\d{3,}元|"
                          r"預售|"
                          r"現場|"
                          r"索票|"
                          r"DOOR\s*\d{3,}|"
                          r"票[:]?\d{3,}|"
                          r"票\s*價|"
                          r"NT", line)
        # 如果有索票 就回傳免費
        if '索票' in prcs or '免費' in prcs:
            prices.append(0)
            return prices
        # 如果這行有 關鍵字 & 有三位數以上的數字，那我就把他加進prices_lines
        contain_number = re.findall(r"\d{3,}", line)
        if prcs and contain_number:
            prices_lines.append(line)
    # 測試
    # for line in prices_lines:
    #     # print('qwe', line)
    # 整理好prices_lines之後，我想要把裡面的價格提取出來
    for line in prices_lines:
        prcs = re.findall(r"\d{3,}", line)
        for prc in prcs:
            prices.append(prc)
    #
    prices = [int(num) for num in prices if int(num) != 2023 and int(num) != 2024]
    # prices = [int(num) for num in prices if 99 < int(num) <= 99999 and int(num) != 2023 and int(num) != 2024]
    # 刪除重複價格
    prices = list(set(prices))
    return prices


# 獲得整理過後的時間文本
def get_time_lines(lines):
    try:
        """ 轉換 """
        # 小寫
        lines = [line.lower() for line in lines]
        # demo 1129
        # 轉換中文數字
        lines = [re.sub(r"二十三", "23", line) for line in lines]
        lines = [re.sub(r"二十二", "22", line) for line in lines]
        lines = [re.sub(r"二十一", "21", line) for line in lines]
        lines = [re.sub(r"二十", "20", line) for line in lines]
        lines = [re.sub(r"十九", "19", line) for line in lines]
        lines = [re.sub(r"十八", "18", line) for line in lines]
        lines = [re.sub(r"十七", "17", line) for line in lines]
        lines = [re.sub(r"十六", "16", line) for line in lines]
        lines = [re.sub(r"十五", "15", line) for line in lines]
        lines = [re.sub(r"十四", "14", line) for line in lines]
        lines = [re.sub(r"十三", "13", line) for line in lines]
        lines = [re.sub(r"十二", "12", line) for line in lines]
        lines = [re.sub(r"十一", "11", line) for line in lines]
        lines = [re.sub(r"十", "10", line) for line in lines]
        lines = [re.sub(r"九", "9", line) for line in lines]
        lines = [re.sub(r"八", "8", line) for line in lines]
        lines = [re.sub(r"七", "7", line) for line in lines]
        lines = [re.sub(r"六", "6", line) for line in lines]
        lines = [re.sub(r"五", "5", line) for line in lines]
        lines = [re.sub(r"四", "4", line) for line in lines]
        lines = [re.sub(r"三", "3", line) for line in lines]
        lines = [re.sub(r"二", "2", line) for line in lines]
        lines = [re.sub(r"一", "1", line) for line in lines]
        # demo 1129
        # 轉換特殊數字
        lines = [re.sub(r"𝟬", "0", line) for line in lines]
        lines = [re.sub(r"𝟭", "1", line) for line in lines]
        lines = [re.sub(r"𝟮", "2", line) for line in lines]
        lines = [re.sub(r"𝟯", "3", line) for line in lines]
        lines = [re.sub(r"𝟰", "4", line) for line in lines]
        lines = [re.sub(r"𝟱", "5", line) for line in lines]
        lines = [re.sub(r"𝟲", "6", line) for line in lines]
        lines = [re.sub(r"𝟳", "7", line) for line in lines]
        lines = [re.sub(r"𝟴", "8", line) for line in lines]
        lines = [re.sub(r"𝟵", "9", line) for line in lines]
        # 票價、演出日期相關的訊息有可能會用的符號都轉換為:
        lines = [re.sub(r'\s*／\s*', ':', line) for line in lines]
        lines = [re.sub(r'\s*｜\s*', ':', line) for line in lines]
        lines = [re.sub(r'\s*\|\s*', ':', line) for line in lines]
        lines = [re.sub(r'\s*⎪\s*', ':', line) for line in lines]
        lines = [re.sub(r"\s*：\s*", ':', line) for line in lines]
        # ~
        lines = [re.sub(r'至', '~', line) for line in lines]
        lines = [re.sub(r"～", '~', line) for line in lines]
        lines = [re.sub(r"-", '~', line) for line in lines]
        lines = [re.sub(r"－", '~', line) for line in lines]
        lines = [re.sub(r"–", '~', line) for line in lines]
        # xx年xx月xx號(日) or xx年xx月xx號(日) 轉換成 xxxx/xx/xx
        lines = [re.sub(r"(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*[日號]", r"\1/\2/\3 ", line) for line in lines]
        lines = [re.sub(r"(\d{1,2})\s*[.月]\s*(\d{1,2})\s*[日號]?", r"\1/\2 ", line) for line in lines]
        lines = [re.sub(r"(\d{4})\s*.\s*(\d{1,2})\s*.\s*(\d{1,2})", r"\1/\2/\3 ", line) for line in lines]
        """ 轉換 """

        """ 左右不要有空格 """
        # /
        lines = [re.sub(r"\s*/\s*", "/", line) for line in lines]
        lines = [re.sub(r"\s*:\s*", ':', line) for line in lines]
        """ 左右不要有空格 """

        """ 左右空一格 """
        # ~
        lines = [re.sub(r"\s*~\s*", " ~ ", line) for line in lines]
        """ 左右空一格 """

        """ 不要的內容 """
        # 括號中的內容
        lines = [re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", line) for line in lines]
        # 入場
        lines = [re.sub(r'[入進]場[:]?\d{1,2}:\d{2}\s*|'
                        r'\d{1,2}:\d{2}\s*[入進]場\s*|'
                        r'[入進]場時間[:]?\d{1,2}:\d{2}\s*|'
                        r'[入進]場時間[:]?預計\d{1,2}:\d{2}\s*|'
                        r'[入進]場時間[:]?\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}\s*|'
                        r'open[:]?\s*\d{1,2}:\d{2}\s*|'
                        r'\d{1,2}:\d{2}\s*open\s*|'
                        r'\d{1,2}:\d{2}\s*開放[入進]場|'
                        r'\d{1,2}:\d{2}\s*開放觀眾[入進]場',
                        '', line) for line in lines]
        # 統一編號
        lines = [line for line in lines if '有限公司' not in line]
        # 有限公司
        lines = [line for line in lines if '統一編號' not in line]
        # \u200b
        lines = [re.sub(r'\u200b', '', line) for line in lines]
        # \u200d
        lines = [re.sub(r'\u200d', '', line) for line in lines]
        # \xa0
        lines = [re.sub(r'\xa0', '', line) for line in lines]
        # \u200d
        lines = [re.sub(r'\u3000', '', line) for line in lines]
        # 特殊文字
        lines = [re.sub(r'[ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘʀꞯꞭꞫꞨꞤᴛᴜᴠᴡʏᴢ]', '', line) for line in lines]
        # 文化部訂定
        lines = [line for line in lines if '文化部訂定' not in line]
        # refer to kktix refund policy
        lines = [line for line in lines if 'refer to kktix refund policy' not in line]
        # 詳細步驟
        lines = [line for line in lines if '詳細步驟' not in line]
        # 購票專區
        lines = [line for line in lines if '購票專區' not in line]
        # 消費者
        lines = [line for line in lines if '消費者' not in line]
        # 身心障礙
        lines = [line for line in lines if '身心障礙' not in line]
        # 郵戳退票不再受理
        lines = [line for line in lines if '郵戳退票不再受理' not in line]
        # kktix退換票規定
        lines = [line for line in lines if 'kktix退換票規定' not in line]
        # 兌換時間以現場公告為準
        lines = [line for line in lines if '兌換時間以現場公告為準' not in line]
        # 粉絲福利預計
        lines = [line for line in lines if '粉絲福利預計' not in line]
        # refund will not be accepted
        lines = [line for line in lines if 'refund will not be accepted' not in line]
        # 身障表單
        lines = [line for line in lines if '身障表單' not in line]
        # 成功於
        lines = [line for line in lines if '成功於' not in line]
        # 註冊
        lines = [line for line in lines if '註冊' not in line]
        # 高鐵
        lines = [line for line in lines if '高鐵' not in line]
        # 不要星期幾、周幾
        lines = [re.sub(r'星期一|星期二|星期三|星期四|星期五|星期六|星期天|星期日|'
                        r'周一|周二|周三|周四|周五|周六|周日|'
                        r'週一|週二|週三|週四|週五|週六|週日', '', line) for line in lines]
        lines = [line for line in lines if '前' not in line and '購' not in line]
        # 空白行
        lines = [line.strip() for line in lines if line.strip()]
        # 、
        lines = [re.sub(r"\s*、\s*", " ", line) for line in lines]
        # ，
        lines = [re.sub(r"，", " ", line) for line in lines]
        # 兌換
        lines = [line for line in lines if '兌換' not in line]
        """ 不要的內容 """

        """ 時間 """
        # 把沒有年份的都補上年份 (check)
        lines = [re.sub(r"\d{4}/\d{1,2}/\d{1,2}|\d{1,2}/\d{1,2}", add_year, line) for line in lines]
        """ 時間轉換 (24小時制) """
        # 時間: 中文
        lines = [re.sub(r"早上[場]?\s*(\d{1,2})\s*[點時]", r"\1:00", line) for line in lines]
        lines = [re.sub(r"早上", " ", line) for line in lines]
        lines = [re.sub(r"上午[場]?\s*(\d{1,2})\s*[點時]", r"\1:00", line) for line in lines]
        lines = [re.sub(r"上午", " ", line) for line in lines]
        lines = [re.sub(r"中午[場]?\s*(\d{1,2})\s*[點時]", r"\1:00", line) for line in lines]
        lines = [re.sub(r"中午", " ", line) for line in lines]
        lines = [re.sub(r"下午[場]?\s*(\d{1,2})\s*[點時]", r'下午\1:00', line) for line in lines]
        lines = [re.sub(r"下午[場]?\s*(\d{1,2}):(\d{2})\s*", chi_am_pm, line) for line in lines]
        lines = [re.sub(r"晚上[場]?\s*(\d{1,2})\s*[點時]", r'晚上\1:00', line) for line in lines]
        lines = [re.sub(r"晚上[場]?\s*(\d{1,2}):(\d{2})\s*", chi_am_pm, line) for line in lines]
        lines = [re.sub(r"(\d{1,2})\s*[點時]", r"\1:00", line) for line in lines]  # demo
        # 兩個空格以上變成單個空格
        lines = [re.sub(r"\s{2,}", " ", line) for line in lines]
        # 時間: 英文
        lines = [re.sub(r"p.m.", 'pm', line) for line in lines]
        lines = [re.sub(r"P.M.", 'pm', line) for line in lines]
        lines = [re.sub(r"PM", 'pm', line) for line in lines]
        lines = [re.sub(r"a.m.", 'am', line) for line in lines]
        lines = [re.sub(r"A.M.", 'am', line) for line in lines]
        lines = [re.sub(r"AM", 'am', line) for line in lines]
        lines = [re.sub(r"(\d{1,2})\s*noon", r"\1:00", line) for line in lines]
        lines = [re.sub(r"(\d{4}/\d{1,2}/\d{1,2})\s*am\s*(\d{1,2}:\d{2})", r"\1 \2", line) for line in lines]
        lines = [re.sub(r"(\d{4}/\d{1,2}/\d{1,2})\s*pm\s*(\d{1,2}:\d{2})", r"\1 \2 pm", line) for line in lines]
        lines = [re.sub(r"(\d{1,2})(?::(\d{2}))?\s*([ap]m)", eng_am_pm, line) for line in lines]
        # 兩個空格以上變成單個空格
        lines = [re.sub(r"\s{2,}", " ", line) for line in lines]
        """ 時間轉換 (24小時制) """

        # """ 幾號到幾號，只取前面 (必須放在時間轉換之後) """
        # # yyyy/mm/dd xx:xx (~ yyyy/mm/dd xx:xx) 括號的時間都刪除
        # lines = [re.sub(r"(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}):(\d{1,2})\s*~\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}",
        #                 r"\1 \2:\3", line) for line in lines]
        # yyyy/mm/dd xx:xx (~ xx:xx) 括號的時間都刪除
        lines = [re.sub(r"(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}):(\d{1,2})\s*~\s*\d{1,2}:\d{1,2}",
                        r"\1 \2:\3", line) for line in lines]
        """ 不要的內容 """
        """ 時間 """

        return lines

    except Exception as e:
        print('發生錯誤 1', e)
        return []


# 獲得售票時間，並把使用到的句子從文本當中刪除
def get_sell(lines):
    sell_lines = []
    # 第一輪
    # 關鍵字 & 日期 & 時間
    for line in lines:
        # 尋找售票的關鍵字
        sell_times = re.findall(r'啟售時間.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'售票日期.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'售票時間.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'正式啟售.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'全面啟售.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'全面開賣.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'全區售票.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'開\s*賣.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'索票時間.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'索票時段.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'會員預售.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'優先購.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'加\s*開.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'啟\s*售.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'public sale.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'open sale.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*[販啟銷]售|'
                                r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*開賣|'
                                r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*售票|'
                                r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*選位|'
                                r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*優先購|'
                                r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*加開|'
                                r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*準時開搶', line)
        # 如果有找到關鍵字，就把這個句子加進sell_lines這個list
        if sell_times:
            # print('has sell_times 1', line)  # test
            for i in range(len(sell_times[0])):
                if sell_times[0][i]:
                    # print('first round', sell_times)  # test
                    sell_lines.append(line)
    # test
    first_round = False
    if sell_lines:
        first_round = True
        # print('sell, first round', sell_lines)

    ''''''

    # 第二輪
    # 關鍵字
    # 時間
    # 先找到關鍵字，再往下一行去確認是否有時間
    if not sell_lines:
        for i, line in enumerate(lines):
            # 關鍵字
            sell_times = re.findall(r'啟售時間|售票日期|售票時間|正式啟售|全面啟售|全面開賣|'
                                    r'全區售票|開賣時間|索票時間|索票時段|會員預售', line)
            # 如果有關鍵字
            if sell_times:
                # print('has sell_times 2', line)
                # 從關鍵字的下一行開始，直到最後一行，只要該行沒有出現時間&日期就跳出
                for j in range(i + 1, len(lines)):
                    dts = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}', lines[j])
                    if dts:
                        # print('!! different line')  # test
                        # print('second round', lines[j])  # test
                        sell_lines.append(lines[j])
                    else:
                        break
    # test
    if not first_round and sell_lines:
        print('sell, second round', sell_lines)

    ''''''

    sell_datetimes = []
    # 把抓取到的售票時間放進sell_datetime這個list裡面
    # 要注意的是list裡面放的都是datetime object
    for sell_line in sell_lines:
        sell_line = re.sub(r"(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}):(\d{1,2})\s*~\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}",
                           r"\1 \2:\3", sell_line)
        dts = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}', sell_line)
        for dt in dts:
            dt_obj = datetime.strptime(dt, "%Y/%m/%d %H:%M")
            # 不要重複的日期與時間
            if dt_obj not in sell_datetimes:
                sell_datetimes.append(dt_obj)
    # test
    # if sell_datetimes:
    #     print('sell, found sell_datetimes', sell_datetimes)

    ''''''

    # 爬取完售票時間之後要爬取表演時間，用過的句子就不可能會是表演時間，因此排除
    for sell_line in sell_lines:
        # print('刪除', sell_line)  # test
        del lines[lines.index(sell_line)]

    ''''''

    # 整理 (已經避開重複的售票時間了)
    # 不要空白行
    lines = [line.strip() for line in lines if line.strip()]
    # 售票時間 (check) (感覺可以留到最後面再整理)
    # sell_datetimes = sort_datetime(sell_datetimes)
    # 轉換成str型態
    sell_datetimes_str = [str(sell_datetime_str)[:-3].replace('-', '/') for sell_datetime_str in sell_datetimes]

    return lines, sell_datetimes_str


# 獲得表演時間以及地點
def get_performance_location(lines):
    ''''''
    ''' 開始第一輪 '''
    performance_datetimes = []
    print('進入第一輪')  # test
    ''' 與下面的@@@一起使用 '''
    # 關鍵字 & 日期 & 時間
    # 關鍵字 yyyy/mm/dd hh:mm
    # (yyyy/mm/dd hh:mm)
    dt_lines = []
    for i, line in enumerate(lines):
        # 關鍵字 yyyy/mm/dd hh:mm
        dts = re.findall(r'演出日期.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                         r'演出時間.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                         r'活動日期.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                         r'活動時間.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                         r'表演日期.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                         r'表演時間.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                         r'原場次.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                         r'加\s*場.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                         r'時\s*間.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                         r'日\s*期.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                         r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*開演|'
                         r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*加演', line)
        # 如果有找到
        if dts:
            if '~' in line and '~' not in line[0]:
                # 1. 關鍵字 yyyy/mm/dd hh:mm ~ yyyy/mm/dd hh:mm
                type1s = re.findall(
                    r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}', line)
                for type1 in type1s:
                    performance_datetimes.append(type1)
                # 2. 關鍵字 yyyy/mm/dd ~ yyyy/mm/dd hh:mm
                type2s = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}', line)
                for type2 in type2s:
                    performance_datetimes.append(type2)
                # 3. 關鍵字 yyyy/mm/dd ~ yyyy/mm/dd
                # 因為時間有可能出現在別處，這個可能給第三輪比較適合
                # type3s = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}', line)
                # for type3 in type3s:
                #     performance_datetimes.append(type3)
            else:
                dt_lines.append(lines[i])
            # 接著檢查下一行是不是也有時間，如果下一行沒有時間就直接跳出
            ''' 
            關鍵字: yyyy/mm/dd hh:mm
            yyyy/mm/dd hh:mm 
            '''
            for j in range(i + 1, len(lines)):
                dts2 = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}', lines[j])
                if dts2:
                    if '~' in lines[j] and '~' not in lines[j][0]:
                        # 1. yyyy/mm/dd hh:mm ~ yyyy/mm/dd hh:mm
                        type1s = re.findall(
                            r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}',
                            lines[j])
                        for type1 in type1s:
                            performance_datetimes.append(type1)
                        # 2. yyyy/mm/dd ~ yyyy/mm/dd hh:mm
                        type2s = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}',
                                            lines[j])
                        for type2 in type2s:
                            performance_datetimes.append(type2)
                        # 3. 關鍵字 yyyy/mm/dd ~ yyyy/mm/dd
                        # 因為時間有可能出現在別處，這個可能給第三輪比較適合
                        # type3s = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}', line)
                        # for type3 in type3s:
                        #     performance_datetimes.append(type3)
                    else:
                        dt_lines.append(lines[j])
                else:
                    break

    # 把第一輪找到的日期 轉換成datetime obj後放進performance_datetimes這個list裡面
    for dt_line in dt_lines:
        dts = re.findall(r"\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}", dt_line)
        for dt in dts:
            performance_datetimes.append(datetime.strptime(dt, '%Y/%m/%d %H:%M'))

    ''''''

    # 第一輪結尾
    if performance_datetimes:
        print('round 1')
        # 時間
        performance_datetimes_str = []
        for performance_datetime in performance_datetimes:
            if isinstance(performance_datetime, str):
                print('in 1st round, is string')
                performance_datetimes_str.append(performance_datetime)
            else:
                print('in 1st round, is datetime obj')
                performance_datetimes_str.append(str(performance_datetime)[:-3].replace('-', '/'))
        performance_datetimes_str = list(set(performance_datetimes_str))

        ''''''

        # 地點
        locations = []
        lctns = get_locations(lines, len(performance_datetimes_str))
        for lctn in lctns:
            locations.append(lctn)

        # 如果只有一個時間，但地點有兩個以上，只保留第一個
        if len(performance_datetimes_str) == 1 and len(locations) > 1:
            locations = [locations[0]]

        ''''''

        print('1111************************************************')
        print('performance_datetimes_str', performance_datetimes_str)
        print('locations', locations)
        if len(performance_datetimes_str) != len(locations):
            print('first round different')
        print('111!************************************************')
        return performance_datetimes_str, locations

    ''' 開始第二輪 '''

    print('進入第二輪')  # test
    # 第二輪
    # 演出日期
    # yyyy/mm/dd hh:mm
    dt_lines = []
    for i, line in enumerate(lines):
        keyword = re.findall(r'演出日期|'
                             r'演出時間|'
                             r'活動日期|'
                             r'活動時間|'
                             r'表演日期|'
                             r'表演時間|'
                             r'原場次|'
                             r'加\s*場|'
                             r'時\s*間|'
                             r'日\s*期', line)
        # 如果有找到表演日期的關鍵字 (第二輪)
        if keyword:
            # 從下一行開始找，直到找不到時間
            for j in range(i + 1, len(lines)):
                dts = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}', lines[j])
                if dts:
                    if '~' in lines[j] and '~' not in lines[j][0]:
                        # 1. yyyy/mm/dd hh:mm ~ yyyy/mm/dd hh:mm
                        type1s = re.findall(
                            r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}',
                            lines[j])
                        for type1 in type1s:
                            performance_datetimes.append(type1)
                        # 2. yyyy/mm/dd ~ yyyy/mm/dd hh:mm
                        type2s = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}',
                                            lines[j])
                        for type2 in type2s:
                            performance_datetimes.append(type2)
                        # 3. 關鍵字 yyyy/mm/dd ~ yyyy/mm/dd
                        # 因為時間有可能出現在別處，這個可能給第三輪比較適合
                        # type3s = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}', line)
                        # for type3 in type3s:
                        #     performance_datetimes.append(type3)
                    else:
                        dt_lines.append(lines[j])
                else:
                    break

    ''''''

    # 把第二輪找到的日期轉換成datetime obj後放進performance_datetimes這個list裡面
    for dt_line in dt_lines:
        # print('dt_line')
        dts = re.findall(r"\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}", dt_line)
        for dt in dts:
            performance_datetimes.append(datetime.strptime(dt, '%Y/%m/%d %H:%M'))

    ''''''

    # 第二輪結尾
    if performance_datetimes:
        print('round 2')
        # 時間
        performance_datetimes_str = []
        for performance_datetime in performance_datetimes:
            if isinstance(performance_datetime, str):
                print('in 1st round, is string')
                performance_datetimes_str.append(performance_datetime)
            else:
                print('in 1st round, is datetime obj')
                performance_datetimes_str.append(str(performance_datetime)[:-3].replace('-', '/'))
        performance_datetimes_str = list(set(performance_datetimes_str))
        # 地點
        locations = []
        lctns = get_locations(lines, len(performance_datetimes_str))
        for lctn in lctns:
            locations.append(lctn)

        # 如果只有一個時間，但地點有兩個以上，只保留第一個
        if len(performance_datetimes_str) == 1 and len(locations) > 1:
            locations = [locations[0]]

        print('2222************************************************')
        print('performance_datetimes_str', performance_datetimes_str)
        print('locations', locations)
        if len(performance_datetimes_str) != len(locations):
            print('second round different')
        print('222!************************************************')
        return performance_datetimes_str, locations

    ''' 開始第三輪 '''

    print('進入第三輪')  # test
    # 第三輪
    # 演出日期: yyyy/mm/dd
    # 演出時間: hh:mm

    # 獲得表演開始的時間
    performance_time = get_start_time(lines)

    ''''''

    # test
    # if performance_time:
    #     print('performance, third round, performance_time', performance_time)

    ''''''

    for i, line in enumerate(lines):
        # 尋找表演時間
        has_date = re.findall(r'演出日期\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}|'
                              r'演出時間\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}|'
                              r'活動日期\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}|'
                              r'活動時間\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}|'
                              r'表演日期\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}|'
                              r'表演時間\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}|'
                              r'原場次\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}|'
                              r'加\s*場\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}|'
                              r'時\s*間\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}|'
                              r'日\s*期\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}|'
                              r'\d{4}/\d{1,2}/\d{1,2}\s*[:]?\s*開演|'
                              r'\d{4}/\d{1,2}/\d{1,2}\s*[:]?\s*加演', line)
        # 找到表演時間 (第三輪)
        if has_date:
            # 幾號到幾號，不要以~開頭的
            if '~' in line and '~' not in line[0]:
                dtods = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}', line)
                for dtod in dtods:
                    # 找到了表演時間
                    if performance_time != '00:00':
                        performance_datetimes.append(f"{dtod} {performance_time}")
                    # 沒有找到表演時間
                    else:
                        performance_datetimes.append(f"{dtod}")
                print('has ~', performance_datetimes)
            # 只有單獨一個時間
            else:
                # 找到了表演時間
                if performance_time != '00:00':
                    dts = re.findall(r"\d{4}/\d{1,2}/\d{1,2}", line)
                    for dt in dts:
                        performance_datetimes.append(f"{dt} {performance_time}")
                # 沒有找到表演時間
                else:
                    ds = re.findall(r"\d{4}/\d{1,2}/\d{1,2}", line)
                    for d in ds:
                        performance_datetimes.append(f"{d} 00:00")
                print('not ~', performance_datetimes)

            # 如果下一行還有日期的話
            for j in range(i + 1, len(lines)):
                dts2 = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', lines[j])
                if dts2:
                    if '~' in lines[j] and '~' not in lines[j][0]:
                        dtods = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}', lines[j])
                        for dtod in dtods:
                            # 找到了表演時間
                            if performance_time != '00:00':
                                performance_datetimes.append(f"{dtod} {performance_time}")
                            # 沒有找到表演時間
                            else:
                                performance_datetimes.append(f"{dtod}")
                        print('has ~', performance_datetimes)
                    else:
                        # 找到了表演時間
                        if performance_time != '00:00':
                            dts = re.findall(r"\d{4}/\d{1,2}/\d{1,2}", lines[j])
                            for dt in dts:
                                performance_datetimes.append(f"{dt} {performance_time}")
                        # 沒有找到表演時間
                        else:
                            ds = re.findall(r"\d{4}/\d{1,2}/\d{1,2}", lines[j])
                            for d in ds:
                                performance_datetimes.append(f"{d} 00:00")
                        print('not ~', performance_datetimes)
                else:
                    break
    ''''''

    # 第三輪結尾
    if performance_datetimes:
        print('round 3')
        # 時間
        performance_datetimes_str = performance_datetimes
        performance_datetimes_str = list(set(performance_datetimes_str))
        # 地點
        locations = []
        lctns = get_locations(lines, len(performance_datetimes_str))
        for lctn in lctns:
            locations.append(lctn)
        # 如果只有一個時間，但地點有兩個以上，只保留第一個
        if len(performance_datetimes_str) == 1 and len(locations) > 1:
            locations = [locations[0]]

        print('3333************************************************')
        print('performance_datetimes_str', performance_datetimes_str)
        print('locations', locations)
        if len(performance_datetimes_str) != len(locations):
            print('third round different')
        print('333!************************************************')
        return performance_datetimes_str, locations

    ''' 開始第四輪 '''
    print('進入第四輪')  # test
    # 獲得表演開始的時間
    performance_time = get_start_time(lines)

    ''''''

    # test
    # if performance_time:
    #     print('performance, third round, performance_time', performance_time)

    ''''''

    for i, line in enumerate(lines):
        # 尋找表演時間
        keyword = re.findall(r'演出日期|'
                             r'演出時間|'
                             r'活動日期|'
                             r'活動時間|'
                             r'表演日期|'
                             r'表演時間|'
                             r'原場次|'
                             r'加\s*場|'
                             r'時\s*間|'
                             r'日\s*期', line)
        # 找到表演時間 (第四輪)
        if keyword:
            # 如果下一行還有日期的話
            for j in range(i + 1, len(lines)):
                dts2 = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', lines[j])
                if dts2:
                    if '~' in lines[j] and '~' not in lines[j][0]:
                        dtods = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}', lines[j])
                        for dtod in dtods:
                            # 找到了表演時間
                            if performance_time != '00:00':
                                performance_datetimes.append(f"{dtod} {performance_time}")
                            # 沒有找到表演時間
                            else:
                                performance_datetimes.append(f"{dtod}")
                        print('has ~', performance_datetimes)
                    else:
                        # 找到了表演時間
                        if performance_time != '00:00':
                            dts = re.findall(r"\d{4}/\d{1,2}/\d{1,2}", lines[j])
                            for dt in dts:
                                performance_datetimes.append(f"{dt} {performance_time}")
                        # 沒有找到表演時間
                        else:
                            ds = re.findall(r"\d{4}/\d{1,2}/\d{1,2}", lines[j])
                            for d in ds:
                                performance_datetimes.append(d)
                        print('not ~', performance_datetimes)
                else:
                    break
    ''''''

    # 第四輪結尾
    if performance_datetimes:
        print('round 4')
        # 時間
        performance_datetimes_str = performance_datetimes
        performance_datetimes_str = list(set(performance_datetimes_str))
        # 地點
        locations = []
        lctns = get_locations(lines, len(performance_datetimes_str))
        for lctn in lctns:
            locations.append(lctn)
        # 如果只有一個時間，但地點有兩個以上，只保留第一個
        if len(performance_datetimes_str) == 1 and len(locations) > 1:
            locations = [locations[0]]

        print('4444************************************************')
        print('performance_datetimes_str', performance_datetimes_str)
        print('locations', locations)
        if len(performance_datetimes_str) != len(locations):
            print('third round different')
        print('444!************************************************')
        return performance_datetimes_str, locations

    ''' 開始第五輪 '''

    print('進入第五輪')  # test
    # print('fourth round locations', locations)  # test
    locations = []  # 必須放在這裡，不能更動
    # xxxx/xx/xx xx:xx 城市 場館
    for line in lines:
        # 表演日期與地點的關鍵字
        dt_lctn = re.findall(r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*([台臺]北[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*([台臺]中[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*([台臺]南[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*([台臺]東[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(新北[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(基隆[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(桃園[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(新竹[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(宜蘭[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(苗栗[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(彰化[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(南投[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(雲林[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(高雄[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(嘉義[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(屏東[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(澎湖[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(花蓮[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(綠島[站]?\s*.*)$|"
                             r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(金門[站]?\s*.*)$", line)
        # 找到關鍵字 (表演日期與地點還沒有配對與排序)
        if dt_lctn:
            # print('qe dt_lctn', dt_lctn)
            # dt_lines.append(line)
            # 為了要把場地與時間配對，我們依照順序把他加進兩個list裡面
            # (這邊不能避免重複，因為順序要完整的對齊)
            # 場館
            for i in range(1, len(dt_lctn[0]), 2):
                if dt_lctn[0][i]:
                    location = dt_lctn[0][i].strip().replace(':', ' ').replace('/', ' ')
                    # print('qa location', location)
                    locations.append(location)
            print('aq locations', locations)
            # 表演時間
            for i in range(0, len(dt_lctn[0]), 2):
                if dt_lctn[0][i]:
                    # yyyy/mm/dd hh:mm (有找到時間)
                    if ':' in dt_lctn[0][i]:
                        performance_datetimes.append(datetime.strptime(dt_lctn[0][i], '%Y/%m/%d %H:%M'))
                        # print('qwqw', performance_datetimes)  # test
                    # yyyy/mm/dd 00:00 (沒有找到時間)
                    else:
                        # 直接把日期obj放進list裡面就好，不需要再額外放入00:00的時間obj
                        performance_datetimes.append(datetime.strptime(dt_lctn[0][i], '%Y/%m/%d'))
                        print('asas', performance_datetimes)  # test

    ''''''

    # 有些可能是找到"yyyy/mm/dd 城市 表演場館"
    # 可是沒有表演時間 所以我們要從內文當中尋找 yyyy/mm/dd hh:mm
    for i, performance_datetime in enumerate(performance_datetimes):
        # 上面的performance_datetimes必須為datetime_obj型態
        # 如果沒有找到時間，下面這個條件都會為真
        if performance_datetime.hour == 0:
            for line in lines:
                # 從內文當中尋找，有沒有相同日期，但是有寫上表演時間的
                # 如果有找到，就在這個日期後面加上時間
                dts = re.findall(r'(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})', line)
                if dts:
                    for j in range(len(dts)):
                        p_date = datetime.strptime(dts[j][0], '%Y/%m/%d').date()
                        p_time = datetime.strptime(dts[j][1], '%H:%M').time()
                        print('yoyo', type(p_date))  # test
                        if performance_datetime.date() == p_date:
                            performance_datetimes[i] = datetime.combine(p_date, p_time)

    ''''''

    # 如果列表中只有表演日期，但沒有時間，那我們就嘗試找到表演的時間然後combine
    # 先確定我們有找到表演時間
    if performance_datetimes:
        # 這個代表了找到日期，但是沒有時間
        if performance_datetimes[0].hour == 0:
            # 獲得表演的時間
            performance_time = get_start_time(lines)
            # 有找到表演的時間，我們把他貼在日期的後面
            if performance_time != '00:00':
                for i in range(len(performance_datetimes)):
                    performance_datetimes[i] = datetime.combine(performance_datetimes[i], datetime.strptime(performance_time, '%H:%M').time())

    ''''''

    # 第五輪結尾
    if performance_datetimes:
        print('round 5')
        # 時間
        performance_datetimes_str = []
        # 把日期從近排到遠
        performance_datetimes, locations = sort_dts_lctns(performance_datetimes, locations)
        pdts_str = [str(performance_datetime_str)[:-3].replace('-', '/') for performance_datetime_str in
                    performance_datetimes]

        for pdt_str in pdts_str:
            performance_datetimes_str.append(pdt_str)

        # 我想要保留00:00 但是下面這段程式碼會讓我的
        # for pdt_str in pdts_str:
        #     if '00:00' in pdt_str:
        #         performance_datetimes_str.append(pdt_str.split(' ')[0])
        #     else:
        #         performance_datetimes_str.append(pdt_str)

        # 日期地點的配對會亂掉
        # performance_datetimes_str = list(set(performance_datetimes_str))

        # test
        print('5555************************************************')
        print('performance_datetimes_str', performance_datetimes_str)
        print('locations', locations)
        if len(performance_datetimes_str) != len(locations):
            print('fourth round different')
        print('555!************************************************')

        return performance_datetimes_str, locations

    ''' 開始第六輪 '''

    print('第六輪開始')  # test
    # 只有單行出現日期或是時間
    dts_lines = []  # 包含任何日期或是時間
    for line in lines:
        # 如果有日期或是時間
        dts = re.findall(r'\d{4}/\d{1,2}/\d{1,2}|\d{1,2}:\d{2}', line)
        if dts:
            dts_lines.append(line)
    print('test for round 5', dt_lines)
    # 假如剛好只有一行
    if len(dts_lines) == 1:
        print('剛好只有一行', dts_lines)  # test
        dts = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}', dts_lines[0])
        if dts:
            for dt in dts:
                performance_datetimes.append(dt)
            print('單行 dts', performance_datetimes)
        else:
            ds = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', dts_lines[0])
            ts = re.findall(r'\d{1,2}:\d{1,2}', dts_lines[0])
            if ds and not ts:
                for d in ds:
                    performance_datetimes.append(d)
                print('單行 ds', performance_datetimes)  # test

    ''''''

    # 第六輪結尾
    if performance_datetimes:
        print('round 6')
        # 時間
        performance_datetimes_str = performance_datetimes
        performance_datetimes_str = list(set(performance_datetimes_str))
        # 地點
        locations = []
        lctns = get_locations(lines, len(performance_datetimes_str))
        for lctn in lctns:
            locations.append(lctn)
        # 如果只有一個時間，但地點有兩個以上，只保留第一個
        if len(performance_datetimes_str) == 1 and len(locations) > 1:
            locations = [locations[0]]
        # test
        print('6666************************************************')
        print('performance_datetimes_str', performance_datetimes_str)
        print('locations', locations)
        if len(performance_datetimes_str) != len(locations):
            print('fifth round different')
        print('666!************************************************')

        return performance_datetimes_str, locations

    ''' 開始第七輪 '''

    print('第七輪開始')
    # 日期只有出現一次
    performance_time = get_start_time(lines)  # 獲得表演的時間
    ds = []
    for line in lines:
        found_ds = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', line)
        if found_ds:
            for found_d in found_ds:
                if found_d not in ds:
                    ds.append(found_d)
    print('第七輪的ds', ds)

    ''''''

    # 假如只有找到一個日期的話，尋找看看有沒有表演的時間，有就補上去
    if len(ds) == 1:
        if performance_time != '00:00':
            performance_datetimes.append(f'{ds[0]} {performance_time}')
        else:
            performance_datetimes.append(f'{ds[0]}')

    ''''''
    # 第七輪結尾
    if performance_datetimes:
        print('round 7')
        # 表演時間
        performance_datetimes_str = performance_datetimes
        performance_datetimes_str = list(set(performance_datetimes_str))
        # 地點
        locations = []
        lctns = get_locations(lines, len(performance_datetimes_str))
        for lctn in lctns:
            locations.append(lctn)
        # 如果只有一個時間，但地點有兩個以上，只保留第一個
        if len(performance_datetimes_str) == 1 and len(locations) > 1:
            locations = [locations[0]]
        # test
        print('7777************************************************')
        print('performance_datetimes_str', performance_datetimes_str)
        print('locations', locations)
        if len(performance_datetimes_str) != len(locations):
            print('sixth round different')
        print('777!************************************************')

        return performance_datetimes, locations

    print('嗚嗚嗚')
    return performance_datetimes, locations


# 取得表演的時間
def get_start_time(lines):
    performance_time = ''
    for line in lines:
        # 表演開始的關鍵字
        starts = re.findall(r'開\s*演\s*[:]?\s*(\d{1,2}:\d{2})|'
                            r'開\s*始\s*[:]?\s*(\d{1,2}:\d{2})|'
                            r'演\s*出\s*[:]?\s*(\d{1,2}:\d{2})|'
                            r'時\s*間\s*[:]?\s*(\d{1,2}:\d{2})|'
                            r'活動開始時間\s*[:]?\s*(\d{1,2}:\d{2})|'
                            r'開演時間\s*[:]?\s*(\d{1,2}:\d{2})|'
                            r'演出時間\s*[:]?\s*(\d{1,2}:\d{2})|'
                            r'開盤時間\s*[:]?\s*(\d{1,2}:\d{2})|'
                            r'活動時間\s*[:]?\s*(\d{1,2}:\d{2})|'
                            r'(\d{1,2}:\d{2})\s*開演|'
                            r'(\d{1,2}:\d{2})\s*開始|'
                            r'(\d{1,2}:\d{2})\s*演出開始|'
                            r'start\s*[:]?\s*(\d{1,2}:\d{2})|'
                            r'(\d{1,2}:\d{2})\s*start|'
                            r'begin\s*[:]?\s*(\d{1,2}:\d{2})|'
                            r'(\d{1,2}:\d{2})\s*begin|'
                            r'(\d{1,2}:\d{2})\s*show start|'
                            r'show start\s*(\d{1,2}:\d{2})|'
                            r'show time\s*[:]?\s*(\d{1,2}:\d{2})', line)
        # 如果有找到關鍵字
        if starts:
            for i in range(len(starts[0])):
                # 通常只會有一個，抓取最後一個出現的表演時間
                if starts[0][i]:
                    performance_time = starts[0][i]
                    # print('performance_time', performance_time)  # test
    if performance_time:
        return performance_time
    else:
        return '00:00'


# 取得位置 (check)
def get_locations(lines, pdt_len):
    locations = []
    key_word = False
    found_key_word_index = []
    for i, line in enumerate(lines):
        # 關鍵字
        lctns = re.findall(r"場｜(.*)$|地點\s*[／:｜|⎪](.*)$|場地[:](.*)$|場館名稱:(.*)$", line)
        # 如果有找到關鍵字
        if lctns:
            key_word = True
            found_key_word_index.append(i)
            for j in range(len(lctns[0])):
                if lctns[0][j]:
                    locations.append(lctns[0][j].strip())
    ''''''

    # 地點
    # XXXX
    # 如果只有找到一次地點的話，就把他放進去locations裡面
    # 但是這樣的寫法沒有辦法應對以下的寫法
    # 地點
    # XXXX
    # OOOO
    # 只能把第一個加進去

    # if key_word and not locations and len(found_key_word_index) == 1:
    #     print('好不好哇')
    #     locations.append(lines[found_key_word_index[0] + 1])

    ''''''

    # 在def那邊新增一個argument: pdt_len
    # 有幾個表演時間，就會有幾個地點
    if key_word and not locations:
        for i in range(pdt_len):
            print('好不好哇')
            locations.append(lines[found_key_word_index[0] + 1 + i])

    return locations


# 把日期與地點捆綁在一起後，由時間最近到最遠依序排列
def sort_dts_lctns(performance_dts, lctns):
    performance_datetimes = []
    deleted_contents = []

    # test
    # print('in sdl2, first')
    # print('in sdl2', performance_dts)
    # print('in sdl2', lctns)

    for i, performance_datetime in enumerate(performance_dts):
        if performance_datetime not in performance_datetimes:
            performance_datetimes.append(performance_datetime)
        else:
            deleted_contents.append(lctns[i])

    for deleted_content in deleted_contents:
        # print('del!', lctns[lctns.index(deleted_content)])  # test
        del lctns[lctns.index(deleted_content)]

    locations = lctns

    dts_lctns = list(zip(performance_datetimes, locations))
    sorted_events = sorted(dts_lctns, key=lambda x: x[0])
    performance_datetimes = []
    locations = []
    sorted_performance_datetimes, sorted_locations = list(zip(*sorted_events))
    for sorted_performance_datetime in sorted_performance_datetimes:
        performance_datetimes.append(sorted_performance_datetime)
    for sorted_location in sorted_locations:
        locations.append(sorted_location)

    # test
    # print('in sdl2, after')
    # print('iu sdl2', performance_datetimes)
    # print('in sdl2', locations)

    return performance_datetimes, locations


# 日期按照近到遠排序
def sort_datetime(datetime_str_list):
    # 1. 將日期時間字符串轉換為datetime對象
    datetime_list = [datetime.strptime(dt_str, '%Y/%m/%d %H:%M') for dt_str in datetime_str_list]

    # 2. 新增一個字典，用於按照日期進行分組
    date_dict = {}
    for dt in datetime_list:
        date = dt.date()
        if date not in date_dict:
            date_dict[date] = []
        date_dict[date].append(dt)

    # 3. 從字典中提取具體時間的日期和沒有相同日期的日期
    final_datetimes = []
    for dt_list in date_dict.values():
        dt_list = list(set(dt_list))
        if len(dt_list) == 1:
            final_datetimes.append(dt_list[0])
        else:
            for dt in dt_list:
                if dt.hour != 0:
                    final_datetimes.append(dt)

    # 4. 排序日期時間並排除過去一年的日期
    current_year = datetime.now().year
    final_datetimes.sort()
    final_datetimes = [final_datetime for final_datetime in final_datetimes if
                       final_datetime.year >= current_year - 1]
    final_datetimes_str = [str(final_datetime)[:-3].replace('-', '/') for final_datetime in final_datetimes]

    return final_datetimes_str
