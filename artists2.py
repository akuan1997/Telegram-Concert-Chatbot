from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import os
import re
import json

from artists import click_actions

# 台灣歌手列表
# https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E6%AD%8C%E6%89%8B%E5%88%97%E8%A1%A8
# 樂團

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E6%AD%8C%E6%89%8B%E5%88%97%E8%A1%A8")

    page.wait_for_load_state('load')
    page.wait_for_timeout(1500)

    rows = page.query_selector_all(".wikitable.sortable.jquery-tablesorter > tbody > tr")
    print(len(rows))

    page.wait_for_timeout(1500)
    for i in range(1, len(rows) + 1):
        s1 = f".wikitable.sortable.jquery-tablesorter > tbody > tr:nth-child({i}) > td:nth-child(1) > a"
        print(f'{i}/{len(rows)}')
        if page.locator(s1).is_visible():
            print('okay')
            page.locator(
                f".wikitable.sortable.jquery-tablesorter > tbody > tr:nth-child({i}) > td:nth-child(1) > a").click()
            click_actions(page, "artists_singers_bands.txt", "artists2.json")
            page.wait_for_load_state('load')
            page.wait_for_timeout(1500)
        else:
            print('!!!!!!!')
            print('\n--------------------------------------------\n')
