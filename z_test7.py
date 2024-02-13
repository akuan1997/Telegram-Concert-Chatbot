# # type-view
# type_view = page.query_selector_all('li.type-view')
# if last_finished_view_index != len(type_view) - 1:
#     print(f'\n\nview start from {page_index}-{last_finished_view_index + 2}\n\n')
#     for i in range(last_finished_view_index + 1, len(type_view)):
#         print(f'{website} view progress - page {page_index}, {i + 1}/{len(type_view)}')
#         # print(f'view {page_index}-{i}')
#         # 演唱會頁面
#         type_view[i].click()
#         print('concert page', page.url)
#         page.wait_for_timeout(500)
#
#         ''''''
#
#         hk = False
#         title = ''
#         sell_datetimes_str_list = []
#         prices = []
#         performance_datetimes_str_list = []
#         location = ''
#         if page.locator("table > thead > tr > th.name").is_visible():
#             # 確認此頁面是否為香港活動
#             # 1. 迴圈 票種、販售時間、售價 物件個數
#             for j in range(
#                     len(page.query_selector_all(
#                         ".table-wrapper > table > tbody > tr"))):
#                 # 貨幣符號
#                 # 如果有找到貨幣符號
#                 if page.locator(".table-wrapper > table > tbody > tr").nth(
#                         j).locator(".price .price > span").nth(0).is_visible():
#                     # 取得貨幣符號
#                     currency = page.locator(".table-wrapper > table > tbody > tr").nth(j).locator(".price .price > span").nth(0).inner_text()
#                     # 檢查是否為港幣
#                     if 'hk' in currency.lower():
#                         hk = True
#                         break
#                 # 找不到貨幣符號
#                 else:
#                     currency = ''
#
#                 ''''''
#
#                 # 售票時間 list
#                 sell_datetimes_str_list = kktix_get_ticketing_time_list(page, j,
#                                                                         sell_datetimes_str_list)
#
#                 ''''''
#
#                 # 票價 list
#                 prices = kktix_get_prices_list(page, j, prices)
#
#                 ''''''
#
#                 # 內文
#                 inner_text = page.locator(".description").inner_text()
#
#                 ''''''
#
#             if not hk:
#                 # 進入購票頁面，獲得地點以及表演時間
#                 page.locator(".outer-wrapper .tickets .btn-point").click()
#                 print('buy ticket page', page.url)
#                 page.wait_for_timeout(1500)
#                 page.wait_for_load_state('load')
#
#                 ''''''
#
#                 # 標題 str
#                 title = kktix_get_title_str(page, title)
#
#                 ''''''
#
#                 # 表演時間 list
#                 performance_datetimes_str_list = kktix_get_performance_list(page,
#                                                                             performance_datetimes_str_list)
#
#                 ''''''
#
#                 # 地點 str
#                 location = kktix_get_location_str(page, location)
#
#                 ''''''
#
#                 page.go_back()
#
#                 if title or performance_datetimes_str_list or location:
#                     print('title', title)  # str
#                     print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
#                     print('prices', prices)  # list
#                     print('performance_datetimes_str_list', performance_datetimes_str_list)  # list
#                     print('location', location)  # str
#
#                     ''''''
#
#                     # 新的一筆資料
#                     new_data = {
#                         'tit': title,
#                         'sdt': sell_datetimes_str_list,
#                         'prc': prices,
#                         'pdt': performance_datetimes_str_list,
#                         'loc': [location],
#                         'cit': "",
#                         'int': inner_text,
#                         'web': f'{website}',
#                         'url': page.url
#                     }
#
#                     ''''''
#
#                     print('\n--- write new data ---\n')
#
#                     write_data_json(json_filename, new_data)
#
#                     last_finished_view_index = i
#                     print(f'finished {page_index}-{last_finished_view_index+1}\n')
#                     print('\n----------------------\n')
#                 else:
#                     last_finished_view_index = i
#                     print(f'no tit, no pdt, no loc, skip\nfinished {page_index}-{last_finished_view_index + 1}\n\n----------------------\n')
#             else:
#                 print('hk activity, skip')
#                 last_finished_view_index = i
#                 print(f'finished {page_index}-{last_finished_view_index+1}\n')
#                 print('\n----------------------\n')
#
#         else:
#             print('integrate webpage, skip')
#             last_finished_view_index = i
#             print(f'finished {page_index}-{last_finished_view_index+1}\n')
#             print('\n----------------------\n')
#             # integrate_webs.append(page.url)
#
#         ''''''
#
#         page.go_back()  # main page
#         type_view = page.query_selector_all('li.type-view')
# else:
#     print('CSS: "type-view" of this page is already finished!')
def get_kktix_second(website, json_filename, txt_filename):
    # global integrate_webs
    with sync_playwright() as p:

        with open(json_filename, 'w', encoding='utf-8') as f:
            f.write('')

        # 待會會從 last_finished_index + 1開始
        last_finished_selling_index = -1
        last_finished_view_index = -1
        last_finished_counter_index = -1
        # 完成的演唱會頁面
        completed_pages = []
        # 發生錯誤的演唱會活動
        current_page_index = -1
        fail_indices = []
        # 統整的網站

        while True:
            try:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                # page.set_default_timeout(60000)

                ''''''

                page.goto("https://kktix.com/events?end_at=&"
                          "event_tag_ids_in=1&max_price=&"
                          "min_price=&page=5"
                          "&search=&start_at=")

                print(f'{website} start!')

                ''''''

                page_index = 5
                current_page_index = page_index

                while True:
                    if page_index in completed_pages:
                        print(f'Error occurred, but page {page_index} is already finished!')

                    else:
                        # type-selling
                        type_selling = page.query_selector_all('li.type-selling')
                        if last_finished_selling_index != len(type_selling) - 1:
                            print(f'\n\nselling start from {page_index}-{last_finished_selling_index + 2}\n\n')
                            for i in range(last_finished_selling_index + 1, len(type_selling)):
                                print(f'{website} selling progress - page {page_index}, {i + 1}/{len(type_selling)}')
                                # print(f'selling {page_index}-{i}')
                                # 演唱會頁面
                                type_selling[i].click()
                                print('concert page', page.url)
                                page.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str_list = []
                                prices = []
                                performance_datetimes_str_list = []
                                location = ''
                                if page.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        sell_datetimes_str_list = kktix_get_ticketing_time_list(page, j,
                                                                                                sell_datetimes_str_list)

                                        ''''''

                                        # 票價 list
                                        prices = kktix_get_prices_list(page, j, prices)

                                        ''''''

                                        # 內文
                                        inner_text = page.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page.url)
                                        page.wait_for_timeout(1500)
                                        page.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        title = kktix_get_title_str(page, title)

                                        ''''''

                                        # 表演時間 list
                                        performance_datetimes_str_list = kktix_get_performance_list(page,
                                                                                                    performance_datetimes_str_list)

                                        ''''''

                                        # 地點 str
                                        location = kktix_get_location_str(page, location)

                                        ''''''

                                        page.go_back()

                                        if title or performance_datetimes_str_list or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_selling_index = i
                                            print(f'finished {page_index}-{last_finished_selling_index + 1}')
                                            print('\n----------------------\n')
                                        else:
                                            last_finished_selling_index = i
                                            print(
                                                f'no tit, no pdt, no loc, skip\nfinished {page_index}-{last_finished_selling_index + 1}\n\n----------------------\n')
                                    else:
                                        print('hk activity, skip')
                                        last_finished_selling_index = i
                                        print(f'finished {page_index}-{last_finished_selling_index + 1}')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_selling_index = i
                                    print(f'finished {page_index}-{last_finished_selling_index + 1}')
                                    print('\n----------------------\n')
                                    # integrate_webs.append(page.url)

                                ''''''

                                page.go_back()  # main page
                                type_selling = page.query_selector_all('li.type-selling')
                        else:
                            print('CSS: "type-selling" of this page is already finished!')

                        # type-view
                        type_view = page.query_selector_all('li.type-view')
                        if last_finished_view_index != len(type_view) - 1:
                            print(f'\n\nview start from {page_index}-{last_finished_view_index + 2}\n\n')
                            for i in range(last_finished_view_index + 1, len(type_view)):
                                print(f'{website} view progress - page {page_index}, {i + 1}/{len(type_view)}')
                                # print(f'view {page_index}-{i}')
                                # 演唱會頁面
                                type_view[i].click()
                                print('concert page', page.url)
                                page.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str_list = []
                                prices = []
                                performance_datetimes_str_list = []
                                location = ''
                                if page.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        sell_datetimes_str_list = kktix_get_ticketing_time_list(page, j,
                                                                                                sell_datetimes_str_list)

                                        ''''''

                                        # 票價 list
                                        prices = kktix_get_prices_list(page, j, prices)

                                        ''''''

                                        # 內文
                                        inner_text = page.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page.url)
                                        page.wait_for_timeout(1500)
                                        page.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        title = kktix_get_title_str(page, title)

                                        ''''''

                                        # 表演時間 list
                                        performance_datetimes_str_list = kktix_get_performance_list(page,
                                                                                                    performance_datetimes_str_list)

                                        ''''''

                                        # 地點 str
                                        location = kktix_get_location_str(page, location)

                                        ''''''

                                        page.go_back()

                                        if title or performance_datetimes_str_list or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_view_index = i
                                            print(f'finished {page_index}-{last_finished_view_index + 1}\n')
                                            print('\n----------------------\n')
                                        else:
                                            last_finished_view_index = i
                                            print(
                                                f'no tit, no pdt, no loc, skip\nfinished {page_index}-{last_finished_view_index + 1}\n\n----------------------\n')
                                    else:
                                        print('hk activity, skip')
                                        last_finished_view_index = i
                                        print(f'finished {page_index}-{last_finished_view_index + 1}\n')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_view_index = i
                                    print(f'finished {page_index}-{last_finished_view_index + 1}\n')
                                    print('\n----------------------\n')
                                    # integrate_webs.append(page.url)

                                ''''''

                                page.go_back()  # main page
                                type_view = page.query_selector_all('li.type-view')
                        else:
                            print('CSS: "type-view" of this page is already finished!')

                        # type-counter
                        type_counter = page.query_selector_all('li.type-counter')
                        if last_finished_counter_index != len(type_counter) - 1:
                            print(f'\n\ncounter start from {page_index}-{last_finished_counter_index + 2}\n\n')
                            for i in range(last_finished_counter_index + 1, len(type_counter)):
                                print(f'{website} counter progress - page {page_index}, {i + 1}/{len(type_counter)}')
                                # print(f'counter {page_index}-{i}')
                                # 演唱會頁面
                                type_counter[i].click()
                                print('concert page', page.url)
                                page.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str_list = []
                                prices = []
                                performance_datetimes_str_list = []
                                location = ''
                                if page.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        sell_datetimes_str_list = kktix_get_ticketing_time_list(page, j,
                                                                                                sell_datetimes_str_list)

                                        ''''''

                                        # 票價 list
                                        prices = kktix_get_prices_list(page, j, prices)

                                        ''''''

                                        # 內文
                                        inner_text = page.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page.url)
                                        page.wait_for_timeout(1500)
                                        page.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        title = kktix_get_title_str(page, title)

                                        ''''''

                                        # 表演時間 list
                                        performance_datetimes_str_list = kktix_get_performance_list(page,
                                                                                                    performance_datetimes_str_list)

                                        ''''''

                                        # 地點 str
                                        location = kktix_get_location_str(page, location)

                                        ''''''

                                        page.go_back()

                                        if title or performance_datetimes_str_list or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_counter_index = i
                                            print(f'finished {page_index}-{last_finished_counter_index + 1}')
                                            print('\n----------------------\n')
                                        else:
                                            last_finished_counter_index = i
                                            print(
                                                f'no tit, no pdt, no loc, skip\nfinished {page_index}-{last_finished_counter_index + 1}\n\n----------------------\n')
                                    else:
                                        print('hk activity, skip')
                                        last_finished_counter_index = i
                                        print(f'finished {page_index}-{last_finished_counter_index + 1}')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_counter_index = i
                                    print(f'finished {page_index}-{last_finished_counter_index + 1}')
                                    print('\n----------------------\n')
                                    # integrate_webs.append(page.url)

                                ''''''

                                page.go_back()  # main page
                                type_counter = page.query_selector_all('li.type-counter')
                        else:
                            print('CSS: "type-counter" of this page is already finished!')

                        ''''''

                        # 完成此頁
                        pagination_div = page.query_selector(".pagination.pull-right")
                        text = pagination_div.inner_text()
                        print(f'\nFinished page {page_index}')
                        completed_pages.append(page_index)
                        last_finished_selling_index = -1
                        last_finished_view_index = -1

                    # 有下一頁
                    if '›' in text:
                        if int(page.locator(
                                "body > div.wrapper > div.page-content > section.explore-container.container > div > div.pagination.pull-right > ul > li.active > a").inner_text()) > 7:
                            break
                        page.locator("div.pagination.pull-right li:last-child").click()
                        page_index += 1
                        current_page_index = page_index
                        print(f'\nGo to page {page_index}\n')

                    # 最後一頁
                    else:
                        print(f'{website} finished')

                        # 程式確認沒有最後一頁後跳出while True的break
                        break

                # 確認全部執行完成，沒有發生錯誤的break
                break

            except Exception as e:
                # 錯誤
                page.close()
                print(e, f'{website} restart')
                if [current_page_index, last_finished_selling_index, last_finished_view_index] not in fail_indices:
                    fail_indices.append([current_page_index, last_finished_selling_index, last_finished_view_index])
                    print('第一次失敗')
                else:
                    print('第二次失敗')
                    print('跳過')

                    if last_finished_view_index == -1:
                        last_finished_selling_index += 1
                    else:
                        last_finished_view_index += 1

                    write_error(website, page.url, e)

                # 重新啟動
                continue

        # 完成
        page.close()

def get_kktix_third(website, json_filename, txt_filename):
    # global integrate_webs
    with sync_playwright() as p:

        with open(json_filename, 'w', encoding='utf-8') as f:
            f.write('')

            # 待會會從 last_finished_index + 1開始
            last_finished_selling_index = -1
            last_finished_view_index = -1
            last_finished_counter_index = -1
            # 完成的演唱會頁面
            completed_pages = []
            # 發生錯誤的演唱會活動
            current_page_index = -1
            fail_indices = []
            # 統整的網站

        while True:
            try:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                # page.set_default_timeout(60000)

                ''''''

                page.goto("https://kktix.com/events?end_at=&"
                          "event_tag_ids_in=1&max_price=&"
                          "min_price=&page=9"
                          "&search=&start_at=")

                print(f'{website} start!')

                ''''''

                page_index = 9
                current_page_index = page_index

                while True:
                    if page_index in completed_pages:
                        print(f'Error occurred, but page {page_index} is already finished!')

                    else:
                        # type-selling
                        type_selling = page.query_selector_all('li.type-selling')
                        if last_finished_selling_index != len(type_selling) - 1:
                            print(f'\n\nselling start from {page_index}-{last_finished_selling_index + 2}\n\n')
                            for i in range(last_finished_selling_index + 1, len(type_selling)):
                                print(f'{website} selling progress - page {page_index}, {i + 1}/{len(type_selling)}')
                                # print(f'selling {page_index}-{i}')
                                # 演唱會頁面
                                type_selling[i].click()
                                print('concert page', page.url)
                                page.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str_list = []
                                prices = []
                                performance_datetimes_str_list = []
                                location = ''
                                if page.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        sell_datetimes_str_list = kktix_get_ticketing_time_list(page, j,
                                                                                                sell_datetimes_str_list)

                                        ''''''

                                        # 票價 list
                                        prices = kktix_get_prices_list(page, j, prices)

                                        ''''''

                                        # 內文
                                        inner_text = page.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page.url)
                                        page.wait_for_timeout(1500)
                                        page.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        title = kktix_get_title_str(page, title)

                                        ''''''

                                        # 表演時間 list
                                        performance_datetimes_str_list = kktix_get_performance_list(page,
                                                                                                    performance_datetimes_str_list)

                                        ''''''

                                        # 地點 str
                                        location = kktix_get_location_str(page, location)

                                        ''''''

                                        page.go_back()

                                        if title or performance_datetimes_str_list or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_selling_index = i
                                            print(f'finished {page_index}-{last_finished_selling_index + 1}')
                                            print('\n----------------------\n')
                                        else:
                                            last_finished_selling_index = i
                                            print(
                                                f'no tit, no pdt, no loc, skip\nfinished {page_index}-{last_finished_selling_index + 1}\n\n----------------------\n')
                                    else:
                                        print('hk activity, skip')
                                        last_finished_selling_index = i
                                        print(f'finished {page_index}-{last_finished_selling_index + 1}')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_selling_index = i
                                    print(f'finished {page_index}-{last_finished_selling_index + 1}')
                                    print('\n----------------------\n')
                                    # integrate_webs.append(page.url)

                                ''''''

                                page.go_back()  # main page
                                type_selling = page.query_selector_all('li.type-selling')
                        else:
                            print('CSS: "type-selling" of this page is already finished!')

                        # type-view
                        type_view = page.query_selector_all('li.type-view')
                        if last_finished_view_index != len(type_view) - 1:
                            print(f'\n\nview start from {page_index}-{last_finished_view_index + 2}\n\n')
                            for i in range(last_finished_view_index + 1, len(type_view)):
                                print(f'{website} view progress - page {page_index}, {i + 1}/{len(type_view)}')
                                # print(f'view {page_index}-{i}')
                                # 演唱會頁面
                                type_view[i].click()
                                print('concert page', page.url)
                                page.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str_list = []
                                prices = []
                                performance_datetimes_str_list = []
                                location = ''
                                if page.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        sell_datetimes_str_list = kktix_get_ticketing_time_list(page, j,
                                                                                                sell_datetimes_str_list)

                                        ''''''

                                        # 票價 list
                                        prices = kktix_get_prices_list(page, j, prices)

                                        ''''''

                                        # 內文
                                        inner_text = page.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page.url)
                                        page.wait_for_timeout(1500)
                                        page.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        title = kktix_get_title_str(page, title)

                                        ''''''

                                        # 表演時間 list
                                        performance_datetimes_str_list = kktix_get_performance_list(page,
                                                                                                    performance_datetimes_str_list)

                                        ''''''

                                        # 地點 str
                                        location = kktix_get_location_str(page, location)

                                        ''''''

                                        page.go_back()

                                        if title or performance_datetimes_str_list or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_view_index = i
                                            print(f'finished {page_index}-{last_finished_view_index + 1}\n')
                                            print('\n----------------------\n')
                                        else:
                                            last_finished_view_index = i
                                            print(
                                                f'no tit, no pdt, no loc, skip\nfinished {page_index}-{last_finished_view_index + 1}\n\n----------------------\n')
                                    else:
                                        print('hk activity, skip')
                                        last_finished_view_index = i
                                        print(f'finished {page_index}-{last_finished_view_index + 1}\n')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_view_index = i
                                    print(f'finished {page_index}-{last_finished_view_index + 1}\n')
                                    print('\n----------------------\n')
                                    # integrate_webs.append(page.url)

                                ''''''

                                page.go_back()  # main page
                                type_view = page.query_selector_all('li.type-view')
                        else:
                            print('CSS: "type-view" of this page is already finished!')

                        # type-counter
                        type_counter = page.query_selector_all('li.type-counter')
                        if last_finished_counter_index != len(type_counter) - 1:
                            print(f'\n\ncounter start from {page_index}-{last_finished_counter_index + 2}\n\n')
                            for i in range(last_finished_counter_index + 1, len(type_counter)):
                                print(f'{website} counter progress - page {page_index}, {i + 1}/{len(type_counter)}')
                                # print(f'counter {page_index}-{i}')
                                # 演唱會頁面
                                type_counter[i].click()
                                print('concert page', page.url)
                                page.wait_for_timeout(500)

                                ''''''

                                hk = False
                                title = ''
                                sell_datetimes_str_list = []
                                prices = []
                                performance_datetimes_str_list = []
                                location = ''
                                if page.locator("table > thead > tr > th.name").is_visible():
                                    # 確認此頁面是否為香港活動
                                    # 1. 迴圈 票種、販售時間、售價 物件個數
                                    for j in range(
                                            len(page.query_selector_all(
                                                ".table-wrapper > table > tbody > tr"))):
                                        # 貨幣符號
                                        # 如果有找到貨幣符號
                                        if page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).is_visible():
                                            # 取得貨幣符號
                                            currency = page.locator(".table-wrapper > table > tbody > tr").nth(
                                                j).locator(".price .price > span").nth(0).inner_text()
                                            # 檢查是否為港幣
                                            if 'hk' in currency.lower():
                                                hk = True
                                                break
                                        # 找不到貨幣符號
                                        else:
                                            currency = ''

                                        ''''''

                                        # 售票時間 list
                                        sell_datetimes_str_list = kktix_get_ticketing_time_list(page, j,
                                                                                                sell_datetimes_str_list)

                                        ''''''

                                        # 票價 list
                                        prices = kktix_get_prices_list(page, j, prices)

                                        ''''''

                                        # 內文
                                        inner_text = page.locator(".description").inner_text()

                                        ''''''

                                    if not hk:
                                        # 進入購票頁面，獲得地點以及表演時間
                                        page.locator(".outer-wrapper .tickets .btn-point").click()
                                        print('buy ticket page', page.url)
                                        page.wait_for_timeout(1500)
                                        page.wait_for_load_state('load')

                                        ''''''

                                        # 標題 str
                                        title = kktix_get_title_str(page, title)

                                        ''''''

                                        # 表演時間 list
                                        performance_datetimes_str_list = kktix_get_performance_list(page,
                                                                                                    performance_datetimes_str_list)

                                        ''''''

                                        # 地點 str
                                        location = kktix_get_location_str(page, location)

                                        ''''''

                                        page.go_back()

                                        if title or performance_datetimes_str_list or location:
                                            print('title', title)  # str
                                            print('sell_datetimes_str_list', sell_datetimes_str_list)  # list
                                            print('prices', prices)  # list
                                            print('performance_datetimes_str_list',
                                                  performance_datetimes_str_list)  # list
                                            print('location', location)  # str

                                            ''''''

                                            # 新的一筆資料
                                            new_data = {
                                                'tit': title,
                                                'sdt': sell_datetimes_str_list,
                                                'prc': prices,
                                                'pdt': performance_datetimes_str_list,
                                                'loc': [location],
                                                'cit': "",
                                                'int': inner_text,
                                                'web': f'{website}',
                                                'url': page.url
                                            }

                                            ''''''

                                            print('\n--- write new data ---\n')

                                            write_data_json(json_filename, new_data)

                                            last_finished_counter_index = i
                                            print(f'finished {page_index}-{last_finished_counter_index + 1}')
                                            print('\n----------------------\n')
                                        else:
                                            last_finished_counter_index = i
                                            print(
                                                f'no tit, no pdt, no loc, skip\nfinished {page_index}-{last_finished_counter_index + 1}\n\n----------------------\n')
                                    else:
                                        print('hk activity, skip')
                                        last_finished_counter_index = i
                                        print(f'finished {page_index}-{last_finished_counter_index + 1}')
                                        print('\n----------------------\n')

                                else:
                                    print('integrate webpage, skip')
                                    last_finished_counter_index = i
                                    print(f'finished {page_index}-{last_finished_counter_index + 1}')
                                    print('\n----------------------\n')
                                    # integrate_webs.append(page.url)

                                ''''''

                                page.go_back()  # main page
                                type_counter = page.query_selector_all('li.type-counter')
                        else:
                            print('CSS: "type-counter" of this page is already finished!')

                        ''''''

                        # 完成此頁
                        pagination_div = page.query_selector(".pagination.pull-right")
                        text = pagination_div.inner_text()
                        print(f'\nFinished page {page_index}')
                        completed_pages.append(page_index)
                        last_finished_selling_index = -1
                        last_finished_view_index = -1
                        last_finished_counter_index = -1

                    # 有下一頁
                    if '›' in text:
                        page.locator("div.pagination.pull-right li:last-child").click()
                        page_index += 1
                        current_page_index = page_index
                        print(f'\nGo to page {page_index}\n')

                    # 最後一頁
                    else:
                        print(f'{website} finished')

                        # 程式確認沒有最後一頁後跳出while True的break
                        break

                # 確認全部執行完成，沒有發生錯誤的break
                break

            except Exception as e:
                # 錯誤
                page.close()
                print(e, f'{website} restart')
                if [current_page_index, last_finished_selling_index, last_finished_view_index] not in fail_indices:
                    fail_indices.append([current_page_index, last_finished_selling_index, last_finished_view_index])
                    print('第一次失敗')
                else:
                    print('第二次失敗')
                    print('跳過')

                    if last_finished_view_index == -1:
                        last_finished_selling_index += 1
                    else:
                        last_finished_view_index += 1

                    write_error(website, page.url, e)

                # 重新啟動
                continue

        # 完成
        page.close()