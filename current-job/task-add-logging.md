# Task: Add Comprehensive Logging

**User Story:** As a developer, I want comprehensive logging throughout the application so that I can easily debug issues, monitor application behavior, and track user interactions.

## Task Breakdown

### 1. Configure the Logging Framework
-   **Goal:** Set up a centralized logging configuration.
-   **File to modify:** `src/flash_zap/config.py`
-   **Details:**
    -   Use Python's built-in `logging` module.
    -   Add a new Pydantic settings class for logging configuration (e.g., `LoggingSettings`).
    -   Define configuration options for log level (e.g., `DEBUG`, `INFO`, `WARNING`, `ERROR`), log file path, and log format.
    -   The default log file should be `flash_zap.log` in the project root.
    -   The format should include a timestamp, log level, module name, and the message.

### 2. Initialize the Logger
-   **Goal:** Initialize the logger when the application starts.
-   **File to create/modify:** `src/flash_zap/logger.py` (new file) and `src/flash_zap/main.py`.
-   **Details:**
    -   Create a new module `src/flash_zap/logger.py` to encapsulate logging setup.
    -   This module will have a function like `setup_logging()` that reads the configuration from `config.py` and configures the root logger.
    -   Call `setup_logging()` in `src/flash_zap/main.py` before any other application logic runs.

### 3. Add Logging to Application Entry Point and Main Menu
-   **Goal:** Log the start and end of the application and main menu interactions.
-   **Files to modify:** `src/flash_zap/main.py`, `src/flash_zap/tui/main_menu.py`.
-   **Details:**
    -   In `main.py`, log the application starting and stopping.
    -   In `main_menu.py`, log which menu option the user selects.

### 4. Add Logging to the Import Service
-   **Goal:** Log the process of importing flashcards.
-   **File to modify:** `src/flash_zap/services/import_service.py`.
-   **Details:**
    -   Log the start and end of the import process.
    -   Log the number of cards found in the JSON file.
    -   Log the number of cards successfully imported.
    -   Log any errors that occur during parsing or saving.

### 5. Add Logging to the Review Session
-   **Goal:** Log the key events within a review session.
-   **Files to modify:** `src/flash_zap/core/review_session.py`, `src/flash_zap/tui/review_view.py`.
-   **Details:**
    -   Log when a review session is started.
    -   Log when a card is presented to the user.
    -   Log the user's answer (or at least that an answer was submitted).
    -   Log the AI grader's response.
    -   Log when the session is finished.

### 6. Add Logging to the AI Grader and SRS Engine
-   **Goal:** Log interactions with the AI service and SRS calculations.
-   **File to modify:** `src/flash_zap/services/ai_grader.py`, `src/flash_zap/services/srs_engine.py`.
-   **Details:**
    -   In `ai_grader.py`, log the request being sent to the AI and the received response.
    -   In `srs_engine.py`, log the input for the SRS calculation (card, grade) and the calculated next review date and mastery level.

### 7. Add Logging for Database interactions
-   **Goal:** Log database session creation and queries.
-   **Details:**
    -   This might be more advanced. A good start is to log when a database session is created and closed. If `SQLAlchemy` is used, it has its own logging capabilities that can be configured to show queries. This should be investigated as part of this task. For now, manually logging before and after database-heavy operations is sufficient.

### 8. Review and Refine
-   **Goal:** Ensure logging is consistent and provides value.
-   **Details:**
    -   Run the application and perform all major actions (import, review).
    -   Inspect `flash_zap.log` to ensure the log messages are clear, informative, and at the correct levels.
    -   Refine log messages and levels as needed. 