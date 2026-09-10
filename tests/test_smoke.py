from playwright.sync_api import Page, expect


def test_ghost_homepage_loads(page: Page, app_url: str):
    page.goto(app_url)

    expect(page).to_have_title("Ghost QA Automation")
    expect(
        page.get_by_role("heading", name="Thoughts, stories and ideas")
    ).to_be_visible()