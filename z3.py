from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(3000)
    not_exists = []
    exists = []
    problems = []
    numbers = [
        "5487",
        "5489",
        "5491",
        "5493",
        "5495",
        "5497",
        "5499",
        "5501",
        "5503",
        "5505",
        "5507",
        "5512",
        "5518",
        "5521",
        "5537",
        "5586",
        "5606",
        "5610",
        "5662",
        "5733",
        "5735",
        "5737",
        "5739",
        "5742"
    ]
    # for number in numbers:
    for i in range(5731, 5773):
        url = f"https://concertinfo.site/?p={i}"
        page.goto(url)
        try:
            page.wait_for_selector(".page-title")
            if '找不到' in page.title():
                not_exists.append(i)
            else:
                exists.append(i)
            print(f"not_exists = {not_exists}")
            print(f"exists = {exists}")
            print(f"problems = {problems}")
            print('---')
        except:
            problems.append(i)
            print(f"not_exists = {not_exists}")
            print(f"exists = {exists}")
            print(f"problems = {problems}")
            print('---')
            continue
