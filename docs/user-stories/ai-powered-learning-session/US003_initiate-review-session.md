# US003: Initiate Review Session and Display First Card

**As a:** User
**I want to:** Start a review session from the main menu
**So that:** I can be presented with the first flashcard that is due for study.

## Acceptance Criteria

```gherkin
Feature: Review Session Initiation

  Scenario: Successfully start a review session with due cards
    Given I have at least one card in the database where the 'next_review_at' date is today or in the past
    And I am at the main menu
    When I select the "Review Cards" option
    Then the application should query the database for all due cards
    And the terminal screen should clear
    And the 'front' text of the first due card should be displayed
    And an input prompt for my answer should be shown below the card's text.

  Scenario: Attempt to start a review session when no cards are due
    Given I have cards in the database, but none have a 'next_review_at' date of today or in the past
    And I am at the main menu
    When I select the "Review Cards" option
    Then I should see a message, such as "Great job! No cards are due for review today."
    And I should be returned to the main menu.

  Scenario: Attempt to start a review session with an empty database
    Given my flashcard database is empty
    And I am at the main menu
    When I select the "Review Cards" option
    Then I should see a message, such as "You have no cards yet. Try importing some first."
    And I should be returned to the main menu.
```

## Details & Notes

*   **Related PRD Epic:** AI-Powered Learning Session
*   **Related PRD Goal(s):**
    *   `2.1 Primary Goal`: This story is the entry point to the core learning habit.
    *   `2.2 Review Cadence`: This is the first step in being able to review cards.
*   **Dependencies:**
    *   `US001: Main Menu Navigation`: To have the menu option to select.
    *   `US002: Import Flashcards from JSON File`: To have cards in the database to review.
*   **UI/UX Considerations:**
    *   The review screen should be minimal to promote focus. Clearing the terminal window before showing the card is important.
    *   The "front" text of the card should be clearly delineated from the user input area.
*   **Performance/Scalability:**
    *   The query for due cards (`SELECT * FROM cards WHERE next_review_at <= NOW()`) must be efficient. A database index on the `next_review_at` column is required to ensure fast startup of the review session, even with thousands of cards.
*   **Testing & QA:**
    *   Requires a test database that can be set up in different states: empty, with cards but none due, with one due card, and with multiple due cards.
    *   The order in which due cards are presented should be deterministic for testing (e.g., ordered by `next_review_at` ascending).
*   **Integration:**
    *   This story requires a read connection to the PostgreSQL database.
    *   It does **not** yet involve the AI API. That interaction is out of scope for this story.