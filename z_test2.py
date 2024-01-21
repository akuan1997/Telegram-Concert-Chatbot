from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import os
folder_path = 'screenshot_no_images'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://zh.wikipedia.org/wiki/%E7%BE%85%E5%BF%97%E7%A5%A5")

    image_name = '123.png'
    file_path = os.path.join(folder_path, image_name)
    page.screenshot(path=file_path)