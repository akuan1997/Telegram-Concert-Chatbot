# https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E6%AD%8C%E6%89%8B%E5%88%97%E8%A1%A8
# 上半部的台灣團體
from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import os
import re
import json

folder_path = '../../artists_images'
finished_urls = 'artists2.txt'  # 要改
json_filename = 'artists2.json'  # 要改


def reset_files():
    with open(finished_urls, 'w', encoding='utf-8') as f:
        f.write('')
    with open(json_filename, 'w', encoding='utf-8') as f:
        f.write('')


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


def name_page_actions():
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
        names.append(nickname.inner_text())

    names = list(set(names))
    # print(names)

    return title_name, names


def image_page_actions(title_name):
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
    file_path = os.path.join(folder_path, image_name)
    with open(file_path, 'wb') as f:
        f.write(image_data)
        print('image okay')

    page.go_back()

    return image_name, cc


def click_actions():
    # 重複的就不要再執行了
    with open(finished_urls, 'r', encoding='utf-8') as f:
        processed_urls = f.readlines()
    processed_urls = [processed_url.replace('\n', '') for processed_url in processed_urls]
    # 頁面有沒有方塊或是作者
    if page.locator(".fn").nth(0).is_visible() or page.locator(".mw-mmv-author > a").nth(
            0).is_visible() or page.locator(
        ".mw-mmv-author").nth(0).is_visible():
        # 有方塊 而且還沒執行過
        if page.url not in processed_urls:
            # 有沒有方塊
            if page.locator(".fn").nth(0).is_visible():
                print('右側有方塊')
                title_name, names = name_page_actions()
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
                        print('找不到作者')
                        provider_name = '-'

                    # title_name 下載圖片的名稱
                    image_name, cc = image_page_actions(title_name)
                    image_page_url = page.url
                    names = [re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", name) for name in names]
                    names = [name.replace('[編輯]', '') for name in names]
                    names = [name.strip() for name in names]
                    names = list(set(names))
                    # 執行完畢，寫入執行完成的url檔案，因為有姓名也有圖片，所以這邊寫上兩個urls
                    with open(finished_urls, 'a', encoding='utf-8') as f:
                        f.write(name_url + '\n' + image_page_url + '\n')
                    # 寫入新資料到json
                    print('\n--- write new data ---\n')
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

                    write_data_json(json_filename, new_data)
                    print('\n--------------------------------------------\n')

                    page.go_back()
                    page.wait_for_load_state('load')
                    page.wait_for_timeout(1500)
                    page.go_back()

                # 這位歌手沒有圖片
                else:
                    print('這位歌手沒有圖片')
                    page.screenshot(path=os.path.join('../screenshot_no_images', f"{title_name}.png"))
                    names = [re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", name) for name in names]
                    names = [name.replace('[編輯]', '') for name in names]
                    names = [name.strip() for name in names]
                    names = list(set(names))
                    # 執行完畢，寫入執行完成的url檔案，因為只有姓名，沒有圖片，所以這邊只寫上一個url
                    with open(finished_urls, 'a', encoding='utf-8') as f:
                        f.write(name_url + '\n')
                    # 寫入新資料到json
                    print('\n--- write new data ---\n')
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


def click_actions_test():
    # 頁面有沒有方塊或是作者
    if page.locator(".fn").nth(0).is_visible() or page.locator(".mw-mmv-author > a").nth(0).is_visible() or page.locator(".mw-mmv-author").nth(0).is_visible():
        # 有方塊 而且還沒執行過
        # 有沒有方塊
        if page.locator(".fn").nth(0).is_visible():
            print('右側有方塊')
            title_name, names = name_page_actions()
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
                    print('找不到作者')
                    provider_name = '-'

                # title_name 下載圖片的名稱
                image_name, cc = image_page_actions(title_name)
                image_page_url = page.url
                names = [re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", name) for name in names]
                names = [name.replace('[編輯]', '') for name in names]
                names = [name.strip() for name in names]
                names = list(set(names))
                # 寫入新資料到json
                print('\n--- write new data ---\n')
                print('names', names)
                print('image name', image_name)
                print('ref', f"This image is provided by {provider_name}, {title_name} article, source: Wikipedia")
                print('article_url', name_url)
                print('image_url', image_page_url)
                print('cc', cc)

                print('\n--------------------------------------------\n')

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
                # 寫入新資料到json
                print('\n--- write new data ---\n')
                print('names', names)
                print('image name', '-')
                print('reference', f"{title_name} article, source: Wikipedia")
                print('article_url', name_url)
                print('image_url', '-')
                print('cc', '-')

                page.go_back()

        else:
            print('這個頁面已經完成了')
            page.go_back()
    else:
        print('右側沒有方塊，返回', page.url)
        print('\n--------------------------------------------\n')
        page.go_back()


with sync_playwright() as p:
    reset_files()

    browser = p.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E6%AD%8C%E6%89%8B%E5%88%97%E8%A1%A8")
    page.wait_for_load_state('load')
    page.wait_for_timeout(1500)

    rows = page.query_selector_all(".wikitable.sortable.jquery-tablesorter > tbody > tr")
    print(len(rows))

    page.wait_for_timeout(1500)
    for i in range(1, len(rows) + 1):
        s1 = f".wikitable.sortable.jquery-tablesorter > tbody > tr:nth-child({i}) > td:nth-child(1) > a"
        print(f'{i}/{len(rows)}')
        if page.locator(s1).is_visible():
            print('okay')
            page.locator(
                f".wikitable.sortable.jquery-tablesorter > tbody > tr:nth-child({i}) > td:nth-child(1) > a").click()
            click_actions()
            page.wait_for_load_state('load')
            page.wait_for_timeout(1500)
        else:
            print('!!!!!!!')
            print('\n--------------------------------------------\n')
