# US001: Display Main Menu and Select Option

**As a:** User
**I want to:** see a main menu with numbered options when I start the application
**So that:** I can quickly navigate to the core functions like reviewing cards or importing new ones.

## Acceptance Criteria

```gherkin
Feature: Main Menu Navigation

  Scenario: Application starts and displays the main menu
    Given I have launched the FlashZap application in my terminal
    When the application is ready
    Then I should see a clear title like "--- FlashZap Main Menu ---"
    And I should see a numbered list of options including:
      | number | option                       |
      | 1      | Review Due Cards             |
      | 2      | Import Flashcards from JSON  |
      | 3      | Exit                         |
    And I should see a prompt indicating how to select an option, like "Select an option (1-3)"

  Scenario: User selects a valid navigation option (e.g., Review)
    Given I am viewing the main menu
    When I press the "1" key
    Then the application should immediately navigate to the "Review Session" flow

  Scenario: User selects the exit option
    Given I am viewing the main menu
    When I press the "3" key
    Then the application should terminate gracefully
    And I should be returned to my terminal's command prompt.

  Scenario: User presses an invalid key
    Given I am viewing the main menu
    When I press a key that does not correspond to a valid option (e.g., "5", "a", "Arrow Up")
    Then the application should ignore the keypress
    And the main menu display should remain unchanged
    And the application should continue to wait for a valid keypress (1, 2, or 3).

```

## Details & Notes

*   **Related PRD Epic:**
    *   Card Lifecycle Management
    *   AI-Powered Learning Session
*   **Dependencies:** None. This is a foundational story.
*   **UI/UX Considerations:**
    *   As a Terminal User Interface (TUI), the menu must be text-based, clear, and uncluttered.
    *   The interaction model must be immediate. The application should react directly to a single keypress (e.g., '1', '2') without requiring the user to press Enter. This requires capturing raw key events, not line-buffered input.
*   **Performance/Scalability:**
    *   Per the PRD's non-functional requirements, this menu interaction must feel instantaneous (render in < 100ms).
*   **Notes:**
    *   This story is only for creating and handling the navigation of the main menu. The features it links to (Reviewing Cards, Importing) will be defined in separate user stories.