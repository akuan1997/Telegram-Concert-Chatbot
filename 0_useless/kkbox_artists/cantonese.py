# 華語 297
# 西洋 390
# 日語 308
# 韓語 314
# 台語 304
# 粵語 320

txt_file = 'cantonese.txt'
record_file = 'cantonese_record.txt'
language = 320

import datetime
from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    with open(record_file, 'r', encoding='utf-8') as f:
        finished_dates = f.readlines()
    current_date = finished_dates[-1].replace('\n', '')

    current_date = datetime.date(int(current_date.split('-')[0]), int(current_date.split('-')[1]),
                                 int(current_date.split('-')[2]))
    print('current_date =', current_date)
    end_date = datetime.date(2024, 4, 26)  # today

    while current_date <= end_date:
        try:
            print(current_date)

            link = f'https://kma.kkbox.com/charts/daily/song?cate={language}&date={current_date}&lang=tc&terr=tw'
            page.goto(link)
            page.wait_for_load_state('load')
            page.wait_for_timeout(1500)

            artists = page.query_selector_all(".charts-list-artist")
            for i in range(len(artists)):
                artist_name = artists[i].inner_text()
                with open(txt_file, 'r', encoding='utf-8') as f:
                    exist_artists = f.readlines()
                exist_artists = [exist_artist.replace('\n', '') for exist_artist in exist_artists]

                if artist_name not in exist_artists:
                    with open(txt_file, 'a', encoding='utf-8') as f:
                        print(artist_name)
                        f.write(artist_name + '\n')
            with open(record_file, 'a', encoding='utf-8') as f:
                f.write(str(current_date) + '\n')
            current_date += datetime.timedelta(days=1)
        except:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            with open(record_file, 'r', encoding='utf-8') as f:
                finished_dates = f.readlines()
            current_date = finished_dates[-1].replace('\n', '')

            current_date = datetime.date(int(current_date.split('-')[0]), int(current_date.split('-')[1]),
                                         int(current_date.split('-')[2]))
            print('current_date =', current_date)
