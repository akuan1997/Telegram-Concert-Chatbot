from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import json

with open('artists1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
urls = []
for i in range(len(data)):
    if data[i]['image_name'] == '-':
#         print(data[i]['names'])
#         print(data[i]['article_url'])
        urls.append(data[i]['article_url'])

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    print(len(urls))
    for i in range(151, len(urls)):
        print(f'i = {i}')
        page.goto(urls[i])
        page.wait_for_timeout(2000)




