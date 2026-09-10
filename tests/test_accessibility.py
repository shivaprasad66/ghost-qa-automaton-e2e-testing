from playwright.sync_api import Page

from axe_playwright_python.sync_playwright import Axe
from pages.login_page import LoginPage


def test_ghost_login_accessibility(page: Page, base_url: str):
    login = LoginPage(page)
    login.open(base_url)

    results = Axe().run(page)
    violations = results.response["violations"]

    print("\nAccessibility violations:")

    for violation in violations:
        print(
            f"- {violation['id']} | "
            f"impact={violation.get('impact')} | "
            f"{violation['help']}"
        )