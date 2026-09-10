from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        self.email_input = page.get_by_role(
            "textbox",
            name="Email address"
        )

        self.password_input = page.get_by_role(
            "textbox",
            name="Password"
        )

        self.sign_in_button = page.get_by_role(
            "button",
            name="Sign in →"
        )

    def open(self, base_url: str):
        self.page.goto(f"{base_url}/ghost/#/signin")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.sign_in_button.click()