from playwright.sync_api import sync_playwright, Playwright
import re

timeout_seconds = 500

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page_indievox = context.new_page()

    page_indievox.goto("https://www.indievox.com/activity/detail/24_iv0278935")

    # 有立即購買的按鈕
    if page_indievox.locator(".list-inline a.btn.btn-default.btn-lg").is_visible():
        # 點擊購買按鈕
        page_indievox.locator(".list-inline a.btn.btn-default.btn-lg").click()
        page_indievox.wait_for_load_state('load')
        page_indievox.wait_for_timeout(timeout_seconds)

        # 有幾行資訊欄
        for j in range(len(page_indievox.query_selector_all("#gameList > table > tbody > tr"))):
            # 表演時間
            performance_datetime = page_indievox.locator('#gameList > table > tbody > tr').nth(
                j).locator('td').nth(
                0).inner_text()
            performance_datetime = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", performance_datetime)
            performance_datetime = re.sub(r"\s{2,}", " ", performance_datetime)
            performance_datetime = performance_datetime.strip()
            # 地點
            # location = page_indievox.locator("#gameList > table > tbody > tr").nth(j).locator("td").nth(
            #     2).inner_text()

            ''''''

            no_price = True

            # 沒票價 但有購票的按鈕 再往前一個頁面
            if no_price and page_indievox.locator('#gameList > table > tbody > tr').nth(j).locator(
                    'td > button').is_visible():
                no_price = True
                page_indievox.locator('#gameList > table > tbody > tr').nth(j).locator(
                    'td > button').click()
                page_indievox.wait_for_load_state('load')
                page_indievox.wait_for_timeout(timeout_seconds)

                for k in range(len(page_indievox.query_selector_all("#ticketPriceList > tbody > tr"))):
                    price_line = re.sub(r',', '',
                                        page_indievox.locator("#ticketPriceList > tbody > tr").nth(
                                            k).locator("td.fcBlue > h4").inner_text())
                    not_digit_index = 0
                    for i in range(len(price_line) - 1, 0, -1):
                        if not price_line[i].isdigit():
                            not_digit_index = i
                            break
                    prices.append(price_line[not_digit_index + 1:])

                    page_indievox.go_back()
                    # 點擊購買按鈕
                    page_indievox.locator(".list-inline a.btn.btn-default.btn-lg").click()
                    page_indievox.wait_for_load_state('load')
                    page_indievox.wait_for_timeout(timeout_seconds)

            ''''''

            # print('tit', title)  # str
            # print('sdt', sell_datetimes_str)  # list
            print('prc', prices)  # list
            print('pdt', performance_datetime)  # str
            # print('loc', location)  # str
            # print('web', 'indievox')
            # print('url', page_indievox.url)

