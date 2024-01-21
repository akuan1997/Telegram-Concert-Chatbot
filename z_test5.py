from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import os
# folder_path = 'artists_images'
# if not os.path.exists(folder_path):
#     os.makedirs(folder_path)
# else:
#     print('already exists')
#     print(folder_path)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://zh.wikipedia.org/wiki/%E7%99%BD%E5%85%89_(%E5%BD%B1%E6%98%9F)#/media/File:Baiguang_1949.jpg")
    page.wait_for_load_state('load')
    page.wait_for_timeout(1500)

    # 憑證
    if page.locator(".mw-mmv-license-li.cc-license .mw-mmv-license").is_visible():
        cc = page.locator(".mw-mmv-license-li.cc-license .mw-mmv-license").inner_text()
    elif page.locator(".mw-mmv-license-li.pd-license .mw-mmv-license").is_visible():
        cc = page.locator(".mw-mmv-license-li.pd-license .mw-mmv-license").inner_text()
    else:
        cc = 'Public'
    print(cc)