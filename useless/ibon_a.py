# 原本這版本是OK的 但是ibon的網站結構改變了 因此目前使用的是B版本
from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import re, os, json
from datetime import datetime, time
import os, sys
from get_data_from_text import get_prices, get_time_lines, get_sell, get_performance_location

# 如果沒有內文的格式，就跳過不加入
# 如果售票時間是過去就為空

json_filename = 'ibon_new.json'
txt_filename = 'ibon_temp.txt'


def get_ibon():
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
                context_ibon = browser.new_context()
                page_ibon = context_ibon.new_page()

                page_ibon.goto("https://ticket.ibon.com.tw/Index/entertainment")

                events = page_ibon.query_selector_all("#content > div > div.container > div:nth-child(2) > div.event-slider.owl-carousel.owl-theme.owl-loaded.owl-drag > div.owl-stage-outer > div > div")  # 獲得各個演場會的物件

                for i in range(last_finished_index + 1, len(events)):
                    print(f'ibon progress - {i + 1}/{len(events)}')
                    events[i].click()  # 資訊 & 售票頁面
                    page_ibon.wait_for_load_state('load')
                    page_ibon.wait_for_timeout(500)

                    # 檢查是否能讀取內文
                    if page_ibon.locator("#detall_info_1 > div").is_visible():
                        # 下載內文
                        with open(txt_filename, 'w', encoding='utf-8') as f:
                            f.write(page_ibon.locator("#detall_info_1 > div").inner_text())
                        # # demo text
                        # with open(f'demo_ibon{i}.txt', 'w', encoding='utf-8') as f:
                        #     f.write(page_ibon.locator("#detall_info_1 > div").inner_text())
                        # 讀取內文
                        with open(txt_filename, 'r', encoding='utf-8') as f:
                            lines = f.readlines()

                        # 票價 (一定得從內文當中獲得)
                        prices = get_prices(lines)

                        # 有購票時間就可以獲得表演時間、地點、售票時間
                        try:
                            # 有購票按鈕
                            if page_ibon.wait_for_selector("#GameInfoList > div > div > p", timeout=1500).is_visible():
                                pass

                            for i in range(
                                    len(page_ibon.query_selector_all("#GameInfoList div.col-12.grid"))):  # 有幾個購票按紐 (方塊)
                                # 標題 str
                                title = page_ibon.locator("#GameInfoList > div").nth(i).locator("div > p").nth(
                                    1).inner_text()
                                print(title)

                                # 表演時間 str
                                performance_d = re.findall(r"\d{4}/\d{1,2}/\d{1,2}",
                                                           page_ibon.locator("#GameInfoList > div").nth(i).locator(
                                                               "div > p").nth(0).inner_text())
                                performance_t = re.findall(r"\d{1,2}:\d{2}",
                                                           page_ibon.locator("#GameInfoList > div").nth(i).locator(
                                                               "div > p").nth(0).inner_text())
                                performance_datetime = performance_d[0] + ' ' + performance_t[0]
                                print(performance_datetime)

                                # 地點 str
                                location = page_ibon.locator("#GameInfoList > div").nth(i).locator("div > p").nth(
                                    2).inner_text()
                                print(location)

                                # 售票時間 str
                                sell_dt = page_ibon.locator("#GameInfoList > div").nth(i).locator("div > p").nth(
                                    3).inner_text()
                                if '開始' in sell_dt:
                                    sell_d = re.findall(r"\d{4}/\d{1,2}/\d{1,2}",
                                                        page_ibon.locator("#GameInfoList > div").nth(i).locator(
                                                            "div > p").nth(3).inner_text())
                                    sell_t = re.findall(r"\d{1,2}:\d{2}",
                                                        page_ibon.locator("#GameInfoList > div").nth(i).locator(
                                                            "div > p").nth(3).inner_text())
                                    sell_datetime = sell_d[0] + ' ' + sell_t[0]
                                else:
                                    sell_datetime = ''
                                print(sell_datetime)

                                ''''''

                                print('tit', title)
                                print('sdt', sell_datetime)  # str
                                print('prc', prices)  # list
                                print('pdt', performance_datetime)  # str
                                print('loc', location)  # str

                                new_data = {
                                    'tit': title,
                                    'sdt': [sell_datetime],
                                    'prc': prices,
                                    'pdt': [performance_datetime],
                                    'loc': [location],
                                    'web': 'ibon',
                                    'url': page_ibon.url
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
                                if page_ibon.url in fail_urls:
                                    del fail_urls[fail_urls.index(page_ibon.url)]

                                print()

                        except Exception as e:
                            # 沒有購票按紐，需要先從內文爬取相關的資訊
                            print('沒有按紐')
                            # 標題 str
                            title = page_ibon.locator(
                                "#content > div > div > div.single-header > div > div.col-lg-5.pl-lg-0 > div > h1").inner_text()
                            # 售票時間 str
                            without_sell_time_lines, sell_datetimes = get_sell(get_time_lines(lines))
                            # 表演時間 list, 地點 list
                            performance_datetimes, locations = get_performance_location(without_sell_time_lines)

                            ''''''

                            print('tit', title)
                            print('sdt', sell_datetimes)  # list
                            print('prc', prices)  # list
                            print('pdt', performance_datetimes)  # list
                            print('loc', locations)  # list

                            new_data = {
                                'tit': title,
                                'sdt': sell_datetimes,
                                'prc': prices,
                                'pdt': performance_datetimes,
                                'loc': locations,
                                'web': 'ibon',
                                'url': page_ibon.url
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
                            if page_ibon.url in fail_urls:
                                del fail_urls[fail_urls.index(page_ibon.url)]

                        page_ibon.go_back()  # 主頁面
                        events = page_ibon.query_selector_all("#content > div > div.container > div:nth-child(2) > "
                                                              "div.event-slider.owl-carousel.owl-theme.owl-loaded.owl-drag > "
                                                              "div.owl-stage-outer > div > div")
                    # 無法讀取到內文
                    else:
                        print('格式怪怪的 跳過')
                        print('\n---------------------\n')
                        page_ibon.go_back()  # 主頁面
                        events = page_ibon.query_selector_all("#content > div > div.container > div:nth-child(2) > "
                                                              "div.event-slider.owl-carousel.owl-theme.owl-loaded.owl-drag > "
                                                              "div.owl-stage-outer > div > div")
                # 完成
                page_ibon.close()
                os.remove(txt_filename)

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

                print('ibon done')
                break

            except Exception as e:
                # 錯誤
                print(e, 'ibon restart')
                print('last finished index = ', last_finished_index)
                if page_ibon.url not in fail_urls:
                    print('第一次失敗')
                    fail_urls.append(page_ibon.url)
                else:
                    print('第二次失敗')
                    print('跳過')
                    last_finished_index += 1

                    with open('../playwright/failure_log.txt', "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    if page_ibon.url + '\n' not in lines:
                        # txt檔案不存在或是裡面沒資料
                        if not os.path.exists('../playwright/failure_log.txt') or os.path.getsize(
                                '../playwright/failure_log.txt') <= 4:
                            # 直接寫入第一筆資料
                            with open('../playwright/failure_log.txt', "w", encoding="utf-8") as f:
                                f.write(f'ibon\n{e}\n{page_ibon.url}\n')
                        # txt檔案存在且裡面已經有一筆以上的資料
                        else:
                            # 讀取現在有的檔案
                            with open('../playwright/failure_log.txt', "a", encoding="utf-8") as f:
                                f.write(f'\nibon\n{e}\n{page_ibon.url}\n')
                    else:
                        print('已經寫進錯誤裡面了!')

                    print('ibon fail urls right now')
                    for url in fail_urls:
                        print(url)

                # 重頭開始
                continue

get_ibon()
