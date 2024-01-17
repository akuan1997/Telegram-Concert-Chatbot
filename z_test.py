from playwright.sync_api import sync_playwright, Playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://zh.wikipedia.org/zh-tw/J.Sheon")

    page.wait_for_timeout(15000)

