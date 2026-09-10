from datetime import datetime

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.posts_page import PostsPage


def test_create_and_publish_post(page: Page, base_url: str):
    title = f"QA Automation Post {datetime.now().strftime('%H%M%S%f')}"
    body = "This post was created by the Ghost QA automation suite."

    login = LoginPage(page)
    login.open(base_url)
    login.login(
        "james@gmail.com",
        "1234567899"
    )

    posts = PostsPage(page)
    posts.open(base_url)
    posts.click_new_post()

    posts.create_post(title, body)
    posts.publish()

    posts.open(base_url)

    expect(
        page.get_by_text(title, exact=True).first
    ).to_be_visible()