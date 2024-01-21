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
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://zh.wikipedia.org/zh-tw/5566")

    if page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).is_visible():
        page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).click()
        print('yes')
        page.wait_for_timeout(1500)
    else:
        print('no')
    # image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/1976bandatMegaport2016.jpg/280px-1976bandatMegaport2016.jpg'
    # image_data = page.goto(image_url).body()
    #
    # title_name = '1976 (樂團)'
    # print(title_name)
    #
    # # # image_name = f'/artists_images/{title_name}.png'
    # image_name = f'{title_name}.png'
    # file_path = os.path.join(folder_path, image_name)
    # with open(file_path, 'wb') as f:
    #     f.write(image_data)
    #     print('Save!')
    # # # image_name = f'download.png'
    # # with open(image_name, 'wb') as f:
    # #     f.write(image_data)
    # #     print('Save!')