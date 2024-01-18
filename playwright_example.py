from web_scraping.sync_api import sync_playwright, Playwright
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

