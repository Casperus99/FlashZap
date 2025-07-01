# Contributing to FlashZap

First off, thank you for considering contributing to FlashZap! This document provides a guide to help you get started.

## Architecture Overview

FlashZap follows a standard Python application structure. Understanding the key components will help you navigate the codebase.

*   **Database ORM**: We use `SQLAlchemy 2.0`. All database models are defined in `src/flash_zap/models/`. The base declarative model that all others inherit from is in `src/flash_zap/models/base.py`.
*   **Database Migrations**: Database schema changes are managed by `Alembic`. The main configuration is in `alembic.ini`, and the environment setup (which defines how to connect to the database and find the models) is in `alembic/env.py`. Migration scripts are stored in `alembic/versions/`.
*   **Core Logic**: Business logic is encapsulated in services located in `src/flash_zap/services/` and core session management in `src/flash_zap/core/`.
*   **User Interface**: This is a Terminal User Interface (TUI) application. The views and TUI-specific logic are located in `src/flash_zap/tui/`.
*   **Configuration**: Application settings are managed using `pydantic-settings` and are defined in `src/flash_zap/config.py`. Local environment variables can be used to override the defaults.
*   **Logging**: The application uses Python's built-in `logging` module. The main setup is handled by the `setup_logging()` function in `src/flash_zap/logger.py`, which is called once when the application starts in `src/flash_zap/main.py`. Configuration, such as the log level and log file path (`flash_zap.log` by default), is managed in `src/flash_zap/config.py`. To add logging to a module, simply `import logging` and use the module-level logger (e.g., `logging.info("My log message")`).

## Development Workflow

We follow a Test-Driven Development (TDD) workflow. When adding a new feature or fixing a bug, please follow these steps:

1.  **Write a Failing Test (RED)**: Add a new test case to the appropriate file in the `tests/` directory that reproduces the bug or defines the new feature. Run `pytest` and verify that the new test fails for the expected reason.
2.  **Write Minimal Code to Pass (GREEN)**: Write the simplest possible implementation in the application code (`src/flash_zap/`) to make the test pass.
3.  **Refactor**: Improve and clean up the implementation code now that you have a passing test as a safety net.

## Making Database Schema Changes

This is a critical workflow. Because we use Alembic to manage the database schema, you must follow these steps whenever you make a change to a model in `src/flash_zap/models/` that affects the database.

1.  **Update the Model**: Make your changes to the model class (e.g., add or modify a `Column`).
2.  **Generate Migration Script**: Run the following command to have Alembic automatically generate a new migration script.
    ```bash
    alembic revision --autogenerate -m "A short, descriptive message about the change"
    ```
3.  **Verify the Script**: **This is a crucial step.** Open the newly generated file in `alembic/versions/` and ensure the `upgrade()` and `downgrade()` functions are correct. The autogenerator is a great tool, but it's not infallible.
4.  **Apply the Migration**: Run the migration to update the database schema.
    ```bash
    alembic upgrade head
    ```

## Running the Application

To run the FlashZap application, execute the following command from the project root:

```bash
flash_zap
```

## Running Tests

To run the full test suite, execute the following command from the project root:

```bash
pytest
``` 