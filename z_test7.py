from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.livenation.com.tw/show/1476056/jp-saxe-a-grey-area-world-tour/taipei/2024-05-23/tw")

    # 下載內文
    inner_text = page.locator(
        "#top > main > div > div.layout__container > div.accordion__accordion > div > div > div").inner_text()

    print(inner_text)
    print('-------------------------------------')
    inner_text = ''
    inner_texts = page.query_selector_all("#top > main > div > div.layout__container > div.accordion__accordion > div > div > div > p")
    for i in range(len(inner_texts)):
        inner_text += inner_texts[i].inner_text()
        # print(inner_texts[i].inner_text())
        # print('---')
    print(inner_text)


