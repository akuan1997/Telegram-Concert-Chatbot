from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://zh.wikipedia.org/zh-tw/%E8%94%A1%E4%BE%9D%E6%9E%97")

    images = page.query_selector_all('meta[property="og:image"][content*="https://upload.wikimedia.org/wikipedia/"]')
    print(len(images))
    print(images[0].get_attribute('content'))
    if page.locator(".cdx-text-input__input").nth(0).is_visible():
        print('hello')
        keyword = '王力宏'
        page.locator(".cdx-text-input__input").nth(0).fill(keyword)
        first_search_result = page.locator("#cdx-menu-item-1 > a > span:nth-child(2) > span > bdi > span").inner_text()
        if keyword in first_search_result:
            print("that's what I want")
            page.locator("#cdx-menu-item-1").click()
    else:
        print('ni hao')
    # page.locator("#p-search > a > span.vector-icon.mw-ui-icon-search.mw-ui-icon-wikimedia-search").click()
    #
    page.wait_for_timeout(30000)
