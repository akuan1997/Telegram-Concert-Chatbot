from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import re, os, json
from datetime import datetime, time
import os, sys

# 如果售票時間對於現在來說是過去，捨棄

json_filename = 'era_new.json'


def get_era():
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
                context_era = browser.new_context()
                page_era = context_era.new_page()
                page_era.set_default_timeout(10000)

                page_era.goto("https://ticket.com.tw/application/UTK01/UTK0101_06.aspx?TYPE=1&CATEGORY=205")

                # 獲得events物件以及數量 (有幾個活動)
                events = page_era.query_selector_all(".column.col-xs-12.col-md-3.moreBox")

                for i in range(last_finished_index + 1, len(events)):
                    print(f'era progress - {i + 1}/{len(events)}')
                    # 資訊頁面
                    events[i].click()

                    ''''''

                    # 內文
                    inner_text = page_era.locator("#ctl00_ContentPlaceHolder1_lbProgramInfo_Content").inner_text()

                    ''''''

                    page_era.locator("#ctl00_ContentPlaceHolder1_btnBuyNow").click()  # 進入售票頁面
                    page_era.wait_for_timeout(1500)

                    # 標題
                    title = page_era.locator("#ctl00_ContentPlaceHolder1_NAME").inner_text()

                    for j in range(len(page_era.query_selector_all(
                            "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr"))):  # 資訊方塊
                        # 表演日期
                        # 日期格式1
                        if page_era.locator(
                                "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                            j).locator("td > div > span > time").is_visible():
                            year_month = page_era.locator(
                                "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                                j).locator("td > div > span > time > strong").inner_text().replace(' - ',
                                                                                                   '/')
                            day = page_era.locator(
                                "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                                j).locator("td > div > span > time > span").nth(
                                0).inner_text()
                            t = page_era.locator(
                                "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                                j).locator(
                                "td > div > span > time > span").nth(1).inner_text()
                            performance_datetime = year_month + '/' + day + ' ' + t
                            print()
                        # 日期格式2
                        else:
                            # 1. 獲得日期 格式為 YYYY/MM/DD HH:MM
                            performance_datetime = page_era.locator(
                                "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                                j).locator(
                                "td > div > span").nth(0).inner_text() + ' ~ ' + page_era.locator(
                                "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                                j).locator(
                                "td > div > span").nth(1).inner_text().replace('|', '').replace('\n', '')
                            print()

                        ''''''

                        # 地點
                        location = page_era.locator(
                            "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                            j).locator(
                            "td").nth(1).locator("span").inner_text()

                        ''''''

                        # 票價
                        prices = []
                        prcs = page_era.locator(
                            "#portfolio > div.container > div:nth-child(4) > div > div > table > tbody > tr").nth(
                            j).locator(
                            "td").nth(2).locator("span").inner_text().split('、')
                        for prc in prcs:
                            prices.append(int(prc))  # 票價列表

                        ''''''

                        # 售票時間 (如果沒有售票時間，列表為空)
                        sell_button = page_era.locator(
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
                            'web': 'era',
                            'url': page_era.url
                        }

                        print('\n--- write new data ---\n')

                        # json檔案不存在或是裡面沒資料
                        if not os.path.exists(json_filename) or os.path.getsize(
                                json_filename) <= 4:
                            # 直接寫入第一筆資料
                            with open(json_filename, "w", encoding="utf-8") as f:
                                json.dump([new_data], f, indent=4, ensure_ascii=False)
                        # json檔案存在且裡面已經有一筆以上的資料
                        else:
                            # 讀取現在有的檔案
                            with open(json_filename, "r", encoding="utf-8") as f:
                                existing_data = json.load(f)
                            # 並新增即將寫入的一筆
                            existing_data.append(new_data)
                            # 寫入
                            with open(json_filename, "w", encoding="utf-8") as f:
                                json.dump(existing_data, f, indent=4, ensure_ascii=False)

                        last_finished_index = i
                        if page_era.url in fail_urls:
                            del fail_urls[fail_urls.index(page_era.url)]

                    # 資訊頁面
                    page_era.go_back()

                    # 主頁面
                    page_era.go_back()

                    # 重新獲取events屬性
                    events = page_era.query_selector_all(".column.col-xs-12.col-md-3.moreBox")

                # 完成
                page_era.close()

                with open(json_filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                for i in range(len(data)):
                    print('i =', i)
                    print(data[i]['tit'])
                    # 如果含有售票時間
                    if data[i]['sdt']:
                        sdts = [sdt for sdt in data[i]['sdt'] if sdt != '']
                        print('sdts', sdts)
                        data[i]['sdt'] = sdts
                        with open(json_filename, 'w', encoding='utf-8') as file:
                            json.dump(data, file, indent=4, ensure_ascii=False)

                print('era done')
                break

            except Exception as e:
                # 錯誤
                print(e, 'era restart')
                print('last finished index = ', last_finished_index)
                if page_era.url not in fail_urls:
                    print('第一次失敗')
                    fail_urls.append(page_era.url)
                else:
                    print('第二次失敗')
                    print('跳過')
                    last_finished_index += 1

                    with open('failure_log.txt', "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    if page_era.url + '\n' not in lines:
                        # txt檔案不存在或是裡面沒資料
                        if not os.path.exists('failure_log.txt') or os.path.getsize('failure_log.txt') <= 4:
                            # 直接寫入第一筆資料
                            with open('failure_log.txt', "w", encoding="utf-8") as f:
                                f.write(f'era\n{e}\n{page_era.url}\n')
                        # txt檔案存在且裡面已經有一筆以上的資料
                        else:
                            # 讀取現在有的檔案
                            with open('failure_log.txt', "a", encoding="utf-8") as f:
                                f.write(f'\nera\n{e}\n{page_era.url}\n')
                    else:
                        print('已經寫進錯誤裡面了!')

                    print('era fail urls right now')
                    for url in fail_urls:
                        print(url)

                # 重新啟動
                continue

# get_era()
