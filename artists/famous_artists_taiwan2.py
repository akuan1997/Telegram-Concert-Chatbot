# https://zh.wikipedia.org/zh-tw/Category:%E5%8F%B0%E7%81%A3%E6%A8%82%E5%9C%98
from web_scraping.sync_api import sync_playwright, Playwright

filename = 'user_defined_lastfm.txt'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://zh.wikipedia.org/zh-tw/Category:%E5%8F%B0%E7%81%A3%E6%A8%82%E5%9C%98")

    singer_groups = page.query_selector_all("#mw-pages > div > div > div")

    for i in range(len(singer_groups)):
        s1 = f'#mw-pages > div > div > div:nth-child({i+1}) > ul > li'
        singers = page.query_selector_all(s1)
        for j in range(len(singers)):
            s2 = f'#mw-pages > div > div > div:nth-child({i+1}) > ul > li:nth-child({j+1}) > a'
            print(page.locator(s2).inner_text())
            with open('user_defined_taiwan_bands.txt', 'a', encoding='utf-8') as f:
                f.write(page.locator(s2).inner_text() + '\n')