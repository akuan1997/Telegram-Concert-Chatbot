from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import re, os, json
from datetime import datetime
import time
from get_data_from_text import get_prices, get_time_lines, get_sell, get_performance_location
import os, sys

json_filename = 'indievox_new.json'
txt_filename = 'indievox_temp.txt'
timeout_seconds = 500


def get_indievox():
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
                context_indievox = browser.new_context()
                page_indievox = context_indievox.new_page()
                page_indievox.set_default_timeout(5000)

                page_indievox.goto(
                    "https://www.indievox.com/activity/list?type=table&startDate=2023%2F11%2F20&endDate=")

                # 只有程式執行的一開始會經過這裡
                if last_finished_index == -1 and all_event_numbers == -1:
                    while (page_indievox.locator("#activityListTab > table > tbody > tr > td > div > a").is_visible()):
                        page_indievox.keyboard.press('End')
                    all_events = page_indievox.query_selector_all("#activityListTab > table > tbody > tr")
                    all_event_numbers = len(all_events)
                    print(all_event_numbers, '\n')

                for i in range(last_finished_index + 1, all_event_numbers):
                    print(f'indievox progress - {i}/{all_event_numbers - 1}')

                    # 第一頁不需要讀取到最後 因此<19的都直接點擊就可以
                    if i > 19:
                        # 讀取到最下面 然後再點擊物件
                        while page_indievox.locator(
                                "#activityListTab > table > tbody > tr > td > div > a").is_visible():
                            page_indievox.locator(
                                "#activityListTab > table > tbody > tr > td > div > a").click()
                            page_indievox.keyboard.press('End')
                            page_indievox.wait_for_timeout(timeout_seconds)
                    all_events = page_indievox.query_selector_all("#activityListTab > table > tbody > tr")

                    # 如果物件標題可見
                    if page_indievox.locator("#activityListTab > table > tbody > tr").nth(i).locator("td").nth(
                            0).is_visible():
                        # 獲得時間
                        # time_line = page_indievox.locator("#activityListTab > table > tbody > tr").nth(i).locator(
                        #     "td").nth(0).inner_text()
                        # ds = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", time_line)
                        # print('ds', ds)

                        # 獲得標題
                        title = page_indievox.locator("#activityListTab > table > tbody > tr").nth(i).locator("td").nth(
                            1).inner_text()

                        # 獲得地點
                        location = page_indievox.locator("#activityListTab > table > tbody > tr").nth(i).locator(
                            "td").nth(2).inner_text()

                        # 點擊物件
                        page_indievox.locator(".fcLightBlue").nth(i).click()
                        page_indievox.wait_for_load_state('load')
                        page_indievox.wait_for_timeout(timeout_seconds)

                    # 下載內文
                    inner_text = page_indievox.locator("#intro").inner_text()
                    with open(txt_filename, 'w', encoding='utf-8') as f:
                        f.write(inner_text)

                    # # demo text
                    # with open(f'demo_indievox{i}.txt', 'w', encoding='utf-8') as f:
                    #     f.write(page_indievox.locator("#intro").inner_text())

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
                    if page_indievox.locator(".list-inline a.btn.btn-default.btn-lg").is_visible():
                        # 點擊購買按鈕
                        page_indievox.locator(".list-inline a.btn.btn-default.btn-lg").click()
                        page_indievox.wait_for_load_state('load')
                        page_indievox.wait_for_timeout(timeout_seconds)

                        # 有幾行資訊欄
                        for j in range(len(page_indievox.query_selector_all("#gameList > table > tbody > tr"))):
                            # 表演時間
                            performance_datetime = page_indievox.locator('#gameList > table > tbody > tr').nth(
                                j).locator('td').nth(
                                0).inner_text()
                            performance_datetime = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", performance_datetime)
                            performance_datetime = re.sub(r"\s{2,}", " ", performance_datetime)
                            performance_datetime = performance_datetime.strip()
                            # 地點
                            # location = page_indievox.locator("#gameList > table > tbody > tr").nth(j).locator("td").nth(
                            #     2).inner_text()

                            ''''''

                            # 沒票價 但有購票的按鈕 再往前一個頁面
                            if no_price and page_indievox.locator('#gameList > table > tbody > tr').nth(j).locator(
                                    'td > button').is_visible():
                                no_price = True
                                page_indievox.locator('#gameList > table > tbody > tr').nth(j).locator(
                                    'td > button').click()
                                page_indievox.wait_for_load_state('load')
                                page_indievox.wait_for_timeout(timeout_seconds)

                                for k in range(len(page_indievox.query_selector_all("#ticketPriceList > tbody > tr"))):
                                    price_line = re.sub(r',', '', page_indievox.locator("#ticketPriceList > tbody > tr").nth(k).locator("td.fcBlue > h4").inner_text())
                                    not_digit_index = 0
                                    for l in range(len(price_line) - 1, 0, -1):
                                        if not price_line[l].isdigit():
                                            not_digit_index = l
                                            break
                                    prices.append(price_line[not_digit_index + 1:])

                                    page_indievox.go_back()
                                    # 點擊購買按鈕
                                    page_indievox.locator(".list-inline a.btn.btn-default.btn-lg").click()
                                    page_indievox.wait_for_load_state('load')
                                    page_indievox.wait_for_timeout(timeout_seconds)

                            ''''''

                            print('tit', title)  # str
                            print('sdt', sell_datetimes_str)  # list
                            print('prc', prices)  # list
                            print('pdt', performance_datetime)  # str
                            print('loc', location)  # str
                            print('web', 'indievox')
                            print('url', page_indievox.url)

                            new_data = {
                                'tit': title,
                                'sdt': sell_datetimes_str,
                                'prc': prices,
                                'pdt': [performance_datetime],
                                'loc': [location],
                                'int': inner_text,
                                'web': 'indievox',
                                'url': page_indievox.url
                            }

                            print('\n--- write new data ---\n')

                            if no_price:
                                prices = []

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
                            if page_indievox.url in fail_urls:
                                del fail_urls[fail_urls.index(page_indievox.url)]

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
                        print('web', 'indievox')
                        print('url', page_indievox.url)

                        new_data = {
                            'tit': title,
                            'sdt': sell_datetimes_str,
                            'prc': prices,
                            'pdt': performance_datetimes,
                            'loc': locations,
                            'int': inner_text,
                            'web': 'indievox',
                            'url': page_indievox.url
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
                        if page_indievox.url in fail_urls:
                            del fail_urls[fail_urls.index(page_indievox.url)]

                    # 返回主頁面
                    page_indievox.go_back()
                    # 等待頁面載入完成
                    page_indievox.wait_for_load_state('load')
                    page_indievox.wait_for_timeout(timeout_seconds)

                # 完成
                page_indievox.close()
                # 移除txt暫存檔
                os.remove(txt_filename)

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
                                print('future', str(sdt_obj)[:-3].replace('-', '/'))
                                # 就加入list裡面
                                future_datetimes.append(str(sdt_obj)[:-3].replace('-', '/'))
                        print('future_datetimes', future_datetimes)
                        # 更改售票時間
                        data[i]['sdt'] = future_datetimes
                        # 寫入檔案
                        with open(json_filename, 'w', encoding='utf-8') as file:
                            json.dump(data, file, indent=4, ensure_ascii=False)

                print('indievox done')
                break

            except Exception as e:
                # 錯誤
                print(e, 'indievox restart')
                print('last finished index = ', last_finished_index)
                if page_indievox.url not in fail_urls:
                    print('第一次失敗')
                    fail_urls.append(page_indievox.url)
                else:
                    print('第二次失敗')
                    print('跳過')
                    last_finished_index += 1

                    with open('failure_log.txt', "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    if page_indievox.url + '\n' not in lines:
                        # txt檔案不存在或是裡面沒資料
                        if not os.path.exists('failure_log.txt') or os.path.getsize('failure_log.txt') <= 4:
                            # 直接寫入第一筆資料
                            with open('failure_log.txt', "w", encoding="utf-8") as f:
                                f.write(f'indievox\n{e}\n{page_indievox.url}\n')
                        # txt檔案存在且裡面已經有一筆以上的資料
                        else:
                            # 讀取現在有的檔案
                            with open('failure_log.txt', "a", encoding="utf-8") as f:
                                f.write(f'\nindievox\n{e}\n{page_indievox.url}\n')
                    else:
                        print('已經寫進錯誤裡面了!')

                    print('----------')
                    print('Fail urls:')
                    for url in fail_urls:
                        print(url)
                    print('----------')
                    print()

                # 重新啟動
                continue

get_indievox()
