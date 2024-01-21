from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

