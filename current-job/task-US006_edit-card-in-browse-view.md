## Description

This task list is generated based on the user story: US006_edit-card-in-browse-view.

### Notes

- The new edit menu should appear after the user finds a card by its ID in the "Browse Cards" view.
- Implementation will require creating new methods in `card_manager.py` for updating card attributes and modifying `browse_view.py` to handle the user interaction for editing.

## Tasks

- [ ] 1.0 Modify `card_manager` to Support Card Updates
  - **File to modify:** `src/flash_zap/core/card_manager.py`
  - **Methods to add:**
    - `update_card_front(session, card_id, new_front)`: Finds a card by its ID and updates the `front` attribute with the new text.
    - `update_card_back(session, card_id, new_back)`: Finds a card by its ID and updates the `back` attribute with the new text.
    - `update_card_mastery(session, card_id, new_mastery_level)`: Finds a card by its ID and updates the `mastery_level`, but only if the new level is less than or equal to the current level.
  - [x] 1.1 Implement `update_card_front(card_id, new_front)` to modify a card's front text.
  - [x] 1.2 Implement `update_card_back(card_id, new_back)` to modify a card's back text.
  - [x] 1.3 Implement `update_card_mastery(card_id, new_mastery_level)` to change a card's mastery level, ensuring the new level cannot be higher than the old one.

- [ ] 2.0 Implement Edit Menu and UI Logic in `browse_view.py`
  - **File to modify:** `src/flash_zap/tui/browse_view.py`
  - **Method to modify:** `display_browse_view(session)`
  - **High-level changes:**
    - After fetching and displaying the card, instead of returning immediately, the function should display a new menu with edit options.
    - It should prompt the user for a choice (1-4).
    - Based on the choice, it should call the corresponding new methods from `card_manager.py`.
    - It needs to handle user input for the new front/back text or mastery level, including input validation.
  - [x] 2.1 After displaying card details, present a new menu with options: "1. Edit front", "2. Edit back", "3. Lower mastery level", "4. Cancel".
  - [x] 2.2 Handle "Edit front" option: prompt for new text, call the update method, and show a confirmation message.
  - [x] 2.3 Handle "Edit back" option: prompt for new text, call the update method, and show a confirmation message.
  - [x] 2.4 Handle "Lower mastery level" option: prompt for a new level, validate that it is a number and not higher than the current level, call the update method, and show a confirmation.
  - [x] 2.5 Handle "Cancel" option: exit the browse view and return to the main menu.
  - [x] 2.6 Display clear error messages for invalid inputs (e.g., non-numeric mastery level).

- [ ] 3.0 Update Documentation
  - **File to modify:** `docs/USER_MANUAL.md`
  - **Section to update:** `3.4. Browse and View a Specific Flashcard`
  - **High-level changes:**
    - Add a description of the new edit menu that appears after a card is viewed.
    - Explain each option: "Edit front," "Edit back," and "Lower mastery level."
    - Describe how to use each editing feature.
  - [x] 3.1 Update the "Browse and View a Specific Flashcard" section in `docs/USER_MANUAL.md` to reflect the new editing capabilities.