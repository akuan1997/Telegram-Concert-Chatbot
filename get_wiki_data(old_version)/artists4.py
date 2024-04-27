from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import os
import re
import json

from artists import country_singers_no_sub_category

# 正在等待爬蟲的category網頁
not_executed_categories = 'artists_categories_waiting1.txt'
# 要寫入哪一個檔案
write_json_file = 'artists4.json'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()

    with open(not_executed_categories, 'r', encoding='utf-8') as f:
        waiting_categories = f.readlines()

    for i, waiting_category in enumerate(waiting_categories):
        page.goto(waiting_category)
        page.wait_for_load_state('load')
        page.wait_for_timeout(1500)

        with open('artists_categories.txt', 'r', encoding='utf-8') as f:
            processed_categories = f.readlines()
        processed_categories = [processed_category.replace('\n', '') for processed_category in processed_categories]

        if page.url not in processed_categories:
            country_singers_no_sub_category(waiting_category, page, "artists_singers_bands.txt", write_json_file)
            with open('artists_categories.txt', 'a', encoding='utf-8') as f:
                f.write(waiting_category)
            with open(not_executed_categories, 'w', encoding='utf-8') as f:
                f.writelines(waiting_categories[i + 1:])
        else:
            print('這個頁面已經完成了!')