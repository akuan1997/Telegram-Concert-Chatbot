from web_scraping.sync_api import sync_playwright, Playwright
# from get_data_from_text import get_prices, get_time_lines, get_sell, get_performance_location
import json
import os
from datetime import datetime

json_filename = 'ticketplus_new.json'
txt_filename = 'ticketplus_temp.txt'

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
            page_ticketplus = context.new_page()
            page_ticketplus.set_default_timeout(10000)

            page_ticketplus.goto("https://ticketplus.com.tw/")

            # 只有程式執行的一開始會經過這裡
            if last_finished_index == -1 and all_event_numbers == -1:
                pressed = False
                while not page_ticketplus.locator(
                        "#app > div > div > div > main > div > div > div.container.py-0.cus-container.mx-auto > div.tab-content.pa-3.pa-md-6 > div > div > div.text-center.pa-3.text-small.mt-6").is_visible():
                    page_ticketplus.keyboard.press('End')
                    if not pressed:
                        page_ticketplus.locator(
                            "#app > div > div > div > main > div > div > div.container.py-0.cus-container.mx-auto > div.tab-content.pa-3.pa-md-6 > div > div > div:nth-child(2) > button > span").click()
                        pressed = True

                all_events = page_ticketplus.query_selector_all(".row > div.d-flex.col-sm-6.col-md-4.col-12")
                all_event_numbers = len(all_events)
                print(all_event_numbers, '\n')

            unique_id = []
            for i in range(last_finished_index + 1, all_event_numbers):
                print(f'Ticketplus progress - {i + 1}/{all_event_numbers}')

                ''' 總數 '''
                if i < 6:
                    page_ticketplus.locator(".row > div.d-flex.col-sm-6.col-md-4.col-12").nth(i).click()
                else:
                    while not page_ticketplus.locator(".row > div.d-flex.col-sm-6.col-md-4.col-12").nth(i).is_visible():
                        page_ticketplus.keyboard.press('End')
                        if page_ticketplus.locator(
                                "#app > div > div > div > main > div > div > div.container.py-0.cus-container.mx-auto > div.tab-content.pa-3.pa-md-6 > div > div > div:nth-child(2) > button > span").is_visible():
                            page_ticketplus.locator(
                                "#app > div > div > div > main > div > div > div.container.py-0.cus-container.mx-auto > div.tab-content.pa-3.pa-md-6 > div > div > div:nth-child(2) > button > span").click()

                    page_ticketplus.locator(".row > div.d-flex.col-sm-6.col-md-4.col-12").nth(i).click()

                if page_ticketplus.locator(
                        "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.px-5.pb-5.font-weight-bold > div.row > div:nth-child(2) > button > span").is_visible():
                    page_ticketplus.locator(
                        "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.px-5.pb-5.font-weight-bold > div.row > div:nth-child(2) > button > span").click()

                # 處理新資料
                ''' 內文 '''
                # 下載內文
                inner_text = page_ticketplus.locator("#activityInfo > div > div").inner_text()
                with open(txt_filename, 'w', encoding='utf-8') as f:
                    f.write(inner_text)
                # 載入內文
                with open(txt_filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                # 票價
                # prices = get_prices(lines)
                # 售票時間
                # without_sell_time_lines, sell_datetimes_str = get_sell(get_time_lines(lines))
                ''' 固定位置 '''
                # 標題
                title = page_ticketplus.locator("#banner > div.pb-6.col.col-12 > h1").inner_text()
                # 資訊欄
                columns = page_ticketplus.query_selector_all("#buyTicket > .sesstion-item")
                for j in range(len(columns)):
                    column_text = page_ticketplus.locator("#buyTicket > .sesstion-item").nth(j).locator("div > div > div").nth(
                        0).inner_text()
                    # print(f'column text {column_text}')
                    column_text = column_text.split('\n')
                    for i in range(len(column_text)):
                        print(column_text[i])
                    # print(f'column text after split\n{column_text}')
                    # 日期 & 時間
                    concert_date = column_text[1].replace('-', '/')
                    concert_date = concert_date[:concert_date.index('(')]
                    # print(f'concert date {concert_date}')
                    concert_time = column_text[2]
                    # print(f'concert time {concert_time}')
                    pdt = concert_date + ' ' + concert_time
                    # print(f'performance datetime {pdt}')
                    # 地點
                    concert_place = column_text[3]
                    # print(f'concert place {concert_place}')
                    # 獨一無二的id識別
                    if f"{title}_{pdt}_{concert_place}" not in unique_id:
                        unique_id.append(f"{title}_{pdt}_{concert_place}")

                        # print('tit', title)
                        # print('sdt', sell_datetimes_str)
                        # print('prc', prices)
                        # print('pdt', pdt)
                        # print('loc', concert_place)
                        # print('web', 'ticketplus')
                        # print('url', page_ticketplus.url)
                        #
                        # new_data = {
                        #     'tit': title,
                        #     'sdt': sell_datetimes_str,
                        #     'prc': prices,
                        #     'pdt': [pdt],
                        #     'loc': [concert_place],
                        #     'int': inner_text,
                        #     'web': 'ticketplus',
                        #     'url': page_ticketplus.url
                        # }

                        # print('\n--- write new data ---\n')
                        #
                        # # json檔案不存在或是裡面沒資料
                        # if not os.path.exists(json_filename) or os.path.getsize(
                        #         json_filename) <= 4:
                        #     # 直接寫入第一筆資料
                        #     with open(json_filename, "w", encoding="utf-8") as f:
                        #         json.dump([new_data], f, indent=4, ensure_ascii=False)
                        # # json檔案存在且裡面已經有一筆以上的資料
                        # else:
                        #     # 讀取現在有的檔案
                        #     with open(json_filename, "r", encoding="utf-8") as f:
                        #         existing_data = json.load(f)
                        #     # 並新增即將寫入的一筆
                        #     existing_data.append(new_data)
                        #     # 寫入
                        #     with open(json_filename, "w", encoding="utf-8") as f:
                        #         json.dump(existing_data, f, indent=4, ensure_ascii=False)
                        # last_finished_index = i
                        # if page_ticketplus.url in fail_urls:
                        #     del fail_urls[fail_urls.index(page_ticketplus.url)]
                    else:
                        print('Skip')
                        continue

                page_ticketplus.go_back()

            # 完成
            page_ticketplus.close()
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
            break

        except Exception as e:
            print(e, 'ticketplus restart')
            print('last finished index = ', last_finished_index)
            if page_ticketplus.url == 'https://ticketplus.com.tw/':
                print('是主頁，所以沒關係')
            else:
                if page_ticketplus.url not in fail_urls:
                    print('第一次失敗')
                    fail_urls.append(page_ticketplus.url)
                else:
                    print('第二次失敗')
                    print('跳過')
                    last_finished_index += 1

                    with open('failure_log.txt', "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    if page_ticketplus.url + '\n' not in lines:
                        # txt檔案不存在或是裡面沒資料
                        if not os.path.exists('failure_log.txt') or os.path.getsize('failure_log.txt') <= 4:
                            # 直接寫入第一筆資料
                            with open('failure_log.txt', "w", encoding="utf-8") as f:
                                f.write(f'Ticketplus\n{e}\n{page_ticketplus.url}\n')
                        # txt檔案存在且裡面已經有一筆以上的資料
                        else:
                            # 讀取現在有的檔案
                            with open('failure_log.txt', "a", encoding="utf-8") as f:
                                f.write(f'\nTicketplus\n{e}\n{page_ticketplus.url}\n')
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



