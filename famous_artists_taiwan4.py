from web_scraping.sync_api import sync_playwright, Playwright

filename = 'user_defined_lastfm.txt'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E6%AD%8C%E6%89%8B%E5%88%97%E8%A1%A8")

    page.wait_for_timeout(1000)

    for i in range(9, 67, 2):
        # print(f'i = {i}')
        s1 = f"#mw-content-text > div.mw-content-ltr.mw-parser-output > table:nth-child({i}) > tbody > tr"
        singers = page.query_selector_all(s1)
        print(f'有{len(singers)}個歌手')
        for j in range(2, len(singers) + 1):
            # print(f'j = {j}')
            s2 = f'#mw-content-text > div.mw-content-ltr.mw-parser-output > table:nth-child({i}) > tbody > tr:nth-child({j}) > td:nth-child(1) > a'
            if page.locator(s2).is_visible():
                print(page.locator(s2).inner_text())
                with open('user_defined_taiwan_singers.txt', 'a', encoding='utf-8') as f:
                    f.write(page.locator(s2).inner_text() + '\n')
            else:
                print('!!!!!!!')
        print('---')
