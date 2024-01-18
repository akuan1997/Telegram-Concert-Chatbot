from web_scraping.sync_api import sync_playwright, Playwright
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.indievox.com/ticket/ticket/24_iv0278935/16510/1/67")

    prices = []

    columns = page.query_selector_all("#ticketPriceList > tbody > tr")
    page.wait_for_timeout(1500)
    print(len(columns))
    for i in range(len(columns)):
        price_line = re.sub(r',', '', page.locator("#ticketPriceList > tbody > tr").nth(i).locator(
            "td.fcBlue > h4").inner_text())
        not_digit_index = 0
        for j in range(len(price_line) - 1, 0, -1):
            if not price_line[j].isdigit():
                not_digit_index = j
                break
        prices.append(price_line[not_digit_index + 1:])
    print(prices)

