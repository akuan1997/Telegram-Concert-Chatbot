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


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # page.goto("https://zh.wikipedia.org/wiki/Category:%E9%98%BF%E6%A0%B9%E5%BB%B7%E7%94%B7%E6%AD%8C%E6%89%8B")
    # page.goto("https://zh.wikipedia.org/wiki/Category:%E6%BE%B3%E5%A4%A7%E5%88%A9%E4%BA%9A%E7%94%B7%E6%AD%8C%E6%89%8B")

    # okay()

    # page.goto("https://zh.wikipedia.org/wiki/Category:%E5%90%84%E5%9B%BD%E7%94%B7%E6%AD%8C%E6%89%8B")

    # taiwan
    page.goto("https://zh.wikipedia.org/zh-tw/%E8%94%A1%E4%BE%9D%E6%9E%97")
    _, names = name_page_actions()
    print(names)

    # countries()
