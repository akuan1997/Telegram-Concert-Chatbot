# 有地址的get_ticketplus
def get_ticketplus2(website, json_filename, txt_filename):
    with sync_playwright() as p:
        with open(json_filename, 'w', encoding='utf-8') as f:
            f.write('')

        # 待會會從 last_finished_index + 1開始
        last_finished_index = -1
        # 物件總數
        all_event_numbers = -1
        # 錯誤的網址
        fail_urls = []
        while True:
            try:
                browser = p.chromium.launch(headless=False, slow_mo=1000)
                context = browser.new_context()
                page = context.new_page()
                page.set_default_timeout(10000)

                page.goto("https://ticketplus.com.tw/")

                # 只有程式執行的一開始會經過這裡
                if last_finished_index == -1 and all_event_numbers == -1:
                    pressed = False
                    while not page.locator(
                            "#app > div > div > div > main > div > div > div.container.py-0.cus-container.mx-auto > div.tab-content.pa-3.pa-md-6 > div > div > div.text-center.pa-3.text-small.mt-6").is_visible():
                        page.keyboard.press('End')
                        if not pressed:
                            page.locator(
                                "#app > div > div > div > main > div > div > div.container.py-0.cus-container.mx-auto > div.tab-content.pa-3.pa-md-6 > div > div > div:nth-child(2) > button > span").click()
                            pressed = True

                    all_events = page.query_selector_all(".row > div.d-flex.col-sm-6.col-md-4.col-12")
                    all_event_numbers = len(all_events)
                    print(all_event_numbers, '\n')

                unique_id = []
                for i in range(last_finished_index + 1, all_event_numbers):
                    # print(f'Ticketplus progress - {i + 1}/{all_event_numbers}')
                    print(f'{website} progress - {i + 1}/{all_event_numbers}')
                    ''' 總數 '''
                    if i < 6:
                        page.locator(".row > div.d-flex.col-sm-6.col-md-4.col-12").nth(i).click()
                    else:
                        while not page.locator(".row > div.d-flex.col-sm-6.col-md-4.col-12").nth(
                                i).is_visible():
                            page.keyboard.press('End')
                            if page.locator(
                                    "#app > div > div > div > main > div > div > div.container.py-0.cus-container.mx-auto > div.tab-content.pa-3.pa-md-6 > div > div > div:nth-child(2) > button > span").is_visible():
                                page.locator(
                                    "#app > div > div > div > main > div > div > div.container.py-0.cus-container.mx-auto > div.tab-content.pa-3.pa-md-6 > div > div > div:nth-child(2) > button > span").click()

                        page.locator(".row > div.d-flex.col-sm-6.col-md-4.col-12").nth(i).click()

                    if page.locator(
                            "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.px-5.pb-5.font-weight-bold > div.row > div:nth-child(2) > button > span").is_visible():
                        page.locator(
                            "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.px-5.pb-5.font-weight-bold > div.row > div:nth-child(2) > button > span").click()

                    # 有時候網路比較慢會什麼都沒讀到就跳出來，如果沒看到內文我就持續讓他等待直到出現
                    while not page.locator("#activityInfo > div > div").is_visible():
                        page.wait_for_timeout(1000)

                    # 處理新資料
                    ''' 內文 '''
                    # 下載內文
                    inner_text = page.locator("#activityInfo > div > div").inner_text()
                    with open(txt_filename, 'w', encoding='utf-8') as f:
                        f.write(inner_text)
                    # 載入內文
                    with open(txt_filename, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    # 票價
                    prices = get_prices(lines)
                    # 售票時間
                    without_sell_time_lines, sell_datetimes_str = get_sell(get_time_lines(lines))
                    ''' 固定位置 '''
                    # 標題
                    title = page.locator("#banner > div.pb-6.col.col-12 > h1").inner_text()
                    # 資訊欄
                    columns = page.query_selector_all("#buyTicket > .sesstion-item")
                    for j in range(len(columns)):
                        column_text = page.locator("#buyTicket > .sesstion-item").nth(j).locator(
                            "div > div > div").nth(
                            0).inner_text()
                        column_text = column_text.split('\n')

                        # 第幾個位置是時間?
                        time_index = -1
                        for k in range(len(column_text)):
                            if ':' in column_text[k] or '：' in column_text[k]:
                                time_index = k
                                break
                        # 日期
                        concert_date = ''
                        for m in range(1, time_index):
                            column_text[m] = column_text[m].replace('-', '/')
                            column_text[m] = re.sub(r"[\(（【［<][^)）】］>]+[\)）】］>]", " ", column_text[m])
                            concert_date += column_text[m]
                        # 時間
                        concert_time = column_text[time_index]
                        # 我只想要開始的時間，捨棄結束的時間
                        if '~' in concert_time:
                            concert_time = concert_time[:concert_time.index('~')]
                        # 日期 & 時間
                        pdt = concert_date + ' ' + concert_time
                        pdt = re.sub(r"~", " ~ ", pdt)
                        pdt = re.sub(r"\s{2,}", " ", pdt)
                        if pdt[-1] == ' ':
                            pdt = pdt[:-1]
                        # 地點
                        concert_place = column_text[time_index + 1]
                        # 地址
                        concert_address = column_text[time_index + 2]
                        # 獨一無二的id識別
                        if f"{title}_{pdt}_{concert_place}" not in unique_id:
                            unique_id.append(f"{title}_{pdt}_{concert_place}")

                            print('tit', title)
                            print('sdt', sell_datetimes_str)
                            print('prc', prices)
                            print('pdt', pdt)
                            print('loc', concert_place)
                            print('add', concert_address)
                            print('web', f'{website}')
                            print('url', page.url)

                            new_data = {
                                'tit': title,
                                'sdt': sell_datetimes_str,
                                'prc': prices,
                                'pdt': [pdt],
                                'loc': [concert_place],
                                'add': concert_address,
                                'int': inner_text,
                                'web': f'{website}',
                                'url': page.url
                            }

                            print('\n--- write new data ---\n')

                            write_data_json(json_filename, new_data)

                            last_finished_index = i
                            if page.url in fail_urls:
                                del fail_urls[fail_urls.index(page.url)]
                        else:
                            print('Skip')
                            continue

                    page.go_back()

                # 完成
                page.close()
                # 移除剛剛使用的暫存文檔
                os.remove(txt_filename)

                delete_blank_sdt(website, json_filename)
                delete_past_ticketing_time(website, json_filename)

                print(f'\n\n\n\n\n\n\n\n{website} done\n\n\n\n\n\n\n\n')
                break

            except Exception as e:
                page.close()
                print(e, f'{website} restart')
                print('last finished index = ', last_finished_index)
                if page.url == 'https://ticketplus.com.tw/':
                    print(f'是{website}的主頁，沒關係的!')
                else:
                    if page.url not in fail_urls:
                        print('第一次失敗')
                        fail_urls.append(page.url)
                    else:
                        print('第二次失敗')
                        print('跳過')
                        last_finished_index += 1

                        write_error(website, page.url, e)

                # 重新啟動
                continue


get_ticketplus2('ticketplus2', 'ticketplus2.json', 'ticketplus2_temp.txt')


def kktix_get_location_str1(page, location, address):
    # 地點 str
    if page.locator("tbody > tr").nth(1).locator("th").is_visible():
        if page.locator("tbody > tr").nth(1).locator(
                "th").inner_text() == '活動地點':
            location_address = \
                page.locator("tbody > tr").nth(1).locator(
                    "td").inner_text().split(
                    '檢視地圖')[
                    0].strip().split(' / ')
            location = location_address[0]
            if len(location_address) == 1:
                address = '-'
            else:
                address = location_address[1]
    else:
        print('locations no')

    return location, address


def get_kktix_first1(website, json_filename, txt_filename):
    # global integrate_webs
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://kktix.com/events/452dac5f-copy-1/registrations/new")

        location = ''
        address = ''
        # 地點 str
        location, address = kktix_get_location_str1(page, location, address)
        print(location)
        print(address)


get_kktix_first1('kktix_test', '-', '-')
