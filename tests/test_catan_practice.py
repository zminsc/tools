from playwright.sync_api import Page, expect


def test_page_loads(page: Page, static_server):
    """Test that the page loads with correct title."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")
    expect(page.locator("h1")).to_have_text("Catan Placement Practice")


def test_initial_state(page: Page, static_server):
    """Test initial game state shows Player 1 placing settlement."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")
    expect(page.locator("#currentPlayer")).to_have_text("Player 1 (Red)")
    expect(page.locator("#phaseInfo")).to_have_text("Place 1st settlement")
    expect(page.locator("#settlementCount")).to_have_text("0")
    expect(page.locator("#roadCount")).to_have_text("0")


def test_board_renders_hexes(page: Page, static_server):
    """Test that the board renders 19 hex tiles."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")
    hexes = page.locator("#board .hex")
    expect(hexes).to_have_count(19)


def test_settlement_hints_visible(page: Page, static_server):
    """Test that settlement placement hints are visible initially."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")
    hints = page.locator("#board .vertex-hint")
    # Should have multiple valid settlement spots
    count = hints.count()
    assert count > 0, "Should show settlement placement hints"


def test_place_settlement(page: Page, static_server):
    """Test placing a settlement."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    # Click first available settlement hint
    hint = page.locator("#board .vertex-hint").first
    hint.click()

    # Should now be in road placement phase
    expect(page.locator("#phaseInfo")).to_have_text("Place a road")
    expect(page.locator("#settlementCount")).to_have_text("1")

    # Settlement should be visible
    settlements = page.locator("#board .settlement")
    expect(settlements).to_have_count(1)


def test_place_road(page: Page, static_server):
    """Test placing a road after settlement."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    # Place settlement
    page.locator("#board .vertex-hint").first.click()

    # Wait for road hints to appear and click
    # Use force=True because SVG line elements can be thin
    road_hint = page.locator("#board .edge-hint").first
    road_hint.click(force=True)

    # Should move to Player 2
    expect(page.locator("#currentPlayer")).to_have_text("Player 2 (Blue)")
    expect(page.locator("#roadCount")).to_have_text("1")


def test_undo_settlement(page: Page, static_server):
    """Test undoing a settlement placement."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    # Place settlement
    page.locator("#board .vertex-hint").first.click()
    expect(page.locator("#settlementCount")).to_have_text("1")

    # Undo
    page.locator("#undoBtn").click()
    expect(page.locator("#settlementCount")).to_have_text("0")
    expect(page.locator("#phaseInfo")).to_have_text("Place 1st settlement")


def test_undo_road(page: Page, static_server):
    """Test undoing a road placement."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    # Place settlement and road
    page.locator("#board .vertex-hint").first.click()
    page.locator("#board .edge-hint").first.click(force=True)
    expect(page.locator("#currentPlayer")).to_have_text("Player 2 (Blue)")

    # Undo road
    page.locator("#undoBtn").click()
    expect(page.locator("#currentPlayer")).to_have_text("Player 1 (Red)")
    expect(page.locator("#phaseInfo")).to_have_text("Place a road")


def test_undo_disabled_initially(page: Page, static_server):
    """Test that undo is disabled when no actions taken."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")
    expect(page.locator("#undoBtn")).to_be_disabled()


def test_new_board_no_confirm_when_empty(page: Page, static_server):
    """Test new board doesn't show confirmation when no placements."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    # Click new board - should not show modal
    page.locator("#newBoardBtn").click()

    # Modal should not be visible
    expect(page.locator("#confirmModal")).not_to_have_class("visible")


def test_new_board_confirms_when_placements_exist(page: Page, static_server):
    """Test new board shows confirmation when placements exist."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    # Place a settlement
    page.locator("#board .vertex-hint").first.click()

    # Click new board - should show modal
    page.locator("#newBoardBtn").click()
    expect(page.locator("#confirmModal")).to_have_class("modal-overlay visible")


def test_confirm_cancel_closes_modal(page: Page, static_server):
    """Test cancel button closes confirmation modal."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    page.locator("#board .vertex-hint").first.click()
    page.locator("#newBoardBtn").click()
    page.locator("#confirmCancel").click()

    expect(page.locator("#confirmModal")).not_to_have_class("visible")
    # Settlement should still exist
    expect(page.locator("#settlementCount")).to_have_text("1")


def test_confirm_yes_generates_new_board(page: Page, static_server):
    """Test confirming new board clears placements."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    page.locator("#board .vertex-hint").first.click()
    page.locator("#newBoardBtn").click()
    page.locator("#confirmYes").click()

    expect(page.locator("#confirmModal")).not_to_have_class("visible")
    expect(page.locator("#settlementCount")).to_have_text("0")
    expect(page.locator("#currentPlayer")).to_have_text("Player 1 (Red)")


def test_save_button_exists(page: Page, static_server):
    """Test save button is present."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")
    expect(page.locator("#saveBtn")).to_be_visible()
    expect(page.locator("#saveBtn")).to_have_text("Copy Board to Clipboard")


def test_load_modal_opens(page: Page, static_server):
    """Test load button opens modal."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")
    page.locator("#loadBtn").click()
    expect(page.locator("#loadModal")).to_have_class("modal-overlay visible")


def test_load_modal_cancel(page: Page, static_server):
    """Test load modal can be cancelled."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")
    page.locator("#loadBtn").click()
    page.locator("#loadCancel").click()
    expect(page.locator("#loadModal")).not_to_have_class("visible")


def test_snake_draft_order(page: Page, static_server):
    """Test the snake draft placement order (1-2-3-4-4-3-2-1)."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    expected_order = [
        ("Player 1 (Red)", "1st"),
        ("Player 2 (Blue)", "1st"),
        ("Player 3 (Orange)", "1st"),
        ("Player 4 (Green)", "1st"),
        ("Player 4 (Green)", "2nd"),
        ("Player 3 (Orange)", "2nd"),
        ("Player 2 (Blue)", "2nd"),
        ("Player 1 (Red)", "2nd"),
    ]

    for i, (player, placement) in enumerate(expected_order):
        expect(page.locator("#currentPlayer")).to_have_text(player)
        expect(page.locator("#phaseInfo")).to_contain_text(f"{placement} settlement")

        # Place settlement
        page.locator("#board .vertex-hint").first.click()
        expect(page.locator("#phaseInfo")).to_have_text("Place a road")

        # Place road - use force=True for thin SVG lines
        page.locator("#board .edge-hint").first.click(force=True)

    # After all placements, setup should be complete
    expect(page.locator("#currentPlayer")).to_have_text("Setup Complete!")


def test_board_visible_on_mobile(page: Page, static_server):
    """Test that the board is fully visible on mobile viewport without horizontal scrolling."""
    # Set mobile viewport (iPhone SE size)
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    # Get the board element
    board = page.locator("#board")
    expect(board).to_be_visible()

    # Get board bounding box
    board_box = board.bounding_box()
    assert board_box is not None, "Board should have a bounding box"

    # Board should fit within viewport width (375px)
    # Account for container padding (10px on each side = 20px total on mobile)
    assert board_box["width"] <= 375, (
        f"Board width ({board_box['width']}px) should fit within mobile viewport (375px)"
    )

    # Board's right edge should be within viewport
    assert board_box["x"] + board_box["width"] <= 375, (
        "Board should not extend beyond viewport width"
    )


def test_board_visible_on_small_mobile(page: Page, static_server):
    """Test board visibility on very small mobile viewport (320px width)."""
    # Set very small mobile viewport
    page.set_viewport_size({"width": 320, "height": 568})
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    board = page.locator("#board")
    expect(board).to_be_visible()

    board_box = board.bounding_box()
    assert board_box is not None, "Board should have a bounding box"

    # Board should scale down to fit 320px viewport
    assert board_box["width"] <= 320, (
        f"Board width ({board_box['width']}px) should fit within small mobile viewport (320px)"
    )


def test_skip_roads_toggle_exists(page: Page, static_server):
    """Test that the skip roads toggle exists."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")
    expect(page.locator("#skipRoadsToggle")).to_be_visible()


def test_skip_roads_toggle_skips_road_phase(page: Page, static_server):
    """Test that enabling skip roads toggle skips road placement phase."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    # Enable skip roads toggle
    page.locator("#skipRoadsToggle").check()

    # Place settlement
    page.locator("#board .vertex-hint").first.click()

    # Should skip road phase and go directly to Player 2
    expect(page.locator("#currentPlayer")).to_have_text("Player 2 (Blue)")
    expect(page.locator("#phaseInfo")).to_have_text("Place 1st settlement")
    expect(page.locator("#roadCount")).to_have_text("0")


def test_skip_roads_toggle_full_draft(page: Page, static_server):
    """Test skip roads toggle allows completing full draft without roads."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    # Enable skip roads toggle
    page.locator("#skipRoadsToggle").check()

    expected_players = [
        "Player 1 (Red)",
        "Player 2 (Blue)",
        "Player 3 (Orange)",
        "Player 4 (Green)",
        "Player 4 (Green)",
        "Player 3 (Orange)",
        "Player 2 (Blue)",
        "Player 1 (Red)",
    ]

    for player in expected_players:
        expect(page.locator("#currentPlayer")).to_have_text(player)
        page.locator("#board .vertex-hint").first.click()

    # After all placements, setup should be complete
    expect(page.locator("#currentPlayer")).to_have_text("Setup Complete!")
    expect(page.locator("#settlementCount")).to_have_text("8")
    expect(page.locator("#roadCount")).to_have_text("0")


def test_board_validation_six_eight_not_adjacent(page: Page, static_server):
    """Test that 6 and 8 are never adjacent on the generated board."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    # Check board validation via JavaScript
    result = page.evaluate("""
        () => {
            // Get all pairs of adjacent hexes with numbers
            for (let i = 0; i < gameState.hexes.length; i++) {
                const hex = gameState.hexes[i];
                if (hex.number === null) continue;

                const adjacentIndices = getAdjacentHexIndices(i, gameState.hexes);
                for (const adjIndex of adjacentIndices) {
                    const adjHex = gameState.hexes[adjIndex];
                    if (adjHex.number === null) continue;

                    // Check if 6 and 8 are adjacent
                    if ((hex.number === 6 && adjHex.number === 8) ||
                        (hex.number === 8 && adjHex.number === 6)) {
                        return { valid: false, error: `6 and 8 are adjacent at hexes ${i} and ${adjIndex}` };
                    }
                }
            }
            return { valid: true };
        }
    """)
    assert result["valid"], result.get("error", "Unknown validation error")


def test_board_validation_same_numbers_not_adjacent(page: Page, static_server):
    """Test that same numbers are never adjacent on the generated board."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    result = page.evaluate("""
        () => {
            for (let i = 0; i < gameState.hexes.length; i++) {
                const hex = gameState.hexes[i];
                if (hex.number === null) continue;

                const adjacentIndices = getAdjacentHexIndices(i, gameState.hexes);
                for (const adjIndex of adjacentIndices) {
                    const adjHex = gameState.hexes[adjIndex];
                    if (adjHex.number === null) continue;

                    // Check if same numbers are adjacent
                    if (hex.number === adjHex.number) {
                        return { valid: false, error: `Same number ${hex.number} at adjacent hexes ${i} and ${adjIndex}` };
                    }
                }
            }
            return { valid: true };
        }
    """)
    assert result["valid"], result.get("error", "Unknown validation error")


def test_board_validation_no_13_pips_vertex(page: Page, static_server):
    """Test that no vertex has 13 or more pips."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    result = page.evaluate("""
        () => {
            const vertexMap = getVerticesWithAdjacentHexes(gameState.hexes);

            for (const [key, hexIndices] of vertexMap) {
                let totalPips = 0;
                const numbers = [];

                for (const hexIndex of hexIndices) {
                    const hex = gameState.hexes[hexIndex];
                    if (hex.number !== null) {
                        totalPips += NUMBER_PROBABILITY[hex.number] || 0;
                        numbers.push(hex.number);
                    }
                }

                if (totalPips >= 13) {
                    return { valid: false, error: `Vertex ${key} has ${totalPips} pips (numbers: ${numbers.join(', ')})` };
                }
            }
            return { valid: true };
        }
    """)
    assert result["valid"], result.get("error", "Unknown validation error")


def test_board_validation_multiple_boards(page: Page, static_server):
    """Test that multiple board generations all pass validation."""
    page.goto("http://127.0.0.1:8123/catan-practice.html")

    # Generate and validate 10 boards
    for i in range(10):
        page.locator("#newBoardBtn").click()

        # Check all validation rules
        result = page.evaluate("""
            () => {
                return isValidBoard(gameState.hexes);
            }
        """)
        assert result, f"Board {i + 1} failed validation"
