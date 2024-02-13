from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(5000)

    page.goto("https://ticketplus.com.tw/activity/c9a76e7d40f6ee078ad521eb85e45846")
    page.wait_for_timeout(1500)
    page.wait_for_load_state('load')
    # 資訊欄
    columns = page.query_selector_all("#buyTicket > .sesstion-item")
    column_text = page.locator("#buyTicket > .sesstion-item").nth(0).locator(
        "div > div > div").nth(
        0).inner_text()

    for j in range(len(columns)):
        column_text = page.locator("#buyTicket > .sesstion-item").nth(j).locator(
            "div > div > div").nth(
            0).inner_text()
        print(column_text)
        column_text = column_text.split('\n')

        # 第幾個位置是時間?
        time_index = -1
        for k in range(1, len(column_text)):
            if ':' in column_text[k] or '：' in column_text[k]:
                time_index = k
                break
        print(f'time_index = {time_index}')
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

