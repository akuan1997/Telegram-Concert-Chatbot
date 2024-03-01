# # import json
# # from playwright.sync_api import sync_playwright, Playwright
# # from playwright.sync_api import expect, Page
# # from fuzzywuzzy import process, fuzz
# #
#
# #
# #
# # def load_table_from_txt(filename):
# #     zh_table = {}
# #     with open(filename, 'r', encoding='utf-8') as file:
# #         for line in file:
# #             key, value = line.strip().split(':')
# #             zh_table[key] = value
# #     return zh_table
# #
# #
# # # def write_table_to_txt(filename, data):
# # #     with open(filename, 'w', encoding='utf-8') as file:
# # #         for key, value in data.items():
# # #             file.write(f"{key}:{value}\n")
# #
# #
# # def stadium_city(stadium, lang, table):
# #     # 先把stadium的字串做處理 小寫 + 去除空格
# #     stadium = stadium.lower()
# #     stadium = stadium.replace(' ', '')
# #     # 中文
# #     if lang == 'zh':
# #         best_match, score = process.extractOne(stadium, table.keys())
# #         # 閥值設為80
# #         if score > 80:
# #             print('score', score)
# #             return table[best_match]
# #         # 沒超過代表找不到
# #         else:
# #             return ''
# #
# #
# # def find_stadium_city(json_file, zh_table):
# #     with sync_playwright() as p:
# #         browser = p.chromium.launch(headless=False)
# #         context = browser.new_context()
# #         page = context.new_page()
# #
# #         with open(json_file, 'r', encoding='utf-8') as f:
# #             data = json.load(f)
# #
# #         for i in range(len(data)):
# #             if data[i]['loc'] == [] or data[i]['loc'] == ['']:
# #                 print('是空白的就直接跳過')
# #             else:
# #                 print(i)
# #                 city = ''
# #                 location = data[i]['loc'][0]
# #                 print('location', location)
# #                 # string (從名稱裡面找到城市名稱)
# #                 for j in range(len(zh_cities)):
# #                     # 臺 -> 台
# #                     location = location.replace('臺', '台')
# #                     # 如果字串裡面就包含了城市的名稱
# #                     if zh_cities[j] in location:
# #                         # 就可以直接找到城市
# #                         print('從名稱就找到城市')
# #                         city = zh_cities[j]
# #                         break
# #
# #                 # table (如果名稱裡面沒有城市名稱，就去table裡面尋找)
# #                 if city == '':
# #                     print('table!')
# #                     # 使用table對照表尋找看看
# #                     city = stadium_city(location, 'zh', load_table_from_txt(zh_table))
# #
# #                 # playwright (如果連table裡面也沒有找到)
# #                 if city == '':
# #                     print('playwright!')
# #                     # 那就靠網路爬蟲來尋找並加入table
# #                     page.goto("https://www.google.com/")
# #                     # fill完成之後會顯示搜尋結果
# #                     page.locator("#APjFqb").fill(location)
# #
# #                     page.wait_for_timeout(1500)
# #
# #                     # 迴圈 全部的搜尋結果 只要出現城市名稱就跳出迴圈
# #                     contents = page.query_selector_all(".G43f7e .lnnVSe .ClJ9Yb > span")
# #                     # 搜尋結果有沒有顯示城市名稱
# #                     for k in range(len(contents)):
# #                         for zh_city in zh_cities:
# #                             if zh_city in contents[k].inner_text():
# #                                 city = zh_city
# #                                 print(f'搜尋結果頁面就有城市了! {city}')
# #                                 break
# #
# #                     # 如果搜尋結果裡面沒有出現城市名稱，那就要進一步去下一個頁面尋找
# #                     if city == '':
# #                         print('搜尋結果沒有出現城市 必須往下一頁面繼續尋找')
# #                         # do something
# #                         page.keyboard.press('Enter')
# #                         page.wait_for_timeout(1500)
# #
# #                         address_phone = page.query_selector_all(".zloOqf.PZPZlf .LrzXr")
# #                         for k in range(len(address_phone)):
# #                             for zh_city in zh_cities:
# #                                 if zh_city in address_phone[k].inner_text():
# #                                     city = zh_city
# #                                     print(f'右側面板找到城市了! {city}')
# #                                     break
# #
# #                         if city == '':
# #                             print('還是沒有找到 看一下第一個搜尋結果 看看有沒有東西')
# #                             search_results = page.query_selector_all(".MjjYud")
# #                             for zh_city in zh_cities:
# #                                 if zh_city in search_results[0].inner_text():
# #                                     city = zh_city
# #                                     break
# #                             if city == '':
# #                                 print('真的找不到')
# #                             else:
# #                                 with open(zh_table, 'a', encoding='utf-8') as f:
# #                                     f.write(f"{location.lower().replace(' ', '')}:{city}\n")
# #
# #                         # 有找到 把配對寫進table裡面
# #                         else:
# #                             if page.locator(".DoxwDb .PZPZlf").is_visible():
# #                                 print(page.locator(".DoxwDb .PZPZlf").inner_text())
# #                                 with open(zh_table, 'a', encoding='utf-8') as f:
# #                                     f.write(f"{page.locator('.DoxwDb .PZPZlf').inner_text()}:{city}\n")
# #                             with open(zh_table, 'a', encoding='utf-8') as f:
# #                                 f.write(f"{location.lower().replace(' ', '')}:{city}\n")
# #
# #                     # 搜尋結果有找到城市 把這個配對寫進table裡面
# #                     else:
# #                         # 把這次網路爬蟲找到的stadium & city寫進table裡面
# #                         print(f"寫入新資料! {location} & {city}")
# #                         location = location.lower()
# #                         location = location.replace(' ', '')
# #                         with open(zh_table, 'a', encoding='utf-8') as f:
# #                             f.write(f"{location}:{city}\n")
# #
# #                 print(city)
# #                 data[i]['cit'] = city
# #                 with open(json_file, 'w', encoding='utf-8') as f:
# #                     json.dump(data, f, indent=4, ensure_ascii=False)
# #                 print('---')
# #
# #
# # find_stadium_city('concert_test.json', 'zh_stadium_table.txt')
# #
# # # with sync_playwright() as p:
# # #     browser = p.chromium.launch(headless=False)
# # #     context = browser.new_context()
# # #     page = context.new_page()
# # #
# # #     page.goto("https://www.google.com/search?q=%E8%80%81%E7%AA%96%E5%AE%A4+Cellarsroom&sca_esv=601452934&rlz=1C1JJTC_zh-TWTW1052TW1052&sxsrf=ACQVn0_J99rr9tLp8vrHd-Nc3Q8LKV2cUQ%3A1706211001924&ei=ubayZYWJONX81e8P7NeA4A0&ved=0ahUKEwjFybmlo_mDAxVVfvUHHewrANwQ4dUDCBA&uact=5&oq=%E8%80%81%E7%AA%96%E5%AE%A4+Cellarsroom&gs_lp=Egxnd3Mtd2l6LXNlcnAiFeiAgeeqluWupCBDZWxsYXJzcm9vbTIEECMYJ0iAA1CVAViVAXABeAGQAQCYATKgATKqAQExuAEDyAEA-AEC-AEBwgIKEAAYRxjWBBiwA-IDBBgAIEGIBgGQBgo&sclient=gws-wiz-serp")
# # #
# # #     kuans = page.query_selector_all(".MjjYud")
# # #     for zh_city in zh_cities:
# # #         if zh_city in kuans[0].inner_text():
# # #             city = zh_city
# # #             break
# # # print(page.locator(".MjjYud").inner_text())
# #
# # #     for kuan in kuans:
# # #         city = ''
# # #         page.goto("https://www.google.com/")
# # #         page.locator("#APjFqb").fill(kuan)
# # #         page.wait_for_timeout(1500)
# # #         page.keyboard.press('Enter')
# # #         page.wait_for_timeout(1500)
# # #         print('stadium', kuan)
# # #
# # #         address_phone = page.query_selector_all(".zloOqf.PZPZlf .LrzXr")
# # #         for i in range(len(address_phone)):
# # #             for zh_city in zh_cities:
# # #                 if zh_city in address_phone[i].inner_text():
# # #                     city = zh_city
# # #                     break
# # #
# # #         print('city', city)
# # #         if city == '':
# # #             print('沒有找到')
# # #             # do something
# # #         else:
# # #             if page.locator(".DoxwDb .PZPZlf").is_visible():
# # #                 print(page.locator(".DoxwDb .PZPZlf").inner_text())
# # #                 with open(zh_table, 'a', encoding='utf-8') as f:
# # #                     f.write(f"{page.locator('.DoxwDb .PZPZlf').inner_text()}:{city}\n")
# # #             with open(zh_table, 'a', encoding='utf-8') as f:
# # #                 f.write(f"{kuan}:{city}\n")
# # #
# # #         print('---')
#
# import json
#
# zh_cities = ["台北", "新北", "桃園", "台中", "台南", "高雄", "基隆", "新竹", "苗栗", "彰化", "南投", "雲林",
#              "嘉義", "屏東", "宜蘭", "花蓮", "台東", "金門", "澎湖", "連江"]
#
# en_cities = ["Taipei", "New Taipei", "Taoyuan", "Taichung", "Tainan", "Kaohsiung", "Keelung", "Hsinchu", "Miaoli",
#              "Changhua", "Nantou", "Yunlin", "Chiayi", "Pingtung", "Yilan", "Hualien", "Taitung", "Kinmen", "Penghu",
#              "Lienchiang"]
#
# city_mapping = dict(zip(zh_cities, en_cities))
#
# with open('concert_test.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# for i in range(len(data)):
#     if 'cit' in data[i]:
#         if data[i]['cit'] in city_mapping:
#             data[i]['cit'] = city_mapping[data[i]['cit']]
#             print(data[i]['cit'])
#
#             with open('concert_test.json', 'w', encoding='utf-8') as f:
#                 json.dump(data, f, indent=4, ensure_ascii=False)
