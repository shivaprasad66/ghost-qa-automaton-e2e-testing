import os

from dotenv import load_dotenv
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


load_dotenv()


def test_valid_login(page: Page, base_url: str):
    email = os.getenv("GHOST_EMAIL")
    password = os.getenv("GHOST_PASSWORD")

    if not email or not password:
        raise RuntimeError(
            "GHOST_EMAIL and GHOST_PASSWORD must be set."
        )

    login = LoginPage(page)

    login.open(base_url)

    login.login(
        email,
        password
    )

    expect(page).not_to_have_url(
        f"{base_url}/ghost/#/signin"
    )