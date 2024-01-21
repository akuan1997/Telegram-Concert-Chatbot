from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import re
import os
import json

folder_path = 'artists_images'
processed_url = 'processed_url.txt'
json_filename = 'artists.json'

def name_page_actions():
    names = []
    # 標題
    # if page.locator(".mw-page-title-main").is_visible():
    #     print(page.locator(".mw-page-title-main").inner_text())
    #     names.append(page.locator(".mw-page-title-main").inner_text())
    # if page.locator("#firstHeading").nth(0).is_visible():
    title_name = page.locator("#firstHeading").nth(0).inner_text()
    title_name = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", title_name)
    title_name = title_name.replace('[編輯]', '')
    title_name = title_name.strip()
    names.append(title_name)

    # 方塊最上面的名字
    # print(page.locator(".fn").nth(0).inner_text())
    if '\n' in page.locator(".fn").nth(0).inner_text():
        split_names = page.locator(".fn").nth(0).inner_text().split('\n')
        for name in split_names:
            names.append(name)
    else:
        names.append(page.locator(".fn").nth(0).inner_text())
    # print(names)

    # 使用 CSS 選擇器定位元素
    element = page.query_selector('span[lang="en"]')
    # 獲得元素的文本
    if element:
        text = element.text_content()
        if '、' in text:
            split_names = element.text_content().split('、')
            for name in split_names:
                names.append(name)
        else:
            names.append(element.text_content())

    names = list(set(names))
    # print(names)

    return title_name, names


def image_page_actions(provider_name, title_name):
    # provider_name = ''
    # if page.locator(".mw-mmv-author > a").nth(0).is_visible():
    #     # print(page.locator(".mw-mmv-author > a").inner_text())
    #     provider_name = page.locator(".mw-mmv-author > a").nth(0).inner_text()
    # elif page.locator(".mw-mmv-author").nth(0).is_visible():
    #     # print(page.locator(".mw-mmv-author").inner_text())
    #     provider_name = page.locator(".mw-mmv-author").inner_text()
    #
    # print('provider okay')

    # 憑證
    if page.locator(".mw-mmv-license-li > a").nth(0).is_visible():
        cc = page.locator(".mw-mmv-license-li > a").nth(0).inner_text()
    else:
        cc = 'check it later'
    print('cc okay')

    # if page.locator(".mw-mmv-license-li.cc-license .mw-mmv-license").is_visible():
    #     cc = page.locator(".mw-mmv-license-li.cc-license .mw-mmv-license").inner_text()
    # elif page.locator(".mw-mmv-license-li.pd-license .mw-mmv-license").is_visible():
    #     cc = page.locator(".mw-mmv-license-li.pd-license .mw-mmv-license").inner_text()
    # else:
    #     cc = 'Public'

    # 選擇要下載的圖片元素（使用 CSS 選擇器）
    image_element = page.locator('.mw-mmv-image-wrapper > .mw-mmv-image-inner-wrapper > .mw-mmv-image > img').nth(0)

    # 取得圖片的URL
    image_url = image_element.get_attribute('src')
    # print(image_url)
    if 'https' not in image_url[:5]:
        image_url = 'https:' + image_url
        # print('加上去了')
    # else:
    # print('原本就有https')
    # print(f"image url\n{image_url}")
    # 下載圖片
    # 保存圖片到本地
    image_data = page.goto(image_url).body()
    image_name = f'{title_name.strip()}.png'
    file_path = os.path.join(folder_path, image_name)
    with open(file_path, 'wb') as f:
        f.write(image_data)
        print('image okay')

    page.go_back()

    return image_name, cc


def click_actions():
    with open('processed_url.txt', 'r', encoding='utf-8') as f:
        processed_urls = f.readlines()
    processed_urls = [processed_url.replace('\n', '') for processed_url in processed_urls]

    if page.locator(".fn").nth(0).is_visible() or page.locator(".mw-mmv-author > a").nth(0).is_visible() or page.locator(
            ".mw-mmv-author").nth(0).is_visible():
        if page.url not in processed_urls:
            if page.locator(".fn").nth(0).is_visible():
                print('has block')
                title_name, names = name_page_actions()
                name_url = page.url

                # 這位歌手有沒有圖片
                if page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).is_visible():
                    print('這位歌手有圖片')
                    page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).click()
                    print('進入歌手圖片頁面')
                    page.wait_for_load_state('load')
                    page.wait_for_timeout(1500)
                    # 找不找得到作者
                    if page.locator(".mw-mmv-author > a").nth(0).is_visible() or page.locator(".mw-mmv-author").nth(0).is_visible():
                        print('找得到作者')
                        if page.locator(".mw-mmv-author > a").nth(0).is_visible():
                            provider_name = page.locator(".mw-mmv-author > a").nth(0).inner_text()
                        elif page.locator(".mw-mmv-author").nth(0).is_visible():
                            provider_name = page.locator(".mw-mmv-author").inner_text()
                    else:
                        provider_name = '-'

                    image_name, cc = image_page_actions(provider_name, title_name)
                    image_page_url = page.url
                    names = [re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", name) for name in names]
                    names = [name.replace('[編輯]', '') for name in names]
                    names = [name.strip() for name in names]
                    names = list(set(names))
                    # print(f'names: {names}')
                    # print(f"provider name: {provider_name}")
                    # with open('processed_url.txt', 'a', encoding='utf-8') as f:
                    #     f.write(name_url + '\n')
                    # with open('processed_url.txt', 'a', encoding='utf-8') as f:
                    #     f.write(image_page_url + '\n')

                    print('\n--- write new data ---\n')

                    # write data
                    print('names', names)
                    print('image name', image_name)
                    print('ref', f"This image is provided by {provider_name}, {title_name} article, source: Wikipedia")
                    print('article_url', name_url)
                    print('image_url', image_page_url)
                    print('cc', cc)

                    new_data = {
                        'names': names,
                        'image_name': image_name,
                        'reference': f"This image is provided by {provider_name}, {title_name} article, source: Wikipedia",
                        'article_url': name_url,
                        'image_url': image_page_url,
                        'cc': cc
                    }

                    # json檔案不存在或是裡面沒資料
                    if not os.path.exists(json_filename) or os.path.getsize(
                            json_filename) <= 4:
                        # 直接寫入第一筆資料
                        with open(json_filename, "w", encoding="utf-8") as f:
                            json.dump([new_data], f, indent=4, ensure_ascii=False)
                    # json檔案存在且裡面已經有一筆以上的資料
                    else:
                        # 讀取現在有的檔案
                        with open(json_filename, "r", encoding="utf-8") as f:
                            existing_data = json.load(f)
                        # 並新增即將寫入的一筆
                        existing_data.append(new_data)
                        # 寫入
                        with open(json_filename, "w", encoding="utf-8") as f:
                            json.dump(existing_data, f, indent=4, ensure_ascii=False)

                    print('----------------------')
                    page.go_back()
                    page.wait_for_load_state('load')
                    page.wait_for_timeout(1500)
                    page.go_back()

                # 這位歌手沒有圖片
                else:
                    print('這位歌手沒有圖片')
                    names = [re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", name) for name in names]
                    names = [name.replace('[編輯]', '') for name in names]
                    names = [name.strip() for name in names]
                    names = list(set(names))
                    # print(f'names: {names}')
                    # with open('processed_url.txt', 'a', encoding='utf-8') as f:
                    #     f.write(name_url + '\n')

                    print('\n--- write new data ---\n')

                    # write data
                    print('names', names)
                    print('image name', '-')
                    print('reference', f"{title_name} article, source: Wikipedia")
                    print('article_url', name_url)
                    print('image_url', '-')
                    print('cc', '-')

                    new_data = {
                        'names': names,
                        'image_name': '-',
                        'reference': f"{title_name} article, source: Wikipedia",
                        'article_url': name_url,
                        'image_url': '-',
                        'cc': '-'
                    }

                    # json檔案不存在或是裡面沒資料
                    if not os.path.exists(json_filename) or os.path.getsize(
                            json_filename) <= 4:
                        # 直接寫入第一筆資料
                        with open(json_filename, "w", encoding="utf-8") as f:
                            json.dump([new_data], f, indent=4, ensure_ascii=False)
                    # json檔案存在且裡面已經有一筆以上的資料
                    else:
                        # 讀取現在有的檔案
                        with open(json_filename, "r", encoding="utf-8") as f:
                            existing_data = json.load(f)
                        # 並新增即將寫入的一筆
                        existing_data.append(new_data)
                        # 寫入
                        with open(json_filename, "w", encoding="utf-8") as f:
                            json.dump(existing_data, f, indent=4, ensure_ascii=False)

                    print('----------------------')
                    page.go_back()

        else:
            print('已經完成了')
            page.go_back()
    else:
        print('no block')
        print(page.url)
        page.go_back()


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://zh.wikipedia.org/wiki/%E9%B3%B3%E9%A3%9B%E9%A3%9B")

    click_actions()