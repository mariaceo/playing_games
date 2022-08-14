import pytest
from playwright.sync_api import Page

from ui_testing.src.pages.checkers_page import CheckersPage


@pytest.fixture
def checkers_page(page: Page) -> CheckersPage:
    return CheckersPage(page)
