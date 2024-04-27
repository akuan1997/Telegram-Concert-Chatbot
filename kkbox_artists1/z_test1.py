from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://google.com")

    page.wait_for_selector("#APjFqb", state="visible")

    page.locator("#APjFqb").fill("SHINee 韓國 維基百科")

    page.keyboard.press('Enter')

    page.wait_for_selector("#hdtb-sc > div > div > div.crJ18e > div.Ap1Qsc > span > div", state="visible")

    if page.locator('span[jscontroller="msmzHf"] a').nth(0).is_visible():
        page.locator('span[jscontroller="msmzHf"] a').nth(0).click()
    else:
        print('找不到')

    page.wait_for_timeout(5000)