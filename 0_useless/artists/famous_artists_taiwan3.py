# https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E6%AD%8C%E6%89%8B%E5%88%97%E8%A1%A8
from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page

filename = 'user_defined_lastfm.txt'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E6%AD%8C%E6%89%8B%E5%88%97%E8%A1%A8")

    page.wait_for_timeout(1000)

    columns = page.query_selector_all("#mw-content-text > div.mw-content-ltr.mw-parser-output > table.wikitable.sortable.jquery-tablesorter > tbody > tr")
    print(len(columns))

    for i in range(len(columns)):
        s1 = f'#mw-content-text > div.mw-content-ltr.mw-parser-output > table.wikitable.sortable.jquery-tablesorter > tbody > tr:nth-child({i+1}) > td:nth-child(1)'
        # with open('user_defined_taiwan_bands2.txt', 'a', encoding='utf-8') as f:
        #     f.write(page.locator(s1).inner_text() + '\n')