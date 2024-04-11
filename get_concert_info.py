from playwright.sync_api import sync_playwright, Playwright, expect, Page
import json
import os
import threading
import shutil
import re
import sys
from datetime import datetime, time
from googletrans import Translator
from get_concert_new_old import *
from get_data_from_text import *
from fuzzywuzzy import process

zh_cities = ["台北", "新北", "桃園", "台中", "台南", "高雄", "基隆", "新竹", "苗栗", "彰化", "南投", "雲林",
             "嘉義", "屏東", "宜蘭", "花蓮", "台東", "金門", "澎湖", "連江"]
en_cities = ["Taipei", "New Taipei", "Taoyuan", "Taichung", "Tainan", "Kaohsiung", "Keelung", "Hsinchu", "Miaoli",
             "Changhua", "Nantou", "Yunlin", "Chiayi", "Pingtung", "Yilan", "Hualien", "Taitung", "Kinmen", "Penghu",
             "Lienchiang"]
concert_json_filenames = ['era.json', 'indievox.json', 'kktix.json', 'livenation.json', 'ticketplus.json']

with open('concert_data_new_zh.json', 'r', encoding='utf-8') as f:
    new_data = json.load(f)

with open('concert_data_old_zh.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

with open('concert_zh.json', 'r', encoding='utf-8') as f:
    all_data = json.load(f)

month = datetime.now().month
day = datetime.now().day
hour = datetime.now().hour

concert_today = f'concert_{month}_{day}_{hour}.json'
print(concert_today)
with open(concert_today, 'w', encoding='utf-8') as f:
    json.dump([], f, indent=4, ensure_ascii=False)


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


def delete_past_ticketing_time(json_filename):
    # 刪除時間已經過去的售票時間
    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i in range(len(data)):
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
            data[i]['sdt'] = future_datetimes  # str, not obj
            # 寫入檔案
            with open(json_filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)


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
                browser = p.chromium.launch(headless=True)  # era
                # browser = p.chromium.launch(headless=False)  # era
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
                            if sell_d and sell_t:
                                sell_datetime = sell_d[0] + ' ' + sell_t[0]
                            else:
                                sell_datetime = ''
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
                            'cit': "",
                            'int': inner_text,
                            'web': f'{website}',
                            'url': page.url,
                            'pin': page.url + str(j),
                            'tim': str(datetime.now())
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

                print(f'\n\n\n\n\n\n\n\n{website} done\n\n\n\n\n\n\n\n')
                break

            except Exception as e:
                # 錯誤
                page.close()
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


def get_era_without_error_mechanism(website, json_filename, txt_filename):
    with sync_playwright() as p:

        with open(json_filename, 'w', encoding='utf-8') as f:
            f.write('')

        # 待會會從 last_finished_index + 1開始
        last_finished_index = -1
        # 錯誤的網址
        fail_urls = []

        browser = p.chromium.launch(headless=True)  # era
        # browser = p.chromium.launch(headless=False)  # era
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
                    if sell_d and sell_t:
                        sell_datetime = sell_d[0] + ' ' + sell_t[0]
                    else:
                        sell_datetime = ''
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
                    'cit': "",
                    'int': inner_text,
                    'web': f'{website}',
                    'url': page.url,
                    'pin': page.url + str(j),
                    'tim': str(datetime.now())
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

        print(f'\n\n\n\n\n\n\n\n{website} done\n\n\n\n\n\n\n\n')


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
                browser = p.chromium.launch(headless=True)  # live nation
                # browser = p.chromium.launch(headless=False)  # live nation
                context = browser.new_context()
                page = context.new_page()

                page.goto("https://www.livenation.com.tw/event/allevents")

                events = page.query_selector_all(".result-card__image")

                for i in range(last_finished_index + 1, len(events)):
                    print(f'{website} progress - {i + 1}/{len(events)}')
                    events[i].click()

                    # 下載內文
                    # inner_text = page.locator(
                    #     "#top > main > div > div.layout__container > div.accordion__accordion > div > div > div").inner_text()
                    inner_text = ''
                    inner_texts = page.query_selector_all(
                        "#top > main > div > div.layout__container > div.accordion__accordion > div > div > div > p")
                    for j in range(len(inner_texts)):
                        inner_text += inner_texts[j].inner_text()

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
                    performance_time = '00:00'
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
                        'cit': "",
                        'int': inner_text,
                        'web': f'{website}',
                        'url': page.url,
                        'pin': page.url + str(i),
                        'tim': str(datetime.now())
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
                # delete_past_ticketing_time(website, json_filename)

                print(f'\n\n\n\n\n\n\n\n{website} done\n\n\n\n\n\n\n\n')
                break

            except Exception as e:
                # 錯誤
                page.close()
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
                browser = p.chromium.launch(headless=True)  # indievox
                # browser = p.chromium.launch(headless=False)  # indievox
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
                                'cit': "",
                                'int': inner_text,
                                'web': f'{website}',
                                'url': page.url,
                                'pin': page.url + str(j),
                                'tim': str(datetime.now())
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
                            'cit': "",
                            'int': inner_text,
                            'web': f'{website}',
                            'url': page.url,
                            'pin': page.url + str(0),
                            'tim': str(datetime.now())
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
                # delete_past_ticketing_time(website, json_filename)

                print(f'\n\n\n\n\n\n\n\n{website} done\n\n\n\n\n\n\n\n')
                break

            except Exception as e:
                # 錯誤
                page.close()
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
                browser = p.chromium.launch(headless=True, slow_mo=1000)  # ticketplus
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
                        for k in range(1, len(column_text)):
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
                        concert_place = column_text[time_index + 1]
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
                                'cit': "",
                                'int': inner_text,
                                'web': f'{website}',
                                'url': page.url,
                                'pin': page.url + str(j),
                                'tim': str(datetime.now())
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
                # delete_past_ticketing_time(website, json_filename)

                print(f'\n\n\n\n\n\n\n\n{website} done\n\n\n\n\n\n\n\n')
                break

            except Exception as e:
                page.close()
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


def kktix_get_ticketing_time_list(page, index, sell_datetimes_str_list):
    # 售票時間 list
    if page.locator(".table-wrapper > table > tbody > tr").nth(
            index).locator(
        ".period .period-time").is_visible():
        ticket_time = page.locator(
            ".table-wrapper > table > tbody > tr").nth(
            index).locator(
            ".period .period-time").inner_text()
        ticket_time = ticket_time[:ticket_time.index('~')]
        ticket_time = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", ticket_time)
        ticket_time = ticket_time.strip()
        if ticket_time not in sell_datetimes_str_list:
            sell_datetimes_str_list.append(ticket_time)

    return sell_datetimes_str_list


def kktix_get_title_str(page, title):
    # 標題 str
    if page.locator(
            "#registrationsNewApp > div > div:nth-child(2) > div.narrow-wrapper.ng-scope > div > h1").is_visible():
        title = page.locator(
            "#registrationsNewApp > div > div:nth-child(2) > div.narrow-wrapper.ng-scope > div > h1").inner_text().replace(
            '\n', '').strip()
    else:
        print('title no')

    return title


def kktix_get_prices_list(page, index, prices):
    # 票價 list
    if page.locator(".table-wrapper > table > tbody > tr").nth(
            index).locator(
        ".price .price > span").nth(1).is_visible():
        price = int(
            float(
                page.locator(".table-wrapper > table > tbody > tr").nth(
                    index).locator(".price .price > span").nth(1).inner_text().replace(
                    ',',
                    '')))
        prices.append(price)
    else:
        prices.append(0)
    prices = list(set(prices))

    return prices


def kktix_get_location_str(page, location):
    # 地點 str
    if page.locator("tbody > tr").nth(1).locator("th").is_visible():
        if page.locator("tbody > tr").nth(1).locator(
                "th").inner_text() == '活動地點':
            location_address = \
                page.locator("tbody > tr").nth(1).locator(
                    "td").inner_text().split(
                    '檢視地圖')[
                    0].strip().split(' / ')
            location = location_address[0]
            # locations.append(concert_place)
    else:
        print('locations no')

    return location


def kktix_get_location_str1(page, location, address):
    # 地點 str
    if page.locator("tbody > tr").nth(1).locator("th").is_visible():
        if page.locator("tbody > tr").nth(1).locator(
                "th").inner_text() == '活動地點':
            location_address = \
                page.locator("tbody > tr").nth(1).locator(
                    "td").inner_text().split(
                    '檢視地圖')[
                    0].strip().split(' / ')
            location = location_address[0]
            if len(location_address) == 1:
                address = '-'
            else:
                address = location_address[1]
    else:
        print('locations no')

    return location, address


def kktix_get_performance_list(page, performance_datetimes_str_list):
    if page.locator("tbody > tr").nth(0).locator("td").is_visible():
        pdt = \
            page.locator("tbody > tr").nth(0).locator(
                "td").inner_text().split(
                '加入行事曆')[
                0].strip()
        pdt = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", pdt)
        if '~' in pdt:
            start_time_date = re.findall(r'\d{4}/\d{1,2}/\d{1,2}',
                                         pdt.split('~')[0])
            finish_time_date = re.findall(r'\d{4}/\d{1,2}/\d{1,2}',
                                          pdt.split('~')[1])
            if start_time_date[0] == finish_time_date[0]:
                pdt = pdt.split('~')[0].strip()
        pdt = re.sub(r"\s{2,}", " ", pdt)
        pdt = pdt.strip()
        performance_datetimes_str_list.append(pdt)
    else:
        print('performance_datetimes no')

    return performance_datetimes_str_list


def get_kktix_first(website, json_filename, txt_filename):
    # global integrate_webs
    # page 1, 2, 3, 4
    with sync_playwright() as p:

        with open(json_filename, 'w', encoding='utf-8') as f:
            f.write('')

        # 待會會從 last_finished_index + 1開始
        last_finished_selling_index = -1
        last_finished_view_index = -1
        last_finished_counter_index = -1
        # 完成的演唱會頁面
        completed_pages = []
        # 發生錯誤的演唱會活動
        current_page_index = -1
        fail_indices = []
        # 統整的網站

        while True:
            try:
                browser = p.chromium.launch(headless=True)  # kktix first
                # browser = p.chromium.launch(headless=False)  # kktix first
                context = browser.new_context()
                page = context.new_page()
                # page.set_default_timeout(60000)

                ''''''

                page.goto("https://kktix.com/events?end_at=&"
                          "event_tag_ids_in=1&max_price=&"
                          "min_price=&page=1"
                          "&search=&start_at=")

                print(f'{website} start!')

                ''''''

                page_index = 1
                current_page_index = page_index

                while True:
                    if page_index in completed_pages:
                        print(f'Error occurred, but page {page_index} is already finished!')

                    else:
                        # type-selling
                        type_selling = page.query_selector_all('li.type-selling')
                        if last_finished_selling_index != len(type_selling) - 1:
                            print(f'\n\nselling start from {page_index}-{last_finished_selling_index + 2}\n\n')
                            for i in range(last_finished_selling_index + 1, len(type_selling)):
                                print(f'{website} selling progress - page {page_index}, {i + 1}/{len(type_selling)}')
                                # print(f'selling {page_index}-{i}')
                                # 演唱會頁面
                                type_selling[i].click()
                                print('concert page', page.url)
                                page.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str_list = []
                                prices = []
                                performance_datetimes_str_list = []
                                location = ''
                                if page.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        sell_datetimes_str_list = kktix_get_ticketing_time_list(page, j,
                                                                                                sell_datetimes_str_list)

                                        ''''''

                                        # 票價 list
                                        prices = kktix_get_prices_list(page, j, prices)

                                        ''''''

                                        # 內文
                                        inner_text = page.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page.url)
                                        page.wait_for_timeout(1500)
                                        page.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        title = kktix_get_title_str(page, title)

                                        ''''''

                                        # 表演時間 list
                                        performance_datetimes_str_list = kktix_get_performance_list(page,
                                                                                                    performance_datetimes_str_list)

                                        ''''''

                                        # 地點 str
                                        location = kktix_get_location_str(page, location)

                                        ''''''

                                        page.go_back()

                                        if title or performance_datetimes_str_list or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_selling_index = i
                                            print(f'finished {page_index}-{last_finished_selling_index + 1}')
                                            print('\n----------------------\n')
                                        else:
                                            # with open('sold_out.txt', 'a', encoding='utf-*') as f:
                                            #     f.write(page.url + '\n')

                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_selling_index = i
                                            print(
                                                f'no tit, no pdt, no loc, skip\nfinished {page_index}-{last_finished_selling_index + 1}\n\n----------------------\n')
                                    else:
                                        print('hk activity, skip')
                                        last_finished_selling_index = i
                                        print(f'finished {page_index}-{last_finished_selling_index + 1}')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_selling_index = i
                                    print(f'finished {page_index}-{last_finished_selling_index + 1}')
                                    print('\n----------------------\n')
                                    # integrate_webs.append(page.url)

                                ''''''

                                page.go_back()  # main page
                                type_selling = page.query_selector_all('li.type-selling')
                        else:
                            print('CSS: "type-selling" of this page is already finished!')

                        # type-view
                        type_view = page.query_selector_all('li.type-view')
                        if last_finished_view_index != len(type_view) - 1:
                            print(f'\n\nview start from {page_index}-{last_finished_view_index + 2}\n\n')
                            for i in range(last_finished_view_index + 1, len(type_view)):
                                print(f'{website} view progress - page {page_index}, {i + 1}/{len(type_view)}')
                                # print(f'view {page_index}-{i}')
                                # 演唱會頁面
                                type_view[i].click()
                                print('concert page', page.url)
                                page.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str_list = []
                                prices = []
                                performance_datetimes_str_list = []
                                location = ''
                                if page.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        sell_datetimes_str_list = kktix_get_ticketing_time_list(page, j,
                                                                                                sell_datetimes_str_list)

                                        ''''''

                                        # 票價 list
                                        prices = kktix_get_prices_list(page, j, prices)

                                        ''''''

                                        # 內文
                                        inner_text = page.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page.url)
                                        page.wait_for_timeout(1500)
                                        page.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        title = kktix_get_title_str(page, title)

                                        ''''''

                                        # 表演時間 list
                                        performance_datetimes_str_list = kktix_get_performance_list(page,
                                                                                                    performance_datetimes_str_list)

                                        ''''''

                                        # 地點 str
                                        location = kktix_get_location_str(page, location)

                                        ''''''

                                        page.go_back()

                                        if title or performance_datetimes_str_list or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_view_index = i
                                            print(f'finished {page_index}-{last_finished_view_index + 1}\n')
                                            print('\n----------------------\n')
                                        else:
                                            # with open('sold_out.txt', 'a', encoding='utf-*') as f:
                                            #     f.write(page.url + '\n')

                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_view_index = i
                                            print(
                                                f'no tit, no pdt, no loc, skip\nfinished {page_index}-{last_finished_view_index + 1}\n\n----------------------\n')
                                    else:
                                        print('hk activity, skip')
                                        last_finished_view_index = i
                                        print(f'finished {page_index}-{last_finished_view_index + 1}\n')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_view_index = i
                                    print(f'finished {page_index}-{last_finished_view_index + 1}\n')
                                    print('\n----------------------\n')
                                    # integrate_webs.append(page.url)

                                ''''''

                                page.go_back()  # main page
                                type_view = page.query_selector_all('li.type-view')
                        else:
                            print('CSS: "type-view" of this page is already finished!')

                        # type-counter
                        type_counter = page.query_selector_all('li.type-counter')
                        if last_finished_counter_index != len(type_counter) - 1:
                            print(f'\n\ncounter start from {page_index}-{last_finished_counter_index + 2}\n\n')
                            for i in range(last_finished_counter_index + 1, len(type_counter)):
                                print(
                                    f'{website} counter progress - page {page_index}, {i + 1}/{len(type_counter)}')
                                # print(f'counter {page_index}-{i}')
                                # 演唱會頁面
                                type_counter[i].click()
                                print('concert page', page.url)
                                page.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str_list = []
                                prices = []
                                performance_datetimes_str_list = []
                                location = ''
                                if page.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        sell_datetimes_str_list = kktix_get_ticketing_time_list(page, j,
                                                                                                sell_datetimes_str_list)

                                        ''''''

                                        # 票價 list
                                        prices = kktix_get_prices_list(page, j, prices)

                                        ''''''

                                        # 內文
                                        inner_text = page.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page.url)
                                        page.wait_for_timeout(1500)
                                        page.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        title = kktix_get_title_str(page, title)

                                        ''''''

                                        # 表演時間 list
                                        performance_datetimes_str_list = kktix_get_performance_list(page,
                                                                                                    performance_datetimes_str_list)

                                        ''''''

                                        # 地點 str
                                        location = kktix_get_location_str(page, location)

                                        ''''''

                                        page.go_back()

                                        if title or performance_datetimes_str_list or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_counter_index = i
                                            print(f'finished {page_index}-{last_finished_counter_index + 1}')
                                            print('\n----------------------\n')
                                        else:
                                            # with open('sold_out.txt', 'a', encoding='utf-*') as f:
                                            #     f.write(page.url + '\n')

                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_counter_index = i
                                            print(
                                                f'no tit, no pdt, no loc, skip\nfinished {page_index}-{last_finished_counter_index + 1}\n\n----------------------\n')
                                    else:
                                        print('hk activity, skip')
                                        last_finished_counter_index = i
                                        print(f'finished {page_index}-{last_finished_counter_index + 1}')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_counter_index = i
                                    print(f'finished {page_index}-{last_finished_counter_index + 1}')
                                    print('\n----------------------\n')
                                    # integrate_webs.append(page.url)

                                ''''''

                                page.go_back()  # main page
                                type_counter = page.query_selector_all('li.type-counter')
                        else:
                            print('CSS: "type-counter" of this page is already finished!')
                        ''''''

                        # 完成此頁
                        pagination_div = page.query_selector(".pagination.pull-right")
                        text = pagination_div.inner_text()
                        print(f'\nFinished page {page_index}')
                        completed_pages.append(page_index)
                        last_finished_selling_index = -1
                        last_finished_view_index = -1
                        last_finished_counter_index = -1

                    # 有下一頁
                    if '›' in text:
                        if int(page.locator(
                                "body > div.wrapper > div.page-content > section.explore-container.container > div > div.pagination.pull-right > ul > li.active > a").inner_text()) > 3:
                            break
                        page.locator("div.pagination.pull-right li:last-child").click()
                        page_index += 1
                        current_page_index = page_index
                        print(f'\nGo to page {page_index}\n')

                    # 最後一頁
                    else:
                        print(f'{website} finished')

                        # 程式確認沒有最後一頁後跳出while True的break
                        break

                # 確認全部執行完成，沒有發生錯誤的break
                break

            except Exception as e:
                # 錯誤
                page.close()
                print(e, f'{website} restart')

                if [current_page_index, last_finished_selling_index, last_finished_view_index] not in fail_indices:
                    fail_indices.append([current_page_index, last_finished_selling_index, last_finished_view_index])
                    print('第一次失敗')
                else:
                    print('第二次失敗')
                    print('跳過')

                    if last_finished_view_index == -1:
                        last_finished_selling_index += 1
                    else:
                        last_finished_view_index += 1

                    write_error(website, page.url, e)

                # 重新啟動
                continue

        # 完成
        page.close()


def get_kktix_second(website, json_filename, txt_filename):
    # global integrate_webs
    # page 5, 6, 7, 8
    with sync_playwright() as p:

        with open(json_filename, 'w', encoding='utf-8') as f:
            f.write('')

        # 待會會從 last_finished_index + 1開始
        last_finished_selling_index = -1
        last_finished_view_index = -1
        last_finished_counter_index = -1
        # 完成的演唱會頁面
        completed_pages = []
        # 發生錯誤的演唱會活動
        current_page_index = -1
        fail_indices = []
        # 統整的網站

        while True:
            try:
                browser = p.chromium.launch(headless=True)  # kktix second
                # browser = p.chromium.launch(headless=False)  # kktix second
                context = browser.new_context()
                page = context.new_page()
                # page.set_default_timeout(60000)

                ''''''

                page.goto("https://kktix.com/events?end_at=&"
                          "event_tag_ids_in=1&max_price=&"
                          "min_price=&page=5"
                          "&search=&start_at=")

                print(f'{website} start!')

                ''''''

                page_index = 5
                current_page_index = page_index

                while True:
                    if page_index in completed_pages:
                        print(f'Error occurred, but page {page_index} is already finished!')

                    else:
                        # type-selling
                        type_selling = page.query_selector_all('li.type-selling')
                        if last_finished_selling_index != len(type_selling) - 1:
                            print(f'\n\nselling start from {page_index}-{last_finished_selling_index + 2}\n\n')
                            for i in range(last_finished_selling_index + 1, len(type_selling)):
                                print(f'{website} selling progress - page {page_index}, {i + 1}/{len(type_selling)}')
                                # print(f'selling {page_index}-{i}')
                                # 演唱會頁面
                                type_selling[i].click()
                                print('concert page', page.url)
                                page.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str_list = []
                                prices = []
                                performance_datetimes_str_list = []
                                location = ''
                                if page.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        sell_datetimes_str_list = kktix_get_ticketing_time_list(page, j,
                                                                                                sell_datetimes_str_list)

                                        ''''''

                                        # 票價 list
                                        prices = kktix_get_prices_list(page, j, prices)

                                        ''''''

                                        # 內文
                                        inner_text = page.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page.url)
                                        page.wait_for_timeout(1500)
                                        page.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        title = kktix_get_title_str(page, title)

                                        ''''''

                                        # 表演時間 list
                                        performance_datetimes_str_list = kktix_get_performance_list(page,
                                                                                                    performance_datetimes_str_list)

                                        ''''''

                                        # 地點 str
                                        location = kktix_get_location_str(page, location)

                                        ''''''

                                        page.go_back()

                                        if title or performance_datetimes_str_list or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_selling_index = i
                                            print(f'finished {page_index}-{last_finished_selling_index + 1}')
                                            print('\n----------------------\n')
                                        else:
                                            # with open('sold_out.txt', 'a', encoding='utf-*') as f:
                                            #     f.write(page.url + '\n')

                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_selling_index = i
                                            print(
                                                f'no tit, no pdt, no loc, skip\nfinished {page_index}-{last_finished_selling_index + 1}\n\n----------------------\n')
                                    else:
                                        print('hk activity, skip')
                                        last_finished_selling_index = i
                                        print(f'finished {page_index}-{last_finished_selling_index + 1}')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_selling_index = i
                                    print(f'finished {page_index}-{last_finished_selling_index + 1}')
                                    print('\n----------------------\n')
                                    # integrate_webs.append(page.url)

                                ''''''

                                page.go_back()  # main page
                                type_selling = page.query_selector_all('li.type-selling')
                        else:
                            print('CSS: "type-selling" of this page is already finished!')

                        # type-view
                        type_view = page.query_selector_all('li.type-view')
                        if last_finished_view_index != len(type_view) - 1:
                            print(f'\n\nview start from {page_index}-{last_finished_view_index + 2}\n\n')
                            for i in range(last_finished_view_index + 1, len(type_view)):
                                print(f'{website} view progress - page {page_index}, {i + 1}/{len(type_view)}')
                                # print(f'view {page_index}-{i}')
                                # 演唱會頁面
                                type_view[i].click()
                                print('concert page', page.url)
                                page.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str_list = []
                                prices = []
                                performance_datetimes_str_list = []
                                location = ''
                                if page.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        sell_datetimes_str_list = kktix_get_ticketing_time_list(page, j,
                                                                                                sell_datetimes_str_list)

                                        ''''''

                                        # 票價 list
                                        prices = kktix_get_prices_list(page, j, prices)

                                        ''''''

                                        # 內文
                                        inner_text = page.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page.url)
                                        page.wait_for_timeout(1500)
                                        page.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        title = kktix_get_title_str(page, title)

                                        ''''''

                                        # 表演時間 list
                                        performance_datetimes_str_list = kktix_get_performance_list(page,
                                                                                                    performance_datetimes_str_list)

                                        ''''''

                                        # 地點 str
                                        location = kktix_get_location_str(page, location)

                                        ''''''

                                        page.go_back()

                                        if title or performance_datetimes_str_list or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_view_index = i
                                            print(f'finished {page_index}-{last_finished_view_index + 1}\n')
                                            print('\n----------------------\n')
                                        else:
                                            # with open('sold_out.txt', 'a', encoding='utf-*') as f:
                                            #     f.write(page.url + '\n')

                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_view_index = i
                                            print(
                                                f'no tit, no pdt, no loc, skip\nfinished {page_index}-{last_finished_view_index + 1}\n\n----------------------\n')
                                    else:
                                        print('hk activity, skip')
                                        last_finished_view_index = i
                                        print(f'finished {page_index}-{last_finished_view_index + 1}\n')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_view_index = i
                                    print(f'finished {page_index}-{last_finished_view_index + 1}\n')
                                    print('\n----------------------\n')
                                    # integrate_webs.append(page.url)

                                ''''''

                                page.go_back()  # main page
                                type_view = page.query_selector_all('li.type-view')
                        else:
                            print('CSS: "type-view" of this page is already finished!')

                        # type-counter
                        type_counter = page.query_selector_all('li.type-counter')
                        if last_finished_counter_index != len(type_counter) - 1:
                            print(f'\n\ncounter start from {page_index}-{last_finished_counter_index + 2}\n\n')
                            for i in range(last_finished_counter_index + 1, len(type_counter)):
                                print(f'{website} counter progress - page {page_index}, {i + 1}/{len(type_counter)}')
                                # print(f'counter {page_index}-{i}')
                                # 演唱會頁面
                                type_counter[i].click()
                                print('concert page', page.url)
                                page.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str_list = []
                                prices = []
                                performance_datetimes_str_list = []
                                location = ''
                                if page.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        sell_datetimes_str_list = kktix_get_ticketing_time_list(page, j,
                                                                                                sell_datetimes_str_list)

                                        ''''''

                                        # 票價 list
                                        prices = kktix_get_prices_list(page, j, prices)

                                        ''''''

                                        # 內文
                                        inner_text = page.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page.url)
                                        page.wait_for_timeout(1500)
                                        page.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        title = kktix_get_title_str(page, title)

                                        ''''''

                                        # 表演時間 list
                                        performance_datetimes_str_list = kktix_get_performance_list(page,
                                                                                                    performance_datetimes_str_list)

                                        ''''''

                                        # 地點 str
                                        location = kktix_get_location_str(page, location)

                                        ''''''

                                        page.go_back()

                                        if title or performance_datetimes_str_list or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_counter_index = i
                                            print(f'finished {page_index}-{last_finished_counter_index + 1}')
                                            print('\n----------------------\n')
                                        else:
                                            # with open('sold_out.txt', 'a', encoding='utf-*') as f:
                                            #     f.write(page.url + '\n')

                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_counter_index = i
                                            print(
                                                f'no tit, no pdt, no loc, skip\nfinished {page_index}-{last_finished_counter_index + 1}\n\n----------------------\n')
                                    else:
                                        print('hk activity, skip')
                                        last_finished_counter_index = i
                                        print(f'finished {page_index}-{last_finished_counter_index + 1}')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_counter_index = i
                                    print(f'finished {page_index}-{last_finished_counter_index + 1}')
                                    print('\n----------------------\n')
                                    # integrate_webs.append(page.url)

                                ''''''

                                page.go_back()  # main page
                                type_counter = page.query_selector_all('li.type-counter')
                        else:
                            print('CSS: "type-counter" of this page is already finished!')

                        ''''''

                        # 完成此頁
                        pagination_div = page.query_selector(".pagination.pull-right")
                        text = pagination_div.inner_text()
                        print(f'\nFinished page {page_index}')
                        completed_pages.append(page_index)
                        last_finished_selling_index = -1
                        last_finished_view_index = -1
                        last_finished_counter_index = -1

                    # 有下一頁
                    if '›' in text:
                        if int(page.locator(
                                "body > div.wrapper > div.page-content > section.explore-container.container > div > div.pagination.pull-right > ul > li.active > a").inner_text()) > 7:
                            break
                        page.locator("div.pagination.pull-right li:last-child").click()
                        page_index += 1
                        current_page_index = page_index
                        print(f'\nGo to page {page_index}\n')

                    # 最後一頁
                    else:
                        print(f'{website} finished')

                        # 程式確認沒有最後一頁後跳出while True的break
                        break

                # 確認全部執行完成，沒有發生錯誤的break
                break

            except Exception as e:
                # 錯誤
                page.close()
                print(e, f'{website} restart')
                if [current_page_index, last_finished_selling_index, last_finished_view_index] not in fail_indices:
                    fail_indices.append([current_page_index, last_finished_selling_index, last_finished_view_index])
                    print('第一次失敗')
                else:
                    print('第二次失敗')
                    print('跳過')

                    if last_finished_view_index == -1:
                        last_finished_selling_index += 1
                    else:
                        last_finished_view_index += 1

                    write_error(website, page.url, e)

                # 重新啟動
                continue

        # 完成
        page.close()


def get_kktix_third(website, json_filename, txt_filename):
    # global integrate_webs
    # page 9, 10, 11 ...
    with sync_playwright() as p:

        with open(json_filename, 'w', encoding='utf-8') as f:
            f.write('')

            # 待會會從 last_finished_index + 1開始
            last_finished_selling_index = -1
            last_finished_view_index = -1
            last_finished_counter_index = -1
            # 完成的演唱會頁面
            completed_pages = []
            # 發生錯誤的演唱會活動
            current_page_index = -1
            fail_indices = []
            # 統整的網站

        while True:
            try:
                browser = p.chromium.launch(headless=True)  # kktix thrid
                # browser = p.chromium.launch(headless=False)  # kktix thrid
                context = browser.new_context()
                page = context.new_page()
                # page.set_default_timeout(60000)

                ''''''

                page.goto("https://kktix.com/events?end_at=&"
                          "event_tag_ids_in=1&max_price=&"
                          "min_price=&page=9"
                          "&search=&start_at=")

                print(f'{website} start!')

                ''''''

                page_index = 9
                current_page_index = page_index

                while True:
                    if page_index in completed_pages:
                        print(f'Error occurred, but page {page_index} is already finished!')

                    else:
                        # type-selling
                        type_selling = page.query_selector_all('li.type-selling')
                        if last_finished_selling_index != len(type_selling) - 1:
                            print(f'\n\nselling start from {page_index}-{last_finished_selling_index + 2}\n\n')
                            for i in range(last_finished_selling_index + 1, len(type_selling)):
                                print(f'{website} selling progress - page {page_index}, {i + 1}/{len(type_selling)}')
                                # print(f'selling {page_index}-{i}')
                                # 演唱會頁面
                                type_selling[i].click()
                                print('concert page', page.url)
                                page.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str_list = []
                                prices = []
                                performance_datetimes_str_list = []
                                location = ''
                                if page.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        sell_datetimes_str_list = kktix_get_ticketing_time_list(page, j,
                                                                                                sell_datetimes_str_list)

                                        ''''''

                                        # 票價 list
                                        prices = kktix_get_prices_list(page, j, prices)

                                        ''''''

                                        # 內文
                                        inner_text = page.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page.url)
                                        page.wait_for_timeout(1500)
                                        page.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        title = kktix_get_title_str(page, title)

                                        ''''''

                                        # 表演時間 list
                                        performance_datetimes_str_list = kktix_get_performance_list(page,
                                                                                                    performance_datetimes_str_list)

                                        ''''''

                                        # 地點 str
                                        location = kktix_get_location_str(page, location)

                                        ''''''

                                        page.go_back()

                                        if title or performance_datetimes_str_list or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_selling_index = i
                                            print(f'finished {page_index}-{last_finished_selling_index + 1}')
                                            print('\n----------------------\n')
                                        else:
                                            # with open('sold_out.txt', 'a', encoding='utf-*') as f:
                                            #     f.write(page.url + '\n')

                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_selling_index = i
                                            print(
                                                f'no tit, no pdt, no loc, skip\nfinished {page_index}-{last_finished_selling_index + 1}\n\n----------------------\n')
                                    else:
                                        print('hk activity, skip')
                                        last_finished_selling_index = i
                                        print(f'finished {page_index}-{last_finished_selling_index + 1}')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_selling_index = i
                                    print(f'finished {page_index}-{last_finished_selling_index + 1}')
                                    print('\n----------------------\n')
                                    # integrate_webs.append(page.url)

                                ''''''

                                page.go_back()  # main page
                                type_selling = page.query_selector_all('li.type-selling')
                        else:
                            print('CSS: "type-selling" of this page is already finished!')

                        # type-view
                        type_view = page.query_selector_all('li.type-view')
                        if last_finished_view_index != len(type_view) - 1:
                            print(f'\n\nview start from {page_index}-{last_finished_view_index + 2}\n\n')
                            for i in range(last_finished_view_index + 1, len(type_view)):
                                print(f'{website} view progress - page {page_index}, {i + 1}/{len(type_view)}')
                                # print(f'view {page_index}-{i}')
                                # 演唱會頁面
                                type_view[i].click()
                                print('concert page', page.url)
                                page.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str_list = []
                                prices = []
                                performance_datetimes_str_list = []
                                location = ''
                                if page.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        sell_datetimes_str_list = kktix_get_ticketing_time_list(page, j,
                                                                                                sell_datetimes_str_list)

                                        ''''''

                                        # 票價 list
                                        prices = kktix_get_prices_list(page, j, prices)

                                        ''''''

                                        # 內文
                                        inner_text = page.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page.url)
                                        page.wait_for_timeout(1500)
                                        page.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        title = kktix_get_title_str(page, title)

                                        ''''''

                                        # 表演時間 list
                                        performance_datetimes_str_list = kktix_get_performance_list(page,
                                                                                                    performance_datetimes_str_list)

                                        ''''''

                                        # 地點 str
                                        location = kktix_get_location_str(page, location)

                                        ''''''

                                        page.go_back()

                                        if title or performance_datetimes_str_list or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_view_index = i
                                            print(f'finished {page_index}-{last_finished_view_index + 1}\n')
                                            print('\n----------------------\n')
                                        else:
                                            # with open('sold_out.txt', 'a', encoding='utf-*') as f:
                                            #     f.write(page.url + '\n')

                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_view_index = i
                                            print(
                                                f'no tit, no pdt, no loc, skip\nfinished {page_index}-{last_finished_view_index + 1}\n\n----------------------\n')
                                    else:
                                        print('hk activity, skip')
                                        last_finished_view_index = i
                                        print(f'finished {page_index}-{last_finished_view_index + 1}\n')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_view_index = i
                                    print(f'finished {page_index}-{last_finished_view_index + 1}\n')
                                    print('\n----------------------\n')
                                    # integrate_webs.append(page.url)

                                ''''''

                                page.go_back()  # main page
                                type_view = page.query_selector_all('li.type-view')
                        else:
                            print('CSS: "type-view" of this page is already finished!')

                        # type-counter
                        type_counter = page.query_selector_all('li.type-counter')
                        if last_finished_counter_index != len(type_counter) - 1:
                            print(f'\n\ncounter start from {page_index}-{last_finished_counter_index + 2}\n\n')
                            for i in range(last_finished_counter_index + 1, len(type_counter)):
                                print(f'{website} counter progress - page {page_index}, {i + 1}/{len(type_counter)}')
                                # print(f'counter {page_index}-{i}')
                                # 演唱會頁面
                                type_counter[i].click()
                                print('concert page', page.url)
                                page.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str_list = []
                                prices = []
                                performance_datetimes_str_list = []
                                location = ''
                                if page.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        sell_datetimes_str_list = kktix_get_ticketing_time_list(page, j,
                                                                                                sell_datetimes_str_list)

                                        ''''''

                                        # 票價 list
                                        prices = kktix_get_prices_list(page, j, prices)

                                        ''''''

                                        # 內文
                                        inner_text = page.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page.url)
                                        page.wait_for_timeout(1500)
                                        page.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        title = kktix_get_title_str(page, title)

                                        ''''''

                                        # 表演時間 list
                                        performance_datetimes_str_list = kktix_get_performance_list(page,
                                                                                                    performance_datetimes_str_list)

                                        ''''''

                                        # 地點 str
                                        location = kktix_get_location_str(page, location)

                                        ''''''

                                        page.go_back()

                                        if title or performance_datetimes_str_list or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_counter_index = i
                                            print(f'finished {page_index}-{last_finished_counter_index + 1}')
                                            print('\n----------------------\n')
                                        else:
                                            # with open('sold_out.txt', 'a', encoding='utf-*') as f:
                                            #     f.write(page.url + '\n')

                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url,
                                                'pin': page.url + str(0),
                                                'tim': str(datetime.now())
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_counter_index = i
                                            print(
                                                f'no tit, no pdt, no loc, skip\nfinished {page_index}-{last_finished_counter_index + 1}\n\n----------------------\n')
                                    else:
                                        print('hk activity, skip')
                                        last_finished_counter_index = i
                                        print(f'finished {page_index}-{last_finished_counter_index + 1}')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_counter_index = i
                                    print(f'finished {page_index}-{last_finished_counter_index + 1}')
                                    print('\n----------------------\n')
                                    # integrate_webs.append(page.url)

                                ''''''

                                page.go_back()  # main page
                                type_counter = page.query_selector_all('li.type-counter')
                        else:
                            print('CSS: "type-counter" of this page is already finished!')

                        ''''''

                        # 完成此頁
                        pagination_div = page.query_selector(".pagination.pull-right")
                        text = pagination_div.inner_text()
                        print(f'\nFinished page {page_index}')
                        completed_pages.append(page_index)
                        last_finished_selling_index = -1
                        last_finished_view_index = -1
                        last_finished_counter_index = -1

                    # 有下一頁
                    if '›' in text:
                        page.locator("div.pagination.pull-right li:last-child").click()
                        page_index += 1
                        current_page_index = page_index
                        print(f'\nGo to page {page_index}\n')

                    # 最後一頁
                    else:
                        print(f'{website} finished')

                        # 程式確認沒有最後一頁後跳出while True的break
                        break

                # 確認全部執行完成，沒有發生錯誤的break
                break

            except Exception as e:
                # 錯誤
                page.close()
                print(e, f'{website} restart')
                if [current_page_index, last_finished_selling_index, last_finished_view_index] not in fail_indices:
                    fail_indices.append([current_page_index, last_finished_selling_index, last_finished_view_index])
                    print('第一次失敗')
                else:
                    print('第二次失敗')
                    print('跳過')

                    if last_finished_view_index == -1:
                        last_finished_selling_index += 1
                    else:
                        last_finished_view_index += 1

                    write_error(website, page.url, e)

                # 重新啟動
                continue

        # 完成
        page.close()


def merge_json_data(json_filenames, final_json_file):
    merged_data = []

    for file in json_filenames:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            merged_data.extend(data)

        with open(final_json_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=4, ensure_ascii=False)


def get_kktix(website, json_filename, txt_filename):
    thread_first = threading.Thread(target=get_kktix_first, args=(website, 'kktix1.json', 'kktix1_temp.txt'))
    thread_second = threading.Thread(target=get_kktix_second, args=(website, 'kktix2.json', 'kktix2_temp.txt'))
    thread_third = threading.Thread(target=get_kktix_third, args=(website, 'kktix3.json', 'kktix3_temp.txt'))

    thread_first.start()
    thread_second.start()
    thread_third.start()

    thread_first.join()
    thread_second.join()
    thread_third.join()

    print('--- 3 KKTIX Scraping Threads Finished!! ---')

    kktix_json_files = ['kktix1.json', 'kktix2.json', 'kktix3.json']
    merge_json_data(kktix_json_files, json_filename)

    delete_blank_sdt(website, json_filename)

    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    delete_titles = ["【免費索票體驗】KKTIX 虛擬活動票務系統，搭配外部串流平台",
                     "【免費索票體驗】KKTIX Live，一站式售票、觀賞活動超流暢",
                     "【免費體驗】KKTIX Live，外部售票系統，輸入兌換碼馬上開播"]

    new_data = [item for item in data if item['tit'] not in delete_titles]
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)

    # delete_past_ticketing_time(website, json_filename)

    for json_filename in kktix_json_files:
        os.remove(json_filename)


def threads_start():
    thread_era.start()
    thread_livenation.start()
    thread_indievox.start()
    thread_kktix.start()
    threading_ticketplus.start()


def threads_join():
    thread_era.join()
    thread_indievox.join()
    thread_kktix.join()
    thread_livenation.join()
    threading_ticketplus.join()


# def threads_integration():
#     merged_data = []
#     for json_file in json_new:
#         with open(json_file, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#             merged_data.extend(data)
#     with open('concert_data_new_zh.json', 'w', encoding='utf-8') as f:
#         json.dump(merged_data, f, indent=4, ensure_ascii=False)


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
    print("New Concert information:")
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


def delete_files(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. 刪除kktix那三個不需要的資料
    # delete_titles = ["【免費索票體驗】KKTIX 虛擬活動票務系統，搭配外部串流平台",
    #                  "【免費索票體驗】KKTIX Live，一站式售票、觀賞活動超流暢",
    #                  "【免費體驗】KKTIX Live，外部售票系統，輸入兌換碼馬上開播"]
    # new_data = [item for item in data if item['tit'] not in delete_titles]

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)


def json_new_to_old():
    # # 打开旧的中文数据文件，读取内容并加载到 old_data 变量中
    # with open('concert_data_old_zh.json', 'r', encoding='utf-8') as old_file:
    #     old_data = json.load(old_file)

    # 打开新的中文数据文件，读取内容并加载到 new_data 变量中
    with open('concert_data_new_zh.json', 'r', encoding='utf-8') as new_file:
        new_data = json.load(new_file)

    # 将新的中文数据写入旧的中文数据文件，格式化并确保不使用 ASCII 编码
    with open('concert_data_old_zh.json', 'w', encoding='utf-8') as old_file:
        json.dump(new_data, old_file, indent=4, ensure_ascii=False)

    # 打开新的中文数据文件，以写入模式清空文件内容
    with open('concert_data_new_zh.json', 'w', encoding='utf-8') as new_file:
        new_file.write('[]')

    # # 打开旧的英文数据文件，读取内容并加载到 old_data 变量中
    # with open('concert_data_old_en.json', 'r', encoding='utf-8') as old_file:
    #     old_data = json.load(old_file)

    # 打开新的英文数据文件，读取内容并加载到 new_data 变量中
    with open('concert_data_new_en.json', 'r', encoding='utf-8') as new_file:
        new_data = json.load(new_file)

    # 将新的英文数据写入旧的英文数据文件，格式化并确保不使用 ASCII 编码
    with open('concert_data_old_en.json', 'w', encoding='utf-8') as old_file:
        json.dump(new_data, old_file, indent=4, ensure_ascii=False)

    # 打开新的英文数据文件，以写入模式清空文件内容
    with open('concert_data_new_en.json', 'w', encoding='utf-8') as new_file:
        new_file.write('[]')


def each_concert_number():  # 驗算用
    with open('era.json', 'r', encoding='utf-8') as f:
        era_data = json.load(f)
    with open('indievox.json', 'r', encoding='utf-8') as f:
        indievox_data = json.load(f)
    with open('kktix.json', 'r', encoding='utf-8') as f:
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


def reset_failure_log():
    with open('failure_log.txt', 'w', encoding='utf-8') as f:
        f.write('')


def move_concert_files(concert_json_filenames):
    for concert_json_file in concert_json_filenames:
        source_file = concert_json_file
        target_folder = 'concert_json_files'

        # 检查目标文件是否存在，如果存在，删除它
        if os.path.exists(os.path.join(target_folder, source_file)):
            os.remove(os.path.join(target_folder, source_file))

        # 使用shutil.move()函数来移动文件
        shutil.move(source_file, target_folder)


def load_table_from_txt(filename):
    zh_table = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            key, value = line.strip().split(':')
            zh_table[key] = value
    return zh_table


def stadium_city(stadium, lang, table):
    # 先把stadium的字串做處理 小寫 + 去除空格
    stadium = stadium.lower()
    stadium = stadium.replace(' ', '')
    # 中文
    if lang == 'zh':
        best_match, score = process.extractOne(stadium, table.keys())
        # 閥值設為80
        if score > 80:
            print('score', score)
            return table[best_match]
        # 沒超過代表找不到
        else:
            return ''


# def get_city_from_stadium():
#     json_file = 'concert_data_new_zh.json'  # 最新獲得的演唱會json
#     zh_table = "zh_stadium_table.txt"  # 使用中文對照表
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)  # city from search
#         # browser = p.chromium.launch(headless=False)  # city from search
#         context = browser.new_context()
#         page = context.new_page()
#
#         with open(json_file, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#
#         for i in range(len(data)):
#             if data[i]['loc'] == [] or data[i]['loc'] == ['']:
#                 print('是空白的就直接跳過')
#             else:
#                 print(i)
#                 city = ''
#                 location = data[i]['loc'][0]
#                 print('location', location)
#                 # string (從名稱裡面找到城市名稱)
#                 for j in range(len(zh_cities)):
#                     # 臺 -> 台
#                     location = location.replace('臺', '台')
#                     # 如果字串裡面就包含了城市的名稱
#                     if zh_cities[j] in location:
#                         # 就可以直接找到城市
#                         print('從名稱就找到城市')
#                         city = zh_cities[j]
#                         break
#
#                 # table (如果名稱裡面沒有城市名稱，就去table裡面尋找)
#                 if city == '':
#                     print('table!')
#                     # 使用table對照表尋找看看
#                     city = stadium_city(location, 'zh', load_table_from_txt(zh_table))
#
#                 # playwright (如果連table裡面也沒有找到)
#                 if city == '':
#                     print('playwright!')
#                     # 那就靠網路爬蟲來尋找並加入table
#                     page.goto("https://www.google.com/")
#                     # fill完成之後會顯示搜尋結果
#                     page.locator("#APjFqb").fill(location)
#
#                     page.wait_for_timeout(1500)
#
#                     # 迴圈 全部的搜尋結果 只要出現城市名稱就跳出迴圈
#                     contents = page.query_selector_all(".G43f7e .lnnVSe .ClJ9Yb > span")
#                     # 搜尋結果有沒有顯示城市名稱
#                     for k in range(len(contents)):
#                         for zh_city in zh_cities:
#                             if zh_city in contents[k].inner_text():
#                                 city = zh_city
#                                 print(f'搜尋結果頁面就有城市了! {city}')
#                                 break
#
#                     # 如果搜尋結果裡面沒有出現城市名稱，那就要進一步去下一個頁面尋找
#                     if city == '':
#                         print('搜尋結果沒有出現城市 必須往下一頁面繼續尋找')
#                         # do something
#                         page.keyboard.press('Enter')
#                         page.wait_for_timeout(1500)
#
#                         address_phone = page.query_selector_all(".zloOqf.PZPZlf .LrzXr")
#                         for k in range(len(address_phone)):
#                             for zh_city in zh_cities:
#                                 if zh_city in address_phone[k].inner_text():
#                                     city = zh_city
#                                     print(f'右側面板找到城市了! {city}')
#                                     break
#
#                         if city == '':
#                             print('還是沒有找到 看一下第一個搜尋結果 看看有沒有東西')
#                             search_results = page.query_selector_all(".MjjYud")
#                             for zh_city in zh_cities:
#                                 if zh_city in search_results[0].inner_text():
#                                     city = zh_city
#                                     break
#                             if city == '':
#                                 print('真的找不到')
#                             else:
#                                 with open(zh_table, 'a', encoding='utf-8') as f:
#                                     f.write(f"{location.lower().replace(' ', '')}:{city}\n")
#
#                         # 有找到 把配對寫進table裡面
#                         else:
#                             if page.locator(".DoxwDb .PZPZlf").is_visible():
#                                 print(page.locator(".DoxwDb .PZPZlf").inner_text())
#                                 with open(zh_table, 'a', encoding='utf-8') as f:
#                                     f.write(f"{page.locator('.DoxwDb .PZPZlf').inner_text()}:{city}\n")
#                             with open(zh_table, 'a', encoding='utf-8') as f:
#                                 f.write(f"{location.lower().replace(' ', '')}:{city}\n")
#
#                     # 搜尋結果有找到城市 把這個配對寫進table裡面
#                     else:
#                         # 把這次網路爬蟲找到的stadium & city寫進table裡面
#                         print(f"寫入新資料! {location} & {city}")
#                         location = location.lower()
#                         location = location.replace(' ', '')
#                         with open(zh_table, 'a', encoding='utf-8') as f:
#                             f.write(f"{location}:{city}\n")
#
#                 print(city)
#                 data[i]['cit'] = city
#                 with open(json_file, 'w', encoding='utf-8') as f:
#                     json.dump(data, f, indent=4, ensure_ascii=False)
#                 print('---')
def get_city_from_stadium(json_file):
    zh_table = "zh_stadium_table.txt"  # 使用中文對照表
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # city from search
        # browser = p.chromium.launch(headless=False)  # city from search
        context = browser.new_context()
        page = context.new_page()

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for i in range(len(data)):
            if data[i]['loc'] == [] or data[i]['loc'] == ['']:
                print('是空白的就直接跳過')
            else:
                print(i)
                city = ''
                location = data[i]['loc'][0]
                print('location', location)
                # string (從名稱裡面找到城市名稱)
                for j in range(len(zh_cities)):
                    # 臺 -> 台
                    location = location.replace('臺', '台')
                    # 如果字串裡面就包含了城市的名稱
                    if zh_cities[j] in location:
                        # 就可以直接找到城市
                        print('從名稱就找到城市')
                        city = zh_cities[j]
                        break

                # table (如果名稱裡面沒有城市名稱，就去table裡面尋找)
                if city == '':
                    print('table!')
                    # 使用table對照表尋找看看
                    city = stadium_city(location, 'zh', load_table_from_txt(zh_table))

                # playwright (如果連table裡面也沒有找到)
                if city == '':
                    print('playwright!')
                    # 那就靠網路爬蟲來尋找並加入table
                    page.goto("https://www.google.com/")
                    # fill完成之後會顯示搜尋結果
                    page.locator("#APjFqb").fill(location)

                    page.wait_for_timeout(1500)

                    # 迴圈 全部的搜尋結果 只要出現城市名稱就跳出迴圈
                    contents = page.query_selector_all(".G43f7e .lnnVSe .ClJ9Yb > span")
                    # 搜尋結果有沒有顯示城市名稱
                    for k in range(len(contents)):
                        for zh_city in zh_cities:
                            if zh_city in contents[k].inner_text():
                                city = zh_city
                                print(f'搜尋結果頁面就有城市了! {city}')
                                break

                    # 如果搜尋結果裡面沒有出現城市名稱，那就要進一步去下一個頁面尋找
                    if city == '':
                        print('搜尋結果沒有出現城市 必須往下一頁面繼續尋找')
                        # do something
                        page.keyboard.press('Enter')
                        page.wait_for_timeout(1500)

                        address_phone = page.query_selector_all(".zloOqf.PZPZlf .LrzXr")
                        for k in range(len(address_phone)):
                            for zh_city in zh_cities:
                                if zh_city in address_phone[k].inner_text():
                                    city = zh_city
                                    print(f'右側面板找到城市了! {city}')
                                    break

                        if city == '':
                            print('還是沒有找到 看一下第一個搜尋結果 看看有沒有東西')
                            search_results = page.query_selector_all(".MjjYud")
                            for zh_city in zh_cities:
                                if zh_city in search_results[0].inner_text():
                                    city = zh_city
                                    break
                            if city == '':
                                print('真的找不到')
                            else:
                                with open(zh_table, 'a', encoding='utf-8') as f:
                                    f.write(f"{location.lower().replace(' ', '')}:{city}\n")

                        # 有找到 把配對寫進table裡面
                        else:
                            if page.locator(".DoxwDb .PZPZlf").is_visible():
                                print(page.locator(".DoxwDb .PZPZlf").inner_text())
                                with open(zh_table, 'a', encoding='utf-8') as f:
                                    f.write(f"{page.locator('.DoxwDb .PZPZlf').inner_text()}:{city}\n")
                            with open(zh_table, 'a', encoding='utf-8') as f:
                                f.write(f"{location.lower().replace(' ', '')}:{city}\n")

                    # 搜尋結果有找到城市 把這個配對寫進table裡面
                    else:
                        # 把這次網路爬蟲找到的stadium & city寫進table裡面
                        print(f"寫入新資料! {location} & {city}")
                        location = location.lower()
                        location = location.replace(' ', '')
                        with open(zh_table, 'a', encoding='utf-8') as f:
                            f.write(f"{location}:{city}\n")

                print(city)
                data[i]['cit'] = city
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                print('---')


def zh_to_en():
    pass


def zh_en():
    city_mapping = dict(zip(zh_cities, en_cities))
    # Copying the original file to a new file for translated content
    shutil.copy('concert_data_new_zh.json', 'concert_data_new_en.json')

    translator = Translator()

    # Open the copied file for reading and translation
    with open('concert_data_new_en.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i in range(len(data)):
        print(f'current progress {i + 1}/{len(data)}')

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

        if 'cit' in data[i]:
            if data[i]['cit'] in city_mapping:
                data[i]['cit'] = city_mapping[data[i]['cit']]
                print(data[i]['cit'])

                # with open('concert_test.json', 'w', encoding='utf-8') as f:
                #     json.dump(data, f, indent=4, ensure_ascii=False)

        print('------------------------------------')

    # Write the translated data back to the file
    with open('concert_data_new_en.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


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


def json_in_order(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Sort the data by the earliest date found in the 'pdt' field
    sorted_data = sorted(data, key=lambda x: extract_earliest_date(x['pdt']))

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=4)


def price_str_to_int(json_filename):
    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i in range(len(data)):
        for index, price in enumerate(data[i]['prc']):
            if isinstance(price, str):
                # print(data[i]['prc'])
                try:
                    data[i]['prc'][index] = int(price)
                    with open(json_filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                except:
                    pass

def price_in_order(json_filename):
    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

        for i in range(len(data)):
            data[i]['prc'] = sorted(data[i]['prc'], reverse=True)
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

def get_latest_concert_info(json_filename):
    reset_failure_log()
    threads_start()  # start the threads
    threads_join()  # wait for all the threads finish
    print('--- Playwright finished ---')
    merge_json_data(concert_json_filenames, json_filename)  # combine all the website json file into the second argument
    print('--- Json merged ---')
    move_concert_files(concert_json_filenames)  # move each website json file to folder "concert_json_files"
    print('--- Json moved ---')
    # delete_files(concert_today)  # nothing to be deleted right now, can uncomment it in the future
    # print('--- Files deleted ---')
    get_city_from_stadium(json_filename)  # open the json file, and fill it the city according to the address
    print('--- Get all city ---')
    json_in_order(json_filename)  # sort the json file according performance time
    print('--- Json in order ---')
    price_str_to_int(json_filename)  # price, if str -> int
    print('--- Replaced str with int for all str! ---')
    price_in_order(json_filename)  # price in order, start from the most highest price
    print('--- Price in order ---')
    # delete_past_ticketing_time(concert_all_data)  # delete past ticketing time
    # print('--- Delete all past ticketing time ---')
    print(f'\n------------------\nzh okay!\n------------------\n')
    ''' new, old, changed concert '''
    # to do
    ''' zh to en '''
    # to do with zh_en() function
    ''' delete old json file and move new json file as old json file '''
    # to do with json_new_to_old()


thread_era = threading.Thread(target=get_era, args=('era', 'era.json', 'era_temp.txt'))
thread_livenation = threading.Thread(target=get_livenation,
                                     args=('Live Nation', 'livenation.json', 'livenation_temp.txt'))
thread_indievox = threading.Thread(target=get_indievox, args=('Indievox', 'indievox.json', 'indievox_temp.txt'))
threading_ticketplus = threading.Thread(target=get_ticketplus,
                                        args=('Ticket Plus', 'ticketplus.json', 'ticketplus_temp.txt'))
thread_kktix = threading.Thread(target=get_kktix, args=('KKTIX', 'kktix.json', "kktix_temp.txt"))

''''''

get_latest_concert_info(concert_today)

''''''



# get_era('era', 'era.json', 'era_temp.txt')
# get_era_without_error_mechanism('era', 'era.json', 'era_temp.txt')
# get_livenation('Live Nation', 'livenation.json', 'livenation_temp.txt')
# get_indievox('Indievox', 'indievox.json', 'indievox_temp.txt')
# get_ticketplus('Ticket Plus', 'ticketplus.json', 'ticketplus_temp.txt')
# get_kktix('KKTIX', 'kktix.json', "kktix_temp.txt")

''''''

# thread_kktix.start()
# 沒有地址
# era
# indievox
# live nation

# 有地址
# kktix
# ticketplus

# def get_kktix_first1(website, json_filename, txt_filename):
#     # global integrate_webs
#     with sync_playwright() as p:
#         # browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#
#         page.goto("https://kktix.com/events/452dac5f-copy-1/registrations/new")
#
#         location = ''
#         address = ''
#         # 地點 str
#         location, address = kktix_get_location_str1(page, location, address)
#         print(location)
#         print(address)
