from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import re, os, json
from datetime import datetime, time
import os, sys
import time
import threading

json_filename_first = 'kktix_new_first.json'
json_filename_second = 'kktix_new_second.json'
json_filename_third = 'kktix_new_third.json'
json_filename = '../kktix_new.json'

integrate_webs = []


def get_kktix_first():
    global integrate_webs
    with sync_playwright() as p:

        with open(json_filename_first, 'w', encoding='utf-8') as f:
            f.write('')

        # 待會會從 last_finished_index + 1開始
        last_finished_selling_index = -1
        last_finished_view_index = -1
        # 完成的演唱會頁面
        completed_pages = []
        # 發生錯誤的演唱會活動
        current_page_index = -1
        fail_indices = []
        # 統整的網站

        while True:
            try:
                browser = p.chromium.launch(headless=False)
                context_kktix = browser.new_context()
                page_kktix_first = context_kktix.new_page()
                # page_kktix_first.set_default_timeout(60000)

                ''''''

                page_kktix_first.goto("https://kktix.com/events?end_at=&"
                                      "event_tag_ids_in=1&max_price=&"
                                      "min_price=&page=1"
                                      "&search=&start_at=")

                print('kktix start!')

                ''''''

                page_index = 1
                current_page_index = page_index

                while True:
                    if page_index in completed_pages:
                        print(f'Error occurred, but page {page_index} is already finished!')

                    else:
                        # type-selling
                        type_selling = page_kktix_first.query_selector_all('li.type-selling')
                        if last_finished_selling_index != len(type_selling) - 1:
                            print(f'\n\nselling start from {page_index}-{last_finished_selling_index + 1}\n\n')
                            for i in range(last_finished_selling_index + 1, len(type_selling)):
                                print(f'kktix selling progress - page {page_index}, {i + 1}/{len(type_selling)}')
                                # print(f'selling {page_index}-{i}')
                                # 演唱會頁面
                                type_selling[i].click()
                                print('concert page', page_kktix_first.url)
                                page_kktix_first.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str = []
                                prices = []
                                performance_datetimes_str = []
                                location = ''
                                if page_kktix_first.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page_kktix_first.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page_kktix_first.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(
                                            ".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page_kktix_first.locator(
                                                ".table-wrapper > table > tbody > tr").nth(
                                                j).locator(
                                                ".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        if page_kktix_first.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(
                                            ".period .period-time").is_visible():
                                            ticket_time = page_kktix_first.locator(
                                                ".table-wrapper > table > tbody > tr").nth(
                                                j).locator(
                                                ".period .period-time").inner_text()
                                            ticket_time = ticket_time[:ticket_time.index('~')]
                                            ticket_time = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", ticket_time)
                                            ticket_time = ticket_time.strip()
                                            if ticket_time not in sell_datetimes_str:
                                                sell_datetimes_str.append(ticket_time)

                                        ''''''

                                        # 票價 list
                                        if page_kktix_first.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(
                                            ".price .price > span").nth(1).is_visible():
                                            price = int(
                                                float(
                                                    page_kktix_first.locator(".table-wrapper > table > tbody > tr").nth(
                                                        j).locator(".price .price > span").nth(1).inner_text().replace(
                                                        ',',
                                                        '')))
                                            prices.append(price)
                                        else:
                                            prices.append(0)
                                        prices = list(set(prices))

                                        ''''''

                                        # 內文
                                        inner_text = page_kktix_first.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page_kktix_first.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page_kktix_first.url)
                                        page_kktix_first.wait_for_timeout(1500)
                                        page_kktix_first.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        if page_kktix_first.locator(
                                                "#registrationsNewApp > div > div:nth-child(2) > div.narrow-wrapper.ng-scope > div > h1").is_visible():
                                            title = page_kktix_first.locator(
                                                "#registrationsNewApp > div > div:nth-child(2) > div.narrow-wrapper.ng-scope > div > h1").inner_text().replace(
                                                '\n', '').strip()
                                        else:
                                            print('title no')

                                        ''''''

                                        # 表演時間 list
                                        if page_kktix_first.locator("tbody > tr").nth(0).locator("td").is_visible():
                                            pdt = \
                                                page_kktix_first.locator("tbody > tr").nth(0).locator(
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
                                            performance_datetimes_str.append(pdt)
                                        else:
                                            print('performance_datetimes no')

                                        ''''''

                                        # 地點 str
                                        if page_kktix_first.locator("tbody > tr").nth(1).locator("th").is_visible():
                                            if page_kktix_first.locator("tbody > tr").nth(1).locator(
                                                    "th").inner_text() == '活動地點':
                                                location_address = \
                                                    page_kktix_first.locator("tbody > tr").nth(1).locator(
                                                        "td").inner_text().split(
                                                        '檢視地圖')[
                                                        0].strip().split(' / ')
                                                location = location_address[0]
                                                # locations.append(concert_place)
                                        else:
                                            print('locations no')

                                        ''''''

                                        page_kktix_first.go_back()
                                        if title or performance_datetimes_str or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str', sell_datetimes_str)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str', performance_datetimes_str)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str,
                                                'loc': [location],
                                                'int': inner_text,
                                                'web': 'kktix',
                                                'url': page_kktix_first.url
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            # json檔案不存在或是裡面沒資料
                                            if not os.path.exists(json_filename_first) or os.path.getsize(
                                                    json_filename_first) <= 4:
                                                # 直接寫入第一筆資料
                                                with open(json_filename_first, "w", encoding="utf-8") as f:
                                                    json.dump([new_data], f, indent=4, ensure_ascii=False)
                                            # json檔案存在且裡面已經有一筆以上的資料
                                            else:
                                                # 讀取現在有的檔案
                                                with open(json_filename_first, "r", encoding="utf-8") as f:
                                                    existing_data = json.load(f)
                                                # 並新增即將寫入的一筆
                                                existing_data.append(new_data)
                                                # 寫入
                                                with open(json_filename_first, "w", encoding="utf-8") as f:
                                                    json.dump(existing_data, f, indent=4, ensure_ascii=False)

                                            last_finished_selling_index = i
                                            print(f'finished {page_index}-{last_finished_selling_index}')
                                            print('\n----------------------\n')

                                    else:
                                        print('hk activity, skip')
                                        last_finished_selling_index = i
                                        print(f'finished {page_index}-{last_finished_selling_index}')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_selling_index = i
                                    print(f'finished {page_index}-{last_finished_selling_index}')
                                    print('\n----------------------\n')
                                    integrate_webs.append(page_kktix_first.url)

                                ''''''

                                page_kktix_first.go_back()  # main page
                                type_selling = page_kktix_first.query_selector_all('li.type-selling')
                        else:
                            print('CSS: "type-selling" of this page is already finished!')

                        ''''''

                        # type-view
                        type_view = page_kktix_first.query_selector_all('li.type-view')
                        print(f'\n\nview start from {page_index}-{last_finished_view_index + 1}\n\n')
                        for i in range(last_finished_view_index + 1, len(type_view)):
                            print(f'kktix view progress - page {page_index}, {i + 1}/{len(type_view)}')
                            # print(f'view {page_index}-{i}')
                            # 演唱會頁面
                            type_view[i].click()
                            print('concert page', page_kktix_first.url)
                            page_kktix_first.wait_for_timeout(500)

                            ''''''

                            hk = False
                            title = ''
                            sell_datetimes_str = []
                            prices = []
                            performance_datetimes_str = []
                            location = ''
                            if page_kktix_first.locator("table > thead > tr > th.name").is_visible():
                                # 確認此頁面是否為香港活動
                                # 1. 迴圈 票種、販售時間、售價 物件個數
                                for j in range(
                                        len(page_kktix_first.query_selector_all(
                                            ".table-wrapper > table > tbody > tr"))):
                                    # 貨幣符號
                                    # 如果有找到貨幣符號
                                    if page_kktix_first.locator(".table-wrapper > table > tbody > tr").nth(j).locator(
                                            ".price .price > span").nth(0).is_visible():
                                        # 取得貨幣符號
                                        currency = page_kktix_first.locator(".table-wrapper > table > tbody > tr").nth(
                                            j).locator(
                                            ".price .price > span").nth(0).inner_text()
                                        # 檢查是否為港幣
                                        if 'hk' in currency.lower():
                                            hk = True
                                            break
                                    # 找不到貨幣符號
                                    else:
                                        currency = ''

                                    ''''''

                                    # 售票時間
                                    if page_kktix_first.locator(".table-wrapper > table > tbody > tr").nth(j).locator(
                                            ".period .period-time").is_visible():
                                        ticket_time = page_kktix_first.locator(
                                            ".table-wrapper > table > tbody > tr").nth(
                                            j).locator(
                                            ".period .period-time").inner_text()
                                        ticket_time = ticket_time[:ticket_time.index('~')]
                                        ticket_time = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", ticket_time)
                                        ticket_time = ticket_time.strip()
                                        if ticket_time not in sell_datetimes_str:
                                            sell_datetimes_str.append(ticket_time)

                                    ''''''

                                    # 票價
                                    if page_kktix_first.locator(".table-wrapper > table > tbody > tr").nth(j).locator(
                                            ".price .price > span").nth(1).is_visible():
                                        price = int(
                                            float(page_kktix_first.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(1).inner_text().replace(',',
                                                                                                               '')))
                                        prices.append(price)
                                    else:
                                        prices.append(0)
                                    prices = list(set(prices))

                                    ''''''

                                    # 內文
                                    inner_text = page_kktix_first.locator(".description").inner_text()

                                    ''''''

                                if not hk:
                                    # 進入購票頁面，獲得地點以及表演時間
                                    page_kktix_first.locator(".outer-wrapper .tickets .btn-point").click()
                                    print('buy ticket page', page_kktix_first.url)
                                    page_kktix_first.wait_for_timeout(1500)
                                    page_kktix_first.wait_for_load_state('load')

                                    ''''''

                                    # 標題
                                    if page_kktix_first.locator(
                                            "#registrationsNewApp > div > div:nth-child(2) > div.narrow-wrapper.ng-scope > div > h1").is_visible():
                                        title = page_kktix_first.locator(
                                            "#registrationsNewApp > div > div:nth-child(2) > div.narrow-wrapper.ng-scope > div > h1").inner_text().replace(
                                            '\n', '').strip()
                                    else:
                                        print('title no')

                                    ''''''

                                    # 表演時間
                                    if page_kktix_first.locator("tbody > tr").nth(0).locator("td").is_visible():
                                        pdt = \
                                            page_kktix_first.locator("tbody > tr").nth(0).locator(
                                                "td").inner_text().split(
                                                '加入行事曆')[
                                                0].strip()
                                        pdt = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", pdt)
                                        if '~' in pdt:
                                            start_time_date = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', pdt.split('~')[0])
                                            finish_time_date = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', pdt.split('~')[1])
                                            if start_time_date[0] == finish_time_date[0]:
                                                pdt = pdt.split('~')[0].strip()
                                        pdt = re.sub(r"\s{2,}", " ", pdt)
                                        pdt = pdt.strip()
                                        performance_datetimes_str.append(pdt)
                                    else:
                                        print('performance_datetimes no')

                                    ''''''

                                    # 地點
                                    if page_kktix_first.locator("tbody > tr").nth(1).locator("th").is_visible():
                                        if page_kktix_first.locator("tbody > tr").nth(1).locator(
                                                "th").inner_text() == '活動地點':
                                            location_address = \
                                                page_kktix_first.locator("tbody > tr").nth(1).locator(
                                                    "td").inner_text().split(
                                                    '檢視地圖')[
                                                    0].strip().split(' / ')
                                            location = location_address[0]
                                            # locations.append(concert_place)
                                    else:
                                        print('locations no')

                                    ''''''

                                    page_kktix_first.go_back()
                                    if title or performance_datetimes_str or location:
                                        print('title', title)  # str
                                        print('sell_datetimes_str', sell_datetimes_str)  # list
                                        print('prices', prices)  # list
                                        print('performance_datetimes_str', performance_datetimes_str)  # list
                                        print('location', location)  # str

                                        # 新的一筆資料
                                        new_data = {
                                            'tit': title,
                                            'sdt': sell_datetimes_str,
                                            'prc': prices,
                                            'pdt': performance_datetimes_str,
                                            'loc': [location],
                                            'int': inner_text,
                                            'web': 'kktix',
                                            'url': page_kktix_first.url
                                        }

                                        print('\n--- write new data ---\n')

                                        # json檔案不存在或是裡面沒資料
                                        if not os.path.exists(json_filename_first) or os.path.getsize(
                                                json_filename_first) <= 4:
                                            # 直接寫入第一筆資料
                                            with open(json_filename_first, "w", encoding="utf-8") as f:
                                                json.dump([new_data], f, indent=4, ensure_ascii=False)
                                        # json檔案存在且裡面已經有一筆以上的資料
                                        else:
                                            # 讀取現在有的檔案
                                            with open(json_filename_first, "r", encoding="utf-8") as f:
                                                existing_data = json.load(f)
                                            # 並新增即將寫入的一筆
                                            existing_data.append(new_data)
                                            # 寫入
                                            with open(json_filename_first, "w", encoding="utf-8") as f:
                                                json.dump(existing_data, f, indent=4, ensure_ascii=False)

                                        last_finished_view_index = i
                                        print(f'finished {page_index}-{last_finished_view_index}\n')
                                        print('\n----------------------\n')


                                else:
                                    print('hk activity, skip')
                                    last_finished_view_index = i
                                    print(f'finished {page_index}-{last_finished_view_index}\n')
                                    print('\n----------------------\n')

                            else:
                                print('integrate webpage, skip')
                                last_finished_view_index = i
                                print(f'finished {page_index}-{last_finished_view_index}\n')
                                print('\n----------------------\n')
                                integrate_webs.append(page_kktix_first.url)

                            ''''''

                            page_kktix_first.go_back()  # main page
                            type_view = page_kktix_first.query_selector_all('li.type-view')

                        ''''''

                        # 完成此頁
                        pagination_div = page_kktix_first.query_selector(".pagination.pull-right")
                        text = pagination_div.inner_text()
                        print(f'\nFinished page {page_index}')
                        completed_pages.append(page_index)
                        last_finished_selling_index = -1
                        last_finished_view_index = -1

                    # 有下一頁
                    if '›' in text:
                        if int(page_kktix_first.locator(
                                "body > div.wrapper > div.page-content > section.explore-container.container > div > div.pagination.pull-right > ul > li.active > a").inner_text()) > 3:
                            break
                        page_kktix_first.locator("div.pagination.pull-right li:last-child").click()
                        page_index += 1
                        current_page_index = page_index
                        print(f'\nGo to page {page_index}\n')

                    # 最後一頁
                    else:
                        print('kktix finished')

                        # 程式確認沒有最後一頁後跳出while True的break
                        break

                # 確認全部執行完成，沒有發生錯誤的break
                break

            except Exception as e:
                # 錯誤
                page_kktix_first.close()
                print(e, 'kktix restart')
                if [current_page_index, last_finished_selling_index, last_finished_view_index] not in fail_indices:
                    fail_indices.append([current_page_index, last_finished_selling_index, last_finished_view_index])
                    print('first failure')
                else:
                    print('second failure')

                    with open('wrong_log.txt', "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    if page_kktix_first.url + '\n' not in lines:
                        # txt檔案不存在或是裡面沒資料
                        if not os.path.exists('wrong_log.txt') or os.path.getsize('wrong_log.txt') <= 4:
                            # 寫入第一筆資料
                            with open('wrong_log.txt', "w", encoding="utf-8") as f:
                                f.write(f'KKTIX\n{e}\n{page_kktix_first.url}\n')
                        # txt檔案存在且裡面已經有一筆以上的資料
                        else:
                            # 讀取現在有的檔案
                            with open('wrong_log.txt', "a", encoding="utf-8") as f:
                                f.write(f'\nKKTIX\n{e}\n{page_kktix_first.url}\n')
                    else:
                        print('已經寫進錯誤裡面了!')

                    print('skip')

                    if last_finished_view_index == -1:
                        last_finished_selling_index += 1
                    else:
                        last_finished_view_index += 1
                # 重新啟動
                continue

        # 完成
        page_kktix_first.close()


def get_kktix_second():
    global integrate_webs
    with sync_playwright() as p:

        with open(json_filename_second, 'w', encoding='utf-8') as f:
            f.write('')

        # 待會會從 last_finished_index + 1開始
        last_finished_selling_index = -1
        last_finished_view_index = -1
        # 完成的演唱會頁面
        completed_pages = []
        # 發生錯誤的演唱會活動
        current_page_index = -1
        fail_indices = []
        # 統整的網站

        while True:
            try:
                browser = p.chromium.launch(headless=False)
                context_kktix = browser.new_context()
                page_kktix_second = context_kktix.new_page()
                # page_kktix_second.set_default_timeout(60000)

                ''''''

                page_kktix_second.goto("https://kktix.com/events?end_at=&"
                                       "event_tag_ids_in=1&max_price=&"
                                       "min_price=&page=5"
                                       "&search=&start_at=")

                print('kktix start!')

                ''''''

                page_index = 5
                current_page_index = page_index

                while True:
                    if page_index in completed_pages:
                        print(f'Error occurred, but page {page_index} is already finished!')

                    else:
                        # type-selling
                        type_selling = page_kktix_second.query_selector_all('li.type-selling')
                        if last_finished_selling_index != len(type_selling) - 1:
                            print(f'\n\nselling start from {page_index}-{last_finished_selling_index + 1}\n\n')
                            for i in range(last_finished_selling_index + 1, len(type_selling)):
                                print(f'kktix selling progress - page {page_index}, {i + 1}/{len(type_selling)}')
                                # print(f'selling {page_index}-{i}')
                                # 演唱會頁面
                                type_selling[i].click()
                                print('concert page', page_kktix_second.url)
                                page_kktix_second.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str = []
                                prices = []
                                performance_datetimes_str = []
                                location = ''
                                if page_kktix_second.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page_kktix_second.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page_kktix_second.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(
                                            ".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page_kktix_second.locator(
                                                ".table-wrapper > table > tbody > tr").nth(
                                                j).locator(
                                                ".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        if page_kktix_second.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(
                                            ".period .period-time").is_visible():
                                            ticket_time = page_kktix_second.locator(
                                                ".table-wrapper > table > tbody > tr").nth(
                                                j).locator(
                                                ".period .period-time").inner_text()
                                            ticket_time = ticket_time[:ticket_time.index('~')]
                                            ticket_time = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", ticket_time)
                                            ticket_time = ticket_time.strip()
                                            if ticket_time not in sell_datetimes_str:
                                                sell_datetimes_str.append(ticket_time)

                                        ''''''

                                        # 票價 list
                                        if page_kktix_second.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(
                                            ".price .price > span").nth(1).is_visible():
                                            price = int(
                                                float(page_kktix_second.locator(
                                                    ".table-wrapper > table > tbody > tr").nth(
                                                    j).locator(".price .price > span").nth(1).inner_text().replace(',',
                                                                                                                   '')))
                                            prices.append(price)
                                        else:
                                            prices.append(0)
                                        prices = list(set(prices))

                                        ''''''

                                        # 內文
                                        inner_text = page_kktix_second.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page_kktix_second.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page_kktix_second.url)
                                        page_kktix_second.wait_for_timeout(1500)
                                        page_kktix_second.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        if page_kktix_second.locator(
                                                "#registrationsNewApp > div > div:nth-child(2) > div.narrow-wrapper.ng-scope > div > h1").is_visible():
                                            title = page_kktix_second.locator(
                                                "#registrationsNewApp > div > div:nth-child(2) > div.narrow-wrapper.ng-scope > div > h1").inner_text().replace(
                                                '\n', '').strip()
                                        else:
                                            print('title no')

                                        ''''''

                                        # 表演時間 list
                                        if page_kktix_second.locator("tbody > tr").nth(0).locator("td").is_visible():
                                            pdt = \
                                                page_kktix_second.locator("tbody > tr").nth(0).locator(
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
                                            performance_datetimes_str.append(pdt)
                                        else:
                                            print('performance_datetimes no')

                                        ''''''

                                        # 地點 str
                                        if page_kktix_second.locator("tbody > tr").nth(1).locator("th").is_visible():
                                            if page_kktix_second.locator("tbody > tr").nth(1).locator(
                                                    "th").inner_text() == '活動地點':
                                                location_address = \
                                                    page_kktix_second.locator("tbody > tr").nth(1).locator(
                                                        "td").inner_text().split(
                                                        '檢視地圖')[
                                                        0].strip().split(' / ')
                                                location = location_address[0]
                                                # locations.append(concert_place)
                                        else:
                                            print('locations no')

                                        ''''''

                                        page_kktix_second.go_back()
                                        if title or performance_datetimes_str or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str', sell_datetimes_str)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str', performance_datetimes_str)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str,
                                                'loc': [location],
                                                'int': inner_text,
                                                'web': 'kktix',
                                                'url': page_kktix_second.url
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            # json檔案不存在或是裡面沒資料
                                            if not os.path.exists(json_filename_second) or os.path.getsize(
                                                    json_filename_second) <= 4:
                                                # 直接寫入第一筆資料
                                                with open(json_filename_second, "w", encoding="utf-8") as f:
                                                    json.dump([new_data], f, indent=4, ensure_ascii=False)
                                            # json檔案存在且裡面已經有一筆以上的資料
                                            else:
                                                # 讀取現在有的檔案
                                                with open(json_filename_second, "r", encoding="utf-8") as f:
                                                    existing_data = json.load(f)
                                                # 並新增即將寫入的一筆
                                                existing_data.append(new_data)
                                                # 寫入
                                                with open(json_filename_second, "w", encoding="utf-8") as f:
                                                    json.dump(existing_data, f, indent=4, ensure_ascii=False)

                                            last_finished_selling_index = i
                                            print(f'finished {page_index}-{last_finished_selling_index}')
                                            print('\n----------------------\n')

                                    else:
                                        print('hk activity, skip')
                                        last_finished_selling_index = i
                                        print(f'finished {page_index}-{last_finished_selling_index}')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_selling_index = i
                                    print(f'finished {page_index}-{last_finished_selling_index}')
                                    print('\n----------------------\n')
                                    integrate_webs.append(page_kktix_second.url)

                                ''''''

                                page_kktix_second.go_back()  # main page
                                type_selling = page_kktix_second.query_selector_all('li.type-selling')
                        else:
                            print('CSS: "type-selling" of this page is already finished!')

                        ''''''

                        # type-view
                        type_view = page_kktix_second.query_selector_all('li.type-view')
                        print(f'\n\nview start from {page_index}-{last_finished_view_index + 1}\n\n')
                        for i in range(last_finished_view_index + 1, len(type_view)):
                            print(f'kktix view progress - page {page_index}, {i + 1}/{len(type_view)}')
                            # print(f'view {page_index}-{i}')
                            # 演唱會頁面
                            type_view[i].click()
                            print('concert page', page_kktix_second.url)
                            page_kktix_second.wait_for_timeout(500)

                            ''''''

                            hk = False
                            title = ''
                            sell_datetimes_str = []
                            prices = []
                            performance_datetimes_str = []
                            location = ''
                            if page_kktix_second.locator("table > thead > tr > th.name").is_visible():
                                # 確認此頁面是否為香港活動
                                # 1. 迴圈 票種、販售時間、售價 物件個數
                                for j in range(
                                        len(page_kktix_second.query_selector_all(
                                            ".table-wrapper > table > tbody > tr"))):
                                    # 貨幣符號
                                    # 如果有找到貨幣符號
                                    if page_kktix_second.locator(".table-wrapper > table > tbody > tr").nth(j).locator(
                                            ".price .price > span").nth(0).is_visible():
                                        # 取得貨幣符號
                                        currency = page_kktix_second.locator(".table-wrapper > table > tbody > tr").nth(
                                            j).locator(
                                            ".price .price > span").nth(0).inner_text()
                                        # 檢查是否為港幣
                                        if 'hk' in currency.lower():
                                            hk = True
                                            break
                                    # 找不到貨幣符號
                                    else:
                                        currency = ''

                                    ''''''

                                    # 售票時間
                                    if page_kktix_second.locator(".table-wrapper > table > tbody > tr").nth(j).locator(
                                            ".period .period-time").is_visible():
                                        ticket_time = page_kktix_second.locator(
                                            ".table-wrapper > table > tbody > tr").nth(
                                            j).locator(
                                            ".period .period-time").inner_text()
                                        ticket_time = ticket_time[:ticket_time.index('~')]
                                        ticket_time = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", ticket_time)
                                        ticket_time = ticket_time.strip()
                                        if ticket_time not in sell_datetimes_str:
                                            sell_datetimes_str.append(ticket_time)

                                    ''''''

                                    # 票價
                                    if page_kktix_second.locator(".table-wrapper > table > tbody > tr").nth(j).locator(
                                            ".price .price > span").nth(1).is_visible():
                                        price = int(
                                            float(page_kktix_second.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(1).inner_text().replace(',',
                                                                                                               '')))
                                        prices.append(price)
                                    else:
                                        prices.append(0)
                                    prices = list(set(prices))

                                    ''''''

                                    # 內文
                                    inner_text = page_kktix_second.locator(".description").inner_text()

                                    ''''''

                                if not hk:
                                    # 進入購票頁面，獲得地點以及表演時間
                                    page_kktix_second.locator(".outer-wrapper .tickets .btn-point").click()
                                    print('buy ticket page', page_kktix_second.url)
                                    page_kktix_second.wait_for_timeout(1500)
                                    page_kktix_second.wait_for_load_state('load')

                                    ''''''

                                    # 標題
                                    if page_kktix_second.locator(
                                            "#registrationsNewApp > div > div:nth-child(2) > div.narrow-wrapper.ng-scope > div > h1").is_visible():
                                        title = page_kktix_second.locator(
                                            "#registrationsNewApp > div > div:nth-child(2) > div.narrow-wrapper.ng-scope > div > h1").inner_text().replace(
                                            '\n', '').strip()
                                    else:
                                        print('title no')

                                    ''''''

                                    # 表演時間
                                    if page_kktix_second.locator("tbody > tr").nth(0).locator("td").is_visible():
                                        pdt = \
                                            page_kktix_second.locator("tbody > tr").nth(0).locator(
                                                "td").inner_text().split(
                                                '加入行事曆')[
                                                0].strip()
                                        pdt = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", pdt)
                                        if '~' in pdt:
                                            start_time_date = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', pdt.split('~')[0])
                                            finish_time_date = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', pdt.split('~')[1])
                                            if start_time_date[0] == finish_time_date[0]:
                                                pdt = pdt.split('~')[0].strip()
                                        pdt = re.sub(r"\s{2,}", " ", pdt)
                                        pdt = pdt.strip()
                                        performance_datetimes_str.append(pdt)
                                    else:
                                        print('performance_datetimes no')

                                    ''''''

                                    # 地點
                                    if page_kktix_second.locator("tbody > tr").nth(1).locator("th").is_visible():
                                        if page_kktix_second.locator("tbody > tr").nth(1).locator(
                                                "th").inner_text() == '活動地點':
                                            location_address = \
                                                page_kktix_second.locator("tbody > tr").nth(1).locator(
                                                    "td").inner_text().split(
                                                    '檢視地圖')[
                                                    0].strip().split(' / ')
                                            location = location_address[0]
                                            # locations.append(concert_place)
                                    else:
                                        print('locations no')

                                    ''''''

                                    page_kktix_second.go_back()
                                    if title or performance_datetimes_str or location:
                                        print('title', title)  # str
                                        print('sell_datetimes_str', sell_datetimes_str)  # list
                                        print('prices', prices)  # list
                                        print('performance_datetimes_str', performance_datetimes_str)  # list
                                        print('location', location)  # str

                                        # 新的一筆資料
                                        new_data = {
                                            'tit': title,
                                            'sdt': sell_datetimes_str,
                                            'prc': prices,
                                            'pdt': performance_datetimes_str,
                                            'loc': [location],
                                            'int': inner_text,
                                            'web': 'kktix',
                                            'url': page_kktix_second.url
                                        }

                                        print('\n--- write new data ---\n')

                                        # json檔案不存在或是裡面沒資料
                                        if not os.path.exists(json_filename_second) or os.path.getsize(
                                                json_filename_second) <= 4:
                                            # 直接寫入第一筆資料
                                            with open(json_filename_second, "w", encoding="utf-8") as f:
                                                json.dump([new_data], f, indent=4, ensure_ascii=False)
                                        # json檔案存在且裡面已經有一筆以上的資料
                                        else:
                                            # 讀取現在有的檔案
                                            with open(json_filename_second, "r", encoding="utf-8") as f:
                                                existing_data = json.load(f)
                                            # 並新增即將寫入的一筆
                                            existing_data.append(new_data)
                                            # 寫入
                                            with open(json_filename_second, "w", encoding="utf-8") as f:
                                                json.dump(existing_data, f, indent=4, ensure_ascii=False)

                                        last_finished_view_index = i
                                        print(f'finished {page_index}-{last_finished_view_index}\n')
                                        print('\n----------------------\n')


                                else:
                                    print('hk activity, skip')
                                    last_finished_view_index = i
                                    print(f'finished {page_index}-{last_finished_view_index}\n')
                                    print('\n----------------------\n')

                            else:
                                print('integrate webpage, skip')
                                last_finished_view_index = i
                                print(f'finished {page_index}-{last_finished_view_index}\n')
                                print('\n----------------------\n')
                                integrate_webs.append(page_kktix_second.url)

                            ''''''

                            page_kktix_second.go_back()  # main page
                            type_view = page_kktix_second.query_selector_all('li.type-view')

                        ''''''

                        # 完成此頁
                        pagination_div = page_kktix_second.query_selector(".pagination.pull-right")
                        text = pagination_div.inner_text()
                        print(f'\nFinished page {page_index}')
                        completed_pages.append(page_index)
                        last_finished_selling_index = -1
                        last_finished_view_index = -1

                    # 有下一頁
                    if '›' in text:
                        if int(page_kktix_second.locator(
                                "body > div.wrapper > div.page-content > section.explore-container.container > div > div.pagination.pull-right > ul > li.active > a").inner_text()) > 7:
                            break
                        page_kktix_second.locator("div.pagination.pull-right li:last-child").click()
                        page_index += 1
                        current_page_index = page_index
                        print(f'\nGo to page {page_index}\n')

                    # 最後一頁
                    else:
                        print('kktix finished')

                        # 程式確認沒有最後一頁後跳出while True的break
                        break

                # 確認全部執行完成，沒有發生錯誤的break
                break

            except Exception as e:
                # 錯誤
                page_kktix_second.close()
                print(e, 'kktix restart')
                if [current_page_index, last_finished_selling_index, last_finished_view_index] not in fail_indices:
                    fail_indices.append([current_page_index, last_finished_selling_index, last_finished_view_index])
                    print('first failure')
                else:
                    print('second failure')

                    with open('wrong_log.txt', "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    if page_kktix_second.url + '\n' not in lines:
                        # txt檔案不存在或是裡面沒資料
                        if not os.path.exists('wrong_log.txt') or os.path.getsize('wrong_log.txt') <= 4:
                            # 寫入第一筆資料
                            with open('wrong_log.txt', "w", encoding="utf-8") as f:
                                f.write(f'KKTIX\n{e}\n{page_kktix_second.url}\n')
                        # txt檔案存在且裡面已經有一筆以上的資料
                        else:
                            # 讀取現在有的檔案
                            with open('wrong_log.txt', "a", encoding="utf-8") as f:
                                f.write(f'\nKKTIX\n{e}\n{page_kktix_second.url}\n')
                    else:
                        print('已經寫進錯誤裡面了!')

                    print('skip')

                    if last_finished_view_index == -1:
                        last_finished_selling_index += 1
                    else:
                        last_finished_view_index += 1
                # 重新啟動
                continue

        # 完成
        page_kktix_second.close()


def get_kktix_third():
    global integrate_webs
    with sync_playwright() as p:

        with open(json_filename_third, 'w', encoding='utf-8') as f:
            f.write('')

        # 待會會從 last_finished_index + 1開始
        last_finished_selling_index = -1
        last_finished_view_index = -1
        # 完成的演唱會頁面
        completed_pages = []
        # 發生錯誤的演唱會活動
        current_page_index = -1
        fail_indices = []
        # 統整的網站

        while True:
            try:
                browser = p.chromium.launch(headless=False)
                context_kktix = browser.new_context()
                page_kktix_third = context_kktix.new_page()
                # page_kktix_third.set_default_timeout(60000)

                ''''''

                page_kktix_third.goto("https://kktix.com/events?end_at=&"
                                      "event_tag_ids_in=1&max_price=&"
                                      "min_price=&page=9"
                                      "&search=&start_at=")

                print('kktix start!')

                ''''''

                page_index = 9
                current_page_index = page_index

                while True:
                    if page_index in completed_pages:
                        print(f'Error occurred, but page {page_index} is already finished!')

                    else:
                        # type-selling
                        type_selling = page_kktix_third.query_selector_all('li.type-selling')
                        if last_finished_selling_index != len(type_selling) - 1:
                            print(f'\n\nselling start from {page_index}-{last_finished_selling_index + 1}\n\n')
                            for i in range(last_finished_selling_index + 1, len(type_selling)):
                                print(f'kktix selling progress - page {page_index}, {i + 1}/{len(type_selling)}')
                                # print(f'selling {page_index}-{i}')
                                # 演唱會頁面
                                type_selling[i].click()
                                print('concert page', page_kktix_third.url)
                                page_kktix_third.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str = []
                                prices = []
                                performance_datetimes_str = []
                                location = ''
                                if page_kktix_third.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page_kktix_third.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page_kktix_third.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(
                                            ".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page_kktix_third.locator(
                                                ".table-wrapper > table > tbody > tr").nth(
                                                j).locator(
                                                ".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        if page_kktix_third.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(
                                            ".period .period-time").is_visible():
                                            ticket_time = page_kktix_third.locator(
                                                ".table-wrapper > table > tbody > tr").nth(
                                                j).locator(
                                                ".period .period-time").inner_text()
                                            ticket_time = ticket_time[:ticket_time.index('~')]
                                            ticket_time = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", ticket_time)
                                            ticket_time = ticket_time.strip()
                                            if ticket_time not in sell_datetimes_str:
                                                sell_datetimes_str.append(ticket_time)

                                        ''''''

                                        # 票價 list
                                        if page_kktix_third.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(
                                            ".price .price > span").nth(1).is_visible():
                                            price = int(
                                                float(
                                                    page_kktix_third.locator(".table-wrapper > table > tbody > tr").nth(
                                                        j).locator(".price .price > span").nth(1).inner_text().replace(
                                                        ',',
                                                        '')))
                                            prices.append(price)
                                        else:
                                            prices.append(0)
                                        prices = list(set(prices))

                                        ''''''

                                        # 內文
                                        inner_text = page_kktix_third.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page_kktix_third.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page_kktix_third.url)
                                        page_kktix_third.wait_for_timeout(1500)
                                        page_kktix_third.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        if page_kktix_third.locator(
                                                "#registrationsNewApp > div > div:nth-child(2) > div.narrow-wrapper.ng-scope > div > h1").is_visible():
                                            title = page_kktix_third.locator(
                                                "#registrationsNewApp > div > div:nth-child(2) > div.narrow-wrapper.ng-scope > div > h1").inner_text().replace(
                                                '\n', '').strip()
                                        else:
                                            print('title no')

                                        ''''''

                                        # 表演時間 list
                                        if page_kktix_third.locator("tbody > tr").nth(0).locator("td").is_visible():
                                            pdt = \
                                                page_kktix_third.locator("tbody > tr").nth(0).locator(
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
                                            performance_datetimes_str.append(pdt)
                                        else:
                                            print('performance_datetimes no')

                                        ''''''

                                        # 地點 str
                                        if page_kktix_third.locator("tbody > tr").nth(1).locator("th").is_visible():
                                            if page_kktix_third.locator("tbody > tr").nth(1).locator(
                                                    "th").inner_text() == '活動地點':
                                                location_address = \
                                                    page_kktix_third.locator("tbody > tr").nth(1).locator(
                                                        "td").inner_text().split(
                                                        '檢視地圖')[
                                                        0].strip().split(' / ')
                                                location = location_address[0]
                                                # locations.append(concert_place)
                                        else:
                                            print('locations no')

                                        ''''''

                                        page_kktix_third.go_back()
                                        if title or performance_datetimes_str or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str', sell_datetimes_str)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str', performance_datetimes_str)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str,
                                                'loc': [location],
                                                'int': inner_text,
                                                'web': 'kktix',
                                                'url': page_kktix_third.url
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            # json檔案不存在或是裡面沒資料
                                            if not os.path.exists(json_filename_third) or os.path.getsize(
                                                    json_filename_third) <= 4:
                                                # 直接寫入第一筆資料
                                                with open(json_filename_third, "w", encoding="utf-8") as f:
                                                    json.dump([new_data], f, indent=4, ensure_ascii=False)
                                            # json檔案存在且裡面已經有一筆以上的資料
                                            else:
                                                # 讀取現在有的檔案
                                                with open(json_filename_third, "r", encoding="utf-8") as f:
                                                    existing_data = json.load(f)
                                                # 並新增即將寫入的一筆
                                                existing_data.append(new_data)
                                                # 寫入
                                                with open(json_filename_third, "w", encoding="utf-8") as f:
                                                    json.dump(existing_data, f, indent=4, ensure_ascii=False)

                                            last_finished_selling_index = i
                                            print(f'finished {page_index}-{last_finished_selling_index}')
                                            print('\n----------------------\n')

                                    else:
                                        print('hk activity, skip')
                                        last_finished_selling_index = i
                                        print(f'finished {page_index}-{last_finished_selling_index}')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_selling_index = i
                                    print(f'finished {page_index}-{last_finished_selling_index}')
                                    print('\n----------------------\n')
                                    integrate_webs.append(page_kktix_third.url)

                                ''''''

                                page_kktix_third.go_back()  # main page
                                type_selling = page_kktix_third.query_selector_all('li.type-selling')
                        else:
                            print('CSS: "type-selling" of this page is already finished!')

                        ''''''

                        # type-view
                        type_view = page_kktix_third.query_selector_all('li.type-view')
                        print(f'\n\nview start from {page_index}-{last_finished_view_index + 1}\n\n')
                        for i in range(last_finished_view_index + 1, len(type_view)):
                            print(f'kktix view progress - page {page_index}, {i + 1}/{len(type_view)}')
                            # print(f'view {page_index}-{i}')
                            # 演唱會頁面
                            type_view[i].click()
                            print('concert page', page_kktix_third.url)
                            page_kktix_third.wait_for_timeout(500)

                            ''''''

                            hk = False
                            title = ''
                            sell_datetimes_str = []
                            prices = []
                            performance_datetimes_str = []
                            location = ''
                            if page_kktix_third.locator("table > thead > tr > th.name").is_visible():
                                # 確認此頁面是否為香港活動
                                # 1. 迴圈 票種、販售時間、售價 物件個數
                                for j in range(
                                        len(page_kktix_third.query_selector_all(
                                            ".table-wrapper > table > tbody > tr"))):
                                    # 貨幣符號
                                    # 如果有找到貨幣符號
                                    if page_kktix_third.locator(".table-wrapper > table > tbody > tr").nth(j).locator(
                                            ".price .price > span").nth(0).is_visible():
                                        # 取得貨幣符號
                                        currency = page_kktix_third.locator(".table-wrapper > table > tbody > tr").nth(
                                            j).locator(
                                            ".price .price > span").nth(0).inner_text()
                                        # 檢查是否為港幣
                                        if 'hk' in currency.lower():
                                            hk = True
                                            break
                                    # 找不到貨幣符號
                                    else:
                                        currency = ''

                                    ''''''

                                    # 售票時間
                                    if page_kktix_third.locator(".table-wrapper > table > tbody > tr").nth(j).locator(
                                            ".period .period-time").is_visible():
                                        ticket_time = page_kktix_third.locator(
                                            ".table-wrapper > table > tbody > tr").nth(
                                            j).locator(
                                            ".period .period-time").inner_text()
                                        ticket_time = ticket_time[:ticket_time.index('~')]
                                        ticket_time = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", ticket_time)
                                        ticket_time = ticket_time.strip()
                                        if ticket_time not in sell_datetimes_str:
                                            sell_datetimes_str.append(ticket_time)

                                    ''''''

                                    # 票價
                                    if page_kktix_third.locator(".table-wrapper > table > tbody > tr").nth(j).locator(
                                            ".price .price > span").nth(1).is_visible():
                                        price = int(
                                            float(page_kktix_third.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(1).inner_text().replace(',',
                                                                                                               '')))
                                        prices.append(price)
                                    else:
                                        prices.append(0)
                                    prices = list(set(prices))

                                    ''''''

                                    # 內文
                                    inner_text = page_kktix_third.locator(".description").inner_text()

                                    ''''''

                                if not hk:
                                    # 進入購票頁面，獲得地點以及表演時間
                                    page_kktix_third.locator(".outer-wrapper .tickets .btn-point").click()
                                    print('buy ticket page', page_kktix_third.url)
                                    page_kktix_third.wait_for_timeout(1500)
                                    page_kktix_third.wait_for_load_state('load')

                                    ''''''

                                    # 標題
                                    if page_kktix_third.locator(
                                            "#registrationsNewApp > div > div:nth-child(2) > div.narrow-wrapper.ng-scope > div > h1").is_visible():
                                        title = page_kktix_third.locator(
                                            "#registrationsNewApp > div > div:nth-child(2) > div.narrow-wrapper.ng-scope > div > h1").inner_text().replace(
                                            '\n', '').strip()
                                    else:
                                        print('title no')

                                    ''''''

                                    # 表演時間
                                    if page_kktix_third.locator("tbody > tr").nth(0).locator("td").is_visible():
                                        pdt = \
                                            page_kktix_third.locator("tbody > tr").nth(0).locator(
                                                "td").inner_text().split(
                                                '加入行事曆')[
                                                0].strip()
                                        pdt = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", pdt)
                                        if '~' in pdt:
                                            start_time_date = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', pdt.split('~')[0])
                                            finish_time_date = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', pdt.split('~')[1])
                                            if start_time_date[0] == finish_time_date[0]:
                                                pdt = pdt.split('~')[0].strip()
                                        pdt = re.sub(r"\s{2,}", " ", pdt)
                                        pdt = pdt.strip()
                                        performance_datetimes_str.append(pdt)
                                    else:
                                        print('performance_datetimes no')

                                    ''''''

                                    # 地點
                                    if page_kktix_third.locator("tbody > tr").nth(1).locator("th").is_visible():
                                        if page_kktix_third.locator("tbody > tr").nth(1).locator(
                                                "th").inner_text() == '活動地點':
                                            location_address = \
                                                page_kktix_third.locator("tbody > tr").nth(1).locator(
                                                    "td").inner_text().split(
                                                    '檢視地圖')[
                                                    0].strip().split(' / ')
                                            location = location_address[0]
                                            # locations.append(concert_place)
                                    else:
                                        print('locations no')

                                    ''''''

                                    page_kktix_third.go_back()
                                    if title or performance_datetimes_str or location:
                                        print('title', title)  # str
                                        print('sell_datetimes_str', sell_datetimes_str)  # list
                                        print('prices', prices)  # list
                                        print('performance_datetimes_str', performance_datetimes_str)  # list
                                        print('location', location)  # str

                                        # 新的一筆資料
                                        new_data = {
                                            'tit': title,
                                            'sdt': sell_datetimes_str,
                                            'prc': prices,
                                            'pdt': performance_datetimes_str,
                                            'loc': [location],
                                            'int': inner_text,
                                            'web': 'kktix',
                                            'url': page_kktix_third.url
                                        }

                                        print('\n--- write new data ---\n')

                                        # json檔案不存在或是裡面沒資料
                                        if not os.path.exists(json_filename_third) or os.path.getsize(
                                                json_filename_third) <= 4:
                                            # 直接寫入第一筆資料
                                            with open(json_filename_third, "w", encoding="utf-8") as f:
                                                json.dump([new_data], f, indent=4, ensure_ascii=False)
                                        # json檔案存在且裡面已經有一筆以上的資料
                                        else:
                                            # 讀取現在有的檔案
                                            with open(json_filename_third, "r", encoding="utf-8") as f:
                                                existing_data = json.load(f)
                                            # 並新增即將寫入的一筆
                                            existing_data.append(new_data)
                                            # 寫入
                                            with open(json_filename_third, "w", encoding="utf-8") as f:
                                                json.dump(existing_data, f, indent=4, ensure_ascii=False)

                                        last_finished_view_index = i
                                        print(f'finished {page_index}-{last_finished_view_index}\n')
                                        print('\n----------------------\n')


                                else:
                                    print('hk activity, skip')
                                    last_finished_view_index = i
                                    print(f'finished {page_index}-{last_finished_view_index}\n')
                                    print('\n----------------------\n')

                            else:
                                print('integrate webpage, skip')
                                last_finished_view_index = i
                                print(f'finished {page_index}-{last_finished_view_index}\n')
                                print('\n----------------------\n')
                                integrate_webs.append(page_kktix_third.url)

                            ''''''

                            page_kktix_third.go_back()  # main page
                            type_view = page_kktix_third.query_selector_all('li.type-view')

                        ''''''

                        # 完成此頁
                        pagination_div = page_kktix_third.query_selector(".pagination.pull-right")
                        text = pagination_div.inner_text()
                        print(f'\nFinished page {page_index}')
                        completed_pages.append(page_index)
                        last_finished_selling_index = -1
                        last_finished_view_index = -1

                    # 有下一頁
                    if '›' in text:
                        page_kktix_third.locator("div.pagination.pull-right li:last-child").click()
                        page_index += 1
                        current_page_index = page_index
                        print(f'\nGo to page {page_index}\n')

                    # 最後一頁
                    else:
                        print('kktix finished')

                        # 程式確認沒有最後一頁後跳出while True的break
                        break

                # 確認全部執行完成，沒有發生錯誤的break
                break

            except Exception as e:
                # 錯誤
                page_kktix_third.close()
                print(e, 'kktix restart')
                if [current_page_index, last_finished_selling_index, last_finished_view_index] not in fail_indices:
                    fail_indices.append([current_page_index, last_finished_selling_index, last_finished_view_index])
                    print('first failure')
                else:
                    print('second failure')

                    with open('wrong_log.txt', "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    if page_kktix_third.url + '\n' not in lines:
                        # txt檔案不存在或是裡面沒資料
                        if not os.path.exists('wrong_log.txt') or os.path.getsize('wrong_log.txt') <= 4:
                            # 寫入第一筆資料
                            with open('wrong_log.txt', "w", encoding="utf-8") as f:
                                f.write(f'KKTIX\n{e}\n{page_kktix_third.url}\n')
                        # txt檔案存在且裡面已經有一筆以上的資料
                        else:
                            # 讀取現在有的檔案
                            with open('wrong_log.txt', "a", encoding="utf-8") as f:
                                f.write(f'\nKKTIX\n{e}\n{page_kktix_third.url}\n')
                    else:
                        print('已經寫進錯誤裡面了!')

                    print('skip')

                    if last_finished_view_index == -1:
                        last_finished_selling_index += 1
                    else:
                        last_finished_view_index += 1
                # 重新啟動
                continue

        # 完成
        page_kktix_third.close()


def get_kktix():
    thread_first = threading.Thread(target=get_kktix_first)
    thread_second = threading.Thread(target=get_kktix_second)
    thread_third = threading.Thread(target=get_kktix_third)

    thread_first.start()
    thread_second.start()
    thread_third.start()

    thread_first.join()
    thread_second.join()
    thread_third.join()

    print('--- Scraping finished!! ---')

    json_filenames = ['kktix_new_first.json',
                      'kktix_new_second.json',
                      'kktix_new_third.json']

    merged_data = []

    for file in json_filenames:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            merged_data.extend(data)

        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=4, ensure_ascii=False)

    os.remove('kktix_new_first.json')
    os.remove('kktix_new_second.json')
    os.remove('kktix_new_third.json')

    print('integrate_webs =', integrate_webs)
    print()

    # integrate_webs = [
    #     'https://best-onlineteam.kktix.cc/events/rtjetycz', 'https://tix-get-go.kktix.cc/events/jungyonghwa2023',
    #     'https://kklivetw.kktix.cc/events/2024-ennocheng-golden-trilogy',
    #     'https://horizons.kktix.cc/events/bossnoeul2312', 'https://best-onlineteam.kktix.cc/events/3ab0b078',
    #     'https://skn.kktix.cc/events/workcation2311', 'https://sunchaseproductions.kktix.cc/events/anpuhk2024',
    #     'https://yourwomansleepwithothers.kktix.cc/events/rthwvs', 'https://rockempire.kktix.cc/events/741e5938',
    #     'https://emergelivehouse2.kktix.cc/events/8842020d', 'https://tix-get-go.kktix.cc/events/harleydavidson',
    #     'https://himmusic.kktix.cc/events/cc65c741', 'https://redholic.kktix.cc/events/samajam',
    #     'https://tix-get-go.kktix.cc/events/okiedokiethaipop', 'https://tix-get-go.kktix.cc/events/alfredhuilive2023',
    #     'https://i-chen.kktix.cc/events/9f5f1aa1', 'https://spaceport.kktix.cc/events/spaceport2023']

    with sync_playwright() as p:
        print('integrated_webs =', integrate_webs)
        print('\n開始統整資料!\n')

        # 完成的web就加進這個list，發生錯誤之後，直接跳過這些完成的web
        completed_webs = []
        # 全部執行之後，仍然失敗的網站
        fail_webs = []
        # 上一個完成的index
        last_finished_index = -1
        current_web = ''
        current_web_index = ''

        # 執行完一般資料後，來確認統整資料
        while True:
            try:

                browser = p.chromium.launch(headless=False)
                context_kktix = browser.new_context()
                page_kktix = context_kktix.new_page()
                page_kktix.set_default_timeout(60000)

                ''''''

                with open(json_filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                ''''''

                for k, web in enumerate(integrate_webs):
                    if web not in completed_webs:
                        current_web = web
                        page_kktix.goto(web)

                        events = page_kktix.query_selector_all(".clearfix > li")

                        # 統整頁面，下方有幾個演唱會物件
                        print(f'\n進入迴圈 {k}-{last_finished_index + 1}\n')
                        for i in range(last_finished_index + 1, len(events)):
                            current_web_index = i
                            if page_kktix.locator(".clearfix > li").nth(i).locator(
                                    "div > div > h2 > a").is_visible():
                                # 演唱會頁面
                                page_kktix.locator(".clearfix > li").nth(i).locator("div > div > h2 > a").click()

                                # 已經瀏覽過
                                duplicate = False
                                for j in range(len(data)):
                                    if page_kktix.url == data[j]['url']:
                                        print('這個重複了')
                                        last_finished_index = i
                                        print('\n----------------------')
                                        print(f'finished {k}-{current_web_index}')
                                        print('----------------------\n')
                                        duplicate = True

                                if not duplicate:
                                    hk = False
                                    title = ''
                                    sell_datetimes_str = []
                                    prices = []
                                    performance_datetimes_str = []
                                    location = ''
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(len(page_kktix.query_selector_all(
                                            ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page_kktix.locator(".table-wrapper > table > tbody > tr").nth(j).locator(
                                                ".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page_kktix.locator(
                                                ".table-wrapper > table > tbody > tr").nth(j).locator(
                                                ".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間
                                        if page_kktix.locator(".table-wrapper > table > tbody > tr").nth(j).locator(
                                                ".period .period-time").is_visible():
                                            ticket_time = page_kktix.locator(
                                                ".table-wrapper > table > tbody > tr").nth(
                                                j).locator(
                                                ".period .period-time").inner_text()
                                            ticket_time = ticket_time[:ticket_time.index('~')]
                                            ticket_time = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", ticket_time)
                                            ticket_time = ticket_time.strip()
                                            if ticket_time not in sell_datetimes_str:
                                                sell_datetimes_str.append(ticket_time)

                                        ''''''

                                        # 票價
                                        if page_kktix.locator(".table-wrapper > table > tbody > tr").nth(j).locator(
                                                ".price .price > span").nth(1).is_visible():
                                            price = int(
                                                float(page_kktix.locator(".table-wrapper > table > tbody > tr").nth(
                                                    j).locator(".price .price > span").nth(1).inner_text().replace(
                                                    ',', '')))
                                            prices.append(price)
                                        else:
                                            prices.append(0)
                                        prices = list(set(prices))

                                        ''''''

                                        # 內文
                                        inner_text = page_kktix.locator(".description").inner_text()

                                        ''''''

                                    # 如果不是香港活動
                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page_kktix.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('購票頁面', page_kktix.url)
                                        page_kktix.wait_for_timeout(1500)
                                        page_kktix.wait_for_load_state('load')

                                        ''''''

                                        # 標題
                                        if page_kktix.locator(
                                                "#registrationsNewApp > div > div:nth-child(2) > div.narrow-wrapper.ng-scope > div > h1").is_visible():
                                            title = page_kktix.locator(
                                                "#registrationsNewApp > div > div:nth-child(2) > div.narrow-wrapper.ng-scope > div > h1").inner_text().replace(
                                                '\n', '').strip()
                                        else:
                                            title = ''
                                            print('title no')

                                        ''''''

                                        # 表演時間
                                        if page_kktix.locator("tbody > tr").nth(0).locator("td").is_visible():
                                            pdt = \
                                                page_kktix.locator("tbody > tr").nth(0).locator(
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
                                            performance_datetimes_str.append(pdt)
                                        else:
                                            print('performance_datetimes no')

                                        ''''''

                                        # 地點
                                        if page_kktix.locator("tbody > tr").nth(1).locator("th").is_visible():
                                            if page_kktix.locator("tbody > tr").nth(1).locator(
                                                    "th").inner_text() == '活動地點':
                                                location_address = \
                                                    page_kktix.locator("tbody > tr").nth(1).locator(
                                                        "td").inner_text().split(
                                                        '檢視地圖')[
                                                        0].strip().split(' / ')
                                                location = location_address[0]
                                        else:
                                            location = ''
                                            print('locations no')

                                        ''''''

                                        page_kktix.go_back()
                                        if title or performance_datetimes_str or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str', sell_datetimes_str)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str', performance_datetimes_str)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str,
                                                'loc': [location],
                                                'int': inner_text,
                                                'web': 'kktix',
                                                'url': page_kktix.url
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
                                            print('\n----------------------')
                                            print(f'finished {k}-{current_web_index}')
                                            print('----------------------\n')
                                            if [current_web, last_finished_index] in fail_webs:
                                                del fail_webs[fail_webs.index([current_web, last_finished_index])]

                                        else:
                                            print('什麼都沒有 不寫')
                                            last_finished_index = i
                                            print('\n----------------------')
                                            print(f'finished {k}-{current_web_index}')
                                            print('----------------------\n')

                                    # 是香港活動，跳過
                                    else:
                                        print('香港活動，跳過')
                                        last_finished_index = i
                                        print('\n----------------------')
                                        print(f'finished {k}-{current_web_index}')
                                        print('----------------------\n')

                                # 返回統整頁面
                                page_kktix.go_back()
                                # 重置完成座標
                                last_finished_index = -1

                        # 這個web完成
                        completed_webs.append(web)
                        print(f'已經完成第{k}頁')

                    else:
                        # 這個統整頁面都點擊完了，換下一個統整頁面
                        print(f'第{k}頁發生錯誤之前已經確認過了!\n')

                break

            except Exception as e:
                page_kktix.close()
                print(e, 'kktix restart')
                print('發生錯誤了!', [current_web, current_web_index])
                if [current_web, current_web_index] not in fail_webs:
                    fail_webs.append([current_web, current_web_index])
                    print('\n是第一次失敗\n')
                else:
                    print('\n已經是第二次失敗了')
                    print('跳過\n')
                    last_finished_index += 1

                # 重新啟動
                continue

        print('\nDelete past ticket sale schedules\n')

        # 刪除時間已經過去的售票時間
        with open(json_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for i in range(len(data)):
            print('i =', i)
            print(data[i]['tit'])
            # 如果含有售票時間
            if data[i]['sdt']:
                # 有些售票時間會是 "~yyyy/mm/dd hh:mm"
                # 這會導致有些售票時間為""，無法通過 datetime.strptime(sdt, '%Y/%m/%d %H:%M')
                # 我們需要把那些""給去除掉
                sdts = [sdt for sdt in data[i]['sdt'] if sdt != '']
                data[i]['sdt'] = sdts
                with open(json_filename, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)

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

        print('kktix done')


# get_kktix()
