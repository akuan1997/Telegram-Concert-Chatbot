from playwright.sync_api import sync_playwright, Playwright, expect, Page
import json
import os
import threading
import shutil
import re
import sys
from datetime import datetime, time
from googletrans import Translator
from get_data_from_text import *


def write_data_json(json_name, new_data):
    # json檔案不存在或是裡面沒資料
    if not os.path.exists(json_name) or os.path.getsize(json_name) <= 4:
        # 直接寫入第一筆資料
        with open(json_name, "w", encoding="utf-8") as f:
            json.dump([new_data], f, indent=4, ensure_ascii=False)
    # json檔案存在且裡面已經有一筆以上的資料
    else:
        # 讀取現在有的檔案
        with open(json_name, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
        # 並新增即將寫入的一筆
        existing_data.append(new_data)
        # 寫入
        with open(json_name, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)


def write_error(website, url, error):
    with open('failure_log.txt', "r", encoding="utf-8") as f:
        lines = f.readlines()

    if url + '\n' not in lines:
        # txt檔案不存在或是裡面沒資料
        if not os.path.exists('failure_log.txt') or os.path.getsize('failure_log.txt') <= 4:
            # 直接寫入第一筆資料
            with open('failure_log.txt', "w", encoding="utf-8") as f:
                f.write(f'{website}\n{error}\n{url}\n')
        # txt檔案存在且裡面已經有一筆以上的資料
        else:
            # 讀取現在有的檔案
            with open('failure_log.txt', "a", encoding="utf-8") as f:
                f.write(f'\n{website}\n{error}\n{url}\n')
    else:
        print('已經寫進錯誤裡面了!')


def delete_blank_sdt(website, json_name):
    '''
        "sdt": [
            ""
        ],
        清空 讓他變成
        "sdt": [],
    '''
    print(f'準備清空{website}的空白sdt!')
    with open(json_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for i in range(len(data)):
        # 如果含有售票時間
        if data[i]['sdt']:
            sdts = [sdt for sdt in data[i]['sdt'] if sdt != '']
            data[i]['sdt'] = sdts
            with open(json_name, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
    print(f'{website}當中空白的sdt清空完成!')


def delete_past_ticketing_time(website, json_filename):
    print(f'準備刪除{website}中sdt為過去的時間')
    # 刪除時間已經過去的售票時間
    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i in range(len(data)):
        # print('i =', i)
        # 如果含有售票時間
        if data[i]['sdt']:
            # 就把所有的售票時間都轉換成datetime object
            sdt_objs = [datetime.strptime(sdt, '%Y/%m/%d %H:%M') for sdt in data[i]['sdt']]
            # 只儲存尚未售票的時間
            future_datetimes = []
            for sdt_obj in sdt_objs:
                # 如果是未來
                if sdt_obj > datetime.now():
                    # print('future', str(sdt_obj)[:-3].replace('-', '/'))
                    # 就加入list裡面
                    future_datetimes.append(str(sdt_obj)[:-3].replace('-', '/'))
            # print('future_datetimes', future_datetimes)
            # 更改售票時間
            data[i]['sdt'] = future_datetimes
            # 寫入檔案
            with open(json_filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
    print(f'{website}中sdt為過去的時間都刪除了!')


def get_era(website, json_filename, txt_filename):
    with sync_playwright() as p:

        with open(json_filename, 'w', encoding='utf-8') as f:
            f.write('')

        # 待會會從 last_finished_index + 1開始
        last_finished_index = -1
        # 錯誤的網址
        fail_urls = []

        while True:
            try:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                page.set_default_timeout(10000)

                page.goto("https://ticket.com.tw/application/UTK01/UTK0101_06.aspx?TYPE=1&CATEGORY=205")

                # 獲得events物件以及數量 (有幾個活動)
                events = page.query_selector_all(".column.col-xs-12.col-md-3.moreBox")

                for i in range(last_finished_index + 1, len(events)):
                    print(f'{website} progress - {i + 1}/{len(events)}')
                    # 資訊頁面
                    events[i].click()

                    ''''''

                    # 內文
                    inner_text = page.locator("#ctl00_ContentPlaceHolder1_lbProgramInfo_Content").inner_text()

                    ''''''

                    page.locator("#ctl00_ContentPlaceHolder1_btnBuyNow").click()  # 進入售票頁面
                    page.wait_for_timeout(1500)

                    # 標題
                    title = page.locator("#ctl00_ContentPlaceHolder1_NAME").inner_text()

                    for j in range(len(page.query_selector_all(
                            "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr"))):  # 資訊方塊
                        # 表演日期
                        # 日期格式1
                        if page.locator(
                                "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                            j).locator("td > div > span > time").is_visible():
                            year_month = page.locator(
                                "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                                j).locator("td > div > span > time > strong").inner_text().replace(' - ',
                                                                                                   '/')
                            day = page.locator(
                                "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                                j).locator("td > div > span > time > span").nth(
                                0).inner_text()
                            t = page.locator(
                                "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                                j).locator(
                                "td > div > span > time > span").nth(1).inner_text()
                            performance_datetime = year_month + '/' + day + ' ' + t
                            print()
                        # 日期格式2
                        else:
                            # 1. 獲得日期 格式為 YYYY/MM/DD HH:MM
                            performance_datetime = page.locator(
                                "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                                j).locator(
                                "td > div > span").nth(0).inner_text() + ' ~ ' + page.locator(
                                "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                                j).locator(
                                "td > div > span").nth(1).inner_text().replace('|', '').replace('\n', '')
                            print()

                        ''''''

                        # 地點
                        location = page.locator(
                            "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                            j).locator(
                            "td").nth(1).locator("span").inner_text()

                        ''''''

                        # 票價
                        prices = []
                        prcs = page.locator(
                            "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                            j).locator(
                            "td").nth(2).locator("span").inner_text().split('、')
                        for prc in prcs:
                            prices.append(int(prc))  # 票價列表

                        ''''''

                        # 售票時間 (如果沒有售票時間，列表為空)
                        sell_button = page.locator(
                            "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                            j).locator("td").nth(3).inner_text()
                        if '尚未開賣' in sell_button:
                            sell_d = re.findall(r"\d{4}/\d{1,2}/\d{1,2}", sell_button)
                            sell_t = re.findall(r"\d{1,2}:\d{2}", sell_button)
                            sell_datetime = sell_d[0] + ' ' + sell_t[0]
                            print('尚未開賣', sell_datetime)
                        else:
                            sell_datetime = ''

                        ''''''

                        print('tit', title)
                        print('sdt', sell_datetime)  # str
                        print('prc', prices)  # list
                        print('pdt', performance_datetime)  # str
                        print('loc', location)  # str

                        # 新的一筆資料
                        new_data = {
                            'tit': title,
                            'sdt': [sell_datetime],
                            'prc': prices,
                            'pdt': [performance_datetime],
                            'loc': [location],
                            'int': inner_text,
                            'web': f'{website}',
                            'url': page.url
                        }

                        print('\n--- write new data ---\n')

                        write_data_json(json_filename, new_data)

                        last_finished_index = i
                        if page.url in fail_urls:
                            del fail_urls[fail_urls.index(page.url)]

                    # 資訊頁面
                    page.go_back()

                    # 主頁面
                    page.go_back()

                    # 重新獲取events屬性
                    events = page.query_selector_all(".column.col-xs-12.col-md-3.moreBox")

                # 完成
                page.close()

                delete_blank_sdt(website, json_filename)

                print(f'{website} done')
                break

            except Exception as e:
                # 錯誤
                print(e, f'{website} restart')
                print('last finished index = ', last_finished_index)

                if page.url == "https://ticket.com.tw/application/UTK01/UTK0101_06.aspx?TYPE=1&CATEGORY=205":
                    print(f'是{website}的主頁，沒關係的!')
                else:
                    if page.url not in fail_urls:
                        print('第一次失敗')
                        fail_urls.append(page.url)
                    else:
                        print('第二次失敗')
                        print('跳過')
                        last_finished_index += 1

                        write_error(website, page.url, e)

                # 重新啟動
                continue


def get_livenation(website, json_filename, txt_filename):
    with sync_playwright() as p:

        with open(json_filename, 'w', encoding='utf-8') as f:
            f.write('')

        # 待會會從 last_finished_index + 1開始
        last_finished_index = -1
        # 錯誤的網址
        fail_urls = []

        while True:
            try:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()

                page.goto("https://www.livenation.com.tw/event/allevents")

                events = page.query_selector_all(".result-card__image")

                for i in range(last_finished_index + 1, len(events)):
                    print(f'{website} progress - {i + 1}/{len(events)}')
                    events[i].click()

                    # 下載內文
                    inner_text = page.locator(
                        "#top > main > div > div.layout__container > div.accordion__accordion > div > div > div").inner_text()
                    with open(txt_filename, 'w', encoding='utf-8') as f:
                        f.write(inner_text)

                    # 讀取內文
                    with open(txt_filename, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    # 演唱會標題
                    title = page.locator(".eventblurb__title[data-ln='EventName']").inner_text().replace(
                        '\n', '').strip()

                    # 票價 (一定得從內文當中獲得)
                    prices = get_prices(lines)

                    # 售票時間 (一定得從內文當中獲得)
                    without_sell_time_lines, sell_datetimes_str = get_sell(get_time_lines(lines))

                    # 表演地點
                    location = page.locator(
                        "#top > main > div > div.layout__container > div.eventblurb__container > div > div > "
                        "div.eventblurb__detailscontainer > h2 > div > a").inner_text()
                    # locations = [location]

                    # 表演時間
                    day = page.locator(
                        "#top > main > div > div.layout__container > div.eventblurb__container > div > div > div:nth-child(1) > "
                        "div > span.date__day").inner_text()
                    month_year = page.locator(
                        "#top > main > div > div.layout__container > div.eventblurb__container > div > div > div:nth-child(1) > "
                        "div > span.date__month").inner_text()
                    year = month_year[month_year.index(' ') + 1:]
                    month = month_year[:month_year.index(' ') - 1]
                    if page.locator(
                            "#top > main > div > div.layout__container > div.eventblurb__container > div > div > "
                            "div.eventblurb__detailscontainer > h3").is_visible():
                        performance_time = page.locator(
                            "#top > main > div > div.layout__container > div.eventblurb__container > div > div > "
                            "div.eventblurb__detailscontainer > h3").inner_text()
                    else:
                        # 找到表演時間
                        start_time = get_start_time(without_sell_time_lines)
                        if start_time != '00:00':
                            performance_time = start_time

                    performance_datetime = year + '/' + month + '/' + day + ' ' + performance_time
                    # performance_datetimes = [performance_datetime]

                    ''''''

                    print('tit', title)
                    print('sel', sell_datetimes_str)  # list
                    print('pri', prices)  # list
                    print('pdt', performance_datetime)  # str
                    print('lcs', location)  # str
                    print('web', f'{website}')
                    print('url', page.url)

                    new_data = {
                        'tit': title,
                        'sdt': sell_datetimes_str,
                        'prc': prices,
                        'pdt': [performance_datetime],
                        'loc': [location],
                        'int': inner_text,
                        'web': f'{website}',
                        'url': page.url
                    }

                    print('\n--- write new data ---\n')

                    write_data_json(json_filename, new_data)

                    last_finished_index = i
                    if page.url in fail_urls:
                        del fail_urls[fail_urls.index(page.url)]

                    # 返回主頁面
                    page.go_back()
                    events = page.query_selector_all(".result-card__image")

                # 完成
                page.close()

                # 刪除文字暫存檔
                os.remove(txt_filename)

                delete_blank_sdt(website, json_filename)
                delete_past_ticketing_time(website, json_filename)

                print(f'{website} done')
                break

            except Exception as e:
                # 錯誤
                print(e, f'{website} restart')
                print('last finished index = ', last_finished_index)

                if page.url == "https://www.livenation.com.tw/event/allevents":
                    print(f'是{website}的主頁，沒關係的!')
                else:
                    if page.url not in fail_urls:
                        print('第一次失敗')
                        fail_urls.append(page.url)
                    else:
                        print('第二次失敗')
                        print('跳過')
                        last_finished_index += 1

                        write_error(website, page.url, e)

                # 重新啟動
                continue


def get_indievox(website, json_filename, txt_filename):
    timeout_seconds = 500

    with sync_playwright() as p:
        # 清空json資料庫
        with open(json_filename, 'w', encoding='utf-8') as f:
            f.write('')
        # 待會會從 last_finished_index + 1開始
        last_finished_index = -1
        # 物件總數
        all_event_numbers = -1
        # 錯誤的網址
        fail_urls = []

        while True:
            try:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                page.set_default_timeout(5000)

                page.goto(
                    "https://www.indievox.com/activity/list?type=table&startDate=2023%2F11%2F20&endDate=")

                # 只有程式執行的一開始會經過這裡
                if last_finished_index == -1 and all_event_numbers == -1:
                    while (page.locator("#activityListTab > table > tbody > tr > td > div > a").is_visible()):
                        page.keyboard.press('End')
                    all_events = page.query_selector_all("#activityListTab > table > tbody > tr")
                    all_event_numbers = len(all_events)
                    print(all_event_numbers, '\n')

                for i in range(last_finished_index + 1, all_event_numbers):
                    # print(f'{website} progress - {i}/{all_event_numbers - 1}')
                    print(f'{website} progress - {i + 1}/{all_event_numbers}')

                    # 第一頁不需要讀取到最後 因此<19的都直接點擊就可以
                    if i > 19:
                        # 讀取到最下面 然後再點擊物件
                        while page.locator(
                                "#activityListTab > table > tbody > tr > td > div > a").is_visible():
                            page.locator(
                                "#activityListTab > table > tbody > tr > td > div > a").click()
                            page.keyboard.press('End')
                            page.wait_for_timeout(timeout_seconds)
                    all_events = page.query_selector_all("#activityListTab > table > tbody > tr")

                    # 如果物件標題可見
                    if page.locator("#activityListTab > table > tbody > tr").nth(i).locator("td").nth(
                            0).is_visible():
                        # 獲得時間
                        # time_line = page.locator("#activityListTab > table > tbody > tr").nth(i).locator(
                        #     "td").nth(0).inner_text()
                        # ds = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", time_line)
                        # print('ds', ds)

                        # 獲得標題
                        title = page.locator("#activityListTab > table > tbody > tr").nth(i).locator("td").nth(
                            1).inner_text()

                        # 獲得地點
                        location = page.locator("#activityListTab > table > tbody > tr").nth(i).locator(
                            "td").nth(2).inner_text()

                        # 點擊物件
                        page.locator(".fcLightBlue").nth(i).click()
                        page.wait_for_load_state('load')
                        page.wait_for_timeout(timeout_seconds)

                    # 下載內文
                    inner_text = page.locator("#intro").inner_text()
                    with open(txt_filename, 'w', encoding='utf-8') as f:
                        f.write(inner_text)

                    # 讀取內文
                    with open(txt_filename, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    no_price = False
                    # 票價 list (一定得從內文當中獲得)
                    prices = get_prices(lines)
                    if not prices:
                        print('no prices found kk')
                        no_price = True
                    else:
                        print('found prices!')

                    # 售票時間 str (一定得從內文當中獲得)
                    without_sell_time_lines, sell_datetimes_str = get_sell(get_time_lines(lines))

                    # 有立即購買的按鈕
                    if page.locator(".list-inline a.btn.btn-default.btn-lg").is_visible():
                        # 點擊購買按鈕
                        page.locator(".list-inline a.btn.btn-default.btn-lg").click()
                        page.wait_for_load_state('load')
                        page.wait_for_timeout(timeout_seconds)

                        # 有幾行資訊欄
                        for j in range(len(page.query_selector_all("#gameList > table > tbody > tr"))):
                            # 表演時間
                            performance_datetime = page.locator('#gameList > table > tbody > tr').nth(
                                j).locator('td').nth(
                                0).inner_text()
                            performance_datetime = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", performance_datetime)
                            performance_datetime = re.sub(r"\s{2,}", " ", performance_datetime)
                            performance_datetime = performance_datetime.strip()
                            # 不從這邊獲得地點，因為我們在主頁那邊獲得了

                            ''''''

                            # 沒票價 但有購票的按鈕 (點開後) 再往前一個頁面
                            if no_price and page.locator('#gameList > table > tbody > tr').nth(j).locator(
                                    'td > button').is_visible():
                                print('No price, Navigate to price webpage')
                                # 前往下一頁
                                page.locator('#gameList > table > tbody > tr').nth(j).locator(
                                    'td > button').click()
                                page.wait_for_load_state('load')
                                page.wait_for_timeout(timeout_seconds)

                                # 購票頁面行數的迴圈
                                for k in range(len(page.query_selector_all("#ticketPriceList > tbody > tr"))):
                                    price_line = re.sub(r',', '',
                                                        page.locator("#ticketPriceList > tbody > tr").nth(
                                                            k).locator("td.fcBlue > h4").inner_text())
                                    not_digit_index = 0
                                    for l in range(len(price_line) - 1, 0, -1):
                                        if not price_line[l].isdigit():
                                            not_digit_index = l
                                            break
                                    prices.append(price_line[not_digit_index + 1:])

                                print(f'Got {prices} from webpage')
                                page.go_back()
                                # 點擊購買按鈕
                                page.locator(".list-inline a.btn.btn-default.btn-lg").click()
                                page.wait_for_load_state('load')
                                page.wait_for_timeout(timeout_seconds)

                            ''''''

                            print('tit', title)  # str
                            print('sdt', sell_datetimes_str)  # list
                            print('prc', prices)  # list
                            print('pdt', performance_datetime)  # str
                            print('loc', location)  # str
                            print('web', f'{website}')
                            print('url', page.url)

                            new_data = {
                                'tit': title,
                                'sdt': sell_datetimes_str,
                                'prc': prices,
                                'pdt': [performance_datetime],
                                'loc': [location],
                                'int': inner_text,
                                'web': f'{website}',
                                'url': page.url
                            }

                            print('\n--- write new data ---\n')

                            if no_price:
                                prices = []

                            write_data_json(json_filename, new_data)

                            last_finished_index = i
                            if page.url in fail_urls:
                                del fail_urls[fail_urls.index(page.url)]

                    # 沒有立即購買的按鈕，只能從內文當中獲得資訊
                    else:
                        print('沒有按紐')
                        # 表演時間, 地點
                        performance_datetimes, locations = get_performance_location(without_sell_time_lines)

                        print('tit', title)  # str
                        print('sdt', sell_datetimes_str)  # list
                        print('prc', prices)  # list
                        print('pdt', performance_datetimes)  # list
                        print('loc', locations)  # list
                        print('web', f'{website}')
                        print('url', page.url)

                        new_data = {
                            'tit': title,
                            'sdt': sell_datetimes_str,
                            'prc': prices,
                            'pdt': performance_datetimes,
                            'loc': locations,
                            'int': inner_text,
                            'web': f'{website}',
                            'url': page.url
                        }

                        print('\n--- write new data ---\n')

                        write_data_json(json_filename, new_data)

                        last_finished_index = i
                        if page.url in fail_urls:
                            del fail_urls[fail_urls.index(page.url)]

                    # 返回主頁面
                    page.go_back()
                    # 等待頁面載入完成
                    page.wait_for_load_state('load')
                    page.wait_for_timeout(timeout_seconds)

                # 完成
                page.close()
                # 移除txt暫存檔
                os.remove(txt_filename)

                delete_blank_sdt(website, json_filename)
                delete_past_ticketing_time(website, json_filename)

                print(f'{website} done')
                break

            except Exception as e:
                # 錯誤
                print(e, f'{website} restart')
                print('last finished index = ', last_finished_index)

                if page.url == "https://www.indievox.com/activity/list?type=table&startDate=2023%2F11%2F20&endDate=":
                    print(f'是{website}的主頁，沒關係的!')
                else:
                    if page.url not in fail_urls:
                        print('第一次失敗')
                        fail_urls.append(page.url)
                    else:
                        print('第二次失敗')
                        print('跳過')
                        last_finished_index += 1

                        write_error(website, page.url, e)

                # 重新啟動
                continue


def get_ticketplus(website, json_filename, txt_filename):
    with sync_playwright() as p:
        with open(json_filename, 'w', encoding='utf-8') as f:
            f.write('')

        # 待會會從 last_finished_index + 1開始
        last_finished_index = -1
        # 物件總數
        all_event_numbers = -1
        # 錯誤的網址
        fail_urls = []
        while True:
            try:
                browser = p.chromium.launch(headless=False, slow_mo=1000)
                context = browser.new_context()
                page = context.new_page()
                page.set_default_timeout(10000)

                page.goto("https://ticketplus.com.tw/")

                # 只有程式執行的一開始會經過這裡
                if last_finished_index == -1 and all_event_numbers == -1:
                    pressed = False
                    while not page.locator(
                            "#app > div > div > div > main > div > div > div.container.py-0.cus-container.mx-auto > div.tab-content.pa-3.pa-md-6 > div > div > div.text-center.pa-3.text-small.mt-6").is_visible():
                        page.keyboard.press('End')
                        if not pressed:
                            page.locator(
                                "#app > div > div > div > main > div > div > div.container.py-0.cus-container.mx-auto > div.tab-content.pa-3.pa-md-6 > div > div > div:nth-child(2) > button > span").click()
                            pressed = True

                    all_events = page.query_selector_all(".row > div.d-flex.col-sm-6.col-md-4.col-12")
                    all_event_numbers = len(all_events)
                    print(all_event_numbers, '\n')

                unique_id = []
                for i in range(last_finished_index + 1, all_event_numbers):
                    # print(f'Ticketplus progress - {i + 1}/{all_event_numbers}')
                    print(f'{website} progress - {i + 1}/{all_event_numbers}')
                    ''' 總數 '''
                    if i < 6:
                        page.locator(".row > div.d-flex.col-sm-6.col-md-4.col-12").nth(i).click()
                    else:
                        while not page.locator(".row > div.d-flex.col-sm-6.col-md-4.col-12").nth(
                                i).is_visible():
                            page.keyboard.press('End')
                            if page.locator(
                                    "#app > div > div > div > main > div > div > div.container.py-0.cus-container.mx-auto > div.tab-content.pa-3.pa-md-6 > div > div > div:nth-child(2) > button > span").is_visible():
                                page.locator(
                                    "#app > div > div > div > main > div > div > div.container.py-0.cus-container.mx-auto > div.tab-content.pa-3.pa-md-6 > div > div > div:nth-child(2) > button > span").click()

                        page.locator(".row > div.d-flex.col-sm-6.col-md-4.col-12").nth(i).click()

                    if page.locator(
                            "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.px-5.pb-5.font-weight-bold > div.row > div:nth-child(2) > button > span").is_visible():
                        page.locator(
                            "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.px-5.pb-5.font-weight-bold > div.row > div:nth-child(2) > button > span").click()

                    # 有時候網路比較慢會什麼都沒讀到就跳出來，如果沒看到內文我就持續讓他等待直到出現
                    while not page.locator("#activityInfo > div > div").is_visible():
                        page.wait_for_timeout(1000)

                    # 處理新資料
                    ''' 內文 '''
                    # 下載內文
                    inner_text = page.locator("#activityInfo > div > div").inner_text()
                    with open(txt_filename, 'w', encoding='utf-8') as f:
                        f.write(inner_text)
                    # 載入內文
                    with open(txt_filename, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    # 票價
                    prices = get_prices(lines)
                    # 售票時間
                    without_sell_time_lines, sell_datetimes_str = get_sell(get_time_lines(lines))
                    ''' 固定位置 '''
                    # 標題
                    title = page.locator("#banner > div.pb-6.col.col-12 > h1").inner_text()
                    # 資訊欄
                    columns = page.query_selector_all("#buyTicket > .sesstion-item")
                    for j in range(len(columns)):
                        column_text = page.locator("#buyTicket > .sesstion-item").nth(j).locator(
                            "div > div > div").nth(
                            0).inner_text()
                        column_text = column_text.split('\n')

                        # 第幾個位置是時間?
                        time_index = -1
                        for k in range(len(column_text)):
                            if ':' in column_text[k] or '：' in column_text[k]:
                                time_index = k
                                break
                        # 日期
                        concert_date = ''
                        for m in range(1, time_index):
                            column_text[m] = column_text[m].replace('-', '/')
                            column_text[m] = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", column_text[m])
                            concert_date += column_text[m]
                        # 時間
                        concert_time = column_text[time_index]
                        # 我只想要開始的時間，捨棄結束的時間
                        if '~' in concert_time:
                            concert_time = concert_time[:concert_time.index('~')]
                        # 日期 & 時間
                        pdt = concert_date + ' ' + concert_time
                        pdt = re.sub(r"~", " ~ ", pdt)
                        pdt = re.sub(r"\s{2,}", " ", pdt)
                        if pdt[-1] == ' ':
                            pdt = pdt[:-1]
                        # 地點
                        concert_place = column_text[3]
                        # 獨一無二的id識別
                        if f"{title}_{pdt}_{concert_place}" not in unique_id:
                            unique_id.append(f"{title}_{pdt}_{concert_place}")

                            print('tit', title)
                            print('sdt', sell_datetimes_str)
                            print('prc', prices)
                            print('pdt', pdt)
                            print('loc', concert_place)
                            print('web', f'{website}')
                            print('url', page.url)

                            new_data = {
                                'tit': title,
                                'sdt': sell_datetimes_str,
                                'prc': prices,
                                'pdt': [pdt],
                                'loc': [concert_place],
                                'int': inner_text,
                                'web': f'{website}',
                                'url': page.url
                            }

                            print('\n--- write new data ---\n')

                            write_data_json(json_filename, new_data)
                            
                            last_finished_index = i
                            if page.url in fail_urls:
                                del fail_urls[fail_urls.index(page.url)]
                        else:
                            print('Skip')
                            continue

                    page.go_back()

                # 完成
                page.close()
                # 移除剛剛使用的暫存文檔
                os.remove(txt_filename)

                delete_blank_sdt(website, json_filename)
                delete_past_ticketing_time(website, json_filename)

                print(f'{website} done\n')
                break

            except Exception as e:
                print(e, f'{website} restart')
                print('last finished index = ', last_finished_index)
                if page.url == 'https://ticketplus.com.tw/':
                    print(f'是{website}的主頁，沒關係的!')
                else:
                    if page.url not in fail_urls:
                        print('第一次失敗')
                        fail_urls.append(page.url)
                    else:
                        print('第二次失敗')
                        print('跳過')
                        last_finished_index += 1

                        write_error(website, page.url, e)

                # 重新啟動
                continue


# get_era('era', 'era.json', _)
# get_livenation('Live Nation', 'livenation.json', 'livenation_temp.txt')
# get_indievox('Indievox', 'indievox.json', 'indievox_temp.txt')
# get_ticketplus('Ticket Plus', 'ticketplus.json', 'ticketplus_temp.txt')
# get_kktix('KKTIX', 'kktix_new.json', 'kktix_temp.txt')

json_new = ['era.json',
            'indievox.json',
            'kktix_new.json',
            'livenation.json',
            'ticketplus.json']

thread_era = threading.Thread(target=get_era, args=('era', 'era.json', 'era_temp.txt'))
thread_livenation = threading.Thread(target=get_livenation,
                                     args=('Live Nation', 'livenation.json', 'livenation_temp.txt'))


# thread_indievox = threading.Thread(target=get_indievox, args=('Indievox', 'indievox.json', 'indievox_temp.txt'))
# threading_ticketplus = threading.Thread(target=get_ticketplus, args=('Ticket Plus', 'ticketplus.json', 'ticketplus_temp.txt'))
# thread_kktix = threading.Thread(target=get_kktix, args=('KKITX', 'kktix_new.json', 'kktix_temp.txt'))
def threads_start():
    thread_era.start()
    thread_livenation.start()
    # thread_indievox.start()
    # thread_kktix.start()
    # threading_ticketplus.start()


# threads_start()


def threads_join():
    thread_era.join()
    # thread_indievox.join()
    # thread_kktix.join()
    thread_livenation.join()
    # threading_ticketplus.join()
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

        # -------------------------------------
        # 表演時間
        # -------------------------------------

        # 创建两个空列表来存储表演时间信息
        performance_datetimes = []
        performance_datetimes_until = []

        # 遍历concert['pdt']中的每个表演时间
        for pdt in concert['pdt']:
            # 检查表演时间中是否包含'~'，如果包含，则将其添加到另一个列表中
            if '~' in pdt:
                performance_datetimes_until.append(pdt)
            else:
                # 否则，将其添加到第一个列表中
                performance_datetimes.append(pdt)

        # 对表演时间进行排序
        performance_datetimes = sort_datetime(performance_datetimes)

        # 创建空字符串来存储表演时间的字符串表示形式
        performance_datetime_str = ''
        performance_datetime_until_str = ''

        # 将排序后的表演时间转换为字符串
        for i, performance_datetime in enumerate(performance_datetimes):
            performance_datetime_str += performance_datetime
            if i < len(performance_datetimes) - 1:
                performance_datetime_str += ', '

        # 如果同时存在performance_datetimes和performance_datetimes_until
        if performance_datetimes and performance_datetimes_until:
            # 将performance_datetimes_until中的时间添加到字符串中
            for i, performance_datetime in enumerate(performance_datetimes_until):
                performance_datetime_until_str += f'({performance_datetime})'
                if i < len(performance_datetimes_until) - 1:
                    performance_datetime_until_str += ', '
            # 合并performance_datetime_str和performance_datetime_until_str，用换行符分隔
            performance_datetime_str = performance_datetime_str + '\n' + performance_datetime_until_str
        # 如果只有performance_datetimes_until
        elif not performance_datetimes and performance_datetimes_until:
            # 直接将performance_datetimes_until中的时间赋值给performance_datetime_str
            for i, performance_datetime in enumerate(performance_datetimes_until):
                performance_datetime_until_str += f'{performance_datetime}'
                if i < len(performance_datetimes_until) - 1:
                    performance_datetime_until_str += ', '
            performance_datetime_str = performance_datetime_until_str

        if performance_datetimes or performance_datetimes_until:
            print(f"表演時間\tPerformance Time:\t{performance_datetime_str}")
        else:
            print(f"表演時間\tPerformance Time:\t-")
        # -------------------------------------
        # 票價
        # -------------------------------------

        prices = []
        for price in concert['prc']:
            prices.append(price)
        price_str = ''
        prices = sorted(list(set(prices)), reverse=True)
        for i, price in enumerate(prices):
            price_str += str(price)
            if i < len(prices) - 1:
                price_str += ', '
        if not prices:
            print(f"票價\t\tPrices:\t\t\t\t-")
        else:
            print(f"票價\t\tPrices:\t\t\t\t{price_str}")

        # -------------------------------------
        # 地點
        # -------------------------------------

        locations = []
        for location in concert['loc']:
            locations.append(location)
        location_str = ''
        for i, location in enumerate(locations):
            location_str += location
            if i < len(locations) - 1:
                location_str += ', '
        if locations:
            print(f"地點\t\tLocations:\t\t\t{location_str}")
        else:
            print(f"地點\t\tLocations:\t\t\t\t-")

        # -------------------------------------
        # 售票時間
        # -------------------------------------

        sell_datetimes = []
        for sdt in concert['sdt']:
            sell_datetimes.append(sdt)
        sell_datetimes = sort_datetime(sell_datetimes)
        sell_datetime_str = ''
        for i, sell_datetime in enumerate(sell_datetimes):
            sell_datetime_str += sell_datetime
            if i < len(sell_datetimes) - 1:
                sell_datetime_str += ', '

        if not concert['sdt']:
            print(f"售票時間\tTicketing Time:\t\t售票中 Available")
        else:
            print(f"售票時間\tTicketing Time:\t{concert['sdt']}")

        # -------------------------------------
        # 售票網站
        # -------------------------------------

        print(f"售票網站\tTicketing Website:\t{concert['web']}")

        # -------------------------------------
        # 網址
        # -------------------------------------

        print(f"網址\t\tURL: {concert['url']}")
        print()


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
    # 打开旧的中文数据文件，读取内容并加载到 old_data 变量中
    with open('concert_data_old_zh.json', 'r', encoding='utf-8') as old_file:
        old_data = json.load(old_file)

    # 打开新的中文数据文件，读取内容并加载到 new_data 变量中
    with open('concert_data_new_zh.json', 'r', encoding='utf-8') as new_file:
        new_data = json.load(new_file)

    # 将新的中文数据写入旧的中文数据文件，格式化并确保不使用 ASCII 编码
    with open('concert_data_old_zh.json', 'w', encoding='utf-8') as old_file:
        json.dump(new_data, old_file, indent=4, ensure_ascii=False)

    # 打开新的中文数据文件，以写入模式清空文件内容
    with open('concert_data_new_zh.json', 'w', encoding='utf-8') as new_file:
        new_file.write('[]')

    # 打开旧的英文数据文件，读取内容并加载到 old_data 变量中
    with open('concert_data_old_en.json', 'r', encoding='utf-8') as old_file:
        old_data = json.load(old_file)

    # 打开新的英文数据文件，读取内容并加载到 new_data 变量中
    with open('concert_data_new_en.json', 'r', encoding='utf-8') as new_file:
        new_data = json.load(new_file)

    # 将新的英文数据写入旧的英文数据文件，格式化并确保不使用 ASCII 编码
    with open('concert_data_old_en.json', 'w', encoding='utf-8') as old_file:
        json.dump(new_data, old_file, indent=4, ensure_ascii=False)

    # 打开新的英文数据文件，以写入模式清空文件内容
    with open('concert_data_new_en.json', 'w', encoding='utf-8') as new_file:
        new_file.write('[]')


def each_concert_number():
    with open('era.json', 'r', encoding='utf-8') as f:
        era_data = json.load(f)
    with open('indievox.json', 'r', encoding='utf-8') as f:
        indievox_data = json.load(f)
    with open('kktix_new.json', 'r', encoding='utf-8') as f:
        kktix_data = json.load(f)
    with open('livenation.json', 'r', encoding='utf-8') as f:
        livenation_data = json.load(f)
    with open('ticketplus.json', 'r', encoding='utf-8') as f:
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
    pass
    # reset_failure_log()
    # threads_start()
    # threads_join()
    # threads_integration()
    # each_concert_number() # 驗算用
    # delete_files()
    # zh_en()
    # new_concerts()
    # json_new_to_old()

# get_latest_concert_info()
