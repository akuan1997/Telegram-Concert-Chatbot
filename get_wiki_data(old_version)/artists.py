from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import os
import re
import json
import threading


def write_data_json(json_name, new_data):
    # json檔案不存在或是裡面沒資料
    if not os.path.exists(json_name) or os.path.getsize(json_name) <= 4:
        # 直接寫入第一筆資料
        with open(json_name, "w", encoding="utf-8") as f:
            json.dump([new_data], f, indent=4, ensure_ascii=False)
    # json檔案存在且裡面已經有一筆以上的資料
    else:
        # 讀取現在有的檔案
        with open(json_name, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
        # 並新增即將寫入的一筆
        existing_data.append(new_data)
        # 寫入
        with open(json_name, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)


def name_page_actions(page):
    names = []
    # 標題名字
    title_name = page.locator("#firstHeading").nth(0).inner_text()
    title_name = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", title_name)
    title_name = title_name.replace('[編輯]', '')
    title_name = title_name.strip()
    names.append(title_name)
    # 右側方塊最上面的名字
    if '\n' in page.locator(".fn").nth(0).inner_text():
        split_names = page.locator(".fn").nth(0).inner_text().split('\n')
        for name in split_names:
            names.append(name)
    else:
        names.append(page.locator(".fn").nth(0).inner_text())
    # lang="en"的英文名字
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
    # 所有的nicknames
    nicknames = page.query_selector_all(".nickname")
    for nickname in nicknames:
        if '、' in nickname.inner_text():
            split_nickname = nickname.inner_text().split('、')
            for name in split_nickname:
                names.append(name)
        elif '\n' in nickname.inner_text():
            split_nickname = nickname.inner_text().split('\n')
            for name in split_nickname:
                names.append(name)
        else:
            names.append(nickname.inner_text())

    names = [name.replace('[1]', '') for name in names]
    names = [name.replace('[2]', '') for name in names]
    names = [name.replace('[3]', '') for name in names]
    names = [name.replace('[4]', '') for name in names]
    names = [name.replace('[5]', '') for name in names]
    names = [name.replace('[6]', '') for name in names]
    names = [name.replace('[7]', '') for name in names]
    names = [name.replace('[8]', '') for name in names]
    names = [name.replace('[9]', '') for name in names]

    names = list(set(names))
    # print(names)

    return title_name, names


def image_page_actions(page, title_name):
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
    # 如果開頭不是https，加上去
    if 'https' not in image_url[:5]:
        image_url = 'https:' + image_url
    # 下載圖片到本地
    # image_name = '123.png'
    # file_path = os.path.join(folder_path, image_name)
    # page.screenshot(path=file_path)
    image_data = page.goto(image_url).body()
    image_name = f'{title_name.strip()}.png'
    file_path = os.path.join('../artists_images', image_name)
    with open(file_path, 'wb') as f:
        f.write(image_data)
        print('image okay')

    page.go_back()

    return image_name, cc


def click_actions(page, finished_urls, json_filename):
    # 重複的就不要再執行了
    with open(finished_urls, 'r', encoding='utf-8') as f:
        processed_urls = f.readlines()

    processed_urls = [processed_url.replace('\n', '') for processed_url in processed_urls]

    name_codes = [processed_url.split('/')[-1] for processed_url in processed_urls]

    # 頁面有沒有方塊或是作者
    if page.locator(".fn").nth(0).is_visible() or page.locator(".mw-mmv-author > a").nth(
            0).is_visible() or page.locator(
        ".mw-mmv-author").nth(0).is_visible():
        # 有方塊 而且還沒執行過
        if page.url.split('/')[-1] not in name_codes:
            # 有沒有方塊
            if page.locator(".fn").nth(0).is_visible():
                print('右側有方塊')
                title_name, names = name_page_actions(page)
                name_url = page.url
                # 這位歌手有沒有圖片
                if page.locator(".mw-default-size .mw-file-description").nth(0).is_visible() or \
                        page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).is_visible():
                    print('這位歌手有圖片')
                    if page.locator(".mw-default-size .mw-file-description").nth(0).is_visible():
                        page.locator(".mw-default-size .mw-file-description").nth(0).click()
                    elif page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).is_visible():
                        page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).click()

                    print('進入歌手圖片頁面')
                    page.wait_for_load_state('load')
                    page.wait_for_timeout(1500)
                    # 找不找得到作者
                    if page.locator(".mw-mmv-author > a").nth(0).is_visible() or page.locator(".mw-mmv-author").nth(
                            0).is_visible():
                        # 找得到作者
                        print('找得到作者')
                        if page.locator(".mw-mmv-author > a").nth(0).is_visible():
                            provider_name = page.locator(".mw-mmv-author > a").nth(0).inner_text()
                        elif page.locator(".mw-mmv-author").nth(0).is_visible():
                            provider_name = page.locator(".mw-mmv-author").inner_text()
                        else:
                            provider_name = '-'
                    else:
                        print('找不到作者')
                        provider_name = '-'

                    # title_name 下載圖片的名稱
                    image_name, cc = image_page_actions(page, title_name)
                    image_page_url = page.url
                    names = [re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", name) for name in names]
                    names = [name.replace('[編輯]', '') for name in names]
                    names = [name.strip() for name in names]
                    names = list(set(names))
                    # 執行完畢，寫入執行完成的url檔案，因為有姓名也有圖片，所以這邊寫上兩個urls
                    with open(finished_urls, 'a', encoding='utf-8') as f:
                        # f.write(name_url + '\n' + image_page_url + '\n')
                        f.write(name_url + '\n')
                    # 寫入新資料到json
                    print('\n--- write new data ---\n')
                    print('title_name', title_name)
                    print('names', names)
                    print('image name', image_name)
                    print('ref', f"This image is provided by {provider_name}, {title_name} article, source: Wikipedia")
                    print('article_url', name_url)
                    print('image_url', image_page_url)
                    print('cc', cc)

                    new_data = {
                        'title_name': title_name,
                        'names': names,
                        'image_name': image_name,
                        'reference': f"This image is provided by {provider_name}, {title_name} article, source: Wikipedia",
                        'article_url': name_url,
                        'image_url': image_page_url,
                        'cc': cc
                    }

                    write_data_json(json_filename, new_data)
                    print('\n--------------------------------------------\n')

                    page.go_back()
                    page.wait_for_load_state('load')
                    page.wait_for_timeout(1500)
                    page.go_back()

                # 這位歌手沒有圖片
                else:
                    print('這位歌手沒有圖片')
                    try:
                        page.screenshot(path=os.path.join('../screenshot_no_images', f"{title_name}.png"))
                    except Exception as e:
                        pass
                    names = [re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", name) for name in names]
                    names = [name.replace('[編輯]', '') for name in names]
                    names = [name.strip() for name in names]
                    names = list(set(names))
                    # 執行完畢，寫入執行完成的url檔案，因為只有姓名，沒有圖片，所以這邊只寫上一個url
                    with open(finished_urls, 'a', encoding='utf-8') as f:
                        f.write(name_url + '\n')
                    # 寫入新資料到json
                    print('\n--- write new data ---\n')
                    print('title_name', title_name)
                    print('names', names)
                    print('image name', '-')
                    print('reference', f"{title_name} article, source: Wikipedia")
                    print('article_url', name_url)
                    print('image_url', '-')
                    print('cc', '-')

                    new_data = {
                        'title_name': title_name,
                        'names': names,
                        'image_name': '-',
                        'reference': f"{title_name} article, source: Wikipedia",
                        'article_url': name_url,
                        'image_url': '-',
                        'cc': '-'
                    }

                    write_data_json(json_filename, new_data)
                    print('\n--------------------------------------------\n')

                    page.go_back()

        else:
            print('這個頁面已經完成了')
            page.go_back()
    else:
        print('右側沒有方塊，返回', page.url)
        print('\n--------------------------------------------\n')
        page.go_back()


def click_actions_for_browsing(page, finished_urls, json_filename):
    # 重複的就不要再執行了
    with open(finished_urls, 'r', encoding='utf-8') as f:
        processed_urls = f.readlines()
    processed_urls = [processed_url.replace('\n', '') for processed_url in processed_urls]

    name_codes = [processed_url.split('/')[-1] for processed_url in processed_urls]

    # 頁面有沒有方塊或是作者
    if page.locator(".fn").nth(0).is_visible() or page.locator(".mw-mmv-author > a").nth(
            0).is_visible() or page.locator(
        ".mw-mmv-author").nth(0).is_visible():
        # 有方塊 而且還沒執行過
        if page.url.split('/')[-1] not in name_codes:
            # 有沒有方塊
            if page.locator(".fn").nth(0).is_visible():
                print('右側有方塊')
                title_name, names = name_page_actions(page)
                name_url = page.url
                # 這位歌手有沒有圖片
                if page.locator(".mw-default-size .mw-file-description").nth(0).is_visible() or \
                        page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).is_visible():
                    print('這位歌手有圖片')
                    if page.locator(".mw-default-size .mw-file-description").nth(0).is_visible():
                        page.locator(".mw-default-size .mw-file-description").nth(0).click()
                    elif page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).is_visible():
                        page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).click()

                    print('進入歌手圖片頁面')
                    page.wait_for_load_state('load')
                    page.wait_for_timeout(1500)
                    # 找不找得到作者
                    if page.locator(".mw-mmv-author > a").nth(0).is_visible() or page.locator(".mw-mmv-author").nth(
                            0).is_visible():
                        # 找得到作者
                        print('找得到作者')
                        if page.locator(".mw-mmv-author > a").nth(0).is_visible():
                            provider_name = page.locator(".mw-mmv-author > a").nth(0).inner_text()
                        elif page.locator(".mw-mmv-author").nth(0).is_visible():
                            provider_name = page.locator(".mw-mmv-author").inner_text()
                        else:
                            provider_name = '-'
                    else:
                        print('找不到作者')
                        provider_name = '-'

                    # title_name 下載圖片的名稱
                    image_name, cc = image_page_actions(page, title_name)
                    image_page_url = page.url
                    names = [re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", name) for name in names]
                    names = [name.replace('[編輯]', '') for name in names]
                    names = [name.strip() for name in names]
                    names = list(set(names))
                    # 執行完畢，寫入執行完成的url檔案，因為有姓名也有圖片，所以這邊寫上兩個urls
                    with open(finished_urls, 'a', encoding='utf-8') as f:
                        # f.write(name_url + '\n' + image_page_url + '\n')
                        f.write(name_url + '\n')
                    # 寫入新資料到json
                    print('\n--- write new data ---\n')
                    print('title_name', title_name)
                    print('names', names)
                    print('image name', image_name)
                    print('ref', f"This image is provided by {provider_name}, {title_name} article, source: Wikipedia")
                    print('article_url', name_url)
                    print('image_url', image_page_url)
                    print('cc', cc)

                    new_data = {
                        'title_name': title_name,
                        'names': names,
                        'image_name': image_name,
                        'reference': f"This image is provided by {provider_name}, {title_name} article, source: Wikipedia",
                        'article_url': name_url,
                        'image_url': image_page_url,
                        'cc': cc
                    }

                    write_data_json(json_filename, new_data)
                    print('\n--------------------------------------------\n')

                    page.go_back()
                    page.wait_for_load_state('load')
                    page.wait_for_timeout(1500)
                    page.go_back()

                # 這位歌手沒有圖片
                else:
                    print('這位歌手沒有圖片')
                    print('123')
                    page.screenshot(path=os.path.join('../screenshot_no_images', f"{title_name}.png"))
                    print('456')
                    names = [re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", name) for name in names]
                    names = [name.replace('[編輯]', '') for name in names]
                    names = [name.strip() for name in names]
                    names = list(set(names))
                    # 執行完畢，寫入執行完成的url檔案，因為只有姓名，沒有圖片，所以這邊只寫上一個url
                    with open(finished_urls, 'a', encoding='utf-8') as f:
                        f.write(name_url + '\n')
                    # 寫入新資料到json
                    print('\n--- write new data ---\n')
                    print('title_name', title_name)
                    print('names', names)
                    print('image name', '-')
                    print('reference', f"{title_name} article, source: Wikipedia")
                    print('article_url', name_url)
                    print('image_url', '-')
                    print('cc', '-')

                    new_data = {
                        'title_name': title_name,
                        'names': names,
                        'image_name': '-',
                        'reference': f"{title_name} article, source: Wikipedia",
                        'article_url': name_url,
                        'image_url': '-',
                        'cc': '-'
                    }

                    write_data_json(json_filename, new_data)
                    print('\n--------------------------------------------\n')

                    page.go_back()

        else:
            print('這個頁面已經完成了')
            page.go_back()


def country_singers_no_sub_category(start_page, page, finished_urls, json_filename):
    alphabets = page.query_selector_all("#mw-pages .mw-category-group")
    print(f'總共有{len(alphabets)}個groups')
    error_index = ''
    for i in range(1, len(alphabets) + 1):
        try:
            s1 = f'#mw-pages .mw-category-group:nth-child({i}) > ul > li'
            group_singers = page.query_selector_all(s1)
            print(f"第{i}個group有{len(group_singers)}位歌手")
            for j in range(1, len(group_singers) + 1):
                print(f'{i}-{j}')
                error_index = f'{i}-{j}'
                s2 = f'#mw-pages .mw-category-group:nth-child({i}) > ul > li:nth-child({j}) > a'
                if page.locator(s2).is_visible():
                    page.locator(s2).click()
                    page.wait_for_load_state('load')
                    page.wait_for_timeout(1500)
                    click_actions(page, finished_urls, json_filename)
                else:
                    print('no')
                print('---')
        except Exception as e:
            with open('artists_fail.txt', 'a', encoding='utf-8') as f:
                f.write(f'{start_page}{error_index}\n')
            page.goto(start_page)
# # 台灣歌手列表
# # https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E6%AD%8C%E6%89%8B%E5%88%97%E8%A1%A8
# def artists1():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, slow_mo=1000)
#         context = browser.new_context()
#         page = context.new_page()
#
#         page.goto("https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E6%AD%8C%E6%89%8B%E5%88%97%E8%A1%A8")
#
#         page.wait_for_load_state('load')
#         page.wait_for_timeout(1500)
#
#         for i in range(9, 67, 2):
#             print(f'i = {i}')
#             s1 = f"#mw-content-text > div.mw-content-ltr.mw-parser-output > table:nth-child({i}) > tbody > tr"
#             singers = page.query_selector_all(s1)
#             print(f'有{len(singers)}個歌手')
#             for j in range(2, len(singers) + 1):
#                 print(f'{i} - {j}')
#                 s2 = f'#mw-content-text > div.mw-content-ltr.mw-parser-output > table:nth-child({i}) > tbody > tr:nth-child({j}) > td:nth-child(1) > a'
#                 if page.locator(s2).is_visible():
#                     print(page.locator(s2).inner_text())
#                     page.locator(s2).click()
#                     click_actions(page, "artists_singers_bands.txt", "artists1.json")
#                     # page.wait_for_load_state('load')
#                     # page.wait_for_timeout(1500)
#                     # page.keyboard.press('End')
#                 else:
#                     print('!!!!!!!')
#             print('---')
#
#
# def artists2():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, slow_mo=1000)
#         context = browser.new_context()
#         page = context.new_page()
#         page.goto("https://zh.wikipedia.org/zh-tw/%E7%BE%85%E5%BF%97%E7%A5%A5")
#         _, names = name_page_actions(page)
#         print(names)
#         page.wait_for_timeout(10000)
#
#
# # ------------------------------------------------------------------------------
# # artists_categories 完成自己填寫
# # finished_urls 歌手以及樂團的頁面 完成後寫進去
# finished_urls = ''
# # json_filename 要寫進去的json檔案
# # with sync_playwright() as p:
# #     browser = p.chromium.launch(headless=False, slow_mo=1000)
# #     context = browser.new_context()
# #     page = context.new_page()
#
# thread_artists1 = threading.Thread(target=artists1)
# # thread_artists2 = threading.Thread(target=artists2)
#
# thread_artists1.start()
# # thread_artists2.start()
