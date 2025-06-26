# US001: Main Menu Navigation

**As a:** User
**I want to:** See a main menu with clear options when I start the application
**So that:** I can easily navigate and choose what I want to do.

## Acceptance Criteria

```gherkin
Feature: Application Main Menu

  Scenario: Application starts and displays the main menu
    Given the application has been launched in the terminal
    When the application is ready
    Then I should see a clear list of options displayed on the screen
    And the list must include "Review Cards"
    And the list must include "Import Flashcards"
    And the list must include "Quit"

  Scenario: User selects a valid option from the menu
    Given the main menu is displayed
    When I select the "Import Flashcards" option
    Then the application should proceed to the card import workflow (as defined in US002)

  Scenario: User quits the application from the menu
    Given the main menu is displayed
    When I select the "Quit" option
    Then the application should terminate cleanly.

  Scenario: User provides invalid input at the menu
    Given the main menu is displayed
    When I enter an input that does not correspond to a valid option
    Then I should see an error message, such as "Invalid option, please try again."
    And the main menu should be displayed again with all the original options.
```

## Details & Notes

*   **Related PRD Epic:** This story supports all epics by providing the entry point to their functions.
*   **Related PRD Goal(s):** 2.3 Performance (the menu itself must be responsive).
*   **Dependencies:** None. This is a foundational story.
*   **UI/UX Considerations:** This will be a simple, text-based menu. Options could be selected by number (e.g., "1. Review Cards") or by typing the command.