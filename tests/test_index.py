from playwright.sync_api import Page, expect


def test_index_loads(page: Page, static_server):
    """Test that the index page loads correctly."""
    page.goto("http://127.0.0.1:8123/")
    expect(page.locator("h1")).to_have_text("Tools")


def test_index_shows_empty_state(page: Page, static_server):
    """Test that empty state is shown when no tools exist."""
    page.goto("http://127.0.0.1:8123/")
    expect(page.locator("#empty-state")).to_be_visible()
