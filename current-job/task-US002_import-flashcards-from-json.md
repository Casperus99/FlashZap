## Description

This task list is generated based on the user story: US002: Import Flashcards from JSON. It is structured to follow a Test-Driven Development (TDD) workflow, where test cases are defined as sub-tasks.

### Notes

- The implementation should provide clear, user-friendly error messages for each failure scenario outlined in the acceptance criteria.
- The import process should fail on the first invalid record encountered in the JSON file.
- Business logic should be developed in `src/flash_zap/services`, models in `src/flash_zap/models`, and tests in `tests/`.
- **Testing Database:** The test suite will be configured to use an in-memory SQLite database for speed and isolation. No external PostgreSQL database setup is required to run the tests.

## Tasks

- [x] 1.0 Update Main Menu TUI
  > **Note:** Modify `src/flash_zap/tui/main_menu.py`. Update the `menu_items` list to include an "Import from JSON" option. Add a new handler method, e.g., `_handle_import_json`, that will be called when this option is selected.
  - [x] 1.1 `test_main_menu_has_import_option`: Write a test to assert that "Import from JSON" is present in the main menu options.
  - [x] 1.2 `test_main_menu_import_calls_handler`: Write a test to ensure that selecting the "Import from JSON" option triggers the correct import handler/service function.

- [ ] 2.0 Implement Data Validation and Parsing Logic
  > **Note:** Create a new file `src/flash_zap/services/import_service.py`. Inside this file, implement a private function like `_parse_and_validate_file(file_path)`. This function will be responsible for opening, reading, and performing all validations on the JSON data. Consider creating a new `src/flash_zap/core/exceptions.py` to define custom exceptions like `InvalidJsonError` or `ValidationError` to be raised by this function.
  - [x] 2.1 `test_import_valid_json_returns_data`: Write a test that provides a path to a valid JSON file and asserts that the function returns the expected list of dictionaries.
  - [x] 2.2 `test_import_raises_error_if_file_not_found`: Write a test that asserts a specific `FileNotFoundError` or custom exception is raised when the JSON file path is invalid.
  - [x] 2.3 `test_import_raises_error_for_malformed_json`: Write a test that asserts a specific `InvalidFileError` or custom exception is raised for a file with malformed JSON.
  - [x] 2.4 `test_import_raises_error_if_json_not_a_list`: Write a test that asserts a specific `ValidationError` is raised if the JSON's root element is not a list.
  - [x] 2.5 `test_import_raises_error_for_missing_keys`: Write a test that asserts a `ValidationError` is raised if a dictionary in the list is missing a "front" or "back" key.
  - [x] 2.6 `test_import_raises_error_for_content_too_long`: Write a test that asserts a `ValidationError` is raised if a "front" or "back" value exceeds 200 characters.

- [ ] 3.0 Implement Database Interaction
  > **Note:** Create a new file `src/flash_zap/models/card.py` to define the `Card` data model/class. Then, in `src/flash_zap/services/import_service.py`, implement a new private function like `_save_cards_to_db(cards_data)` that takes the validated list of card dictionaries and persists them to the database.
  - [x] 3.1 `test_card_model_can_be_created`: Write a test to create an instance of the `Card` model and verify its attributes.
  - [x] 3.2 `test_save_cards_to_database`: Write a test for a service function that takes a list of valid card data, saves it to a test database, and confirms the records were created.

- [ ] 4.0 Integrate Components and Finalize User Flow
  > **Note:** In `src/flash_zap/services/import_service.py`, create the main public function, e.g., `import_cards_from_json()`. This function will prompt the user for a file path, call the private validation and database functions, and handle all exceptions to print user-friendly success or error messages to the console. The `_handle_import_json` method in `main_menu.py` will call this public service function.
  - [x] 4.1 `test_full_import_flow_success`: Write an integration test that mocks user input for the file path and verifies that the correct success message (including card count) is printed to the console.
  - [x] 4.2 `test_full_import_flow_shows_file_not_found_error`: Write an integration test that mocks a non-existent path and verifies the correct "File not found" error message is printed.
  - [x] 4.3 `test_full_import_flow_shows_invalid_format_error`: Write an integration test with a malformed JSON file and verify the correct "Invalid JSON format" error message is printed.
  - [x] 4.4 `test_full_import_flow_shows_missing_key_error`: Write an integration test with a file containing a record with a missing key and verify the correct "Invalid record" error message is printed.
  - [x] 4.5 `test_full_import_flow_shows_content_too_long_error`: Write an integration test with a file containing a record with content exceeding the length limit and verify the correct "Card content exceeds limit" error message is printed. 