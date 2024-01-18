from playwright.sync_api import sync_playwright, Playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://ticketplus.com.tw/activity/8455304be5b4ffef154340fd40d9dfa7")
    page.wait_for_timeout(1500)
    columns = page.query_selector_all("#buyTicket > .sesstion-item")
    print(len(columns))
    for j in range(len(columns)):
        text = page.locator("#buyTicket > .sesstion-item").nth(j).inner_text()
        print(text)
        print('--------------------------------------------')
        # print(f'j = {j}')
        # css = f'#buyTicket > .sesstion-item:nth-child{j + 1}'
        # print(page.locator(css).inner_text())
    # for j in range(len(columns)):
    #     print(page.locator("#buyTicket > .sesstion-item").nth(j))
    # print('0')
    # print(page.locator("#buyTicket > .sesstion-item").nth(0).locator("div").nth(0).inner_text())
    # print('1')
    # print(page.locator("#buyTicket > .sesstion-item").nth(0).locator("div").nth(1).inner_text())
    # print('2')
    # print(page.locator("#buyTicket > .sesstion-item").nth(0).locator("div").nth(2).inner_text())
    # print('3')
    # print(page.locator("#buyTicket > .sesstion-item").nth(0).locator("div").nth(3).inner_text())
    # print('4')
    # print(page.locator("#buyTicket > .sesstion-item").nth(0).locator("div").nth(4).inner_text())
    # print('5')
    # print(page.locator("#buyTicket > .sesstion-item").nth(0).locator("div").nth(5).inner_text())
    # print('6')
    # print(page.locator("#buyTicket > .sesstion-item").nth(0).locator("div").nth(6).inner_text())
    # print('7')
    # print(page.locator("#buyTicket > .sesstion-item").nth(0).locator("div").nth(7).inner_text())
    # print('8')
    # print(page.locator("#buyTicket > .sesstion-item").nth(0).locator("div").nth(8).inner_text())
    # print('9')
    # print(page.locator("#buyTicket > .sesstion-item").nth(0).locator("div").nth(9).inner_text())
    # for j in range(len(columns)):
    #     column_text = page.locator("#buyTicket > .sesstion-item").nth(j).locator("div > div > div").nth(
    #         0).inner_text()
    #     print('---')
    #     print(column_text)
    #     print('---')
    #     column_text = column_text.split('\n')
    #     # 日期 & 時間
    #     concert_date = column_text[1].replace('-', '/')
    #     concert_date = concert_date[:concert_date.index('(')]
    #     concert_time = column_text[2]
    #     pdt = concert_date + ' ' + concert_time
    #     # 地點
    #     concert_place = column_text[3]
    #
    #     print('date', concert_date)
    #     print('time', concert_time)
    #     print('pdt', pdt)
    #     print('place', concert_place)
