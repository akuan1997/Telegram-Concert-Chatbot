from playwright.sync_api import sync_playwright, Playwright

filename = 'user_defined_lastfm.txt'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://hackmd.io/BCIhXTjNRz2F49nWeWFSFQ?both&fbclid=IwAR3Iom46SvA0HOkLUICld4LC3y3M5M-5WWKc85QwQbsGQJZBna-sMzt6v_E")

    for i in range(5, 81, 2):
        singers = page.query_selector_all(f'#doc > ul:nth-child({i}) > li')
        for j in range(1, len(singers) + 1):
            s1 = f'#doc > ul:nth-child({i}) > li:nth-child({j}) > span'
            s2 = f'#doc > ul:nth-child({i}) > li:nth-child({j}) > a > span'
            if page.locator(s1).is_visible():
                print(page.locator(s1).inner_text())
                with open('user_defined_taiwan_bands3.txt', 'a', encoding='utf-8') as f:
                    f.write(page.locator(s1).inner_text() + '\n')
            elif page.locator(s2).is_visible():
                print(page.locator(s2).inner_text())
                with open('user_defined_taiwan_bands3.txt', 'a', encoding='utf-8') as f:
                    f.write(page.locator(s2).inner_text() + '\n')
            else:
                print('!!!')
        print('---')