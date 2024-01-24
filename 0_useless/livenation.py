from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import re, os, json
from datetime import datetime, time
import os, sys
from get_data_from_text import get_prices, get_time_lines, get_sell, get_performance_location, get_start_time

json_filename = '../livenation.json'
txt_filename = 'livenation_temp.txt'


def get_livenation():
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
                context_livenation = browser.new_context()
                page_livenation = context_livenation.new_page()

                page_livenation.goto("https://www.livenation.com.tw/event/allevents")

                events = page_livenation.query_selector_all(".result-card__image")

                for i in range(last_finished_index + 1, len(events)):
                    print(f'live nation progress - {i + 1}/{len(events)}')
                    events[i].click()

                    # 下載內文
                    inner_text = page_livenation.locator(
                            "#top > main > div > div.layout__container > div.accordion__accordion > div > div > div").inner_text()
                    with open(txt_filename, 'w', encoding='utf-8') as f:
                        f.write(inner_text)

                    # # demo text
                    # with open(f'demo_livenation{i}.txt', 'w', encoding='utf-8') as f:
                    #     f.write(page_livenation.locator(
                    #         "#top > main > div > div.layout__container > div.accordion__accordion > div > div > div").inner_text())

                    # 讀取內文
                    with open(txt_filename, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    # 演唱會標題
                    title = page_livenation.locator(".eventblurb__title[data-ln='EventName']").inner_text().replace(
                        '\n', '').strip()

                    # 票價 (一定得從內文當中獲得)
                    prices = get_prices(lines)

                    # 售票時間 (一定得從內文當中獲得)
                    without_sell_time_lines, sell_datetimes_str = get_sell(get_time_lines(lines))

                    # 表演地點
                    location = page_livenation.locator(
                        "#top > main > div > div.layout__container > div.eventblurb__container > div > div > "
                        "div.eventblurb__detailscontainer > h2 > div > a").inner_text()
                    # locations = [location]

                    # 表演時間
                    day = page_livenation.locator(
                        "#top > main > div > div.layout__container > div.eventblurb__container > div > div > div:nth-child(1) > "
                        "div > span.date__day").inner_text()
                    month_year = page_livenation.locator(
                        "#top > main > div > div.layout__container > div.eventblurb__container > div > div > div:nth-child(1) > "
                        "div > span.date__month").inner_text()
                    year = month_year[month_year.index(' ') + 1:]
                    month = month_year[:month_year.index(' ') - 1]
                    if page_livenation.locator(
                        "#top > main > div > div.layout__container > div.eventblurb__container > div > div > "
                        "div.eventblurb__detailscontainer > h3").is_visible():
                        performance_time = page_livenation.locator(
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
                    print('web', 'live nation')
                    print('url', page_livenation.url)

                    new_data = {
                        'tit': title,
                        'sdt': sell_datetimes_str,
                        'prc': prices,
                        'pdt': [performance_datetime],
                        'loc': [location],
                        'int': inner_text,
                        'web': 'live nation',
                        'url': page_livenation.url
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
                    if page_livenation.url in fail_urls:
                        del fail_urls[fail_urls.index(page_livenation.url)]

                    # 返回主頁面
                    page_livenation.go_back()
                    events = page_livenation.query_selector_all(".result-card__image")

                # 完成
                page_livenation.close()
                # 刪除文字暫存檔
                os.remove(txt_filename)

                # 刪除時間已經過去的售票時間
                with open(json_filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                for i in range(len(data)):
                    print('i =', i)
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

                print('livenation done')
                break

            except Exception as e:
                # 錯誤
                print(e, 'liveanation restart')
                print('last finished index = ', last_finished_index)
                if page_livenation.url not in fail_urls:
                    print('第一次失敗')
                    fail_urls.append(page_livenation.url)
                else:
                    print('第二次失敗')
                    print('跳過')
                    last_finished_index += 1

                    with open('../failure_log.txt', "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    if page_livenation.url + '\n' not in lines:
                        # txt檔案不存在或是裡面沒資料
                        if not os.path.exists('../failure_log.txt') or os.path.getsize('../failure_log.txt') <= 4:
                            # 直接寫入第一筆資料
                            with open('../failure_log.txt', "w", encoding="utf-8") as f:
                                f.write(f'liveanation\n{e}\n{page_livenation.url}\n')
                        # txt檔案存在且裡面已經有一筆以上的資料
                        else:
                            # 讀取現在有的檔案
                            with open('../failure_log.txt', "a", encoding="utf-8") as f:
                                f.write(f'\nliveanation\n{e}\n{page_livenation.url}\n')
                    else:
                        print('已經寫進錯誤裡面了!')

                    print('liveanation fail urls right now')
                    for url in fail_urls:
                        print(url)

                # 重新啟動
                continue


# get_livenation()
