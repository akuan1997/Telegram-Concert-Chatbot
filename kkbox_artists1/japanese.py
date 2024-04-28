from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import os
import re
import json
import threading
from fuzzywuzzy import fuzz

# japanese
language = '日本'
json_file = 'japanese.json'
waiting_artists = 'japanese_waiting.txt'
finished_artists = 'japanese_z.txt'
problem_file1 = 'japanese_problem1.txt'  # 名稱對不起來
problem_file2 = 'japanese_problem2.txt'  # 不是wikipedia
link_file = 'japanese_link.txt'

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


#
# def get_wiki_data(current_url, singer_name, full_name):
#     # 先判斷這個網頁有沒有造訪過
#     with open('z_visited_urls.txt', 'r', encoding='utf-8') as f:
#         visited_urls = f.readlines()
#
#     visited_urls = [visited_url.replace('\n', '') for visited_url in visited_urls]
#
#     names = [visited_url.split('/')[-1] for visited_url in visited_urls]
#
#     current_page_name = current_url.split('/')[-1]
#
#     if current_page_name in names:
#         print('已經處理過了')
#         return '-'
#     else:
#         # 這個頁面是歌手頁面或是歌手圖片頁面
#         if page.locator(".fn").nth(0).is_visible() or page.locator(".mw-mmv-author > a").nth(
#                 0).is_visible() or page.locator(
#             ".mw-mmv-author").nth(0).is_visible():
#             print('step 1')
#             # 右側有方塊
#             if page.locator(".fn").nth(0).is_visible():
#                 print('step 2')
#                 singer_page_url = page.url
#
#                 # 有圖片
#                 image_uploads = page.query_selector_all(
#                     'meta[property="og:image"][content*="https://upload.wikimedia.org/wikipedia/"]')
#                 if len(image_uploads) > 0:
#                     print('step 3')
#                     jpg_url = image_uploads[0].get_attribute('content')
#                     # 右側有方塊也有圖片
#                     if page.locator(".mw-default-size .mw-file-description").nth(0).is_visible() or \
#                             page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).is_visible():
#                         # files = page.query_selector_all('a[href*="/wiki/File:"]')
#                         # if len(files) > 0:
#                         # if page.locator(".mw-file-description").nth(0).is_visible():
#                         print('step 4')
#                         # 點擊進入歌手圖片頁面
#                         '''
#                         使用.mw-file-description的話有可能會點擊到無效頁面
#                         '''
#                         if page.locator(".mw-default-size .mw-file-description").nth(0).is_visible():
#                             page.locator(".mw-default-size .mw-file-description").nth(0).click()
#                         elif page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).is_visible():
#                             page.locator(".infobox.vcard.plainlist .mw-file-description").nth(0).click()
#                         # page.locator('a[href*="/wiki/File:"]').nth(0).click()
#                         # image_url = files[0].get_attribute('href')
#                         # print(image_url)
#                         page.wait_for_load_state('load')
#                         page.wait_for_timeout(1500)
#                         singer_image_page_url = page.url
#
#                         # 歌手頁面找得到作者
#                         if page.locator(".mw-mmv-author > a").nth(0).is_visible() or page.locator(".mw-mmv-author").nth(
#                                 0).is_visible():
#                             if page.locator(".mw-mmv-author > a").nth(0).is_visible():
#                                 provider_name = page.locator(".mw-mmv-author > a").nth(0).inner_text()
#                             elif page.locator(".mw-mmv-author").nth(0).is_visible():
#                                 provider_name = page.locator(".mw-mmv-author").inner_text()
#                             else:
#                                 provider_name = '-'
#                         # 歌手頁面找不到作者
#                         else:
#                             provider_name = '-'
#
#                         # 歌手頁面找得到作品標題
#                         if page.locator(".mw-mmv-title").nth(0).is_visible():
#                             image_name = page.locator(".mw-mmv-title").nth(0).inner_text()
#                         # 歌手頁面找不到作品標題
#                         else:
#                             image_name = '-'
#
#                         # 歌手頁面找得到CC
#                         if page.locator(".mw-mmv-license-li > a").nth(0).is_visible():
#                             cc = page.locator(".mw-mmv-license-li > a").nth(0).inner_text()
#                         # 歌手頁面找不到CC
#                         else:
#                             cc = 'check it later'
#
#                         new_data = {
#                             'singer_name': singer_name,
#                             'singer_page_url': singer_page_url,
#                             'singer_image_page_url': singer_image_page_url,
#                             'jpg_url': jpg_url,
#                             'provider_name': provider_name,
#                             'image_name': image_name,
#                             'cc': cc
#                         }
#
#                         print('singer_name = ', singer_name)
#                         print('singer_page_url = ', singer_page_url)
#                         print('singer_image_page_url = ', singer_image_page_url)
#                         print('jpg_url = ', jpg_url)
#                         print('provider_name = ', provider_name)
#                         print('image_name = ', image_name)
#                         print('cc = ', cc)
#                         print('---')
#
#                         write_data_json(json_file, new_data)
#
#                         with open('z_visited_urls.txt', 'a', encoding='utf-8') as f:
#                             f.write(singer_page_url + '\n')
#
#                         with open(finished_artists, 'a', encoding='utf-8') as f:
#                             f.write(full_name + '\n')
#
#                     # 有方塊，也有圖片，但是卻點不進去
#                     else:
#                         print('! step 4')
#
#                         with open('z_image_but_problem.txt', 'a', encoding='utf-8') as f:
#                             f.write(singer_page_url + '\n')
#                 # 有方塊，但是沒有圖片
#                 else:
#                     jpg_url = '-'
#                     singer_image_page_url = '-'
#                     provider_name = '-'
#                     image_name = '-'
#                     cc = '-'
#
#                     print('! step 3')
#                     print('singer_page_url = ', singer_page_url)
#                     print('jpg_url = ', jpg_url)
#                     print('singer_image_page_url = ', singer_image_page_url)
#                     print('provider_name = ', provider_name)
#                     print('image_name = ', image_name)
#                     print('cc = ', cc)
#
#                     with open('z_visited_urls.txt', 'a', encoding='utf-8') as f:
#                         f.write(singer_page_url + '\n')
#
#                     with open(finished_artists, 'a', encoding='utf-8') as f:
#                         f.write(full_name + '\n')
#
#             # 這個頁面右側沒有方塊
#             else:
#                 print('! step 2')
#                 return '-'
#         # 這個頁面不是歌手頁面或是歌手圖片頁面
#         else:
#             print('! step 1')
#             return '-'

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

                        with open(finished_artists, 'a', encoding='utf-8') as f:
                            f.write(singer_name + '\n')

                    # 有方塊，也有圖片，但是卻點不進去
                    else:
                        print('! step 4')

                        with open('z_image_but_problem.txt', 'a', encoding='utf-8') as f:
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

                    with open(finished_artists, 'a', encoding='utf-8') as f:
                        f.write(singer_name + '\n')

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
            start_url = "https://google.com"

            page.goto(start_url)
            page.wait_for_selector("#APjFqb", state="visible")

            while True:
                with open(waiting_artists, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                if lines != []:
                    full_name = lines.pop(0).replace('\n', '')

                    page.locator("#APjFqb").fill(f"{full_name} {language} 維基百科")

                    page.keyboard.press('Enter')

                    page.wait_for_selector("#hdtb-sc > div > div > div.crJ18e > div.Ap1Qsc > span > div",
                                           state="visible")

                    if page.locator('span[jscontroller="msmzHf"] a').nth(0).is_visible():
                        page.locator('span[jscontroller="msmzHf"] a').nth(0).click()

                        if 'wikipedia' in page.url:
                            page.wait_for_selector("#content", state="visible")

                            title_name = page.locator("#firstHeading").nth(0).inner_text().replace('[編輯]', '').strip()
                            if '(' in title_name:
                                title_name = title_name[:title_name.index('(')].strip()

                            print('title name = ', title_name)
                            print('full name = ', full_name)
                            sim = fuzz.ratio(title_name, full_name)

                            if full_name.lower() in title_name.lower() or title_name.lower() in full_name.lower():
                                print("that's what I like")
                                with open(link_file, 'a', encoding='utf-8') as f:
                                    f.write(f'{full_name}|||{page.url}\n')
                            elif sim > 80:
                                print("that's what I like 2")
                                with open(link_file, 'a', encoding='utf-8') as f:
                                    f.write(f'{full_name}|||{page.url}\n')
                            else:
                                with open(problem_file1, 'a', encoding='utf-8') as f:
                                    f.write(f'title name = {title_name}\nfull name = {full_name}\n{page.url}\n---\n')

                            print('---')
                        else:
                            with open(problem_file2, 'a', encoding='utf-8') as f:
                                f.write(f'{page.url}\n---\n')

                    # if '(' in full_name:
                    #     type_name = full_name.split('(')[0].strip()
                    # else:
                    #     type_name = full_name.strip()
                    # print('type_name = ', type_name)

                    # 搜尋欄位可見
                    # page.wait_for_selector('.cdx-text-input__input:nth-child(1)', state="visible")
                    # # if page.locator(".cdx-text-input__input").nth(0).is_visible():
                    # page.locator(".cdx-text-input__input").nth(0).fill(type_name)  # 填入關鍵字
                    # page.wait_for_timeout(3000)
                    # # if page.locator("#cdx-menu-item-1 > a > span:nth-child(2) > span > bdi > span").is_visible():
                    # if page.locator("#cdx-menu-item-1").nth(0).is_visible():
                    #     # first_search_result = page.locator(
                    #     #     "#cdx-menu-item-1 > a > span:nth-child(2) > span > bdi > span").inner_text()
                    #     page.locator("#cdx-menu-item-1").click()  # 前往頁面
                    #     page.wait_for_load_state('load')
                    #     page.wait_for_timeout(1500)
                    #
                    #     if page.locator("#firstHeading").nth(0).is_visible():
                    #         title_name = page.locator("#firstHeading").nth(0).inner_text()
                    #
                    #         if type_name in title_name:
                    #             get_wiki_data(page.url, full_name)
                    #         else:
                    #             print('名字對不起來')
                    #             with open('z_wiki_cannot_find.txt', 'a', encoding='utf-8') as f:
                    #                 f.write(full_name + '\n')
                    #     else:
                    #         print('沒有標題')
                    #         with open('z_wiki_cannot_find.txt', 'a', encoding='utf-8') as f:
                    #             f.write(full_name + '\n')
                    # else:
                    #     print('哇 根本沒有搜尋結果')
                    #     with open('z_wiki_cannot_find.txt', 'a', encoding='utf-8') as f:
                    #         f.write(full_name + '\n')
                    #
                    with open(waiting_artists, 'w', encoding='utf-8') as f:
                        f.writelines(lines)

                    page.goto(start_url)
                    page.wait_for_selector("#APjFqb", state="visible")

                else:
                    break
            break

        except Exception as e:
            print(e)
            page.close()

            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.set_default_timeout(10000)

            continue
