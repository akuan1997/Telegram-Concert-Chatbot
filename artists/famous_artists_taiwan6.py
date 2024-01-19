from web_scraping.sync_api import sync_playwright, Playwright

filename = 'user_defined_global_top100.txt'

with open(filename, 'w', encoding='utf-8') as f:
    f.write('')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    for i in range(6, 24):
        if i < 10:
            s1 = f'https://www.billboard.com/charts/year-end/200{i}/hot-100-artists/'
            page.goto(s1)
        else:
            s2 = f'https://www.billboard.com/charts/year-end/20{i}/hot-100-artists/'
            page.goto(s2)

        for j in range(1, 110):
            s3 = f'.o-chart-results-list-row-container:nth-child({j}) > ul:nth-child(1) > li:nth-child(3) > ul > li > h3'
            if page.locator(s3).is_visible():
                with open(filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                lines = [line.replace('\n', '') for line in lines]

                if page.locator(s3).inner_text() not in lines:
                    print(page.locator(s3).inner_text())
                    with open('user_defined_global_top100.txt', 'a', encoding='utf-8') as f:
                        f.write(page.locator(s3).inner_text() + '\n')
                else:
                    print('已經有了')
