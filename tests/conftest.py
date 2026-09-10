import pytest


@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:3001"


@pytest.fixture
def app_url(base_url):
    return base_url


@pytest.fixture
def bdd_data():
    return {}