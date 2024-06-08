from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import os


def os_show_file_title(folder_path):
    json_filenames = []
    # 使用os模块列出文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            # print(filename.replace('.mhtml', ''))
            json_filenames.append(filename)
    return json_filenames

def download_image():
    folder_path = '0_useless/screenshot_no_images'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://zh.wikipedia.org/wiki/%E7%BE%85%E5%BF%97%E7%A5%A5")

        image_name = '123.png'
        file_path = os.path.join(folder_path, image_name)
        page.screenshot(path=file_path)

print(os_show_file_title("concert_jsons"))