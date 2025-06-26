# US005: Update Card SRS Data Based on AI Grade

**As a:** User
**I want to:** Have the card's review schedule automatically updated based on the AI's grade
**So that:** The Spaced Repetition System can correctly schedule the card for my next review, optimizing my learning.

## Acceptance Criteria

```gherkin
Feature: SRS Data Update

  Scenario: Card's SRS interval is advanced after a correct answer
    Given I am in a review session and have just answered a card
    And the AI service has graded my answer as "correct"
    And the card's current SRS interval is '3 days'
    And the next configured SRS interval is '7 days'
    When I acknowledge the AI's feedback to continue
    Then the application must update the card's record in the database
    And the card's 'current_interval' must be set to '7 days'
    And the card's 'next_review_at' timestamp must be set to approximately 7 days from now
    And the application proceeds to the next due card.

  Scenario: Card's SRS interval is reset after an incorrect answer
    Given I am in a review session and have just answered a card
    And the AI service has graded my answer as "incorrect"
    And the first configured SRS interval is '1 day'
    When I acknowledge the AI's feedback to continue
    Then the application must update the card's record in the database
    And the card's 'current_interval' must be reset to '1 day'
    And the card's 'next_review_at' timestamp must be set to approximately 1 day from now
    And the application proceeds to the next due card.

  Scenario: Card's SRS data is not updated if AI grading fails
    Given I am in a review session
    And the AI grading process failed due to a network or API key error
    When I acknowledge the error message to continue
    Then the application must not perform any write operations to the database for that card
    And the card's original 'current_interval' and 'next_review_at' data must remain unchanged
    And the application proceeds to the next due card, leaving the failed card in the queue for the current session.
```

## Details & Notes

*   **Related PRD Epic:** Spaced Repetition System (SRS) Engine, AI-Powered Learning Session
*   **Related PRD Goal(s):**
    *   `2.1 Primary Goal`: Automating the SRS update is fundamental to making the learning habit efficient and effective.
*   **Dependencies:**
    *   `US004: Submit Answer for AI Grading`: This story is triggered by the result of US004.
*   **UI/UX Considerations:**
    *   This is a background process with no direct user interface. The user experience is simply the seamless transition to the next card after acknowledging feedback.
*   **Integration:**
    *   This involves a critical write operation to the PostgreSQL database. The application must ensure data integrity (e.g., use transactions).
*   **Testing & QA:**
    *   Requires testing the database update logic under different conditions: correct answer, incorrect answer, and AI failure.
    *   Tests must verify that the `next_review_at` timestamp is calculated correctly.
    *   A key part of testing is how the application parses the AI's natural language response (from US004) into a simple "correct" or "incorrect" state. This logic needs to be robust (e.g., case-insensitive check for the word "correct").
*   **Note on SRS Logic:**
    *   This story assumes a set of pre-defined SRS intervals exists. The mechanism for the user to *change* these intervals will be covered in a separate configuration story.
    *   For the initial implementation, the card that was just reviewed should be removed from the current session's queue, even if answered incorrectly, to prevent immediate repetition within the same session. It will appear again on its next scheduled day.