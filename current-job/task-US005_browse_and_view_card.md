## Description

This task list is generated based on the user story: [US005: Browse and View a Specific Flashcard](./docs/user-stories/card-lifecycle-management/US005_browse_and_view_card.md).

### Notes

- This feature will be read-only.
- Focus on clear user interaction and error messages.

## Tasks

- [ ] 1.0 Update Main Menu UI
  - **Note:** Modify `src/flash_zap/tui/main_menu.py`. Update the `show` method to include "Browse Cards" as a menu choice and adjust the selection logic to handle this new option.
  - [x] 1.1 In `src/flash_zap/tui/main_menu.py`, add a "Browse Cards" option to the menu.
  - [x] 1.2 Ensure the new option is handled in the menu's logic to call the browsing functionality.
- [ ] 2.0 Create Card Display View
  - **Note:** Create a new file `src/flash_zap/tui/browse_view.py`. Implement a new function `show_card_view(session)` that will prompt the user for a card ID, display the card details, and wait for a key press.
  - [x] 2.1 Create a new file `src/flash_zap/tui/browse_view.py`.
  - [x] 2.2 Implement a function `show_card_view(session)` in `browse_view.py`.
  - [x] 2.3 `show_card_view()` should prompt the user for a card ID.
  - [x] 2.4 It should display the card's front, back, mastery level, and next review date.
  - [x] 2.5 The view must wait for a key press before returning.
- [ ] 3.0 Implement Card Retrieval Logic
  - **Note:** Create `src/flash_zap/core/card_manager.py` with a function `get_card_by_id(session, card_id)`. This function will be responsible for fetching a single card from the database by its ID.
  - [x] 3.1 Create a new file `src/flash_zap/core/card_manager.py`.
  - [x] 3.2 In `card_manager.py`, create a function `get_card_by_id(session, card_id)`.
  - [x] 3.3 This function should query the database for a card with the given `card_id`. It should return the card object or `None` if not found.
- [ ] 4.0 Integrate into Application Flow
  - **Note:** Modify the main application loop in `src/flash_zap/main.py` to call `show_card_view` upon user selection. In `src/flash_zap/tui/browse_view.py`, import and use the `get_card_by_id` function to retrieve card data.
  - [x] 4.1 In `src/flash_zap/main.py`, modify the main loop to call `show_card_view()` when the user selects "Browse Cards", passing the database session.
  - [x] 4.2 In `src/flash_zap/tui/browse_view.py`, import and call `get_card_by_id` from `card_manager`.
- [ ] 5.0 Implement Error Handling
  - **Note:** Enhance `show_card_view` in `src/flash_zap/tui/browse_view.py` to handle potential errors, such as invalid user input for the card ID (`ValueError`) or a card not being found in the database.
  - [x] 5.1 In `show_card_view()`, add a `try-except` block to handle `ValueError` if the user enters a non-integer ID. Show an error message.
  - [x] 5.2 If `get_card_by_id()` returns `None`, `show_card_view()` should display a "Card not found" message.
  - [x] 5.3 After showing an error, the function should exit, returning the user to the main menu. 