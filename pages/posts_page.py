from playwright.sync_api import Page


class PostsPage:
    def __init__(self, page: Page):
        self.page = page

        self.new_post_button = page.locator(
            '[data-test-new-post-button], [data-test-nav="new-story"]'
        ).first

    def open(self, base_url: str):
        self.page.goto(f"{base_url}/ghost/#/posts")

    def click_new_post(self):
        self.new_post_button.click()

    def create_post(self, title: str, body: str):
        self.page.get_by_role(
            "textbox",
            name="Post title"
        ).fill(title)

        self.page.locator(
            '[contenteditable="true"]'
        ).first.fill(body)

    def publish(self):
        self.page.get_by_role(
            "button",
            name="Publish"
        ).first.click()

        self.page.get_by_role(
            "button",
            name="Publish"
        ).last.click()