from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import expect, Page


def get_enews_emails():
    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=False)
        browser = p.chromium.launch(headless=True, slow_mo=1000)
        context = browser.new_context()
        page = context.new_page()
        wait_seconds = 3000
        page.goto('https://concertinfo.site/wp-admin')

        page.locator("#user_login").fill('user')
        page.locator("#user_pass").fill('FHDortmund_Kuan')
        page.wait_for_timeout(wait_seconds)
        page.keyboard.press('Enter')
        # page.wait_for_load_state('load')
        page.wait_for_timeout(wait_seconds)
        page.wait_for_selector(".wp-menu-name")
        menu_names = page.query_selector_all(".wp-menu-name")
        print(len(menu_names))
        for i in range(len(menu_names)):
            if 'CRM Entries' in menu_names[i].text_content():
                break
        menu_names[i].click()
        # page.wait_for_load_state('load')
        page.wait_for_timeout(wait_seconds)
        page.wait_for_selector("#entries_form")
        page.locator("#entries_form").click()
        # page.wait_for_load_state('load')
        page.wait_for_timeout(wait_seconds)
        page.wait_for_selector("#entries_form")
        page.locator("#entries_form").select_option(value="wp_393")
        # page.wait_for_load_state('load')
        page.wait_for_timeout(wait_seconds)
        page.wait_for_selector("#vx_entries_table > tbody > tr")
        emails = page.query_selector_all("#vx_entries_table > tbody > tr")
        enews_emails = []
        for i in range(len(emails)):
            email = page.locator("#vx_entries_table > tbody > tr").nth(i).locator("td").nth(2).inner_text()
            email = email.replace('\n', '').replace('View | Trash', '')
            enews_emails.append(email)
            print(email)
        print(enews_emails)
        return list(set(enews_emails))

# get_enews_emails()
