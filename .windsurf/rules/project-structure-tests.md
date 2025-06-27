---
trigger: manual
---

# Guidelines for Project Testing

## General Principles

1.  **Framework:** All tests **must** be written using the `pytest` framework. Leverage `pytest` features like fixtures for setup/teardown and its powerful assertion introspection.
2.  **Location:** All test code **must** reside in the root `tests/` directory, which is a sibling to the `src/` directory. No test files should ever be placed inside `src/`.
3.  **Structure Mirroring:** The directory structure within `tests/` **must** mirror the package structure inside `src/`. This makes it intuitive to locate the tests for any given application module. For example, tests for `src/my_app/core/srs_engine.py` should be in `tests/test_core/test_srs_engine.py`.
4.  **Isolation:** Tests **must** be completely independent and able to run in any order. No test shall depend on the state left by a previously run test. State should be managed exclusively by fixtures.
5.  **External Dependencies:**
    *   **Database:** All tests that interact with the database **must** use a separate, temporary test database, not the development or production database. The state of this database should be controlled by fixtures.
    *   **AI Service:** Any interaction with the external AI grading service **must** be mocked. Tests should never make real network calls to the AI API. This ensures tests are fast, reliable, and free of cost.
6.  **Test Naming:** Test files must follow the `test_*.py` pattern. Test functions must be prefixed with `test_`. This is required for `pytest` discovery.

## Testing Directory Structure and Instructions

The agent must create and maintain the following structure.

```
FlashZap/
└── tests/
    ├── __init__.py
    ├── conftest.py             # Shared fixtures for all tests
    │
    ├── test_core/              # Mirrors the 'core' sub-package in src
    │   ├── __init__.py
    │   └── ...
    │
    ├── test_db/                # Mirrors the 'db' sub-package in src
    │   ├── __init__.py
    │   └── ...
    │
    └── .../                    # Other test folders

```

### 1. `tests/conftest.py`

*   **Purpose:** To define fixtures that are shared across multiple test files. This is the central place for setting up test environments.
*   **What it should consist of:**
    *   A `pytest` fixture for managing a connection to the **test database**. This fixture should handle creating the connection, setting up the necessary tables, yielding the session to the test, and then tearing down/cleaning the database after the test completes.
    *   A `pytest` fixture that provides a **mocked AI client**. This client should mimic the real client's interface but return predictable, hard-coded responses without making network calls.
    *   Fixtures for creating temporary data, such as a temporary JSON file for testing the card import feature.
*   **Instruction to AI:**
    *   Create and maintain a `tests/conftest.py` file.
    *   Implement a `test_db_session` fixture that connects to a test PostgreSQL database, creates all schema (defined in `src/my_app/db/models.py`), and truncates all tables after each test to ensure isolation.
    *   Implement a `mock_ai_client` fixture using `unittest.mock` that can be configured to return specific grades and feedback for testing the learning session loop.

## Types of Tests and Instructions

The AI agent is responsible for creating these types of tests for the relevant parts of the application.

### 1. Unit Tests

*   **Purpose:** To test the smallest units of code (e.g., a single function or method) in complete isolation from the rest of the system (including the database and filesystem).
*   **What to test:**
    *   Logic within the `SRS Engine`: Given a card's history, does the algorithm calculate the next review date correctly?
    *   Utility functions: Does the JSON file parser correctly handle valid and invalid file formats?
*   **Instruction to AI:**
    *   Unit tests **must not** use the `test_db_session` fixture. If a function needs a database model object, it should be created in-memory and passed in directly.
    *   All dependencies must be mocked.

    *   **Example Unit Test (`tests/test_core/test_srs_engine.py`):**
        ```python
        from my_app.core.srs_engine import calculate_next_review

        def test_calculate_next_review_for_new_card():
            # GIVEN a new card with no review history
            # WHEN we calculate the next review date
            next_date = calculate_next_review(history=[], performance="good")
            # THEN the result should be the first interval in the SRS schedule
            assert next_date == ... # Expected outcome
        ```

### 2. Integration Tests

*   **Purpose:** To test how different components of the application work together. This is where you test interactions with the database.
*   **What to test:**
    *   **Card Lifecycle Management Epic:** Does the "Import Flashcards" feature correctly parse a JSON file and persist the cards in the (test) database?
    *   **AI-Powered Learning Session Epic:** Can the system retrieve a due card from the database, send its data to the **mocked** AI client, receive a grade, and correctly update the card's history in the database?
*   **Instruction to AI:**
    *   Integration tests **must** use the `test_db_session` fixture to interact with a real (but temporary) database.
    *   Integration tests **must** use the `mock_ai_client` fixture. They must not make real network calls.

    *   **Example Integration Test:**
        ```python
        from my_app.features import card_importer # Assumed module

        def test_import_cards_from_json(test_db_session, tmp_path):
            # GIVEN a valid JSON file with two cards
            json_content = '[{"front": "Q1", "back": "A1"}, {"front": "Q2", "back": "A2"}]'
            json_file = tmp_path / "cards.json"
            json_file.write_text(json_content)

            # WHEN the import function is called with the file path
            card_importer.import_from_file(str(json_file), test_db_session)

            # THEN two cards should exist in the database
            count = test_db_session.query(Card).count()
            assert count == 2
        ```

### 3. Functional / CLI Tests

*   **Purpose:** To test the application from the end user's perspective by running the CLI and asserting its behavior (prompts, output, exit codes).
*   **What to test:**
    *   Running the main menu and selecting an option.
    *   Simulating a full review session: starting the session, answering a prompt, seeing the feedback, and moving to the next card.
    *   Testing the import command-line flow.
*   **Instruction to AI:**
    *   Use a library like `pytest-subprocess` or the built-in `subprocess` module to execute the CLI application.
    *   The test should provide input to `stdin` and capture `stdout` and `stderr` to check for expected prompts and messages.
    *   These tests will orchestrate components, so they will likely use both the `test_db_session` and `mock_ai_client` fixtures to control the environment the CLI runs in.

## Final Check for AI Agent

*   After writing tests, verify the following:
*   Does the `tests/` directory structure accurately mirror `src/my_app/`?
*   Are all external services (AI) and stateful resources (DB) managed through `pytest` fixtures from `conftest.py`?
*   Are tests properly categorized? (e.g., unit tests are isolated, integration tests use the test DB).
*   Are test names clear and descriptive of what they are testing?