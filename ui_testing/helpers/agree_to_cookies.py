from playwright.sync_api import Page


def agree_to_cookies(page: Page):
    try:
        page.locator('text=We value your privacy').wait_for()
        page.locator('button:has-text("AGREE")').click()
    except:
        pass
