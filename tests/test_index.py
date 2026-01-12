from playwright.sync_api import Page, expect


def test_index_loads(page: Page, static_server):
    """Test that the index page loads correctly."""
    page.goto("http://127.0.0.1:8123/")
    expect(page.locator("h1")).to_have_text("Tools")


def test_index_shows_tools_list(page: Page, static_server):
    """Test that tools list is shown when tools exist."""
    page.goto("http://127.0.0.1:8123/")
    expect(page.locator("#tools-list")).to_be_visible()
    expect(page.locator("#empty-state")).not_to_be_visible()


def test_index_shows_catan_tool(page: Page, static_server):
    """Test that Catan Placement Practice tool is listed."""
    page.goto("http://127.0.0.1:8123/")
    expect(page.locator(".tool-name")).to_contain_text("Catan Placement Practice")
