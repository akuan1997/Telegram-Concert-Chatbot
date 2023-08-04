from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import re, os, json
from datetime import datetime, time
from get_data_functions import \
    get_all_performance_time_single_line, \
    al_lines, sort_datetime, \
    prc_lines, get_prices, \
    get_sell_datetimes, get_dts_lctns
import os, sys

filename = 'livenation_folder/livenation_new_concert_data_test.json'


def get_livenation():
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('')

    with sync_playwright() as p:
        while True:
            try:
                browser = p.chromium.launch(headless=False)
                context_livenation = browser.new_context()
                page_livenation = context_livenation.new_page()

                page_livenation.goto("https://www.livenation.com.tw/event/allevents")

                events = page_livenation.query_selector_all(".result-card__image")

                for i in range(len(events)):
                    events[i].click()

                    with open('livenation_folder/livenation_temp_test.txt', 'w', encoding='utf-8') as f:
                        f.write(page_livenation.locator(
                            "#top > main > div > div.layout__container > div.accordion__accordion > div > div > div").inner_text())

                    with open('livenation_folder/livenation_temp_test.txt', 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    ''' 票價 (price_lines) '''
                    price_lines = prc_lines(lines)
                    prices = get_prices(price_lines)

                    ''' 售票時間 (all_lines) '''
                    all_lines, sell_datetimes = get_sell_datetimes(al_lines(lines))

                    ''' 演唱會標題 '''
                    title = page_livenation.locator(".eventblurb__title[data-ln='EventName']").inner_text().replace(
                        '\n',
                        '').strip()

                    ''' 表演地點 '''
                    location = page_livenation.locator(
                        "#top > main > div > div.layout__container > div.eventblurb__container > div > div > "
                        "div.eventblurb__detailscontainer > h2 > div > a").inner_text()
                    locations = [location]
                    ''' 表演時間 '''
                    day = page_livenation.locator(
                        "#top > main > div > div.layout__container > div.eventblurb__container > div > div > div:nth-child(1) > "
                        "div > span.date__day").inner_text()
                    month_year = page_livenation.locator(
                        "#top > main > div > div.layout__container > div.eventblurb__container > div > div > div:nth-child(1) > "
                        "div > span.date__month").inner_text()
                    year = month_year[month_year.index(' ') + 1:]
                    month = month_year[:month_year.index(' ') - 1]
                    performance_datetime = year + '/' + month + '/' + day + ' ' + page_livenation.locator(
                        "#top > main > div > div.layout__container > div.eventblurb__container > div > div > "
                        "div.eventblurb__detailscontainer > h3").inner_text()
                    performance_datetimes = [performance_datetime]
                    print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
                    print('tit', title)
                    print('sel', sell_datetimes)
                    print('pri', prices)
                    print('pdt', performance_datetimes)
                    print('lcs', locations)
                    print('web', 'live nation')
                    print('url', page_livenation.url)
                    # print('------------------------------------------------------')

                    sell_datetimes_str = [str(sell_datetime)[:-3].replace('-', '/') for sell_datetime in sell_datetimes]
                    # performance_datetimes_str = [str(performance_datetime)[:-3].replace('-', '/') for
                    #                              performance_datetime in performance_datetimes]

                    new_data = {
                        'title': title,
                        'sell_datetimes': sell_datetimes_str,
                        'prices': prices,
                        'performance_datetimes': performance_datetimes,
                        'locations': locations,
                        'website': 'live nation',
                        'url': page_livenation.url
                    }

                    if not os.path.exists(filename) or os.path.getsize(filename) <= 4:  # json file not exists
                        with open(filename, "w", encoding="utf-8") as f:
                            json.dump([new_data], f, indent=4, ensure_ascii=False)
                    else:  # json file exists
                        with open(filename, "r", encoding="utf-8") as f:
                            existing_data = json.load(f)

                        existing_data.append(new_data)
                        with open(filename, "w", encoding="utf-8") as f:
                            json.dump(existing_data, f, indent=4, ensure_ascii=False)

                    print()

                    page_livenation.go_back()
                    events = page_livenation.query_selector_all(".result-card__image")

                page_livenation.close()
                print('livenation finished')
                break
            except Exception as e:
                print(e, 'livenation restart')
                continue

# get_livenation()