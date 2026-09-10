from datetime import datetime
import os

from dotenv import load_dotenv
from playwright.sync_api import Page, expect
from pytest_bdd import given, when, then, scenarios

from pages.login_page import LoginPage
from pages.posts_page import PostsPage


load_dotenv()

scenarios("../features/publishing.feature")


@given("I am logged into Ghost")
def logged_in(page: Page, base_url: str, bdd_data: dict):
    email = os.getenv("GHOST_EMAIL")
    password = os.getenv("GHOST_PASSWORD")

    if not email or not password:
        raise RuntimeError(
            "GHOST_EMAIL and GHOST_PASSWORD must be set in .env"
        )

    login = LoginPage(page)
    login.open(base_url)
    login.login(email, password)

    bdd_data["login"] = login


@when("I create and publish a new post")
def create_and_publish(page: Page, base_url: str, bdd_data: dict):
    title = (
        f"BDD QA Post "
        f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    )

    posts = PostsPage(page)

    posts.open(base_url)
    posts.click_new_post()

    posts.create_post(
        title,
        "This post was created through a BDD scenario."
    )

    posts.publish()

    bdd_data["posts"] = posts
    bdd_data["title"] = title


@then("the published post should appear in the Posts list")
def verify_published_post(
    page: Page,
    base_url: str,
    bdd_data: dict
):
    posts = bdd_data["posts"]

    posts.open(base_url)

    post = page.get_by_text(
        bdd_data["title"],
        exact=True
    ).first

    expect(post).to_be_visible()