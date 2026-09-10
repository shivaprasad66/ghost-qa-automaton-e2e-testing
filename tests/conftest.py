import os

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("GHOST_URL", "http://localhost:3001")


@pytest.fixture
def app_url(base_url):
    return base_url


@pytest.fixture
def bdd_data():
    return {}


@pytest.fixture(scope="session")
def ghost_credentials():
    email = os.getenv("GHOST_EMAIL")
    password = os.getenv("GHOST_PASSWORD")

    if not email or not password:
        raise RuntimeError(
            "GHOST_EMAIL and GHOST_PASSWORD must be set."
        )

    return {
        "email": email,
        "password": password,
    }