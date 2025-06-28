## Description

This task list is generated based on the user story: US001: Display Main Menu and Select Option.

### Notes

- The interaction model must be immediate. The application should react directly to a single keypress (e.g., '1', '2') without requiring the user to press Enter. This requires capturing raw key events, not line-buffered input.
- The features this menu links to (Reviewing Cards, Importing) will be defined in separate user stories. For this task, create placeholder functions that are called upon selection.

## Tasks

- [x] 1.0 Parent Task: Display Main Menu on Application Start
  - **Note:** Create a new `tui` subpackage `src/flash_zap/tui/` with a `main_menu.py` file. This file will contain a `display_main_menu` function responsible for rendering the static menu interface.
  - [x] 1.1 Launching the application displays a title: "--- FlashZap Main Menu ---".
  - [x] 1.2 The menu displays option: "1. Review Due Cards".
  - [x] 1.3 The menu displays option: "2. Import Flashcards from JSON".
  - [x] 1.4 The menu displays option: "3. Exit".
  - [x] 1.5 The menu displays a prompt: "Select an option (1-3)".
- [x] 2.0 Parent Task: Handle Valid Menu Navigation 
  - **Note:** In `src/flash_zap/tui/main_menu.py`, a new `handle_menu_input` function will be created. It will listen for keypresses and call the appropriate placeholder functions based on valid input.
  - [x] 2.1 Pressing "1" navigates to the (placeholder) "Review Session" flow.
  - [x] 2.2 Pressing "2" navigates to the (placeholder) "Import" flow.
- [x] 3.0 Parent Task: Handle Application Exit
  - **Note:** The `handle_menu_input` function in `src/flash_zap/tui/main_menu.py` will include logic to exit the application loop when the '3' key is pressed.
  - [x] 3.1 Pressing "3" terminates the application gracefully and returns to the command prompt.
- [x] 4.0 Parent Task: Handle Invalid User Input
  - **Note:** The `handle_menu_input` function in `src/flash_zap/tui/main_menu.py` will ignore any keypresses that are not '1', '2', or '3', ensuring the menu display remains unchanged.
  - [x] 4.1 Pressing an invalid number (e.g., "5") is ignored and the menu remains displayed.
  - [x] 4.2 Pressing an invalid letter (e.g., "a") is ignored and the menu remains displayed.
  - [x] 4.3 Pressing a special key (e.g., "Arrow Up") is ignored and the menu remains displayed.
- [ ] 5.0 Parent Task: Technical Implementation and Setup
  - **Note:** Modify `src/flash_zap/main.py` and `src/flash_zap/__main__.py` to call the menu display and handling functions from `src/flash_zap/tui/main_menu.py`.
  - [x] 5.1 Configure the project's entry point to launch the main menu interface.
  - [x] 5.2 Select and integrate a TUI library that supports capturing raw keypress events.