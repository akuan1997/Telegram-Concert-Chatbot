# from playwright.sync_api import sync_playwright, Playwright
# from playwright.sync_api import expect, Page
#
# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#
#     page.goto("https://zh.wikipedia.org/zh-tw/%E8%94%A1%E4%BE%9D%E6%9E%97")
#
#     images = page.query_selector_all('meta[property="og:image"][content*="https://upload.wikimedia.org/wikipedia/"]')
#     print(len(images))
#     print(images[0].get_attribute('content'))
#     if page.locator(".cdx-text-input__input").nth(0).is_visible():
#         print('hello')
#         keyword = '王力宏'
#         page.locator(".cdx-text-input__input").nth(0).fill(keyword)
#         first_search_result = page.locator("#cdx-menu-item-1 > a > span:nth-child(2) > span > bdi > span").inner_text()
#         if keyword in first_search_result:
#             print("that's what I want")
#             page.locator("#cdx-menu-item-1").click()
#     else:
#         print('ni hao')
#     # page.locator("#p-search > a > span.vector-icon.mw-ui-icon-search.mw-ui-icon-wikimedia-search").click()
#     #
#     page.wait_for_timeout(30000)

''''''

import json
import re
from datetime import datetime, timedelta

with open('concert_4_15_1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


def replace_time(text):
    pattern = r'\d{2}:\d{2}'  # 匹配時間的正則表達式模式
    text = re.sub(pattern, '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()  # 去除首尾空格


def format_date(date_str):
    parts = date_str.split('-')
    month = parts[1].zfill(2)  # 用 zfill(2) 將月份填充成兩位數
    day = parts[2].zfill(2)  # 用 zfill(2) 將日期填充成兩位數
    return f"{parts[0]}-{month}-{day}"


def generate_date_range(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    date_range = []
    current_date = start_date

    while current_date <= end_date:
        date_range.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    return date_range


for i in range(len(data)):
    if data[i]['pdt']:
        date = replace_time(data[i]['pdt'][0]).replace('/', '-')

        if '~' not in date:
            date = format_date(date)
            print(date)
        else:
            date = f"{format_date(date.split(' ~ ')[0])} ~ {date.split(' ~ ')[1]}"
            date_range = generate_date_range(date.split(' ~ ')[0], date.split(' ~ ')[1])
            concert_dates = []
            for i in range(len(date_range)):
                concert_dates.append({f"concert_date": date_range[i]})
            print(concert_dates)

''''''
