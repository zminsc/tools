# Tools Repository Structure Guide

## Repository Overview

**Location**: `/home/user/tools/`
**Type**: Static HTML/JavaScript web tools
**Hosting**: GitHub Pages (tools.zminsc.dev)
**Testing**: Playwright + pytest for automated testing

---

## 1. Repository Structure

```
/home/user/tools/
├── *.html                    # Individual tool files
├── *.docs.md                 # Documentation/descriptions for each tool
├── tests/
│   ├── conftest.py          # Shared pytest fixtures
│   └── test_*.py            # Pytest test files
├── .github/workflows/
│   └── test.yml             # Runs pytest/playwright
├── README.md                # Main listing of all tools
├── index.html               # Homepage/tool registry
├── pyproject.toml           # Python project config and dependencies
└── .gitignore
```

---

## 2. Tool File Naming Convention

- **HTML file**: `{tool-name}.html` (e.g., `catan-practice.html`)
- **Docs file**: `{tool-name}.docs.md` (e.g., `catan-practice.docs.md`)
- **Test file**: `tests/test_{tool_name}.py` (e.g., `tests/test_catan_practice.py`)

### Example docs.md:
```markdown
Brief description of what the tool does and how to use it.
```

---

## 3. Common HTML Structure Patterns

### Basic Tool Template
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tool Name</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                         Helvetica, Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }
        /* Mobile-friendly media query */
        @media (max-width: 600px) {
            body { padding: 10px; }
            h1 { font-size: 24px; }
        }
    </style>
</head>
<body>
    <h1>Tool Name</h1>
    <p>Brief description of what this tool does</p>

    <!-- Tool UI elements -->

    <script>
        // Event listeners and processing logic
    </script>
</body>
</html>
```

**Key characteristics:**
- Responsive `<meta name="viewport">`
- Box-sizing border-box universally
- Centered max-width layout
- Real-time event listeners (`input`, `change`, `click`)
- Mobile media query at ~600px breakpoint

---

## 4. Mobile-Friendly UI Patterns

### Responsive Patterns:
1. **Max-width centered containers** (600-1200px)
2. **Flexbox layouts** for responsive grids
3. **Media queries** for breakpoints (600px, 768px, 920px)
4. **Padding adjustments** for mobile

### Example:
```css
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.game-layout {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
    justify-content: center;
}

@media (max-width: 600px) {
    body { padding: 10px; }
    .container { padding: 15px; }
}
```

---

## 5. Common UI Component Patterns

### Copy to Clipboard Button
```javascript
copyButton.addEventListener('click', () => {
    navigator.clipboard.writeText(textToCopy.value).then(() => {
        const originalText = copyButton.textContent;
        copyButton.textContent = 'Copied!';

        setTimeout(() => {
            copyButton.textContent = originalText;
        }, 2000);
    });
});
```

### Loading States
```javascript
button.disabled = true;
button.textContent = 'Loading...';

try {
    const result = await processData();
    displayResult(result);
} finally {
    button.disabled = false;
    button.textContent = 'Original text';
}
```

### Error Messages
```html
<div id="error" class="error"></div>

<style>
.error {
    color: #e74c3c;
    padding: 12px;
    background: #fef5f5;
    border-radius: 4px;
    display: none;
}
.error.visible {
    display: block;
}
</style>

<script>
function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.add('visible');
}
</script>
```

---

## 6. Test Structure

### Setup (tests/conftest.py)
```python
from http.client import HTTPConnection
import pathlib
import pytest
from subprocess import Popen, PIPE
import time

test_dir = pathlib.Path(__file__).parent.absolute()
root = test_dir.parent.absolute()

@pytest.fixture(scope="module")
def static_server():
    """Start a local HTTP server for testing."""
    process = Popen(
        ["python", "-m", "http.server", "8123", "--directory", str(root)],
        stdout=PIPE,
        stderr=PIPE,
    )
    retries = 5
    while retries > 0:
        conn = HTTPConnection("127.0.0.1:8123")
        try:
            conn.request("HEAD", "/")
            response = conn.getresponse()
            if response is not None:
                yield process
                break
        except ConnectionRefusedError:
            time.sleep(1)
            retries -= 1

    if not retries:
        raise RuntimeError("Failed to start http server")
    else:
        process.terminate()
        process.wait()
```

### Test Examples
```python
from playwright.sync_api import Page, expect

def test_initial_state(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/tool-name.html")
    expect(page.locator("h1")).to_have_text("Tool Name")

def test_functionality(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/tool-name.html")
    # Interact with the tool
    page.locator("#input").fill("test value")
    page.locator("#button").click()
    # Verify results
    expect(page.locator("#output")).to_have_text("expected output")
```

### Running Tests
```bash
# Install dependencies
pip install -e .
playwright install chromium

# Run all tests
pytest

# Run specific test
pytest tests/test_tool_name.py -v

# Run with verbose output
pytest -v
```

---

## 7. GitHub Workflow (.github/workflows/test.yml)
```yaml
name: Test
on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"
          cache-dependency-path: "pyproject.toml"
      - name: Cache Playwright browsers
        uses: actions/cache@v4
        with:
          path: ~/.cache/ms-playwright/
          key: ${{ runner.os }}-browsers
      - name: Install dependencies
        run: |
          pip install -e .
          playwright install chromium
      - name: Run tests
        run: pytest -v
```

---

## 8. Adding a New Tool

### Checklist

1. [ ] Create `{tool-name}.html` following the HTML template pattern
2. [ ] Create `{tool-name}.docs.md` with a brief description
3. [ ] Add the tool to `index.html` registry
4. [ ] Create `tests/test_{tool_name}.py` with Playwright tests
5. [ ] Implement mobile-friendly responsive design
6. [ ] Test locally with `python -m http.server 8000`
7. [ ] Run tests with `pytest -v`
8. [ ] Update README.md with the new tool listing

---

## 9. Useful Commands

```bash
# Start local development server
python -m http.server 8000

# Install test dependencies
pip install -e .
playwright install chromium

# Run all tests
pytest

# Run specific test file
pytest tests/test_tool_name.py -v
```

---

## Summary

This repository follows a **lightweight, stateless HTML5 pattern** where:
1. Each tool is a **single, self-contained HTML file**
2. Tools are **mobile-responsive** with CSS media queries
3. **Real-time processing** via JavaScript event listeners
4. **No build step** required for individual tools
5. **Tests** use Playwright + pytest for automation
6. **Documentation** in companion `.docs.md` files
