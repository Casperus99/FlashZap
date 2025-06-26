# US006: Configure SRS Intervals via File

**As a:** User
**I want to:** Define my own sequence of SRS intervals in a configuration file
**So that:** I can customize the learning schedule to fit my personal pace and subject matter difficulty.

## Acceptance Criteria

```gherkin
Feature: SRS Interval Configuration

  Scenario: Application loads custom SRS intervals from a valid configuration file
    Given a configuration file exists at a predefined location (e.g., '~/.config/srs-app/config.json')
    And the file contains a valid list of numbers for SRS intervals, such as `{"srs_intervals_days": [1, 3, 7, 16, 35]}`
    When the application starts
    Then it must load this sequence of intervals into the SRS Engine
    And when a card is answered correctly (as in US005), the next interval must be chosen from this custom list.

  Scenario: Application uses default intervals when the configuration file is missing
    Given the configuration file does not exist at the predefined location
    When the application starts
    Then it must not crash
    And it must load a hardcoded, default list of SRS intervals (e.g., [1, 2, 4, 8, 16, 32])
    And it should proceed to function normally using these default values.

  Scenario: Application handles a malformed or invalid configuration file
    Given a configuration file exists but its content is not valid JSON or the 'srs_intervals_days' key contains invalid data (e.g., a string, an object)
    When the application starts
    Then it must not crash
    And it must log a clear warning to the console, such as "Warning: Could not parse SRS intervals from config file. Using default values."
    And it must fall back to using the hardcoded, default list of SRS intervals.
```

## Details & Notes

*   **Related PRD Epic:** Spaced Repetition System (SRS) Engine
*   **Related PRD Goal(s):** This feature directly supports the goal of creating a highly personalized and efficient learning tool.
*   **Dependencies:** The effect of this configuration is realized in `US005: Update Card SRS Data Post-Grading`.
*   **UI/UX Considerations:**
    *   There is no in-app UI for this feature. Configuration is handled by the user directly editing the file.
    *   The expected location and format of the configuration file must be clearly documented for the user (e.g., in a README).
*   **Integration:**
    *   Requires file system access to read the configuration file on startup.
*   **Testing & QA:**
    *   Test cases must cover:
        1.  App behavior with a valid config file.
        2.  App behavior with a missing config file (fallback to default).
        3.  App behavior with a syntactically incorrect JSON file.
        4.  App behavior with a semantically incorrect file (e.g., wrong data type for intervals).
*   **Note on Implementation:** The application should only read the configuration file once at startup to avoid performance overhead during the review session.