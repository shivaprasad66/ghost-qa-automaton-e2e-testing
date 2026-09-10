from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


def test_valid_login(page: Page, base_url: str):
    login = LoginPage(page)

    login.open(base_url)
    login.login(
        "james@gmail.com",
        "1234567899"
    )

    expect(page).not_to_have_url(
        f"{base_url}/ghost/#/signin"
    )