from playwright.sync_api import sync_playwright, Playwright
from get_data_from_text import get_prices, get_time_lines, get_sell, get_performance_location
import json
import os
from datetime import datetime

json_filename = '../playwright/ticketplus_new.json'
txt_filename = '../playwright/ticketplus_temp.txt'

with sync_playwright() as p:
    with open(json_filename, 'w', encoding='utf-8') as f:
        f.write('')

    last_finished_index = -1

    browser = p.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(10000)

    page.goto("https://ticketplus.com.tw/")

    # 獲得活動數量的總數
    pressed = False
    while not page.locator(
            "#app > div > div > div > main > div > div > div.container.py-0.cus-container.mx-auto > div.tab-content.pa-3.pa-md-6 > div > div > div.text-center.pa-3.text-small.mt-6").is_visible():
        page.keyboard.press('End')
        if not pressed:
            page.locator(
                "#app > div > div > div > main > div > div > div.container.py-0.cus-container.mx-auto > div.tab-content.pa-3.pa-md-6 > div > div > div:nth-child(2) > button > span").click()
            pressed = True

    events = page.query_selector_all(".row > div.d-flex.col-sm-6.col-md-4.col-12")
    # 獲得活動數量的總數。
    numbers = len(events)

    unique_id = []
    for i in range(numbers):
        print(f'current progress {i + 1}/{numbers}')

        ''' 總數 '''
        if i < 6:
            page.locator(".row > div.d-flex.col-sm-6.col-md-4.col-12").nth(i).click()
        else:
            while not page.locator(".row > div.d-flex.col-sm-6.col-md-4.col-12").nth(i).is_visible():
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
            column_text = page.locator("#buyTicket > .sesstion-item").nth(j).locator("div > div > div").nth(
                0).inner_text()
            column_text = column_text.split('\n')
            # 日期 & 時間
            concert_date = column_text[1].replace('-', '/')
            concert_date = concert_date[:concert_date.index('(')]
            concert_time = column_text[2]
            pdt = concert_date + ' ' + concert_time
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
                print('web', 'ticketplus')
                print('url', page.url)

                new_data = {
                    'tit': title,
                    'sdt': sell_datetimes_str,
                    'prc': prices,
                    'pdt': [pdt],
                    'loc': [concert_place],
                    'int': inner_text,
                    'web': 'ticketplus',
                    'url': page.url
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

            else:
                print('Skip')
                continue

        page.go_back()

    # 完成
    page.close()
    # 移除剛剛使用的暫存文檔
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

    print('\nticketplus done\n')

