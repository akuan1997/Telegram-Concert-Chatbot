from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page
import re


def country_singers():
    events = page.query_selector_all(".mw-category-group")
    print(len(events))

    for i in range(1, len(events) + 1):
        s1 = f'.mw-category-group:nth-child({i}) > ul > li'
        events2 = page.query_selector_all(s1)
        print(len(events2))
        for j in range(1, len(events2) + 1):
            print(f'{i}-{j}')
            s2 = f'.mw-category-group:nth-child({i}) > ul > li:nth-child({j}) > a'
            if page.locator(s2).is_visible():
                page.locator(s2).click()
                page.wait_for_load_state('load')
                page.wait_for_timeout(1500)
                page.go_back()
            print('---')


def taiwan_singers():
    page.locator("#mw-content-textmw-pages")


def countries():
    events = page.query_selector_all(".mw-category-group")
    print(len(events))

    for i in range(2, len(events) + 1):
        s1 = f'.mw-category-group:nth-child({i}) > ul > li'
        events2 = page.query_selector_all(s1)
        print(len(events2))
        for j in range(1, len(events2) + 1):
            print(f'{i}-{j}')
            s2 = f'.mw-category-group:nth-child({i}) > ul > li:nth-child({j}) > div > div > a'
            if page.locator(s2).is_visible():
                page.locator(s2).click()
                page.wait_for_load_state('load')
                page.wait_for_timeout(1500)
                page.go_back()
            print('---')


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


# def country_singers_no_sub_category(page):
#     alphabets = page.query_selector_all("#mw-pages .mw-category-group")
#     print(f'總共有{len(alphabets)}個groups')
#     for i in range(1, len(alphabets)+1):
#         s1 = f'#mw-pages .mw-category-group:nth-child({i}) > ul > li'
#         group_singers = page.query_selector_all(s1)
#         print(f"第{i}個group有{len(group_singers)}位歌手")
#         for j in range(1, len(group_singers)+1):
#             print(f'{i}-{j}')
#             s2 = f'#mw-pages .mw-category-group:nth-child({i}) > ul > li:nth-child({j}) > a'
#             if page.locator(s2).is_visible():
#                 page.locator(s2).click()
#
#                 page.wait_for_load_state('load')
#                 page.wait_for_timeout(1500)
#                 page.go_back()
#             else:
#                 print('no')
#             print('---')


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://zh.wikipedia.org/wiki/Category:%E5%8F%B0%E7%81%A3%E5%98%BB%E5%93%88%E9%9F%B3%E6%A8%82%E5%9C%98%E9%AB%94")
    country_singers_no_sub_category(page)
    # _, names = name_page_actions()
    # print(names)

    # countries()
