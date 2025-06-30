# US003: Review a Due Flashcard with AI Evaluation

**As a:** User
**I want to:** have my open-ended answers evaluated by an AI during a review session
**So that:** I can get objective, actionable feedback on my understanding and improve my knowledge retention.

## Acceptance Criteria

```gherkin
Feature: AI-Powered Flashcard Review

  Scenario: Successfully reviewing a due card
    Given I have selected the "Review Due Cards" option from the main menu
    And there is at least one card due for review
    And the application is displaying the "front" of a due card
    When I type my detailed answer and submit it
    Then my answer and the card's "back" content are sent to the AI evaluation service
    And the application displays an "AI Grade" ("Correct" or "Incorrect")
    And the application displays "AI Feedback" explaining the grade
    And the application displays the original "Correct Answer" from the card's "back" for my comparison.

  Scenario: AI service is temporarily unavailable or returns an error
    Given I am in a review session and have submitted an answer for a card
    When the AI evaluation service fails to respond or returns an error
    Then the application should not crash
    And I should see an error message like "Error: The AI grading service is currently unavailable. Please try again later."
    And the review session for that card should be halted, awaiting user acknowledgement before proceeding or exiting.

  Scenario: User attempts to review when no cards are due
    Given I have selected the "Review Due Cards" option from the main menu
    And there are no cards currently scheduled for review
    When the application checks for due cards
    Then the application should display a message like "Great job! There are no cards due for review right now."
    And I should be returned to the main menu.

```

## Details & Notes

*   **Related PRD Epic:** AI-Powered Learning Session
*   **Dependencies:**
    *   `US001`: Main Menu Navigation (to start the review)
    *   `US002`: Import Flashcards from JSON (to have cards to review)
*   **Note on "Due Cards":** For the initial implementation of this story, the definition of a "due card" is simplified. We will consider **any card that has not yet been reviewed during the current session** as being "due." The full Spaced Repetition System (SRS) logic for calculating due dates will be implemented in a subsequent user story.
*   **UI/UX Considerations:**
    *   While waiting for the AI response (which may take up to 3 seconds), the UI should display a clear loading/processing indicator (e.g., "AI is grading your answer...").
    *   The presentation of the grade, feedback, and correct answer must be clean and easy to parse in the terminal.
*   **Security Considerations:**
    *   The API key for the AI service must be loaded securely from a `.env` file and not be exposed in the source code.
*   **Testing & QA:**
    *   Requires mocking the AI service to test various responses: "Correct", "Incorrect", and error states.
    *   Test cases should include answers with varying levels of correctness to ensure the feedback is handled appropriately.