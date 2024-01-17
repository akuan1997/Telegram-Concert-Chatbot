from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # 确保使用完整的文件路径和 file:// 协议
    page.goto("file:///C:/Users/pfii1/akuan/git-repos/Retrieval_model_practice/年代售票 _ 【再會!我的愛人】.mhtml")

    print(page.title())

    page.locator("#ctl00_ContentPlaceHolder1_btnBuyNow").click()
    page.wait_for_timeout(100000)
    page.close()
