import re
from datetime import datetime, timedelta, time
from collections import Counter


def replace_chinese(match):
    # print(match)
    hour = int(match.group(1))
    # print(hour)
    minute = match.group(2) if match.group(2) else "00"
    # print(minute)
    if hour < 12:
        hour += 12
    return f"{hour}:{minute}"


def replace_english(match):
    hour = int(match.group(1))
    minute = match.group(2) if match.group(2) else "00"
    am_pm = match.group(3)

    if am_pm.lower() == "pm" and hour < 12:
        hour += 12

    return f"{hour}:{minute}"


def convert_special_font(text):
    # 定义替换规则
    replacement = {'𝟬': '0', '𝟭': '1', '𝟮': '2', '𝟯': '3', '𝟰': '4', '𝟱': '5', '𝟲': '6', '𝟳': '7', '𝟴': '8', '𝟵': '9'}

    # 执行替换
    converted_text = ''.join(replacement.get(c, c) for c in text)
    return converted_text


def add_year(match):
    date = match.group()
    # print('hello', date)
    if len(date) < 6:
        # print('hello')
        month = date.split('/')[0]
        day = date.split('/')[1]
        # print(month, day)
        try:
            new_date = '2023/' + month + '/' + day
            datetime.strptime(new_date, "%Y/%m/%d")
            # print('test successful', new_date)
            return new_date
        except:
            return date
    else:
        return date


def adjacent_date(match):
    start_date_str = match.group(1)
    performance_time_str = match.group(2)
    end_date_str = match.group(3)
    end_time_str = match.group(4)

    performance_time = datetime.strptime(performance_time_str, "%H:%M").time()
    end_time = datetime.strptime(end_time_str, "%H:%M").time()
    # print('performance_time', performance_time)
    # print('end_time', end_time)

    start_datetime_str = start_date_str + " " + performance_time_str
    end_datetime_str = end_date_str + " " + end_time_str

    start_datetime = datetime.strptime(start_datetime_str, "%Y/%m/%d %H:%M")
    end_datetime = datetime.strptime(end_datetime_str, "%Y/%m/%d %H:%M")
    time_difference = end_datetime - start_datetime

    if performance_time > end_time:
        previous_day = datetime.strptime(end_date_str, "%Y/%m/%d") - timedelta(days=1)
        end_date_str = str(previous_day.year) + '/' + str(previous_day.month) + '/' + str(previous_day.day)

    if time_difference.total_seconds() < 24 * 3600:
        return start_date_str + ' ' + performance_time_str
    else:
        return start_date_str + ' ~ ' + end_date_str + ' ' + performance_time_str

    # if performance_time < end_time:
    #     start_datetime_str = start_date_str + " " + performance_time_str
    #     end_datetime_str = end_date_str + " " + end_time_str
    #
    #     start_datetime = datetime.strptime(start_datetime_str, "%Y/%m/%d %H:%M")
    #     end_datetime = datetime.strptime(end_datetime_str, "%Y/%m/%d %H:%M")
    #     time_difference = end_datetime - start_datetime
    #
    #     if time_difference.total_seconds() < 24 * 3600:
    #         return start_date_str + ' ' + performance_time_str
    #     else:
    #         return start_date_str + ' ~ ' + end_date_str + ' ' + performance_time_str
    # else:
    #     start_datetime_str = start_date_str + " " + performance_time_str
    #     end_datetime_str = end_date_str + " " + end_time_str
    #
    #     start_datetime = datetime.strptime(start_datetime_str, "%Y/%m/%d %H:%M")
    #     end_datetime = datetime.strptime(end_datetime_str, "%Y/%m/%d %H:%M")
    #     time_difference = end_datetime - start_datetime
    #
    #     previous_day = datetime.strptime(end_date_str, "%Y/%m/%d") - timedelta(days=1)
    #     end_date_str = str(previous_day.year) + '/' + str(previous_day.month) + '/' + str(previous_day.day)
    #
    #     if time_difference.total_seconds() < 24 * 3600:
    #         return start_date_str + ' ' + performance_time_str
    #     else:
    #         return start_date_str + ' ~ ' + end_date_str + ' ' + performance_time_str


def prc_lines(lines):
    lines = [line.strip() for line in lines if line.strip()]  # 不要空白行
    ''' 先把特殊文字轉換 '''
    lines = [convert_special_font(line) for line in lines]
    ''' 不要括號內容 '''
    lines = [re.sub(r"[\(（「<][^)）」>]+[\)）」>]", " ", line) for line in lines]  # 不要括號和全形括號內容
    lines = [re.sub(r'\(', "", line) for line in lines]
    lines = [re.sub(r'\)', "", line) for line in lines]
    ''' / 左右不要有空格 '''
    lines = [re.sub(r"\s*/\s*", "/", line) for line in lines]
    ''' : 的轉換 '''
    lines = [re.sub(r"：", ':', line) for line in lines]
    '''   '''
    lines = [re.sub(r" ", ' ', line) for line in lines]
    ''' : 左右不要有空格 '''
    lines = [re.sub(r"\s*:\s*", ':', line) for line in lines]
    ''' 不要有逗號 '''
    lines = [re.sub(r"，", ' ', line) for line in lines]
    ''' ~ 的轉換 '''
    lines = [re.sub(r'至', '~', line) for line in lines]
    lines = [re.sub(r"～", '~', line) for line in lines]
    lines = [re.sub(r"-", '~', line) for line in lines]
    lines = [re.sub(r"－", '~', line) for line in lines]
    lines = [re.sub(r"–", '~', line) for line in lines]
    lines = [re.sub(r"\s*~\s*", " ~ ", line) for line in lines]
    ''' 兩個空格以上都變成單個 '''
    lines = [re.sub(r"\s{2,}", " ", line) for line in lines]
    ''' 不要加價購 '''
    lines = [re.sub(r'\+.*?元|\+.*?\$\d{3,5}', "", line) for line in lines]
    ''' 價格不要有, '''
    lines = [re.sub(r",(\d{3})", r"\1", line) for line in lines]
    ''' 價格的 $ 左右不要有空格 '''
    lines = [re.sub(r"\s*\$\s*(\d{3,6})", r'$\1', line) for line in lines]
    ''' 價格的 元 左右不要有空格 '''
    lines = [re.sub(r"\s*(\d{3,6})\s*元", r'\1元', line) for line in lines]
    ''' @ '''
    lines = [re.sub(r'@', '', line) for line in lines]
    ''' 不要入場 '''
    lines = [re.sub(
        r"\d{2}:\d{2}\s?[入進][場站]|[入進]場\d{2}:\d{2}\s?|[入進]場.*\d{2}:\d{2}|\d{2}:\d{2}\s?open|open\d{2}:\d{2}\s?",
        "", line) for line in lines]
    ''' 不要身障票 '''
    lines = [re.sub(r'身障[\u4e00-\u9fff]{0,3}[$:]?\d{3,6}|'
                    r'身障[\u4e00-\u9fff]{0,3}\s*NT[$:]?\d{3,6}|'
                    r'身障\s*NT[$]?\d{3,6}|'
                    r'(身障票.*\d{3,6})', '', line) for line in lines]
    lines = [re.sub(r'愛心[\u4e00-\u9fff]{0,3}[$:]?\d{3,6}|'
                    r'愛心[\u4e00-\u9fff]{0,3}\s*NT[$:]?\d{3,6}|'
                    r'愛心\s*NT[$]?\d{3,6}|'
                    r'(愛心票.*\d{3,6})', '', line) for line in lines]
    lines = [re.sub(r'.*身障優惠.*', '', line) for line in lines]
    lines = [re.sub(r'.*身障表單.*', '', line) for line in lines]
    lines = [re.sub(r'.*身心障礙.*', '', line) for line in lines]
    # lines = [re.sub(r'身障[\u4e00-\u9fff]{0,3}', "", line) for line in lines]
    # lines = [re.sub(r'身障票[:種]?\s*[$]?\s*\d{3,4}\s*[元]?|'
    #                 r'身障席[:}?\s*[$]?\s*\d{3,4}\s*[元]?|身障席\s*[$]?\s*\d{3,4}[元]?]|'
    #                 r'身障\s*NT[$]?\d{3,4}[元]?|'
    #                 r'愛心.*NT\s*\$\s*\d{3,6}\s*|'
    #                 r'愛心.*\d{3,6}',
    #                 '', line) for line in lines]
    # lines = [re.sub(r'身障.*\d{3,6}|'
    #                 r'愛心.*\d{3,6}|'
    #                 r'身心障礙.*\d{3,6}|'
    #                 r'殘障.*\d{3,6}',
    #                 '', line) for line in lines]
    # lines = [re.sub(r'輪椅席區.*', '', line) for line in lines]
    # lines = [re.sub(r'.*身障.*', '', line) for line in lines]
    # 【單日票】單日愛心票(需出示殘障手冊) NT$1, 000
    # ''' 不要open '''
    # lines = [re.sub(r'(\d{1,2}:\d{2})\s*open', '', line) for line in lines]
    # ''' 傳真 '''
    # lines = [re.sub(r'.*傳真.*', '', line) for line in lines]
    # ''' 工作天 '''
    # lines = [re.sub(r'.*工作天.*', '', line) for line in lines]
    # ''' 福利 '''
    # lines = [re.sub(r'.*福利.*', '', line) for line in lines]
    ''' 贊助金額 '''
    lines = [re.sub(r".*贊助[NT]?\$(\d+)", "", line) for line in lines]
    ''' 不要XXXX年 '''
    lines = [re.sub(r"\d{4}\s*年", "", line) for line in lines]
    ''' \u200b|\u200d|\xa0 '''
    lines = [re.sub(r'\u200b', '', line) for line in lines]
    lines = [re.sub(r'\u200d', '', line) for line in lines]
    lines = [re.sub(r'\xa0', '', line) for line in lines]
    ''' 超過 '''
    lines = [re.sub(r'超過.*\d{3,6}|more than.*\d{3,6}', '', line) for line in lines]
    ''' 單日上限 '''
    lines = [re.sub(r'上限.*\d{3,6}|spending limit.*\d{3,6}', '', line) for line in lines]
    ''' 舉例說明 '''
    lines = [re.sub(r'.*舉例說明.*', '', line) for line in lines]
    ''' 退票 '''
    lines = [re.sub(r'.*退票.*', '', line) for line in lines]
    ''' 票價每席 '''
    lines = [re.sub(r'票價每席\d{3,6}', '', line) for line in lines]
    # ''' 票價之間不要有空格 '''
    # lines = [re.sub(r'票\s*價', '票價', line) for line in lines]
    # ''' 手續費 '''
    # lines = [re.sub(r'.*手續費.*', '', line) for line in lines]
    # ''' 未退票 '''
    # lines = [re.sub(r'.*未退票.*', '', line) for line in lines]
    # ''' 未退票 '''
    # lines = [re.sub(r'.*來回票.*', '', line) for line in lines]
    # ''' 折抵 '''
    # lines = [re.sub(r'.*折抵.*', '', line) for line in lines]
    # ''' 不要年分 '''
    # lines = [re.sub(r"(?<!\d{2}月)\d{4}年(?!\d{1,2}月)", "", line) for line in lines]
    return lines


def al_lines(lines):
    try:
        lines = [line.strip() for line in lines if line.strip()]  # 不要空白行
        ''' 全部都小寫 '''
        lines = [line.lower() for line in lines]
        ''' 先把特殊文字轉換 '''
        lines = [convert_special_font(line) for line in lines]
        ''' 不要括號內容 '''
        lines = [re.sub(r"[\(（「<《][^)）」>》]+[\)）」>》]", " ", line) for line in lines]  # 不要括號和全形括號內容
        lines = [re.sub(r'\(', "", line) for line in lines]
        lines = [re.sub(r'\)', "", line) for line in lines]
        ''' 特殊符號 -> : '''
        lines = [re.sub(r'\s*／\s*', ':', line) for line in lines]
        lines = [re.sub(r'\s*｜\s*', ':', line) for line in lines]
        lines = [re.sub(r'\s*\|\s*', ':', line) for line in lines]
        lines = [re.sub(r'\s*⎪\s*', ':', line) for line in lines]
        lines = [re.sub(r"\s*：\s*", ':', line) for line in lines]
        lines = [re.sub(r"\s*:\s*", ':', line) for line in lines]
        ''' 、替換成空格 '''
        lines = [re.sub(r"\s*、\s*", " ", line) for line in lines]
        ''' / 左右不要有空格 '''
        lines = [re.sub(r"\s*/\s*", "/", line) for line in lines]
        ''' 逗號 -> blank space  '''
        lines = [re.sub(r"，", ' ', line) for line in lines]
        ''' ~ 的轉換 '''
        lines = [re.sub(r'至', '~', line) for line in lines]
        lines = [re.sub(r"～", '~', line) for line in lines]
        lines = [re.sub(r"-", '~', line) for line in lines]
        lines = [re.sub(r"－", '~', line) for line in lines]
        lines = [re.sub(r"–", '~', line) for line in lines]
        lines = [re.sub(r"\s*~\s*", " ~ ", line) for line in lines]
        ''' \u200b|\u200d|\xa0 '''
        lines = [re.sub(r'\u200b', '', line) for line in lines]
        lines = [re.sub(r'\u200d', '', line) for line in lines]
        lines = [re.sub(r'\xa0', '', line) for line in lines]
        # ''' 不要加價購 '''
        # lines = [re.sub(r'\+.*?元|\+.*?\$\d{3,5}', "", line) for line in lines]
        # ''' 價格不要有, '''
        # lines = [re.sub(r",(\d{3})", r"\1", line) for line in lines]
        # ''' 價格的 $ 左右不要有空格 '''
        # lines = [re.sub(r"\s*\$\s*(\d{3,6})", r'$\1', line) for line in lines]
        # ''' @ '''
        # lines = [re.sub(r'@', '', line) for line in lines]
        # ''' 價格的 元 左右不要有空格 '''
        # lines = [re.sub(r"\s*(\d{3,6})\s*元", r'\1元', line) for line in lines]

        ''' 不要入場 '''
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
        # lines = [re.sub(r'[入進]場[:]?\d{1,2}:\d{2}\s*|'
        #                 r'\d{1,2}:\d{2}\s*[入進]場\s*|'
        #                 r'[入進]場時間[:]?\d{1,2}:\d{2}\s*|'
        #                 r'[入進]場時間[:]?預計\d{1,2}:\d{2}\s*|'
        #                 r'open[:]?\s*\d{1,2}:\d{2}\s*|'
        #                 r'\d{1,2}:\d{2}\s*open\s*|'
        #                 r'\d{1,2}:\d{2}\s*開放[入進]場|'
        #                 r'\d{1,2}:\d{2}\s*開放觀眾[入進]場'
        #                 r'[入進]場[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}\s*|'
        #                 r'\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}\s*[入進]場\s*|'
        #                 r'[入進]場時間[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}\s*|'
        #                 r'[入進]場時間[:]?預計\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}\s*|'
        #                 r'open[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\s*\d{1,2}:\d{2}\s*|'
        #                 r'\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}\s*open\s*|'
        #                 r'\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}\s*開放[入進]場|'
        #                 r'\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}\s*開放觀眾[入進]場',
        #                 '', line) for line in lines]
        # ''' 不要身障票 '''
        # lines = [re.sub(r'身障[\u4e00-\u9fff]{0,3}[$:]?\d{3,6}|'
        #                 r'身障[\u4e00-\u9fff]{0,3}\s*NT[$:]?\d{3,6}|'
        #                 r'身障\s*NT[$]?\d{3,6}|'
        #                 r'(身障票.*\d{3,6})', '', line) for line in lines]
        # lines = [re.sub(r'愛心[\u4e00-\u9fff]{0,3}[$:]?\d{3,6}|'
        #                 r'愛心[\u4e00-\u9fff]{0,3}\s*NT[$:]?\d{3,6}|'
        #                 r'愛心\s*NT[$]?\d{3,6}|'
        #                 r'(愛心票.*\d{3,6})', '', line) for line in lines]
        # lines = [re.sub(r'.*身障優惠.*', '', line) for line in lines]
        # lines = [re.sub(r'.*身障表單.*', '', line) for line in lines]
        # lines = [re.sub(r'.*身心障礙.*', '', line) for line in lines]
        ''' xx年xx月xx號(日) or xx年xx月xx號(日) 轉換成 xxxx/xx/xx'''
        lines = [re.sub(r"(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*[日號]", r"\1/\2/\3 ", line) for line in lines]
        lines = [re.sub(r"(\d{1,2})\s*[.月]\s*(\d{1,2})\s*[日號]?", r"\1/\2 ", line) for line in lines]
        lines = [re.sub(r"(\d{4})\s*.\s*(\d{1,2})\s*.\s*(\d{1,2})", r"\1/\2/\3 ", line) for line in lines]
        ''' 把沒有年份的都補上年份 '''
        lines = [re.sub(r"\d{4}/\d{1,2}/\d{1,2}|\d{1,2}/\d{1,2}", add_year, line) for line in lines]
        ''' xxxx/xx/xx (Mon.) xx:xx start 刪除 '''
        lines = [re.sub(r'(\d{1,2})\s*?([A-Za-z]{3}\.\s*?)', r'\1 ', line) for line in lines]
        ''' 不要星期幾 周幾 '''
        lines = [re.sub(r'星期一|星期二|星期三|星期四|星期五|星期六|星期天|星期日|'
                        r'周一|周二|周三|周四|周五|周六|周日|'
                        r'週一|週二|週三|週四|週五|週六|週日', '', line) for line in lines]
        ''' 怪怪的句子 '''
        lines = [re.sub(r'.*文化部訂定.*', '', line) for line in lines]
        lines = [re.sub(r'.*refer to kktix refund policy*.', '', line) for line in lines]
        lines = [re.sub(r'.*成功於.*之前', '', line) for line in lines]
        lines = [re.sub(r'.*詳細步驟.*', '', line) for line in lines]
        lines = [re.sub(r'.*粉絲福利預計.*', '', line) for line in lines]
        lines = [re.sub(r'.*兌換時間以現場公告為準.*', '', line) for line in lines]
        lines = [re.sub(r'.*kktix退換票規定.*', '', line) for line in lines]
        lines = [re.sub(r'.*refund will not be accepted.*', '', line) for line in lines]
        lines = [re.sub(r'.*郵戳退票不再受理.*', '', line) for line in lines]
        lines = [re.sub(r'.*身障表單.*', '', line) for line in lines]
        lines = [re.sub(r'.*身心障礙.*', '', line) for line in lines]
        lines = [re.sub(r'.*註冊.*會員.*', '', line) for line in lines]
        lines = [re.sub(r'.*消費者.*', '', line) for line in lines]
        lines = [re.sub(r'.*購票專區.*', '', line) for line in lines]
        # lines = [re.sub(r'.*.*', '', line) for line in lines]
        # lines = [re.sub(r'.*.*', '', line) for line in lines]
        '-------------------------------------------------------------------------------------------'
        ''' 中文 轉換 數字型態 '''
        lines = [re.sub(r"早上[場]?\s*(\d{1,2})\s*[點時]", r"\1:00", line) for line in lines]
        lines = [re.sub(r"早上", " ", line) for line in lines]
        lines = [re.sub(r"上午[場]?\s*(\d{1,2})\s*[點時]", r"\1:00", line) for line in lines]
        lines = [re.sub(r"上午", " ", line) for line in lines]
        lines = [re.sub(r"中午[場]?\s*(\d{1,2})\s*[點時]", r"\1:00", line) for line in lines]
        lines = [re.sub(r"中午", " ", line) for line in lines]
        lines = [re.sub(r"下午[場]?\s*(\d{1,2})\s*[點時]", r'下午\1:00', line) for line in lines]
        lines = [re.sub(r"下午[場]?\s*(\d{1,2}):(\d{2})\s*", replace_chinese, line) for line in lines]
        lines = [re.sub(r"晚上[場]?\s*(\d{1,2})\s*[點時]", r'晚上\1:00', line) for line in lines]
        lines = [re.sub(r"晚上[場]?\s*(\d{1,2}):(\d{2})\s*", replace_chinese, line) for line in lines]
        ''' 兩個空格以上都變成單個 '''
        lines = [re.sub(r"\s{2,}", " ", line) for line in lines]
        ''' 英文 轉換 數字 '''
        lines = [re.sub(r"p.m.", 'pm', line) for line in lines]
        lines = [re.sub(r"P.M.", 'pm', line) for line in lines]
        lines = [re.sub(r"PM", 'pm', line) for line in lines]
        lines = [re.sub(r"a.m.", 'am', line) for line in lines]
        lines = [re.sub(r"A.M.", 'am', line) for line in lines]
        lines = [re.sub(r"AM", 'am', line) for line in lines]
        lines = [re.sub(r"(\d{1,2})\s*noon", r"\1:00", line) for line in lines]
        lines = [re.sub(r"(\d{4}/\d{1,2}/\d{1,2})\s*am\s*(\d{1,2}:\d{2})", r"\1 \2", line) for line in lines]
        lines = [re.sub(r"(\d{4}/\d{1,2}/\d{1,2})\s*pm\s*(\d{1,2}:\d{2})", r"\1 \2 pm", line) for line in lines]
        lines = [re.sub(r"(\d{1,2})(?::(\d{2}))?\s*([ap]m)", replace_english, line) for line in lines]
        ''' 兩個空格以上都變成單個 '''
        lines = [re.sub(r"\s{2,}", " ", line) for line in lines]
        '-------------------------------------------------------------------------------------------'
        ''' 改時間 '''
        lines = [
            re.sub(r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*改.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})', r'\2', line)
            for line in lines]
        ''' 幾號前購買 '''
        lines = [re.sub(r"\d{4}/\d{1,2}/\d{1,2}\s*前.*購買|"
                        r"\d{4}/\d{1,2}/\d{1,2}\s*起.*加購",
                        "", line) for line in lines]
        lines = [re.sub(r"\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}\s*前.*購買|"
                        r"\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}\s*起.*加購",
                        "", line) for line in lines]
        ''' xx:xx (~ xx:xx) 括號的時間都刪除 '''
        lines = [re.sub(r"(\d{1,2}):(\d{2})\s*~\s*\d{1,2}:\d{2}", r"\1:\2", line) for line in lines]
        ''' xxxx/xx/xx xx:xx ~ xxxx/xx/xx 相差24小時 對字串做處理 版本2 '''
        lines = [re.sub(r"(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})\s*~\s*(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})",
                        adjacent_date, line) for line in lines]
        return lines

    except Exception as e:
        print('發生錯誤 1', e)
        return []


# get datetimes in a line xxxx/xx/xx ~ oooo/oo/oo
def get_all_performance_time_single_line(line):
    dp = r"(\d{4}/\d{1,2}/\d{1,2})\s*~\s*(\d{4}/\d{1,2}/\d{1,2})"
    tp = r"\d{4}/\d{1,2}/\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}\s*(\d{1,2}:\d{2})"
    date_match = re.search(dp, line)
    time_match = re.search(tp, line)
    if not date_match:
        return get_all_performance_time_single_line2(line)
    if time_match:
        time_str = time_match.group(1)
        time_obj = datetime.strptime(time_str, "%H:%M").time()
    else:
        time_obj = time(0, 0)

    # print('found', date_match.group(1))
    # print('found', date_match.group(2))
    # print('found', time_obj)  # datetime.time

    start_date = datetime.strptime(date_match.group(1), "%Y/%m/%d")
    end_date = datetime.strptime(date_match.group(2), "%Y/%m/%d")

    dates = []
    current_date = start_date

    while current_date <= end_date:
        dates.append(current_date.strftime("%Y/%m/%d"))
        current_date += timedelta(days=1)
    print('dates', dates)

    ''' datetime.date '''
    date_objs = [datetime.strptime(date, "%Y/%m/%d").date() for date in dates]
    # print('date_objs')
    # for datet_obj in date_objs:
    #     print(datet_obj)
    # print('date_objs')
    print('date_objs', date_objs)

    ''' datetime.datetime'''
    datetime_objs = [datetime.combine(date_obj, time_obj) for date_obj in date_objs]
    # print('datetime_obj')
    # for datetime_obj in datetime_objs:
    #     print(datetime_obj)
    # print('datetime_obj')
    print('datetime_objs', datetime_objs)

    # return dates
    # return date_objs
    return datetime_objs


# get datetimes in a line
def get_all_performance_time_single_line2(line):
    # print('get_all_performance_time_single_line2')
    dates = re.findall(r"\d{4}/\d{1,2}/\d{1,2}", line)
    times = re.findall(r"\d{1,2}:\d{2}", line)
    # if dates or times:
    #     print('get_all_performance_time_single_line2', line)
    #     print('chih', line)
    #     print('chun', dates)
    #     print('kuan', times)
    # if len(dates) == 1 and len(times) == 2:
    #     print('the world')
    if not dates:
        # print('get_all_performance_time_single_line2 no dates')
        return []
    elif len(dates) == len(times):
        # print('times = dates')
        datetime_objs = []
        for i in range(len(dates)):
            datetime_objs.append(datetime.combine(datetime.strptime(dates[i], "%Y/%m/%d").date(),
                                                  datetime.strptime(times[i], "%H:%M").time()))
        # dttms = re.findall(r"\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}", line)
        # print(dttms)
        # print('1')
        # datetime_objs = [datetime.strptime(dttm, "%Y/%m/%d %H:%M") for dttm in dttms]
        # print('qwe', datetime_objs)
        return datetime_objs
    elif times and (len(dates) > len(times)):
        # print('has time, dates > times')
        time_obj = datetime.strptime(times[0], "%H:%M").time()
        date_objs = [datetime.strptime(date, '%Y/%m/%d').date() for date in dates]
        datetime_objs = [datetime.combine(date_obj, time_obj) for date_obj in date_objs]
        return datetime_objs
    elif not times and (len(dates) > len(times)):
        # print('not times, dates > times')
        time_obj = time(0, 0)
        date_objs = [datetime.strptime(date, '%Y/%m/%d').date() for date in dates]
        datetime_objs = [datetime.combine(date_obj, time_obj) for date_obj in date_objs]
        return datetime_objs
    elif len(dates) == 1 and len(times) >= 2:
        # print('za warudo')
        date_obj = datetime.strptime(dates[0], '%Y/%m/%d').date()
        time_objs = [datetime.strptime(tm, "%H:%M").time() for tm in times]
        datetime_objs = [datetime.combine(date_obj, time_obj) for time_obj in time_objs]
        return datetime_objs
    # if dates:
    #     date_objs = [datetime.strptime(date, '%Y/%m/%d').date() for date in dates]
    #     # print('date_objs', date_objs)
    #     # for date in dates:
    #     #
    #     # date_obj = datetime.strptime(dates[0], '%Y/%m/%d')
    #     # print(type(date_obj))
    #     # date_obj = datetime.strptime(dates[0], '%Y/%m/%d').date()
    #     # print(type(date_obj))
    # else:
    #     return []
    #

    #
    # datetime_objs = [datetime.combine(date_obj, time_obj) for date_obj in date_objs]
    # # for datetime_obj in datetime_objs:
    # #     print(datetime_obj)
    #
    # return datetime_objs


# get datetimes if
def dt_untils(line):
    performance_datetimes = []
    dp = r"(\d{4}/\d{1,2}/\d{1,2})\s*~\s*(\d{4}/\d{1,2}/\d{1,2})"
    tp = r"\d{4}/\d{1,2}/\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}\s*(\d{1,2}:\d{2})"

    date_untils = re.findall(dp, line)

    if date_untils:
        # print('found until', line)
        start_date = datetime.strptime(date_untils[0][0], "%Y/%m/%d")
        end_date = datetime.strptime(date_untils[0][1], "%Y/%m/%d")
        time_str = re.findall(tp, line)
        if time_str:
            time_obj = datetime.strptime(time_str[0], "%H:%M").time()
        else:
            time_obj = time(0, 0)

        dates = []
        current_date = start_date

        while current_date <= end_date:
            dates.append(current_date.strftime("%Y/%m/%d"))
            current_date += timedelta(days=1)

        date_objs = [datetime.strptime(date, "%Y/%m/%d").date() for date in dates]
        datetime_objs = [datetime.combine(date_obj, time_obj) for date_obj in date_objs]
        for datetime_obj in datetime_objs:
            performance_datetimes.append(datetime_obj)
        # print(performance_dates)
        return performance_datetimes


def get_performance_city(lines):
    locations = []
    for line in lines:
        # lctns = re.findall(r"(臺北)[場站]|(台北)[場站]|"
        #                    r"(新北)[場站]|(基隆)[場站]|"
        #                    r"(桃園)[場站]|(新竹)[場站]|"
        #                    r"(宜蘭)[場站]|(臺中)[場站]|"
        #                    r"(台中)[場站]|(苗栗)[場站]|"
        #                    r"(彰化)[場站]|(南投)[場站]|"
        #                    r"(雲林)[場站]|(高雄)[場站]|"
        #                    r"(臺南)[場站]|(嘉義)[場站]|"
        #                    r"(屏東)[場站]|(澎湖)[場站]|"
        #                    r"(花蓮)[場站]|(臺東)[場站]|"
        #                    r"(台東)[場站]|(綠島)[場站]|"
        #                    r"(金門)[場站]", line)
        # lctns = re.findall(r'([台臺]北)[場站]|'
        #                    r'([台臺]中)[場站]|'
        #                    r'([台臺]南)[場站]|'
        #                    r'([台臺]東)[場站]|'
        #                    r'(新北)[場站]|'
        #                    r'(基隆)[場站]|'
        #                    r'(桃園)[場站]|'
        #                    r'(新竹)[場站]|'
        #                    r'(宜蘭)[場站]|'
        #                    r'(苗栗)[場站]|'
        #                    r'(彰化)[場站]|'
        #                    r'(南投)[場站]|'
        #                    r'(雲林)[場站]|'
        #                    r'(高雄)[場站]|'
        #                    r'(嘉義)[場站]|'
        #                    r'(屏東)[場站]|'
        #                    r'(澎湖)[場站]|'
        #                    r'(花蓮)[場站]|'
        #                    r'(綠島)[場站]|'
        #                    r'(金門)[場站]', line)
        lctns = re.findall(r'([台臺]北)|'
                           r'([台臺]中)|'
                           r'([台臺]南)|'
                           r'([台臺]東)|'
                           r'(新北)|'
                           r'(基隆)|'
                           r'(桃園)|'
                           r'(新竹)|'
                           r'(宜蘭)|'
                           r'(苗栗)|'
                           r'(彰化)|'
                           r'(南投)|'
                           r'(雲林)|'
                           r'(高雄)|'
                           r'(嘉義)|'
                           r'(屏東)|'
                           r'(澎湖)|'
                           r'(花蓮)|'
                           r'(綠島)|'
                           r'(金門)', line)
        for i, lctn in enumerate(lctns):
            for j in range(len(lctns[0])):
                # print(lctns[0][i])
                if lctns[0][j]:
                    locations.append(lctns[0][j])
    # print(locations2)
    counter = Counter(locations)
    most_common = counter.most_common(1)
    # print('most_common', most_common)
    if most_common:
        city = most_common[0][0]
        return city
    else:
        return ''


# main
def get_prices(lines):
    prices_lines = []
    prices = []
    for line in lines:
        # 如果這行有這些關鍵字
        # numbers = re.findall(r'\d{3,6}', line)
        # if numbers:
        #     print(line)
        #     disabled = re.findall(r'身障[\u4e00-\u9fff]{0,3}[$:]?\d{3,6}|'
        #                           r'身障[\u4e00-\u9fff]{0,3}\s*NT[$:]?\d{3,6}|'
        #                           r'身障\s*NT[$]?\d{3,6}', line)
        #     if disabled:
        #         print('發現!', disabled)
        prcs = re.findall(r"\$\d{3,6}|"
                          r"\d{3,6}元|"
                          r"預售|"
                          r"現場|"
                          r"索票|"
                          r"DOOR\s*\d{3,6}|"
                          r"票[:]?\d{3,6}|"
                          r"票\s*價|"
                          r"NT", line)
        # 如果有索票 就回傳免費
        if '索票' in prcs or '免費' in prcs:
            prices.append(0)
            return prices
        # 如果這行關鍵字 又有三位數以上的數字 那我就把他加進prices_lines
        contain_number = re.findall(r"\d{3,6}", line)
        if prcs:
            print('has prcs', line)
        if prcs and contain_number:
            prices_lines.append(line)
    # 整理好prices_lines之後 我想要把裡面的價格提取出來
    for line in prices_lines:
        prcs = re.findall(r"\d{3,6}", line)
        for prc in prcs:
            prices.append(prc)
    prices = list(set(prices))
    prices = [int(num) for num in prices if 99 < int(num) <= 99999 and int(num) != 2023 and int(num) != 2024]
    prices = sorted(prices, reverse=True)
    return prices


def get_performance_datetimes(lines):
    performance_datetimes = []
    for line in lines:
        dts = re.findall(r"\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}", line)
        if dts:
            for dt in dts:
                try:
                    print('qwe', line)
                    dttms = get_all_performance_time_single_line(dt)
                    for dttm in dttms:
                        if dttm not in performance_datetimes:
                            performance_datetimes.append(dttm)
                    # print(dttm)
                except Exception as e:
                    print('發生錯誤 2', e)
    return performance_datetimes


def get_start_time(lines):
    performance_time = ''
    for line in lines:
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
                            r'start\s*[:]?\s*(\d{1,2}:\d{2})|'
                            r'(\d{1,2}:\d{2})\s*start|'
                            r'begin\s*[:]?\s*(\d{1,2}:\d{2})|'
                            r'(\d{1,2}:\d{2})\s*begin|'
                            r'(\d{1,2}:\d{2})\s*show start|'
                            r'show start\s*(\d{1,2}:\d{2})|'
                            r'show time\s*[:]?\s*(\d{1,2}:\d{2})', line)
        if starts:
            for i in range(len(starts[0])):
                if starts[0][i]:
                    # print('start time', starts[0][i])
                    performance_time = starts[0][i]
    if len(performance_time) >= 4:
        # print('catch performance time', performance_time)
        # print()
        return datetime.strptime(performance_time, "%H:%M").time()
        # return performance_time
    else:
        # return datetime.time(0, 0)
        return '00:00'


def get_single_performance_date(lines):
    performance_dates = []
    for line in lines:
        performance_dts = re.findall(r"\d{4}/\d{1,2}/\d{1,2}", line)
        if performance_dts:
            for performance_dt in performance_dts:
                try:
                    dt = datetime.strptime(performance_dt, "%Y/%m/%d").date()
                    if dt.year >= 2023 and dt not in performance_dates:
                        performance_dates.append(dt)
                except:
                    pass
    if len(performance_dates) == 1:
        # print('catch a performance date 1', performance_dates[0])
        # print()
        return performance_dates[0]
    elif len(performance_dates) > 1:
        # print('> 1 performance_dates', performance_dates)
        performance_dates = []
        for line in lines:
            dts = re.findall(r'演出日期.*(\d{4}/\d{1,2}/\d{1,2})|'
                             r'演出時間.*(\d{4}/\d{1,2}/\d{1,2})|'
                             r'表演時間.*(\d{4}/\d{1,2}/\d{1,2})|'
                             r'活動日期.*(\d{4}/\d{1,2}/\d{1,2})|'
                             r'^時間.*(\d{4}/\d{1,2}/\d{1,2})|'
                             r'^日期.*(\d{4}/\d{1,2}/\d{1,2})|'
                             r'(\d{4}/\d{1,2}/\d{1,2}).*開演|'
                             r'(\d{4}/\d{1,2}/\d{1,2}).*加演', line)
            if dts:
                for i in range(len(dts[0])):
                    if dts[0][i]:
                        try:
                            # print('qwer', dts[0][i])
                            performance_dates.append(datetime.strptime(dts[0][i], "%Y/%m/%d").date())
                        except Exception as e:
                            print('發生錯誤 6', e)
    if len(performance_dates) == 1:
        return performance_dates[0]
        # else:
        #     print('now', performance_dates)
        # else:
        #     print('hello', performance_dates)
        #         performance_dts = re.findall(r'日期.*(\d{4}/\d{1,2}/\d{1,2})', line)
        #         # performance_dts = [performance_dt.strip() for performance_dt in performance_dts]
        #         for performance_dt in performance_dts:
        #             try:
        #                 dt = datetime.strptime(performance_dt, "%Y/%m/%d").date()
        #                 if dt.year >= 2023 and dt not in performance_dates:
        #                     performance_dates.append(dt)
        #             except Exception as e:
        #                 print('顯示錯誤 5', e)
        #         if len(performance_dates) == 1:
        #             print('catch a performance date 2', performance_dates[0])
        #             return performance_dates[0]
        ''' 備份 '''
        # print('> 1 performance_dates', performance_dates)
        # performance_dates = []
        # for line in lines:
        #     performance_dts = re.findall(r'日期.*(\d{4}/\d{1,2}/\d{1,2})', line)
        #     performance_dts = [performance_dt.strip() for performance_dt in performance_dts]
        #     for performance_dt in performance_dts:
        #         try:
        #             dt = datetime.strptime(performance_dt, "%Y/%m/%d").date()
        #             if dt.year >= 2023 and dt not in performance_dates:
        #                 performance_dates.append(dt)
        #         except Exception as e:
        #             print('顯示錯誤 5', e)
        #     if len(performance_dates) == 1:
        #         print('catch a performance date 2', performance_dates[0])
        #         return performance_dates[0]


def get_single_performance_datetime(lines):
    performance_time = get_start_time(lines)
    performance_date = get_single_performance_date(lines)
    # print('zaza', performance_time)
    # print('qaqa', performance_date, type(performance_date))
    if performance_time != '00:00' and performance_date is not None:
        return datetime.combine(performance_date, performance_time)
    # if performance_time is not None and performance_date is not None:
    #     return datetime.combine(performance_date, datetime.strptime(performance_time, "%H:%M").time())
    # elif performance_date is None:
    #     print('no date found')
    elif performance_date is not None:
        print('單日 但是只有找到日期 沒有時間', datetime.combine(performance_date, time(0, 0)))
        return datetime.combine(performance_date, time(0, 0))
        # return performance_date


def date_city_locations(lines):
    performance_datetimes = []
    locations = []
    delete_lines = []
    for line in lines:
        dts_lctns = re.findall(r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*([台臺]北[站]?\s*.*)$|"
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
        if dts_lctns:
            delete_lines.append(line)
            for i in range(1, len(dts_lctns[0]), 2):
                if dts_lctns[0][i]:
                    location = dts_lctns[0][i]
                    location = location.replace('\xa0', '')
                    locations.append(location)
            for i in range(0, len(dts_lctns[0]), 2):
                if dts_lctns[0][i]:
                    if ':' in dts_lctns[0][i]:
                        performance_datetimes.append(datetime.strptime(dts_lctns[0][i], '%Y/%m/%d %H:%M'))
                    else:
                        performance_datetimes.append(
                            datetime.combine(datetime.strptime(dts_lctns[0][i], '%Y/%m/%d').date(), time(0, 0)))

    return performance_datetimes, locations, delete_lines


def get_locations_of_date_city_locations(lines):
    locations = []
    for line in lines:
        lctns = re.findall(r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*[台臺]北[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*[台臺]中[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*[台臺]南[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*[台臺]東[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*新北[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*基隆[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*桃園[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*新竹[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*宜蘭[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*苗栗[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*彰化[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*南投[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*雲林[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*高雄[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*嘉義[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*屏東[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*澎湖[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*花蓮[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*綠島[站]?\s*(.*)$|"
                           r"\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?\s*金門[站]?\s*(.*)$", line)
        if lctns:
            for i in range(lctns[0]):
                if lctns[0][i]:
                    print(lctns[0][i])
                    locations.append(lctns[0][i])
    return locations


# sort datetimes
def sort_datetime(datetime_list):
    # 创建一个字典，用于按日期进行分组
    date_dict = {}
    for dt in datetime_list:
        date = dt.date()
        if date not in date_dict:
            date_dict[date] = []
        date_dict[date].append(dt)

    # 从字典中提取具体时间的日期和没有相同日期的日期
    final_datetimes = []
    for dt_list in date_dict.values():
        dt_list = list(set(dt_list))
        if len(dt_list) == 1:
            final_datetimes.append(dt_list[0])
        else:
            for dt in dt_list:
                if dt.hour != 0:
                    final_datetimes.append(dt)
    final_datetimes = list(set(final_datetimes))
    final_datetimes.sort()
    final_datetimes = [final_datetime for final_datetime in final_datetimes if
                       final_datetime.year >= datetime.now().year - 1]
    return final_datetimes


# sort datetimes and locations


def sort_dts_lctns(performance_dts, lctns):
    performance_datetimes = []
    deleted_contents = []

    # print('in sdl2, first')
    # print('in sdl2', performance_dts)
    # print('in sdl2', lctns)

    for i, performance_datetime in enumerate(performance_dts):
        if performance_datetime not in performance_datetimes:
            performance_datetimes.append(performance_datetime)
        else:
            deleted_contents.append(lctns[i])

    for deleted_content in deleted_contents:
        # print('del!', lctns[lctns.index(deleted_content)])
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

    # print('in sdl2, after')
    # print('iu sdl2', performance_datetimes)
    # print('in sdl2', locations)

    return performance_datetimes, locations


# main
def get_sell_datetimes(lines):
    sell_lines = []
    sell_dts = []
    sell_datetimes = []

    for line in lines:
        whatevers = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}', line)
        if whatevers:
            print('found date and time', line)

    for line in lines:
        sell_times = re.findall(r'啟售時間.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'售票日期.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'售票時間.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'正式啟售.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'全面啟售.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'全面開賣.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'全區售票.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
                                r'開賣時間.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
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
        if sell_times:
            print('has sell_times 1', line)
            for i in range(len(sell_times[0])):
                if sell_times[0][i]:
                    # print('first round', sell_times)
                    sell_lines.append(line)
        #             sell_dts.append(sell_times[0][i])
        # sell_times = re.findall(r'啟售時間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                         r'售票日期.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                         r'售票時間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                         r'正式啟售.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                         r'全面啟售.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                         r'全面開賣.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                         r'全區售票.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                         r'開賣時間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                         r'索票時間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                         r'索票時段.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                         r'會員預售.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                         r'優先購.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                         r'加\s*開.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                         r'啟\s*售.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                         r'public sale.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                         r'open sale.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                         r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}.*[販啟銷]售|'
        #                         r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}.*開賣|'
        #                         r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}.*售票|'
        #                         r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}.*選位|'
        #                         r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}.*優先購|'
        #                         r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}.*加開|'
        #                         r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}.*準時開搶', line)
        # if sell_times:
        #     print('first round', sell_times)
        #     sell_lines.append(line)
    # print('after first round', sell_lines)

    if not sell_lines:
        for i, line in enumerate(lines):
            sell_times = re.findall(r'啟售時間|售票日期|售票時間|正式啟售|全面啟售|全面開賣|'
                                    r'全區售票|開賣時間|索票時間|索票時段|會員預售', line)
            if sell_times:
                print('has sell_times 2', line)
                for j in range(i + 1, len(lines)):
                    dts = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}', lines[j])
                    if dts:
                        # print('!! different line')
                        # print('second round', lines[j])
                        sell_lines.append(lines[j])
                    else:
                        break

    for sell_line in sell_lines:
        a = re.findall(r'~.s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}\s*~', sell_line)
        b = re.findall(r'~.s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}', sell_line)
        if a:
            pass
        elif b:
            sell_line = re.sub(r'~.s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}\s*~', '', sell_line)
        dts = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{1,2}', sell_line)
        # print('gg', dts)
        if len(dts) > 1:
            print('hello')
        for dt in dts:
            sell_datetimes.append(datetime.strptime(dt, "%Y/%m/%d %H:%M"))

    for sell_line in sell_lines:
        # print('刪除', sell_line)
        del lines[lines.index(sell_line)]

    for sell_datetime in sell_datetimes:
        date_str = str(sell_datetime.date()).replace('-', '/')
        date2 = date_str.split('/')  # list
        date2_str = ''
        if int(date2[1]) <= 9:
            if len(date2[1]) == 1:
                date2_str = date2[0] + '/' + '0' + date2[1] + '/' + date2[2]
            elif len(date2[1]) == 2:
                date2_str = date2[0] + '/' + date2[1][1:] + '/' + date2[2]
        else:
            date2_str = date_str
        datetime_str = date_str + ' ' + str(sell_datetime.time())[:5]
        datetime2_str = date2_str + ' ' + str(sell_datetime.time())[:5]

        # print('date_str', date_str)
        # print('date2_str', date2_str)
        # print('datetime_str', datetime_str)
        # print('datetime2_str', datetime2_str)

        for i, line in enumerate(lines):
            finds = re.findall(
                fr'\b{re.escape(datetime_str)}|{re.escape(datetime2_str)}|{re.escape(date_str)}|{re.escape(date_str)}\b',
                line)
            if finds:
                # print('bef lines[i]', lines[i])
                lines[i] = re.sub(
                    fr'\b{re.escape(datetime_str)}|{re.escape(datetime2_str)}|{re.escape(date_str)}|{re.escape(date_str)}\b',
                    '', lines[i])
                # print('aft lines[i]', lines[i])

    lines = [line.strip() for line in lines if line.strip()]  # 不要空白行
    sell_datetimes = sort_datetime(sell_datetimes)
    return lines, sell_datetimes
    # if not sell_dts:
    #     for i, line in enumerate(lines):
    #         sell_times = re.findall(r'啟售時間|售票日期|售票時間|正式啟售|全面啟售|全面開賣|'
    #                                 r'全區售票|開賣時間|索票時間|索票時段|會員預售', line)
    #         if sell_times:
    #             for j in range(i + 1, len(lines)):
    #                 dts = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}', lines[j])
    #                 if dts:
    #                     sell_lines.append(line)
    #                 else:
    #                     break
    #     for sell_line in sell_lines:
    #         for dt in get_all_performance_time_single_line(sell_line):
    #             sell_dts.append(dt)

    # for sell_datetime in sell_dts:
    #     dttms = get_all_performance_time_single_line(sell_datetime)
    #     for dttm in dttms:
    #         sell_datetimes.append(dttm)
    #
    # sell_datetimes = sort_datetime(sell_datetimes)

    # return sell_datetimes, sell_lines


# main
def get_dts_lctns(lines, lines2):
    performance_datetimes = []
    locations = []
    # dp = r"(\d{4}/\d{1,2}/\d{1,2})\s*~\s*(\d{4}/\d{1,2}/\d{1,2})"
    # tp = r"\d{4}/\d{1,2}/\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}\s*(\d{1,2}:\d{2})"
    ''' test '''
    for line in lines:
        whatevers = re.findall(r'\d{4}/\d{1,2}/\d{1,2}|\d{1,2}:\d{2}', line)
        if whatevers:
            print('w', line)
    '--------------------------------------------------------------------'
    ''' xxxx/xx/xx xx:xx 城市 場館 '''
    dt_lines = []
    for line in lines:
        dtls = re.findall(r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*([台臺]北[站]?\s*.*)$|"
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
        # 表演日期與地點還沒有配對與排序
        if dtls:
            dt_lines.append(line)
            # 表演時間與場館 根據~有兩種處理方法
            if '~' in line:
                location = ''
                # 找到~之中的所有日期
                for dt_until in dt_untils(line):
                    performance_datetimes.append(dt_until)
                # 地點只會有一個 直接=第0個
                for i in range(len(dtls[0])):
                    lctns = re.findall(r'[\u4e00-\u9fff]{1,20}', dtls[0][i])
                    if lctns:
                        location = lctns[0].strip().replace(':', ' ').replace('/', ' ')
                # 地點只會有一個 把長度拉長到與表演時間相同
                for i in range(len(performance_datetimes)):
                    locations.append(location)
            else:
                # 場館
                for i in range(1, len(dtls[0]), 2):
                    if dtls[0][i]:
                        location = dtls[0][i].strip().replace(':', ' ').replace('/', ' ')
                        locations.append(location)
                # 表演時間
                for i in range(0, len(dtls[0]), 2):
                    if dtls[0][i]:
                        # xxxx/xx/xx xx:xx (有找到時間)
                        if ':' in dtls[0][i]:
                            performance_datetimes.append(datetime.strptime(dtls[0][i], '%Y/%m/%d %H:%M'))
                        # xxxx/xx/xx 00:00 (沒有找到時間)
                        else:
                            performance_datetimes.append(
                                datetime.combine(datetime.strptime(dtls[0][i], '%Y/%m/%d').date(), time(0, 0)))
    # print('測試')
    # print('測試', dt_lines)
    # print('測試', len(dt_lines))
    # print('測試', performance_datetimes)
    ''' 找到XXXX/XX/XX 城市 表演場館 可是沒有表演時間 所以我們要從內文當中尋找 XXXX/XX/XX XX:XX 表演時間 '''
    for i, performance_datetime in enumerate(performance_datetimes):
        if performance_datetime.hour == 0:
            for line in lines:
                start_times = re.findall(r'(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})', line)
                if start_times:
                    for j in range(len(start_times)):
                        p_date = datetime.strptime(start_times[j][0], '%Y/%m/%d').date()
                        p_time = datetime.strptime(start_times[j][1], '%H:%M').time()
                        if performance_datetime.date() == p_date:
                            performance_datetimes[i] = datetime.combine(p_date, p_time)
    # print('尋找時間1', performance_datetimes)
    ''' 對於只有一個表演時間的 那我們就找到表演時間之後補上 '''
    # if len(performance_datetimes) == 1:
    #     if performance_datetimes[0].hour == 0:
    #         start_time = get_start_time(lines)
    #         print('start_time', start_time)
    #         if start_time != '00:00':
    #             print('before', performance_datetimes[0])
    #             performance_datetimes[0] = datetime.combine(performance_datetimes[0].date(), start_time)
    #             print('after', performance_datetimes[0])
    if len(dt_lines) == 1:
        # print('only 1 line')
        start_time = get_start_time(lines)
        if start_time != '00:00':
            # print('find start time')
            for i, performance_datetime in enumerate(performance_datetimes):
                performance_datetimes[i] = datetime.combine(performance_datetime, start_time)
    # print('尋找時間2', performance_datetimes)
    if performance_datetimes:
        print('round 1')
        performance_datetimes, locations = sort_dts_lctns(performance_datetimes, locations)
        # performance_datetimes = list(set(performance_datetimes))
        # print(f'!!!!! 找到{len(performance_datetimes)}個表演時間 !!!!!')
        print('1123', len(performance_datetimes), len(locations))
        for i in range(len(performance_datetimes)):
            print(performance_datetimes[i])
            print(locations[i])
        # for performance_datetime in performance_datetimes:
        #     print(performance_datetime)
        # for location in locations:
        #     print(location)
        # print(locations)
        print()
        return performance_datetimes, locations
    '--------------------------------------------------------------------'
    ''' 演出日期 2023/XX/XX XX:XX '''
    dt_lines = []
    locations = []
    for i, line in enumerate(lines):
        # dts = re.findall(r'演出日期.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'演出時間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'活動日期.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'活動時間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'表演日期.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'表演時間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'原場次.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'加\s*場.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'時\s*間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'日\s*期.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}.*開演|'
        #                  r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}.*加演', line)
        # dts = re.findall(r'演出日期\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'演出時間\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'活動日期\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'活動時間\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'表演日期\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'表演時間\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'原場次\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'加\s*場\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'時\s*間\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'日\s*期\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}\s*[:]?\s*開演|'
        #                  r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}\s*[:]?\s*加演', line)
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
        if dts:
            dt_lines.append(lines[i])
            for j in range(i + 1, len(lines)):
                dts2 = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}', lines[j])
                if dts2:
                    print('asd', lines[j])
                    dt_lines.append(lines[j])
                else:
                    break
    for dt_line in dt_lines:
        # print('dt_line')
        for performance_datetime in get_all_performance_time_single_line(dt_line):
            performance_datetimes.append(performance_datetime)
    lctns = get_locations(lines2)
    for lctn in lctns:
        locations.append(lctn)

    #     dts = re.findall(r'演出日期.*(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})|'
    #                      r'演出時間.*(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})|'
    #                      r'活動日期.*(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})|'
    #                      r'活動時間.*(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})|'
    #                      r'表演日期.*(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})|'
    #                      r'表演時間.*(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})|'
    #                      r'^時間.*(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})|'
    #                      r'^日期.*(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})|'
    #                      r'(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2}).*開演|'
    #                      r'(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2}).*加演', line)
    #     if dts:
    #         for i in range(0, len(dts[0]), 2):
    #             if dts[0][i]:
    #                 dates.append(datetime.strptime(dts[0][i], '%Y/%m/%d').date())
    #         for i in range(1, len(dts[0]), 2):
    #             if dts[0][i]:
    #                 times.append(datetime.strptime(dts[0][i], '%H:%M').time())
    # for i in range(len(dates)):
    #     performance_datetimes.append(datetime.combine(dates[i], times[i]))
    if performance_datetimes:
        print('round 2')
        while len(locations) > len(performance_datetimes):
            del locations[-1]
        # print(f'!!!!! 找到{len(performance_datetimes)}個表演時間 !!!!!')
        # for performance_datetime in performance_datetimes:
        #     print(performance_datetime)
        # print(f'!!!!! 找到{len(locations)}個地點 !!!!!')
        # for location in locations:
        #     print(location)
        # if len(locations) > 1:
        #     print('aaaa', locations)
        # if len(locations) > 1 and len(performance_datetimes) > 1 and len(locations) != len(performance_datetimes):
        if len(performance_datetimes) == len(locations) > 1:
            performance_datetimes, locations = sort_dts_lctns(performance_datetimes, locations)
        else:
            performance_datetimes = sort_datetime(performance_datetimes)
        print('1123', len(performance_datetimes), len(locations))
        # print(f'!!!!! 找到{len(performance_datetimes)}個表演時間 !!!!!')
        for performance_datetime in performance_datetimes:
            print(performance_datetime)
        # print(f'!!!!! 找到{len(locations)}個地點 !!!!!')
        for location in locations:
            print(location)
        print()
        return performance_datetimes, locations
    '--------------------------------------------------------------------'
    ''' 演出日期 
        2023/XX/XX XX:XX '''
    dt_lines = []
    locations = []
    for i, line in enumerate(lines):
        dts = re.findall(r'演出日期|'
                         r'演出時間|'
                         r'活動日期|'
                         r'活動時間|'
                         r'表演日期|'
                         r'表演時間|'
                         r'原場次|'
                         r'加\s*場|'
                         r'時\s*間|'
                         r'日\s*期', line)
        if dts:
            for j in range(i + 1, len(lines)):
                dts2 = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}', lines[j])
                if dts2:
                    # print('asd', lines[j])
                    dt_lines.append(lines[j])
                else:
                    break
    for dt_line in dt_lines:
        print('dt_line')
        for performance_datetime in get_all_performance_time_single_line(dt_line):
            performance_datetimes.append(performance_datetime)
    lctns = get_locations(lines2)
    for lctn in lctns:
        locations.append(lctn)
    if performance_datetimes:
        print('round 3')
        performance_datetimes = sort_datetime(performance_datetimes)
        print('1123', len(performance_datetimes), len(locations))
        # print(f'!!!!! 找到{len(performance_datetimes)}個表演時間 !!!!!')
        for performance_datetime in performance_datetimes:
            print(performance_datetime)
        # print(f'!!!!! 找到{len(locations)}個地點 !!!!!')
        for location in locations:
            print(location)
        # print(performance_datetimes)
        print()
        return performance_datetimes, locations
    '--------------------------------------------------------------------'
    ''' 演出日期: 2023/XX/XX 
        演出時間: XX:XX '''
    performance_time = get_start_time(lines)
    locations = []
    for line in lines:
        # dts = re.findall(r'演出日期.*\d{4}/\d{1,2}/\d{1,2}|'
        #                  r'演出時間.*\d{4}/\d{1,2}/\d{1,2}|'
        #                  r'活動日期.*\d{4}/\d{1,2}/\d{1,2}|'
        #                  r'活動時間.*\d{4}/\d{1,2}/\d{1,2}|'
        #                  r'表演日期.*\d{4}/\d{1,2}/\d{1,2}|'
        #                  r'表演時間.*\d{4}/\d{1,2}/\d{1,2}|'
        #                  r'原場次.*\d{4}/\d{1,2}/\d{1,2}|'
        #                  r'加\s*場.*\d{4}/\d{1,2}/\d{1,2}|'
        #                  r'時\s*間.*\d{4}/\d{1,2}/\d{1,2}\s*|'
        #                  r'日\s*期.*\d{4}/\d{1,2}/\d{1,2}\s*|'
        #                  r'\d{4}/\d{1,2}/\d{1,2}\s*.*開演|'
        #                  r'\d{4}/\d{1,2}/\d{1,2}\s*.*加演', line)
        dts = re.findall(r'演出日期\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}|'
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
        if dts:
            if performance_time != '00:00':
                for performance_datetime in get_all_performance_time_single_line(line):
                    print(performance_datetime.date())
                    print('有找到時間', performance_time)
                    performance_datetimes.append(datetime.combine(performance_datetime.date(), performance_time))
            else:
                for performance_datetime in get_all_performance_time_single_line(line):
                    print(performance_datetime.date())
                    print('沒有找到時間')
                    performance_datetimes.append(datetime.combine(performance_datetime.date(), time(0, 0)))
    lctns = get_locations(lines2)
    for lctn in lctns:
        locations.append(lctn)
    if performance_datetimes:
        print('round 4')
        performance_datetimes = list(set(performance_datetimes))
        print('1123', len(performance_datetimes), len(locations))
        # print(f'!!!!! 找到{len(performance_datetimes)}個表演時間 !!!!!')
        for performance_datetime in performance_datetimes:
            print(performance_datetime)
        for location in locations:
            print(location)
        print()
        return performance_datetimes, locations
    '--------------------------------------------------------------------'
    ''' 只有單行出現日期或是時間 '''
    dts_lines = []
    locations = []
    for line in lines:
        dts = re.findall(r'\d{4}/\d{1,2}/\d{1,2}|\d{1,2}:\d{2}', line)
        if dts:
            dts_lines.append(line)
    if len(dts_lines) == 1:
        for performance_datetime in get_all_performance_time_single_line(dts_lines[0]):
            performance_datetimes.append(performance_datetime)
    lctns = get_locations(lines2)
    for lctn in lctns:
        locations.append(lctn)
    if performance_datetimes:
        print('round 5')
        performance_datetimes = list(set(performance_datetimes))
        print('1123', len(performance_datetimes), len(locations))
        # print(f'!!!!! 找到{len(performance_datetimes)}個表演時間 !!!!!')
        for performance_datetime in performance_datetimes:
            print(performance_datetime)
        for location in locations:
            print(location)
        print()
        return performance_datetimes, locations
    '--------------------------------------------------------------------'
    ''' 日期只有出現一次'''
    performance_time = get_start_time(lines)
    locations = []
    ds = []
    for line in lines:
        dts = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', line)
        if dts:
            for dt in dts:
                try:
                    ds.append(datetime.strptime(dt, '%Y/%m/%d').date())
                except:
                    pass
    ds = list(set(ds))
    lctns = get_locations(lines2)
    for lctn in lctns:
        locations.append(lctn)
    if len(ds) == 1:
        if performance_time != '00:00':
            performance_datetimes.append(datetime.combine(ds[0], performance_time))
        else:
            performance_datetimes.append(datetime.combine(ds[0], time(0, 0)))
    if performance_datetimes:
        print('round 6')
        performance_datetimes = list(set(performance_datetimes))
        # print(f'!!!!! 找到{len(performance_datetimes)}個表演時間 !!!!!')
        print('1123', len(performance_datetimes), len(locations))
        for performance_datetime in performance_datetimes:
            print(performance_datetime)
        for location in locations:
            print(location)
        print()
        return performance_datetimes, locations
    '--------------------------------------------------------------------'
    if not performance_datetimes:
        print('z2')
    if not locations:
        print('z3')
    print('nothing')
    return performance_datetimes, locations
    # dts = re.findall(r'演出時間[及時間]?|'
    #                  r'演出日期[及時間]?|'
    #                  r'活動時間[及時間]?|'
    #                  r'活動日期[及時間]?|'
    #                  r'表演時間[及時間]?|'
    #                  r'表演日期[及時間]?|'
    #                  r'^時間|'
    #                  r'^日期|'
    #                  r'加演', line)
    # contain_numbers = re.findall(r'\d{3,6}', line)
    # if dts and contain_numbers:

    # date_untils = re.findall(dp, line)
    #
    # if date_untils:
    #     print('found until', line)
    #     start_date = datetime.strptime(date_untils[0][0], "%Y/%m/%d")
    #     end_date = datetime.strptime(date_untils[0][1], "%Y/%m/%d")
    #     time_str = re.findall(tp, line)
    #     if time_str:
    #         time_obj = datetime.strptime(time_str[0], "%H:%M").time()
    #     else:
    #         time_obj = time(0, 0)
    #
    #     dates = []
    #     current_date = start_date
    #
    #     while current_date <= end_date:
    #         dates.append(current_date.strftime("%Y/%m/%d"))
    #         current_date += timedelta(days=1)
    #
    #     date_objs = [datetime.strptime(date, "%Y/%m/%d").date() for date in dates]
    #     datetime_objs = [datetime.combine(date_obj, time_obj) for date_obj in date_objs]
    #     for datetime_obj in datetime_objs:
    #         performance_datetimes.append(datetime_obj)
    #     # print(performance_dates)
    #     return performance_datetimes, locations

    # performance_datetimes = []
    # locations = []
    # delete_lines = []
    # for line in lines:
    #     dts_lctns = re.findall(r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*([台臺]北[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*([台臺]中[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*([台臺]南[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*([台臺]東[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(新北[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(基隆[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(桃園[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(新竹[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(宜蘭[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(苗栗[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(彰化[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(南投[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(雲林[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(高雄[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(嘉義[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(屏東[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(澎湖[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(花蓮[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(綠島[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(金門[站]?\s*.*)$", line)
    #     if dts_lctns:
    #         delete_lines.append(line)
    #         # 加入 locations
    #         for i in range(1, len(dts_lctns[0]), 2):
    #             if dts_lctns[0][i]:
    #                 location = dts_lctns[0][i]
    #                 location = location.replace('\xa0', '')
    #                 locations.append(location)
    #         # 加入performance_datetimes
    #         for i in range(0, len(dts_lctns[0]), 2):
    #             if dts_lctns[0][i]:
    #                 # xxxx/xx/xx xx:xx (有找到時間)
    #                 if ':' in dts_lctns[0][i]:
    #                     performance_datetimes.append(datetime.strptime(dts_lctns[0][i], '%Y/%m/%d %H:%M'))
    #                 # xxxx/xx/xx 00:00 (沒有找到時間)
    #                 else:
    #                     performance_datetimes.append(datetime.combine(datetime.strptime(dts_lctns[0][i], '%Y/%m/%d').date(), time(0, 0)))
    # if performance_datetimes and locations and delete_lines:
    #     print('ab', performance_datetimes)
    #     print('cd', locations)
    #     print('ef', delete_lines)
    #     return performance_datetimes, locations, delete_lines
    # else:
    #     pass


# main chage order
def get_dts_lctns2(lines, lines2):
    performance_datetimes = []
    locations = []
    # dp = r"(\d{4}/\d{1,2}/\d{1,2})\s*~\s*(\d{4}/\d{1,2}/\d{1,2})"
    # tp = r"\d{4}/\d{1,2}/\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}\s*(\d{1,2}:\d{2})"
    ''' test '''
    for line in lines:
        whatevers = re.findall(r'\d{4}/\d{1,2}/\d{1,2}|\d{1,2}:\d{2}', line)
        if whatevers:
            print('w', line)
    '--------------------------------------------------------------------'
    ''' 演出日期 2023/XX/XX XX:XX '''
    dt_lines = []
    locations = []
    for i, line in enumerate(lines):
        # dts = re.findall(r'演出日期.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'演出時間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'活動日期.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'活動時間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'表演日期.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'表演時間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'原場次.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'加\s*場.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'時\s*間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'日\s*期.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}.*開演|'
        #                  r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}.*加演', line)
        # dts = re.findall(r'演出日期\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'演出時間\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'活動日期\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'活動時間\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'表演日期\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'表演時間\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'原場次\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'加\s*場\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'時\s*間\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'日\s*期\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
        #                  r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}\s*[:]?\s*開演|'
        #                  r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}\s*[:]?\s*加演', line)
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
        if dts:
            dt_lines.append(lines[i])
            for j in range(i + 1, len(lines)):
                dts2 = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}', lines[j])
                if dts2:
                    print('asd', lines[j])
                    dt_lines.append(lines[j])
                else:
                    break
    for dt_line in dt_lines:
        # print('dt_line')
        for performance_datetime in get_all_performance_time_single_line(dt_line):
            performance_datetimes.append(performance_datetime)
    lctns = get_locations(lines2)
    for lctn in lctns:
        locations.append(lctn)
    if performance_datetimes:
        print('kuan1: 演出日期 2023/XX/XX XX:XX')
        while len(locations) > len(performance_datetimes):
            del locations[-1]
        # print(f'!!!!! 找到{len(performance_datetimes)}個表演時間 !!!!!')
        # for performance_datetime in performance_datetimes:
        #     print(performance_datetime)
        # print(f'!!!!! 找到{len(locations)}個地點 !!!!!')
        # for location in locations:
        #     print(location)
        # if len(locations) > 1:
        #     print('aaaa', locations)
        # if len(locations) > 1 and len(performance_datetimes) > 1 and len(locations) != len(performance_datetimes):
        if len(performance_datetimes) == len(locations) > 1:
            performance_datetimes, locations = sort_dts_lctns(performance_datetimes, locations)
        else:
            performance_datetimes = sort_datetime(performance_datetimes)
        print('1123', len(performance_datetimes), len(locations))
        # print(f'!!!!! 找到{len(performance_datetimes)}個表演時間 !!!!!')
        for performance_datetime in performance_datetimes:
            print(performance_datetime)
        # print(f'!!!!! 找到{len(locations)}個地點 !!!!!')
        for location in locations:
            print(location)
        print()
        return performance_datetimes, locations
    '--------------------------------------------------------------------'
    ''' 演出日期 
        2023/XX/XX XX:XX '''
    dt_lines = []
    locations = []
    for i, line in enumerate(lines):
        dts = re.findall(r'演出日期|'
                         r'演出時間|'
                         r'活動日期|'
                         r'活動時間|'
                         r'表演日期|'
                         r'表演時間|'
                         r'原場次|'
                         r'加\s*場|'
                         r'時\s*間|'
                         r'日\s*期', line)
        if dts:
            for j in range(i + 1, len(lines)):
                dts2 = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}', lines[j])
                if dts2:
                    # print('asd', lines[j])
                    dt_lines.append(lines[j])
                else:
                    break
    for dt_line in dt_lines:
        print('dt_line')
        for performance_datetime in get_all_performance_time_single_line(dt_line):
            performance_datetimes.append(performance_datetime)
    lctns = get_locations(lines2)
    for lctn in lctns:
        locations.append(lctn)
    if performance_datetimes:
        print('kuan1: 演出日期')
        print('kuan1: 2023/XX/XX XX:XX')
        performance_datetimes = sort_datetime(performance_datetimes)
        print('1123', len(performance_datetimes), len(locations))
        # print(f'!!!!! 找到{len(performance_datetimes)}個表演時間 !!!!!')
        for performance_datetime in performance_datetimes:
            print(performance_datetime)
        # print(f'!!!!! 找到{len(locations)}個地點 !!!!!')
        for location in locations:
            print(location)
        # print(performance_datetimes)
        print()
        return performance_datetimes, locations
    '--------------------------------------------------------------------'
    ''' 演出日期: 2023/XX/XX 
        演出時間: XX:XX '''
    performance_time = get_start_time(lines)
    locations = []
    for line in lines:
        # dts = re.findall(r'演出日期.*\d{4}/\d{1,2}/\d{1,2}|'
        #                  r'演出時間.*\d{4}/\d{1,2}/\d{1,2}|'
        #                  r'活動日期.*\d{4}/\d{1,2}/\d{1,2}|'
        #                  r'活動時間.*\d{4}/\d{1,2}/\d{1,2}|'
        #                  r'表演日期.*\d{4}/\d{1,2}/\d{1,2}|'
        #                  r'表演時間.*\d{4}/\d{1,2}/\d{1,2}|'
        #                  r'原場次.*\d{4}/\d{1,2}/\d{1,2}|'
        #                  r'加\s*場.*\d{4}/\d{1,2}/\d{1,2}|'
        #                  r'時\s*間.*\d{4}/\d{1,2}/\d{1,2}\s*|'
        #                  r'日\s*期.*\d{4}/\d{1,2}/\d{1,2}\s*|'
        #                  r'\d{4}/\d{1,2}/\d{1,2}\s*.*開演|'
        #                  r'\d{4}/\d{1,2}/\d{1,2}\s*.*加演', line)
        dts = re.findall(r'演出日期\s*[:]?\s*\d{4}/\d{1,2}/\d{1,2}|'
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
        if dts:
            if performance_time != '00:00':
                for performance_datetime in get_all_performance_time_single_line(line):
                    print(performance_datetime.date())
                    print('有找到時間', performance_time)
                    performance_datetimes.append(datetime.combine(performance_datetime.date(), performance_time))
            else:
                for performance_datetime in get_all_performance_time_single_line(line):
                    print(performance_datetime.date())
                    print('沒有找到時間')
                    performance_datetimes.append(datetime.combine(performance_datetime.date(), time(0, 0)))
    lctns = get_locations(lines2)
    for lctn in lctns:
        locations.append(lctn)
    if performance_datetimes:
        print('kuan1: 演出日期: 2023/XX/XX')
        print('kuan1: 演出時間: XX:XX')
        performance_datetimes = list(set(performance_datetimes))
        print('1123', len(performance_datetimes), len(locations))
        # print(f'!!!!! 找到{len(performance_datetimes)}個表演時間 !!!!!')
        for performance_datetime in performance_datetimes:
            print(performance_datetime)
        for location in locations:
            print(location)
        print()
        return performance_datetimes, locations
    '--------------------------------------------------------------------'
    ''' xxxx/xx/xx xx:xx 城市 場館 '''
    dt_lines = []
    for line in lines:
        dtls = re.findall(r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*([台臺]北[站]?\s*.*)$|"
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
        # 表演日期與地點還沒有配對與排序
        if dtls:
            dt_lines.append(line)
            # 表演時間與場館 根據~有兩種處理方法
            if '~' in line:
                location = ''
                # 找到~之中的所有日期
                for dt_until in dt_untils(line):
                    performance_datetimes.append(dt_until)
                # 地點只會有一個 直接=第0個
                for i in range(len(dtls[0])):
                    lctns = re.findall(r'[\u4e00-\u9fff]{1,20}', dtls[0][i])
                    if lctns:
                        location = lctns[0].strip().replace(':', ' ').replace('/', ' ')
                # 地點只會有一個 把長度拉長到與表演時間相同
                for i in range(len(performance_datetimes)):
                    locations.append(location)
            else:
                # 場館
                for i in range(1, len(dtls[0]), 2):
                    if dtls[0][i]:
                        location = dtls[0][i].strip().replace(':', ' ').replace('/', ' ')
                        locations.append(location)
                # 表演時間
                for i in range(0, len(dtls[0]), 2):
                    if dtls[0][i]:
                        # xxxx/xx/xx xx:xx (有找到時間)
                        if ':' in dtls[0][i]:
                            performance_datetimes.append(datetime.strptime(dtls[0][i], '%Y/%m/%d %H:%M'))
                        # xxxx/xx/xx 00:00 (沒有找到時間)
                        else:
                            performance_datetimes.append(
                                datetime.combine(datetime.strptime(dtls[0][i], '%Y/%m/%d').date(), time(0, 0)))
    # print('測試')
    # print('測試', dt_lines)
    # print('測試', len(dt_lines))
    # print('測試', performance_datetimes)
    ''' 找到XXXX/XX/XX 城市 表演場館 可是沒有表演時間 所以我們要從內文當中尋找 XXXX/XX/XX XX:XX 表演時間 '''
    for i, performance_datetime in enumerate(performance_datetimes):
        if performance_datetime.hour == 0:
            for line in lines:
                start_times = re.findall(r'(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})', line)
                if start_times:
                    for j in range(len(start_times)):
                        p_date = datetime.strptime(start_times[j][0], '%Y/%m/%d').date()
                        p_time = datetime.strptime(start_times[j][1], '%H:%M').time()
                        if performance_datetime.date() == p_date:
                            performance_datetimes[i] = datetime.combine(p_date, p_time)
    # print('尋找時間1', performance_datetimes)
    ''' 對於只有一個表演時間的 那我們就找到表演時間之後補上 '''
    # if len(performance_datetimes) == 1:
    #     if performance_datetimes[0].hour == 0:
    #         start_time = get_start_time(lines)
    #         print('start_time', start_time)
    #         if start_time != '00:00':
    #             print('before', performance_datetimes[0])
    #             performance_datetimes[0] = datetime.combine(performance_datetimes[0].date(), start_time)
    #             print('after', performance_datetimes[0])
    if len(dt_lines) == 1:
        # print('only 1 line')
        start_time = get_start_time(lines)
        if start_time != '00:00':
            # print('find start time')
            for i, performance_datetime in enumerate(performance_datetimes):
                performance_datetimes[i] = datetime.combine(performance_datetime, start_time)
    # print('尋找時間2', performance_datetimes)
    if performance_datetimes:
        print('kuan1: xxxx/xx/xx xx:xx 城市 場館')
        performance_datetimes, locations = sort_dts_lctns(performance_datetimes, locations)
        # performance_datetimes = list(set(performance_datetimes))
        # print(f'!!!!! 找到{len(performance_datetimes)}個表演時間 !!!!!')
        print('1123', len(performance_datetimes), len(locations))
        for i in range(len(performance_datetimes)):
            print(performance_datetimes[i])
            print(locations[i])
        # for performance_datetime in performance_datetimes:
        #     print(performance_datetime)
        # for location in locations:
        #     print(location)
        # print(locations)
        print()
        return performance_datetimes, locations
    '--------------------------------------------------------------------'
    ''' 只有單行出現日期或是時間 '''
    dts_lines = []
    locations = []
    for line in lines:
        dts = re.findall(r'\d{4}/\d{1,2}/\d{1,2}|\d{1,2}:\d{2}', line)
        if dts:
            dts_lines.append(line)
    if len(dts_lines) == 1:
        for performance_datetime in get_all_performance_time_single_line(dts_lines[0]):
            performance_datetimes.append(performance_datetime)
    lctns = get_locations(lines2)
    for lctn in lctns:
        locations.append(lctn)
    if performance_datetimes:
        print('kuan1: 只有單行出現日期或是時間')
        performance_datetimes = list(set(performance_datetimes))
        print('1123', len(performance_datetimes), len(locations))
        # print(f'!!!!! 找到{len(performance_datetimes)}個表演時間 !!!!!')
        for performance_datetime in performance_datetimes:
            print(performance_datetime)
        for location in locations:
            print(location)
        print()
        return performance_datetimes, locations
    '--------------------------------------------------------------------'
    ''' 日期只有出現一次'''
    performance_time = get_start_time(lines)
    locations = []
    ds = []
    for line in lines:
        dts = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', line)
        if dts:
            for dt in dts:
                try:
                    ds.append(datetime.strptime(dt, '%Y/%m/%d').date())
                except:
                    pass
    ds = list(set(ds))
    lctns = get_locations(lines2)
    for lctn in lctns:
        locations.append(lctn)
    if len(ds) == 1:
        if performance_time != '00:00':
            performance_datetimes.append(datetime.combine(ds[0], performance_time))
        else:
            performance_datetimes.append(datetime.combine(ds[0], time(0, 0)))
    if performance_datetimes:
        print('kuan1: 日期只有出現一次')
        performance_datetimes = list(set(performance_datetimes))
        # print(f'!!!!! 找到{len(performance_datetimes)}個表演時間 !!!!!')
        print('1123', len(performance_datetimes), len(locations))
        for performance_datetime in performance_datetimes:
            print(performance_datetime)
        for location in locations:
            print(location)
        print()
        return performance_datetimes, locations
    '--------------------------------------------------------------------'
    if not performance_datetimes:
        print('z2')
    if not locations:
        print('z3')
    print('nothing')
    return performance_datetimes, locations
    # dts = re.findall(r'演出時間[及時間]?|'
    #                  r'演出日期[及時間]?|'
    #                  r'活動時間[及時間]?|'
    #                  r'活動日期[及時間]?|'
    #                  r'表演時間[及時間]?|'
    #                  r'表演日期[及時間]?|'
    #                  r'^時間|'
    #                  r'^日期|'
    #                  r'加演', line)
    # contain_numbers = re.findall(r'\d{3,6}', line)
    # if dts and contain_numbers:

    # date_untils = re.findall(dp, line)
    #
    # if date_untils:
    #     print('found until', line)
    #     start_date = datetime.strptime(date_untils[0][0], "%Y/%m/%d")
    #     end_date = datetime.strptime(date_untils[0][1], "%Y/%m/%d")
    #     time_str = re.findall(tp, line)
    #     if time_str:
    #         time_obj = datetime.strptime(time_str[0], "%H:%M").time()
    #     else:
    #         time_obj = time(0, 0)
    #
    #     dates = []
    #     current_date = start_date
    #
    #     while current_date <= end_date:
    #         dates.append(current_date.strftime("%Y/%m/%d"))
    #         current_date += timedelta(days=1)
    #
    #     date_objs = [datetime.strptime(date, "%Y/%m/%d").date() for date in dates]
    #     datetime_objs = [datetime.combine(date_obj, time_obj) for date_obj in date_objs]
    #     for datetime_obj in datetime_objs:
    #         performance_datetimes.append(datetime_obj)
    #     # print(performance_dates)
    #     return performance_datetimes, locations

    # performance_datetimes = []
    # locations = []
    # delete_lines = []
    # for line in lines:
    #     dts_lctns = re.findall(r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*([台臺]北[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*([台臺]中[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*([台臺]南[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*([台臺]東[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(新北[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(基隆[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(桃園[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(新竹[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(宜蘭[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(苗栗[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(彰化[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(南投[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(雲林[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(高雄[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(嘉義[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(屏東[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(澎湖[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(花蓮[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(綠島[站]?\s*.*)$|"
    #                            r"(\d{4}/\d{1,2}/\d{1,2}(?:\s*\d{1,2}:\d{2})?)\s*(金門[站]?\s*.*)$", line)
    #     if dts_lctns:
    #         delete_lines.append(line)
    #         # 加入 locations
    #         for i in range(1, len(dts_lctns[0]), 2):
    #             if dts_lctns[0][i]:
    #                 location = dts_lctns[0][i]
    #                 location = location.replace('\xa0', '')
    #                 locations.append(location)
    #         # 加入performance_datetimes
    #         for i in range(0, len(dts_lctns[0]), 2):
    #             if dts_lctns[0][i]:
    #                 # xxxx/xx/xx xx:xx (有找到時間)
    #                 if ':' in dts_lctns[0][i]:
    #                     performance_datetimes.append(datetime.strptime(dts_lctns[0][i], '%Y/%m/%d %H:%M'))
    #                 # xxxx/xx/xx 00:00 (沒有找到時間)
    #                 else:
    #                     performance_datetimes.append(datetime.combine(datetime.strptime(dts_lctns[0][i], '%Y/%m/%d').date(), time(0, 0)))
    # if performance_datetimes and locations and delete_lines:
    #     print('ab', performance_datetimes)
    #     print('cd', locations)
    #     print('ef', delete_lines)
    #     return performance_datetimes, locations, delete_lines
    # else:
    #     pass


# main
def get_locations(lines):
    locations = []
    for line in lines:
        lctns = re.findall(r"場｜(.*)$|地點\s*[／:｜|⎪](.*)$|場地[:](.*)$|場館名稱:(.*)$", line)
        if lctns:
            for i in range(len(lctns[0])):
                # if lctns[0][i] and '即將' not in lctns[0][i]:
                if lctns[0][i]:
                    locations.append(lctns[0][i].strip())
    return locations


# test
def print_file(index, mode):
    for i in range(index, index + 1):
        file = 'tindievox' + str(i) + '.txt'

        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            lines1 = lines
            lines1 = [line.strip() for line in lines1 if line.strip()]  # 不要空白行
            if mode == 'price':
                lines2 = prc_lines(lines)
            if mode == 'all':
                lines2 = al_lines(lines)

            for i, line1 in enumerate(lines1):
                for j, line2 in enumerate(lines2):
                    if i == j:
                        # numbers = re.findall(r'\d', line1)
                        # if numbers:
                        print(line1.replace('\n', ''))
                        print(line2.replace('\n', ''))
                        print()
    print('****************************************************************************************')


def single_duplicate(lsts):
    print('before lsts', lsts)
    if len(lsts) > 1:
        dif_lsts = list(set(lsts))
        if len(dif_lsts) == 1:
            lsts = list(set(lsts))
    print('after lsts', lsts)
    return lsts

# def get_performance_dts2(lines):
#     performance_datetimes = []
#     for line in lines:
#         dp = r"(\d{4}/\d{1,2}/\d{1,2})\s*~\s*(\d{4}/\d{1,2}/\d{1,2})"
#         tp = r"\d{4}/\d{1,2}/\d{1,2}\s*~\s*\d{4}/\d{1,2}/\d{1,2}\s*(\d{1,2}:\d{2})"
#         date_match = re.search(dp, line)
#         time_match = re.search(tp, line)
#
#         if not date_match:
#             continue
#         #     return get_all_performance_time_single_line2(line)
#
#         print('~~~')
#         if time_match:
#             time_str = time_match.group(1)
#             time_obj = datetime.strptime(time_str, "%H:%M").time()
#         else:
#             time_obj = time(0, 0)
#
#         # if date_match:
#         #     print('found', date_match.group(1))
#         #     print('found', date_match.group(2))
#         #     print('found', time_obj)  # datetime.time
#
#         start_date = datetime.strptime(date_match.group(1), "%Y/%m/%d")
#         end_date = datetime.strptime(date_match.group(2), "%Y/%m/%d")
#
#         dates = []
#         current_date = start_date
#
#         while current_date <= end_date:
#             dates.append(current_date.strftime("%Y/%m/%d"))
#             current_date += timedelta(days=1)
#
#         ''' datetime.date '''
#         date_objs = [datetime.strptime(date, "%Y/%m/%d").date() for date in dates]
#         print('dates', date_objs)
#         print('time', time_obj)
#
#         ''' datetime.datetime'''
#         datetime_objs = [datetime.combine(date_obj, time_obj) for date_obj in date_objs]
#         print('datetime_objs', datetime_objs)
#
#         for date_obj in date_objs:
#             performance_datetimes.append(date_obj)
#         return performance_datetimes

# def get_performance_dts(lines):
#     performance_datetimes = []
#     '''
#     '''
#
#     ''' 演出日期 2023/XX/XX XX:XX '''
#     for line in lines:
#         dts = re.findall(r'演出日期.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
#                          r'演出時間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
#                          r'表演時間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
#                          r'活動日期.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
#                          # r'(?<!索票)時間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
#                          # r'(?<!★)時間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
#                          r'^時間.*\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}|'
#                          r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}.*開演|'
#                          r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}.*加演', line)
#         if dts:
#             for i in range(len(dts)):
#                 try:
#                     dttms = get_all_performance_time_single_line(line)
#                     for dttm in dttms:
#                         if dttm not in performance_datetimes:
#                             performance_datetimes.append(dttm)
#                     # print(dttm)
#                 except Exception as e:
#                     print('發生錯誤 4', e)
#     if performance_datetimes:
#         return performance_datetimes
#     else:
#         '''
#         演出日期: 2023/XX/XX
#         演出時間: XX:XX
#         '''
#         single_dt = get_single_performance_datetime(lines)
#         if single_dt:
#             performance_datetimes.append(single_dt)
#         # print('lalala', performance_datetimes)
#     if performance_datetimes:
#         return performance_datetimes
#     else:
#         '''
#         演出日期
#         2023/XX/XX XX:XX
#         '''
#         performance_datetimes_lines = []
#         for i, line in enumerate(lines):
#             dts = re.findall(r'演出日期|演出時間|表演時間|活動日期|^時間|^日期|開演|加演', line)
#             if dts:
#                 for j in range(i + 1, len(lines)):
#                     dts = re.findall(r'\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}', lines[j])
#                     if dts:
#                         # print(lines[j])
#                         performance_datetimes_lines.append(lines[j])
#                     if not dts:
#                         break
#         for performance_datetimes_line in performance_datetimes_lines:
#             performance_dts = get_all_performance_time_single_line(performance_datetimes_line)
#             for performance_dt in performance_dts:
#                 performance_datetimes.append(performance_dt)
#     if performance_datetimes:
#         performance_datetimes = sort_datetime(performance_datetimes)
#         return performance_datetimes
#     else:
#         ''' 找不到 回傳空 '''
#         return performance_datetimes
#         # performance_datetimes = []
#         # for line in lines:
#         #     dts = re.findall(r'演出日期.*(\d{4}/\d{1,2}/\d{1,2})|'
#         #                      r'演出時間.*(\d{4}/\d{1,2}/\d{1,2})|'
#         #                      r'表演時間.*(\d{4}/\d{1,2}/\d{1,2})|'
#         #                      r'活動日期.*(\d{4}/\d{1,2}/\d{1,2})|'
#         #                      r'^時間.*(\d{4}/\d{1,2}/\d{1,2})|'
#         #                      r'(\d{4}/\d{1,2}/\d{1,2}).*開演|'
#         #                      r'(\d{4}/\d{1,2}/\d{1,2}).*加演', line)
#         #     if dts:
#         #         for i in range(len(dts[0])):
#         #             if dts[0][i]:
#         #                 performance_datetimes.append(dts[0][i])
#         # print('yoyo', performance_datetimes)
#
#         # if starts:
#         #     for i in range(len(starts[0])):
#         #         if starts[0][i]:
#         #             performance_time = starts[0][i]
#     # sell_times = re.findall(r'演出日期[及時間]?.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})+|'
#     #                         r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*開演|'
#     #                         r'', line)
#
#     # performance_datetimes = []
#     # for line in lines:
#     #     dts = re.findall(r"\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}", line)
#     #     if dts:
#     #         for dt in dts:
#     #             try:
#     #                 print(line)
#     #                 dttms = get_all_performance_time_single_line(dt)
#     #                 for dttm in dttms:
#     #                     if dttm not in performance_datetimes:
#     #                         performance_datetimes.append(dttm)
#     #                 # print(dttm)
#     #             except Exception as e:
#     #                 print('發生錯誤', e)
#     # return performance_datetimes
#     #         if sell_times:
#     #             for i in range(len(sell_times[0])):
#     #                 if sell_times[0][i]:
#     #                     # print(line)
#     #                     sell_lines.append(line)
#     #                     sell_dts.append(sell_times[0][i])
#     #     except Exception as e:
#     #         print('發生錯誤', e)
#     #         print()
#     #
#     # for sell_datetime in sell_dts:
#     #     dttms = get_all_performance_time_single_line(sell_datetime)
#     #     for dttm in dttms:
#     #         sell_datetimes.append(dttm)
#     #
#     # sell_datetimes = sort_datetime(sell_datetimes)
#     #
#     # return sell_datetimes, sell_lines


# def get_performance_datetime_single(lines):
#     performance_time = ''
#     performance_dates = []
#     for line in lines:
#         starts = re.findall(r'開演:(\d{1,2}:\d{2})|'
#                             r'(\d{1,2}:\d{2})開演|'
#                             r'begin\s*(\d{1,2}:\d{2})|'
#                             r'演出\s*(\d{1,2}:\d{2})|'
#                             r'演出時間:(\d{1,2}:\d{2})|'
#                             r'(\d{1,2}:\d{2})\s*開始|'
#                             r'活動開始時間:(\d{1,2}:\d{2})|'
#                             r'start\s*(\d{1,2}:\d{2})|'
#                             r'(\d{1,2}:\d{2})\s*start.', line)
#         if starts:
#             # for start in starts:
#             for i in range(len(starts[0])):
#                 # print(i, starts[0][i])
#                 if starts[0][i]:
#                     performance_time = starts[0][i]
#
#         performance_dts = re.findall(r"\d{4}/\d{1,2}/\d{1,2}", line)
#         if performance_dts:
#             for performance_dt in performance_dts:
#                 try:
#                     dt = datetime.strptime(performance_dt, "%Y/%m/%d").date()
#                     if dt.year >= 2023 and dt not in performance_dates:
#                         performance_dates.append(dt)
#                 except:
#                     pass
#         if len(performance_dates) == 1 and performance_time:
#             return datetime.combine(performance_dates[0], datetime.strptime(performance_time, "%H:%M").time())
#             # performance_datetimes.append(datetime.combine(performance_dates[0], datetime.strptime(performance_time, "%H:%M").time()))

# avoids = ['來回票', '身障', '售完', '福利', '退票', '舉辦', '截止', '抽獎']


# def get_sell_datetimes(lines):
#     sell_datetimes = []
#     sell_lines = []
#     for line in lines:
#         try:
#             # sell_times = re.findall(r'.*啟售時間\s*[:｜⎪]\s*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#             #                         r'.*售票日期\s*[:｜⎪]\s*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#             #                         r'.*售票時間\s*[:｜⎪]\s*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#             #                         r'.*正式啟售\s*:\s*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#             #                         r'.*全面啟售\s*:\s*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#             #                         r'.*全區售票\s*:\s*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#             #                         r'.*優先購\s*:\s*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#             #                         r'.*加開.*[:｜⎪].*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#             #                         r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*[販啟銷]售|'
#             #                         r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*開賣|'
#             #                         r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*售票|'
#             #                         r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*選位|'
#             #                         r'', line)
#             sell_times = re.findall(r'啟售時間.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#                                     r'售票日期.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#                                     r'售票時間.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#                                     r'正式啟售.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#                                     r'全面啟售.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#                                     r'全區售票.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#                                     r'開賣時間.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#                                     r'優先購.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#                                     r'加開.*(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2})|'
#                                     r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*[販啟銷]售|'
#                                     r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*開賣|'
#                                     r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*售票|'
#                                     r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*選位|'
#                                     r'(\d{4}/\d{1,2}/\d{1,2}\s*\d{1,2}:\d{2}).*加開|'
#                                     r'', line)
#             if '購' in line or '售' in line or '賣' in line or '選' in line or '索票' in line:
#                 # if '售完' in line\
#                 # or '福利' in line or '退票' in line or '舉辦' in line\
#                 # or '截止' in line or '抽獎' in line or '出道' in line\
#                 # or '搖滾' in line or '單日' in line or '註冊' in line\
#                 # or '成年' in line or '來自' in line:
#                 #     continue
#                 dttms = get_all_performance_time_single_line(line)
#                 if dttms:
#                     print(line)
#                     sell_lines.append(line)
#                     for dttm in dttms:
#                         sell_datetimes.append(dttm)
#         except Exception as e:
#             print('發生錯誤', e)
#             print()
#
#     sell_datetimes = sort_datetime(sell_datetimes)
#
#     return sell_datetimes, sell_lines

# def change_time(line):
#     ''' 先把特殊文字轉換 '''
#     line = convert_special_font(line)
#     ''' 不要括號內容 '''
#     line = re.sub(r"[\(（][^)）]+[\)）]", " ", line)  # 不要括號內容
#     ''' / 左右不要有空格 '''
#     line = re.sub(r"\s*/\s*", "/", line)
#     ''' : 左右不要有空格 '''
#     line = re.sub(r"\s*:\s*", ':', line)
#     ''' ~ 的轉換 '''
#     line = re.sub(r"：", ':', line)
#     line = re.sub(r"～", '~', line)
#     line = re.sub(r"-", '~', line)
#     line = re.sub(r"－", '~', line)
#     line = re.sub(r"–", '~', line)
#     line = re.sub(r"\s*~\s*", " ~ ", line)
#     ''' xx月xx號(日) 轉換成 xxxx/xx/xx'''
#     line = re.sub(r"(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*[日號]", r"\1/\2/\3 ", line)
#     line = re.sub(r"(\d{4})\s*.\s*(\d{1,2})\s*.\s*(\d{1,2})", r"\1/\2/\3 ", line)
#     line = re.sub(r"(\d{1,2})\s*[.月]\s*(\d{1,2})\s*[日號]?", r"\1/\2 ", line)
#     ''' xxxx/xx/xx Mon. xx:xx start '''
#     line = re.sub(r'\s*?([A-Za-z]{3}\.\s*?)', ' ', line)
#     ''' 中文 轉換 數字型態 '''
#     line = re.sub(r"中午", "", line)
#     line = re.sub(r"下午\s*(\d{1,2})\s*點", replace_chinese, line)
#     line = re.sub(r"晚上\s*(\d{1,2})\s*點", replace_chinese, line)
#     line = re.sub(r"下午\s*(\d{1,2})\s*點", r"\1:00", line)
#     line = re.sub(r"晚上\s*(\d{1,2})\s*點", r"\1:00", line)
#     line = re.sub(r"上午\s*(\d{1,2})\s*點", r"\1:00", line)
#     ''' 英文 轉換 數字型態 '''
#     line = re.sub(r"p.m.", 'pm', line)
#     line = re.sub(r"P.M.", 'pm', line)
#     line = re.sub(r"PM", 'pm', line)
#     line = re.sub(r"a.m.", 'am', line)
#     line = re.sub(r"A.M.", 'am', line)
#     line = re.sub(r"AM", 'am', line)
#     line = re.sub(r"(\d{1,2})(?::(\d{2}))?\s*([ap]m)", replace_english, line)
#     ''' 再次確認 '''
#     ''' / 左右不要有空格 '''
#     line = re.sub(r"\s*/\s*", "/", line)
#     ''' : 左右不要有空格 '''
#     line = re.sub(r"\s*:\s*", ':', line)
#     ''' ~ 的轉換 '''
#     line = re.sub(r"\s*~\s*", " ~ ", line)
#     ''' 兩個空格以上都變成單個 '''
#     line = re.sub(r"\s{2,}", " ", line)
#     ''' xx:xx (~ xx:xx) 括號的時間都刪除 '''
#     line = re.sub(r"(\d{1,2}):\d{2}\s*~\s*\d{1,2}:\d{2}", r"\1:00", line)
#     ''' 把沒有年份的都補上年份 '''
#     line = re.sub(r"\d{4}/\d{1,2}/\d{1,2}|\d{1,2}/\d{1,2}", add_year, line)
#     ''' xxxx/xx/xx xx:xx ~ xxxx/xx/x(x+0 or x+1) 刪除~之後的 版本1 '''
#     # line = re.sub(r"(\d{4}/\d{1,2}/\d{1,2})\s*\d{1,2}:\d{2}\s*~\s*(\d{4}/\d{1,2}/\d{1,2})\s*\d{1,2}:\d{2}", adjacent_date, line)
#     ''' xxxx/xx/xx xx:xx ~ xxxx/xx/xx 相差24小時 對字串做處理 版本2 '''
#     line = re.sub(r"(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})\s*~\s*(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})",
#                   adjacent_date, line)
#     ''' 不要加價購 '''
#     # line = re.sub(r'\+.*?元|\+.*?\$\d{3,5}', "", line)
#     ''' 價格不要有, '''
#     # line = re.sub(r",(\d{3})", r"\1", line)
#     ''' 不要進場時間 '''
#     # line = re.sub(r"\d{2}:\d{2}\s?[入進][場站]|[入進]場\d{2}:\d{2}\s?|[入進]場.*\d{2}:\d{2}|\d{2}:\d{2}\s?Open|Open\d{2}:\d{2}\s?","", line)  # 不要進場的時間
#
#     return line


# line = "2023/7/8 23:00 ~ 2023/7/9 11:00"
# pattern_w_year = r"(\d{4}/\d{1,2}/\d{1,2})\s*\d{1,2}:\d{2}\s*~\s*(\d{4}/\d{1,2}/\d{1,2})\s*\d{1,2}:\d{2}"

# 補年分
# p = r"\d{4}/\d{1,2}/\d{1,2}|\d{1,2}/\d{1,2}"
# dates = re.findall(p, line)
# for i, date in enumerate(dates):
#     if len(date) < 6:
#         line = line.replace(date, '2023/' + date)
#         # dates[i] = '2023/' + date
# print(line)

# ''' 版本1 '''
# def adjacent_date(match):
#     start_date_str = match.group(1)
#     end_date_str = match.group(2)
#
#     start_date = datetime.strptime(start_date_str, "%Y/%m/%d")
#     end_date = datetime.strptime(end_date_str, "%Y/%m/%d")
#
#     if (end_date - start_date == timedelta(days=1)) or (end_date - start_date == timedelta(days=0)):
#         return match.group(0)[:match.group(0).index(' ~ ')]
#     else:
#         return match.group(0)

# ''' 版本2 not function'''
# a = re.search(r"(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})\s*~\s*(\d{4}/\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})", line)
# if a:
#     print(a.group(0))
#     print(a.group(1))
#     print(a.group(2))
#     print(a.group(3))
#     print(a.group(4))
#     start_date_str = a.group(1)
#     performance_time_str = a.group(2)
#     end_date_str = a.group(3)
#     end_time_str = a.group(4)
#     start_datetime_str = start_date_str + " " + performance_time_str
#     end_datetime_str = end_date_str + " " + end_time_str
#     start_datetime = datetime.strptime(start_datetime_str, "%Y/%m/%d %H:%M")
#     end_datetime = datetime.strptime(end_datetime_str, "%Y/%m/%d %H:%M")
#     time_difference = end_datetime - start_datetime
#     print('time_difference', time_difference)
#     if time_difference.total_seconds() < 24 * 3600:
#         print('< 24 hours')
#         line = start_date_str + ' ' + performance_time_str
#         # line = line[:line.index(' ~ ')]
#     else:
#         print('> 24 hours')
#         line = start_date_str + ' ~ ' + end_date_str + ' ' + performance_time_str
#         # line = line[:line.index(end_time_str)]
#     print(line)


# ''' 版本2 '''
# def adjacent_date(match):
#     start_date_str = match.group(1)
#     performance_time_str = match.group(2)
#     end_date_str = match.group(3)
#     end_time_str = match.group(4)
#
#     performance_time = datetime.strptime(performance_time_str, "%H:%M").time()
#     end_time = datetime.strptime(end_time_str, "%H:%M").time()
#     print('performance_time', performance_time)
#     print('end_time', end_time)
#
#     if performance_time < end_time:
#         start_datetime_str = start_date_str + " " + performance_time_str
#         end_datetime_str = end_date_str + " " + end_time_str
#
#         start_datetime = datetime.strptime(start_datetime_str, "%Y/%m/%d %H:%M")
#         end_datetime = datetime.strptime(end_datetime_str, "%Y/%m/%d %H:%M")
#         time_difference = end_datetime - start_datetime
#
#         if time_difference.total_seconds() < 24 * 3600:
#             return start_date_str + ' ' + performance_time_str
#         else:
#             return start_date_str + ' ~ ' + end_date_str + ' ' + performance_time_str
#     else:
#         start_datetime_str = start_date_str + " " + performance_time_str
#         end_datetime_str = end_date_str + " " + end_time_str
#
#         start_datetime = datetime.strptime(start_datetime_str, "%Y/%m/%d %H:%M")
#         end_datetime = datetime.strptime(end_datetime_str, "%Y/%m/%d %H:%M")
#         time_difference = end_datetime - start_datetime
#
#         previous_day = datetime.strptime(end_date_str, "%Y/%m/%d") - timedelta(days=1)
#         end_date_str = str(previous_day.year) + '/' + str(previous_day.month) + '/' + str(previous_day.day)
#
#         if time_difference.total_seconds() < 24 * 3600:
#             return start_date_str + ' ' + performance_time_str
#         else:
#             return start_date_str + ' ~ ' + end_date_str + ' ' + performance_time_str

# ''' 版本2 縮減版 '''
# def sort_dts_lctns(performance_datetimes, locations):
#     print('bef1', performance_datetimes)
#     print('bef1', locations)
#     dts_lctns = list(set(list(zip(performance_datetimes, locations))))
#     print('dts_lctns', dts_lctns)
#     for dt_lctn in dts_lctns:
#         print('dt_lctn', dt_lctn)
#     sorted_events = sorted(dts_lctns, key=lambda x: x[0])
#     performance_datetimes = []
#     locations = []
#     sorted_performance_datetimes, sorted_locations = list(zip(*sorted_events))
#     for sorted_performance_datetime in sorted_performance_datetimes:
#         performance_datetimes.append(sorted_performance_datetime)
#     for sorted_location in sorted_locations:
#         locations.append(sorted_location)
#     print('aft1', performance_datetimes)
#     print('aft1', locations)
#     return performance_datetimes, locations
