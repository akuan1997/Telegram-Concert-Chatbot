from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import os
import re
import json
import threading
from fuzzywuzzy import fuzz

json_file = 'b_concert.json'
waiting_links = 'b_all_links_waiting.txt'
finished_links = 'b_all_links_z.txt'
visited_file = 'b_visited_urls.txt'
error_file = 'b_error_record.txt'
image_problem_file = 'b_image_but_problem.txt'


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
    with open(visited_file, 'r', encoding='utf-8') as f:
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

                        print('載入圖片')
                        # page.wait_for_load_state('load')
                        # page.wait_for_timeout(1500)
                        # page.wait_for_selector("#content", state="visible")
                        # page.wait_for_selector("#footer", state="visible")
                        page.wait_for_selector(".mw-mmv-image-wrapper:nth-child(2)", state="visible")
                        page.wait_for_selector(".mw-mmv-license:nth-child(1)", state="visible")
                        print('載入成功')

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

                        write_data_json(json_file, new_data)

                        with open(visited_file, 'a', encoding='utf-8') as f:
                            f.write(singer_page_url + '\n')

                        # with open(finished_artists, 'a', encoding='utf-8') as f:
                        #     f.write(singer_name + '\n')

                    # 有方塊，也有圖片，但是卻點不進去
                    else:
                        print('! step 4')

                        with open(image_problem_file, 'a', encoding='utf-8') as f:
                            f.write(singer_page_url + '\n')
                # 有方塊，但是沒有圖片
                else:
                    jpg_url = '-'
                    singer_image_page_url = '-'
                    provider_name = '-'
                    image_name = '-'
                    cc = '-'

                    new_data = {
                        'singer_name': singer_name,
                        'singer_page_url': singer_page_url,
                        'singer_image_page_url': singer_image_page_url,
                        'jpg_url': jpg_url,
                        'provider_name': provider_name,
                        'image_name': image_name,
                        'cc': cc
                    }

                    print('! step 3')
                    print('singer_page_url = ', singer_page_url)
                    print('jpg_url = ', jpg_url)
                    print('singer_image_page_url = ', singer_image_page_url)
                    print('provider_name = ', provider_name)
                    print('image_name = ', image_name)
                    print('cc = ', cc)

                    write_data_json(json_file, new_data)

                    with open(visited_file, 'a', encoding='utf-8') as f:
                        f.write(singer_page_url + '\n')

                    # with open(finished_artists, 'a', encoding='utf-8') as f:
                    #     f.write(singer_name + '\n')

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
    page.set_default_timeout(10000)

    while True:
        try:
            while True:
                with open(waiting_links, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                if lines != []:
                    first_line = lines.pop(0).replace('\n', '')

                    singer_name = first_line.split('|||')[0]
                    print(singer_name)
                    singer_url = first_line.split('|||')[1]
                    print(singer_url)

                    page.goto(singer_url)
                    print('載入網址')
                    page.wait_for_selector("#content", state="visible")
                    print('載入成功')
                    # page.wait_for_selector("#footer", state="visible")

                    get_wiki_data(singer_url, singer_name)

                    with open(finished_links, 'a', encoding='utf-8') as f:
                        f.write(first_line + '\n')

                    with open(waiting_links, 'w', encoding='utf-8') as f:
                        f.writelines(lines)

                    print('---')
                else:
                    page.close()
                    break
            break
        except Exception as e:
            print(e)
            page.close()
            with open(error_file, 'r', encoding='utf-8') as f:
                error_record = f.readlines()
            error_record = [line.replace('\n', '') for line in error_record]
            if singer_url not in error_record:
                print('寫入第一次失敗')
                with open(error_file, 'a', encoding='utf-8') as f:
                    f.write(singer_url + '\n')
            else:
                print('再次失敗，跳過')
                with open(waiting_links, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
            ''''''
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.set_default_timeout(10000)
            continue
