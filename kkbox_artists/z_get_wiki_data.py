from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import os
import re
import json
import threading

# chiense
json_file = 'artist_chinese.json'
waiting_artists = 'chinese_sorted_waiting.txt'
finished_artists = 'chinese_sorted_finished.txt'


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


def get_wiki_data(current_url, singer_name):
    # 先判斷這個網頁有沒有造訪過
    with open('z_visited_urls.txt', 'r', encoding='utf-8') as f:
        visited_urls = f.readlines()

    visited_urls = [visited_url.replace('\n', '') for visited_url in visited_urls]

    names = [visited_url.split('/')[-1] for visited_url in visited_urls]

    current_page_name = current_url.split('/')[-1]

    if current_page_name in names:
        print('已經處理過了')
        return '-'
    else:
        # 這個頁面是歌手頁面或是歌手圖片頁面
        if page.locator(".fn").nth(0).is_visible() or page.locator(".mw-mmv-author > a").nth(
                0).is_visible() or page.locator(
            ".mw-mmv-author").nth(0).is_visible():
            print('step 1')
            # 右側有方塊
            if page.locator(".fn").nth(0).is_visible():
                print('step 2')
                singer_page_url = page.url

                # 有圖片
                image_uploads = page.query_selector_all(
                    'meta[property="og:image"][content*="https://upload.wikimedia.org/wikipedia/"]')
                if len(image_uploads) > 0:
                    print('step 3')
                    jpg_url = image_uploads[0].get_attribute('content')
                    # 右側有方塊也有圖片
                    if page.locator(".mw-default-size .mw-file-description").nth(0).is_visible() or \
                            page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).is_visible():
                        # files = page.query_selector_all('a[href*="/wiki/File:"]')
                        # if len(files) > 0:
                        # if page.locator(".mw-file-description").nth(0).is_visible():
                        print('step 4')
                        # 點擊進入歌手圖片頁面
                        '''
                        使用.mw-file-description的話有可能會點擊到無效頁面
                        '''
                        if page.locator(".mw-default-size .mw-file-description").nth(0).is_visible():
                            page.locator(".mw-default-size .mw-file-description").nth(0).click()
                        elif page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).is_visible():
                            page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).click()
                        # page.locator('a[href*="/wiki/File:"]').nth(0).click()
                        # image_url = files[0].get_attribute('href')
                        # print(image_url)
                        page.wait_for_load_state('load')
                        page.wait_for_timeout(1500)
                        singer_image_page_url = page.url

                        # 歌手頁面找得到作者
                        if page.locator(".mw-mmv-author > a").nth(0).is_visible() or page.locator(".mw-mmv-author").nth(
                                0).is_visible():
                            if page.locator(".mw-mmv-author > a").nth(0).is_visible():
                                provider_name = page.locator(".mw-mmv-author > a").nth(0).inner_text()
                            elif page.locator(".mw-mmv-author").nth(0).is_visible():
                                provider_name = page.locator(".mw-mmv-author").inner_text()
                            else:
                                provider_name = '-'
                        # 歌手頁面找不到作者
                        else:
                            provider_name = '-'

                        # 歌手頁面找得到作品標題
                        if page.locator(".mw-mmv-title").nth(0).is_visible():
                            image_name = page.locator(".mw-mmv-title").nth(0).inner_text()
                        # 歌手頁面找不到作品標題
                        else:
                            image_name = '-'

                        # 歌手頁面找得到CC
                        if page.locator(".mw-mmv-license-li > a").nth(0).is_visible():
                            cc = page.locator(".mw-mmv-license-li > a").nth(0).inner_text()
                        # 歌手頁面找不到CC
                        else:
                            cc = 'check it later'

                        new_data = {
                            'singer_name': singer_name,
                            'singer_page_url': singer_page_url,
                            'singer_image_page_url': singer_image_page_url,
                            'jpg_url': jpg_url,
                            'provider_name': provider_name,
                            'image_name': image_name,
                            'cc': cc
                        }

                        print('singer_name = ', singer_name)
                        print('singer_page_url = ', singer_page_url)
                        print('singer_image_page_url = ', singer_image_page_url)
                        print('jpg_url = ', jpg_url)
                        print('provider_name = ', provider_name)
                        print('image_name = ', image_name)
                        print('cc = ', cc)
                        print('---')

                        write_data_json(json_file, new_data)

                        with open('z_visited_urls.txt', 'a', encoding='utf-8') as f:
                            f.write(singer_page_url + '\n')

                    # 有方塊，也有圖片，但是卻點不進去
                    else:
                        print('! step 4')

                        with open('z_image_but_problem.txt', 'a', encoding='utf-8') as f:
                            f.write(singer_page_url + '\n')

                        with open('z_visited_urls.txt', 'a', encoding='utf-8') as f:
                            f.write(singer_page_url + '\n')
                # 有方塊，但是沒有圖片
                else:
                    jpg_url = '-'
                    singer_image_page_url = '-'
                    provider_name = '-'
                    image_name = '-'
                    cc = '-'

                    print('! step 3')
                    print('singer_page_url = ', singer_page_url)
                    print('jpg_url = ', jpg_url)
                    print('singer_image_page_url = ', singer_image_page_url)
                    print('provider_name = ', provider_name)
                    print('image_name = ', image_name)
                    print('cc = ', cc)

                    with open('z_visited_urls.txt', 'a', encoding='utf-8') as f:
                        f.write(singer_page_url + '\n')
            # 這個頁面右側沒有方塊
            else:
                print('! step 2')
                return '-'
        # 這個頁面不是歌手頁面或是歌手圖片頁面
        else:
            print('! step 1')
            return '-'


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    start_url = "https://zh.wikipedia.org/zh-tw/%E8%94%A1%E4%BE%9D%E6%9E%97"
    # start_url = "https://zh.wikipedia.org/zh-tw/%E7%BE%85%E5%BF%97%E7%A5%A5" # 羅志祥
    # start_url = "https://zh.wikipedia.org/zh-tw/%E7%8E%8B%E5%8A%9B%E5%AE%8F"
    # start_url = "https://zh.wikipedia.org/zh-tw/%E6%9E%97%E6%84%B7%E5%80%AB"
    # start_url = "https://zh.wikipedia.org/zh-tw/%E5%91%A8%E6%9D%B0%E5%80%AB"

    page.goto(start_url)
    page.wait_for_load_state('load')
    page.wait_for_timeout(1500)

    while True:
        with open(waiting_artists, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if lines:
            full_name = lines.pop(0).replace('\n', '')
            if '(' in full_name:
                type_name = full_name.split('(')[0]
            else:
                type_name = full_name

            # 搜尋欄位可見
            page.wait_for_selector('.cdx-text-input__input:nth-child(1)')
            # if page.locator(".cdx-text-input__input").nth(0).is_visible():
            page.locator(".cdx-text-input__input").nth(0).fill(type_name)  # 填入關鍵字
            first_search_result = page.locator("#cdx-menu-item-1 > a > span:nth-child(2) > span > bdi > span").inner_text()
            # 如果第一個搜尋結果就是我要的
            if type_name in first_search_result:
                print("that's what I want")
                page.locator("#cdx-menu-item-1").click()  # 前往頁面
                page.wait_for_load_state('load')
                page.wait_for_timeout(1500)

                get_wiki_data(page.url, full_name)
            else:
                with open('z_wiki_cannot_find.txt', 'a', encoding='utf-8') as f:
                    f.write(full_name + '\n')

            with open(finished_artists, 'a', encoding='utf-8') as f:
                f.write(full_name)

            with open(waiting_artists, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            page.goto(start_url)
            page.wait_for_load_state('load')
            page.wait_for_timeout(1500)

        else:
            break


