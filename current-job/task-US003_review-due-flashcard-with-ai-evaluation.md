## Description

This task list is generated based on the user story: US003: Review a Due Flashcard with AI Evaluation. It is structured to follow a Test-Driven Development (TDD) workflow, where test cases are defined as sub-tasks.

### Notes

- The AI service for grading will be Google Gemini.
- The definition of a "due card" for this task is simplified: any card that has not yet been reviewed in the current session.
- API keys will be managed via a `.env` file and loaded in `src/flash_zap/config.py`.

## Tasks

- [ ] 1.0 Configure Project for Gemini API
  > **Note:** This involves setting up dependencies and configuration for the AI service.
  > 
  > **Implementation Details:**
  > - **Modify:** `pyproject.toml` to add `google-generativeai` and `python-dotenv`.
  > - **Modify:** `src/flash_zap/config.py` to add a `Settings` class that loads `GEMINI_API_KEY` from environment variables.
  > - **Create:** `.env.example` and add `.env` to `.gitignore`.
  > - **Create:** `tests/test_config.py` to test the new configuration logic.
  - [x] 1.1 `test_config_loads_gemini_api_key`: Write a test in a new `tests/test_config.py` to ensure that `config.py` correctly loads the `GEMINI_API_KEY` from mocked environment variables.
  - [x] 1.2 Manually add `google-generativeai` and `python-dotenv` to `pyproject.toml`.
  - [x] 1.3 Manually create a `.env.example` file and add `.env` to `.gitignore`.

- [x] 2.0 Develop AI Grading Service
  > **Note:** Create a new file `src/flash_zap/services/ai_grader.py` and its corresponding test file `tests/test_services/test_ai_grader.py`. Define a custom exception like `AIGraderError` in `src/flash_zap/core/exceptions.py`.
  >
  > **Implementation Details:**
  > - **Modify:** `src/flash_zap/core/exceptions.py` to add a new `AIGraderError` class.
  > - **Create:** `src/flash_zap/services/ai_grader.py`. It will contain a `grade_answer(user_answer: str, correct_answer: str)` function that prompts the Gemini API, parses the result into "Correct"/"Incorrect" and feedback, and raises `AIGraderError` on API failure.
  > - **Create:** `tests/test_services/test_ai_grader.py` to test the new service.
  - [x] 2.1 `test_grade_answer_returns_correct_for_positive_ai_response`: Write a test that mocks the Gemini client to return a "Correct" evaluation and asserts that the `grade_answer` function returns a `("Correct", "feedback_text")` tuple.
  - [x] 2.2 `test_grade_answer_returns_incorrect_for_negative_ai_response`: Write a test that mocks the Gemini client to return an "Incorrect" evaluation and asserts that the `grade_answer` function returns an `("Incorrect", "feedback_text")` tuple.
  - [x] 2.3 `test_grade_answer_raises_custom_exception_on_api_failure`: Write a test that mocks the Gemini client to raise an API error and asserts that the `grade_answer` function catches it and raises a custom `AIGraderError`.

- [x] 3.0 Implement Core Review Session Logic
  > **Note:** Create a new file `src/flash_zap/core/review_session.py` and its test file `tests/test_core/test_review_session.py`. This will manage the state of a single review session.
  >
  > **Implementation Details:**
  > - **Create:** `src/flash_zap/core/review_session.py`. It will contain a `ReviewSession` class.
  > - **Add:** A method `get_next_card() -> Card | None` to fetch one unseen card at a time from the database for the current session.
  > - **Add:** A method `process_answer(card: Card, user_answer: str)` that calls the `ai_grader` service.
  > - **Create:** `tests/test_core/test_review_session.py` to test the session logic.
  - [x] 3.1 `test_get_next_card_returns_unseen_card`: Write a test with a seeded test database that asserts the function returns the first card, and when called again, returns the second card.
  - [x] 3.2 `test_get_next_card_returns_none_when_all_cards_are_seen`: Write a test that asserts `get_next_card` returns `None` after all available cards in the test database have been fetched once within the session.
  - [x] 3.3 `test_review_session_calls_ai_grader_service`: Write an integration test for the session logic that mocks the `ai_grader.grade_answer` function and asserts it is called with the correct arguments when a review is processed.

- [x] 4.0 Develop TUI for Review Session
  > **Note:** Create `src/flash_zap/tui/review_view.py` and `tests/test_tui/test_review_view.py`. These tests will likely involve mocking `rich.console` or capturing printed output.
  >
  > **Implementation Details:**
  > - **Create:** `src/flash_zap/tui/review_view.py`.
  > - **Add:** A main function `start_review_session()` that orchestrates the TUI flow. It will initialize the `ReviewSession`, loop to display cards, get user input, show a loading state, and then display the results from the `ai_grader` or handle any errors.
  > - **Create:** `tests/test_tui/test_review_view.py`.
  - [x] 4.1 `test_review_view_displays_card_front`: Write a test to check if the TUI correctly prints the "front" text of a given card.
  - [x] 4.2 `test_review_view_shows_loading_indicator`: Write a test to ensure a "Grading..." message is printed after an answer is submitted but before the result is ready.
  - [x] 4.3 `test_review_view_displays_grade_and_feedback`: Write a test that provides a mocked AI grade and feedback and asserts they are correctly printed to the console.
  - [x] 4.4 `test_review_view_displays_no_cards_due_message`: Write a test for the scenario where the review session starts with no due cards and assert the correct "Great job! No cards are due for review." message is printed.
  - [x] 4.5 `test_review_view_displays_service_error_message`: Write a test where the AI grader service is mocked to raise an `AIGraderError` and assert the corresponding "Sorry, the AI grading service is currently unavailable." message is printed.

- [x] 5.0 Integrate Review Session into Main Application
  > **Note:** This involves connecting the main menu to the new review session flow.
  >
  > **Implementation Details:**
  > - **Modify:** `src/flash_zap/tui/main_menu.py`.
  > - **Update:** The handler method for the "Review Due Cards" option (e.g., `_handle_review_cards`) to call the `start_review_session()` function from the new `review_view.py`.
  - [x] 5.1 `test_main_menu_review_option_starts_review_session`: In `tests/test_tui/test_main_menu.py`, write a test that mocks the `review_view` and asserts it is called when the user selects the "Review Due Cards" option. 