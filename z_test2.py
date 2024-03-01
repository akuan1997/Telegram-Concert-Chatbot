# from playwright.sync_api import sync_playwright, Playwright
# from playwright.sync_api import expect, Page
# import json
#
# cities = ["台北", "新北", "桃園", "台中", "台南", "高雄", "基隆", "新竹", "新竹", "苗栗", "彰化", "南投", "雲林",
#           "嘉義", "嘉義", "屏東", "宜蘭", "花蓮", "台東", "金門", "澎湖", "連江"]
#
# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#
#     page.goto("https://www.google.com.tw/maps/")
#
#     with open('concert_data_new_zh.json', 'r', encoding='utf-8') as f:
#         data = json.load(f)
#
#     for i in range(len(data)):
#         page.locator('#searchboxinput').fill(data[i]['loc'][0])
#
#         page.wait_for_timeout(1500)
#
#         s1 = ".fontBodyMedium.DAdBuc > div"  # 有幾個搜尋結果
#         results = page.query_selector_all(s1)
#         print(data[i]['loc'][0], len(results))
#         for j in range(len(results)):
#             s2 = f'#cell{j}x0 > span:nth-child(6) > span:nth-child(1)'  # 搜尋結果後面有沒有地址
#             if page.locator(s2).is_visible():
#                 print(f'第{j}行找到地址!')
#                 print(page.locator(s2).inner_text())
#                 break
#                 # if page.locator(s2).inner_text() in cities:
#                 #     print('yes')
#                 # else:
#                 #     print('no')
#         print('----')
