# import json
# from playwright.sync_api import sync_playwright, Playwright
# from playwright.sync_api import expect, Page
# from fuzzywuzzy import process
#
# zh_cities = ["台北", "新北", "桃園", "台中", "台南", "高雄", "基隆", "新竹", "新竹", "苗栗", "彰化", "南投", "雲林",
#              "嘉義", "嘉義", "屏東", "宜蘭", "花蓮", "台東", "金門", "澎湖", "連江"]
#
#
# def load_table_from_txt(filename):
#     zh_table = {}
#     with open(filename, 'r', encoding='utf-8') as file:
#         for line in file:
#             key, value = line.strip().split(':')
#             print(key, value)
#             zh_table[key] = value
#     return zh_table
#
#
# def load_table_from_txt1(filename):
#     zh_table = {}
#     with open(filename, 'r', encoding='utf-8') as file:
#         for line in file:
#             key, value = line.strip().split(':')
#             print(key, value)
#             zh_table[key] = value
#     return zh_table
#
#
# load_table_from_txt("zh_stadium_table.txt")
#
#
# def stadium_city(stadium, lang, table):
#     # 先把stadium的字串做處理 小寫 + 去除空格
#     stadium = stadium.lower()
#     stadium = stadium.replace(' ', '')
#     # 中文
#     if lang == 'zh':
#         best_match, score = process.extractOne(stadium, table.keys())
#         # 閥值設為80
#         if score > 80:
#             print('score', score)
#             return table[best_match]
#         # 沒超過代表找不到
#         else:
#             return ''
#
#
# def add_stadium_city(json_filename, zh_table):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#
#         with open(json_filename, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#
#         for i in range(len(data)):
#             print(i)
#             print(data[i]['loc'][0])
#             city = ''
#             if not data[i]['loc'][0] == '':
#                 # string (從名稱裡面找到城市名稱)
#                 for j in range(len(zh_cities)):
#                     # 臺 -> 台
#                     data[i]['loc'][0] = data[i]['loc'][0].replace('臺', '台')
#                     # 如果字串裡面就包含了城市的名稱
#                     if zh_cities[j] in data[i]['loc'][0]:
#                         # 就可以直接找到城市
#                         print('從名稱就找到城市')
#                         city = zh_cities[j]
#                         break
#
#                 # table (如果名稱裡面沒有城市名稱，就去table裡面尋找)
#                 if city == '':
#                     print('table!')
#                     # 使用table對照表尋找看看
#                     city = stadium_city(data[i]['loc'][0], 'zh', load_table_from_txt(zh_table))
#
#                 # playwright (如果連table裡面也沒有找到)
#                 if city == '':
#                     print('playwright!')
#                     # 那就靠網路爬蟲來尋找並加入table
#                     page.goto("https://www.google.com/")
#                     # fill完成之後會顯示搜尋結果
#                     page.locator("#APjFqb").fill(data[i]['loc'][0])
#
#                     page.wait_for_timeout(1500)
#
#                     # 迴圈 全部的搜尋結果 只要出現城市名稱就跳出迴圈
#                     contents = page.query_selector_all(".G43f7e .lnnVSe .ClJ9Yb > span")
#                     # 搜尋結果有沒有顯示城市名稱
#                     for k in range(len(contents)):
#                         for zh_city in zh_cities:
#                             if zh_city in contents[k].inner_text():
#                                 city = zh_city
#                                 print(f'搜尋結果頁面就有城市了! {city}')
#                                 break
#
#                     # 如果搜尋結果裡面沒有出現城市名稱，那就要進一步去下一個頁面尋找
#                     if city == '':
#                         print('搜尋結果沒有出現城市 必須往下一頁面繼續尋找')
#                         # do something
#                         page.keyboard.press('Enter')
#                         page.wait_for_timeout(1500)
#
#                         address_phone = page.query_selector_all(".zloOqf.PZPZlf .LrzXr")
#                         for k in range(len(address_phone)):
#                             for zh_city in zh_cities:
#                                 if zh_city in address_phone[k].inner_text():
#                                     city = zh_city
#                                     print(f'右側面板找到城市了! {city}')
#                                     break
#
#                         if city == '':
#                             print('還是沒有找到 看一下第一個搜尋結果 看看有沒有東西')
#                             search_results = page.query_selector_all(".MjjYud")
#                             for zh_city in zh_cities:
#                                 if zh_city in search_results[0].inner_text():
#                                     city = zh_city
#                                     break
#                             if city == '':
#                                 print('真的找不到')
#                             else:
#                                 with open(zh_table, 'a', encoding='utf-8') as f:
#                                     f.write(f"{data[i]['loc'][0].lower().replace(' ', '')}:{city}\n")
#
#                         # 有找到 把配對寫進table裡面
#                         else:
#                             if page.locator(".DoxwDb .PZPZlf").is_visible():
#                                 print(page.locator(".DoxwDb .PZPZlf").inner_text())
#                                 with open(zh_table, 'a', encoding='utf-8') as f:
#                                     f.write(f"{page.locator('.DoxwDb .PZPZlf').inner_text()}:{city}\n")
#                             with open(zh_table, 'a', encoding='utf-8') as f:
#                                 f.write(f"{data[i]['loc'][0].lower().replace(' ', '')}:{city}\n")
#
#                     # 搜尋結果有找到城市 把這個配對寫進table裡面
#                     else:
#                         # 把這次網路爬蟲找到的stadium & city寫進table裡面
#                         print(f"寫入新資料! {data[i]['loc'][0]} & {city}")
#                         data[i]['loc'][0] = data[i]['loc'][0].lower()
#                         data[i]['loc'][0] = data[i]['loc'][0].replace(' ', '')
#                         with open(zh_table, 'a', encoding='utf-8') as f:
#                             f.write(f"{data[i]['loc'][0]}:{city}\n")
#
#                 print(city)
#                 print('---')
