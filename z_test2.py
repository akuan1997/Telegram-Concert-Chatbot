from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import os
import re
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


def image_page_actions(title_name):
    provider_name = ''
    if page.locator(".mw-mmv-author > a").nth(0).is_visible():
        # print(page.locator(".mw-mmv-author > a").inner_text())
        provider_name = page.locator(".mw-mmv-author > a").nth(0).inner_text()
    elif page.locator(".mw-mmv-author").nth(0).is_visible():
        # print(page.locator(".mw-mmv-author").inner_text())
        provider_name = page.locator(".mw-mmv-author").inner_text()

    print('provider okay')
    # 憑證
    if page.locator(".mw-mmv-license-li > a").is_visible():
        cc = page.locator(".mw-mmv-license-li > a").inner_text()
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
    image_name = f'{title_name}.png'
    file_path = os.path.join(folder_path, image_name)
    with open(file_path, 'wb') as f:
        f.write(image_data)
        print('image okay')

    page.go_back()

    return provider_name, cc


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
                # print('名字 成功')
                if page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).is_visible():
                    page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).click()
                    page.wait_for_load_state('load')
                    page.wait_for_timeout(1500)
                    if page.locator(".mw-mmv-author > a").nth(0).is_visible() or page.locator(".mw-mmv-author").nth(0).is_visible():
                        provider_name, cc = image_page_actions(title_name)
                        image_page_url = page.url
                        names = [re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", name) for name in names]
                        names = [name.replace('[編輯]', '') for name in names]
                        names = [name.strip() for name in names]
                        names = list(set(names))
                        # print(f'names: {names}')
                        # print(f"provider name: {provider_name}")
                        with open('processed_url.txt', 'a', encoding='utf-8') as f:
                            f.write(name_url + '\n')
                        with open('processed_url.txt', 'a', encoding='utf-8') as f:
                            f.write(image_page_url + '\n')

                        print('\n--- write new data ---\n')

                        # write data
                        print('names', names)
                        print('ref', f"This image is provided by {provider_name}, {title_name} article, source: Wikipedia")
                        print('article_url', name_url)
                        print('image_url', image_page_url)
                        print('cc', cc)

                        new_data = {
                            'names': names,
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

                    else:
                        provider_name = '-'
                        print('provider None')

                        if page.locator(".mw-mmv-license-li > a").is_visible():
                            cc = page.locator(".mw-mmv-license-li > a").inner_text()
                        else:
                            cc = 'check it later'
                        print('cc okay')

                        image_page_url = page.url

                        with open('processed_url.txt', 'a', encoding='utf-8') as f:
                            f.write(name_url + '\n')
                        with open('processed_url.txt', 'a', encoding='utf-8') as f:
                            f.write(image_page_url + '\n')

                        print('\n--- write new data ---\n')

                        # write data
                        print('names', names)
                        print('ref', f"This image is provided by {provider_name}, {title_name} article, source: Wikipedia")
                        print('article_url', name_url)
                        print('image_url', image_page_url)
                        print('cc', cc)

                        new_data = {
                            'names': names,
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

                else:
                    names = [re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", name) for name in names]
                    names = [name.replace('[編輯]', '') for name in names]
                    names = [name.strip() for name in names]
                    names = list(set(names))
                    # print(f'names: {names}')
                    with open('processed_url.txt', 'a', encoding='utf-8') as f:
                        f.write(name_url + '\n')

                    print('\n--- write new data ---\n')

                    # write data
                    print('names', names)
                    print('reference', f"{title_name} article, source: Wikipedia")
                    print('article_url', name_url)
                    print('image_url', '-')
                    print('cc', '-')

                    new_data = {
                        'names': names,
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

    # 李玖哲
    # page.goto("https://zh.wikipedia.org/zh-tw/%E6%9D%8E%E7%8E%96%E5%93%B2")
    # IVE
    # page.goto("https://zh.wikipedia.org/zh-tw/IVE_(%E7%B5%84%E5%90%88)")
    # 羅志祥
    # page.goto("https://zh.wikipedia.org/zh-tw/%E7%BE%85%E5%BF%97%E7%A5%A5")
    # jay park
    # page.goto("https://zh.wikipedia.org/zh-tw/%E6%9C%B4%E8%BC%89%E7%AF%84")
    # 黃鴻升
    # page.goto("https://zh.wikipedia.org/zh-tw/%E9%BB%83%E9%B4%BB%E5%8D%87")
    # Post Malone
    # page.goto("https://zh.wikipedia.org/zh-tw/%E6%B3%A2%E5%85%B9%C2%B7%E9%A9%AC%E9%BE%99")
    # 5566
    # page.goto("https://zh.wikipedia.org/zh-tw/5566")
    # 安溥
    # page.goto("https://zh.wikipedia.org/zh-tw/%E5%AE%89%E6%BA%A5")

    # start_url = "https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E6%AD%8C%E6%89%8B%E5%88%97%E8%A1%A8"

    page.goto("https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E6%AD%8C%E6%89%8B%E5%88%97%E8%A1%A8")

    # --------------------------------------

    page.wait_for_load_state('load')
    print('載入完成')
    print('----------------------')

    with open('processed_url.txt', 'w', encoding='utf-8') as f:
        f.write('')

    # while True:
    #     click_actions()

    # for i in range(9, 67, 2):
    for i in range(23, 67, 2):
        print(f'i = {i}')
        s1 = f"#mw-content-text > div.mw-content-ltr.mw-parser-output > table:nth-child({i}) > tbody > tr"
        singers = page.query_selector_all(s1)
        print(f'有{len(singers)}個歌手')
        for j in range(2, len(singers) + 1):
        # for j in range(4, len(singers) + 1):
            print(f'{i} - {j}')
            s2 = f'#mw-content-text > div.mw-content-ltr.mw-parser-output > table:nth-child({i}) > tbody > tr:nth-child({j}) > td:nth-child(1) > a'
            if page.locator(s2).is_visible():
                print(page.locator(s2).inner_text())
                page.locator(s2).click()
                click_actions()
                # page.wait_for_load_state('load')
                # page.wait_for_timeout(1500)
                # page.keyboard.press('End')
            else:
                print('!!!!!!!')
        print('---')