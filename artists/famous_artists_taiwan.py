# https://www.last.fm/tag/taiwanese/artists?page=1
from web_scraping.sync_api import sync_playwright, Playwright

filename = 'user_defined_lastfm.txt'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.last.fm/tag/taiwanese/artists?page=1")

    page_number = int(page.locator(
        "#mantle_skin > div:nth-child(3) > div > div.col-main > nav > ul > li:nth-child(8) > a").inner_text())

    for i in range(page_number - 1):
        names = page.query_selector_all(".big-artist-list-title")
        for j in range(len(names)):
            print(names[j].inner_text())

            with open('user_defined_lastfm.txt', 'r', encoding='utf-8') as f:
                exist_singer_names = f.readlines()

            if names[j].inner_text() not in exist_singer_names:
                with open('user_defined_lastfm.txt', 'a', encoding='utf-8') as f:
                    f.write(names[j].inner_text() + '\n')

        # 下一頁
        page.locator("#mantle_skin > div:nth-child(3) > div > div.col-main > nav > ul > li.pagination-next").click()
        page.wait_for_timeout(1500)
