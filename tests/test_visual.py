import pytest
from pathlib import Path

from PIL import Image, ImageChops
from playwright.sync_api import Page


BASELINE = Path("screenshots/baseline/ghost-home.png")
CURRENT = Path("screenshots/current/ghost-home.png")


def test_ghost_homepage_visual(
    page: Page,
    base_url: str,
    browser_name: str
):
    if browser_name != "chromium":
        pytest.skip("Visual baseline is maintained for Chromium only")

    page.set_viewport_size({
        "width": 1280,
        "height": 720
    })

    page.goto(base_url)

    page.screenshot(
        path=str(CURRENT),
        full_page=True
    )

    baseline = Image.open(BASELINE).convert("RGB")
    current = Image.open(CURRENT).convert("RGB")

    assert baseline.size == current.size, (
        f"Screenshot size changed: "
        f"{baseline.size} -> {current.size}"
    )

    diff = ImageChops.difference(baseline, current)

    assert diff.getbbox() is None, (
        "Visual difference detected between baseline and current screenshot"
    )