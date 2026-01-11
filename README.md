# Tools

A collection of browser-based utilities hosted at [tools.zminsc.dev](https://tools.zminsc.dev).

## Tools

*No tools yet - check back soon!*

## Development

Each tool is a self-contained HTML file. To add a new tool:

1. Create `{tool-name}.html` in the root directory
2. Create `{tool-name}.docs.md` with a brief description
3. Add the tool to the registry in `index.html`
4. Add tests in `tests/test_{tool_name}.py`

### Local Development

```bash
# Start a local server
python -m http.server 8000

# Run tests
pip install -e .
playwright install
pytest
```

## License

MIT
