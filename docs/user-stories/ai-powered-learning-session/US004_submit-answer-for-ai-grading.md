# US004: Submit Answer for AI Grading and Receive Feedback

**As a:** User
**I want to:** Submit my typed answer for a flashcard to be graded by an AI
**So that:** I can get objective feedback on my response and see the correct answer.

## Acceptance Criteria

```gherkin
Feature: AI-Powered Answer Grading

  Scenario: Successfully grade a valid answer via the AI service
    Given I am in a review session and the front of a card is displayed
    And the correct answer for this card is "The mitochondria is the powerhouse of the cell."
    When I type the answer "The mitochondria is the part of the cell that generates energy." and submit it
    Then the application must send my answer and the correct answer to the configured AI service
    And the application should display the AI's feedback (e.g., "Correct. You captured the main idea.")
    And the application must display the original correct answer: "The mitochondria is the powerhouse of the cell."
    And the application should wait for me to acknowledge before proceeding (e.g., "Press Enter to continue...").

  Scenario: AI service returns an error or times out
    Given I am in a review session and have submitted my answer
    And the external AI service is unreachable or returns an error (e.g., 503 Service Unavailable)
    When the application attempts to get a grade from the AI
    Then the application must not crash
    And I must see a clear error message, like "Error: Could not connect to the AI service. Please check your network or configuration."
    And the original correct answer must still be displayed to me
    And the review session for that card should be paused, awaiting my input to continue.

  Scenario: AI API key is invalid or not configured
    Given the application is configured with an invalid or missing AI API key
    And I am in a review session and have submitted my answer
    When the application attempts to make an API call
    Then the API call must be prevented
    And I must see a specific error message, such as "Error: AI API key is invalid or missing. Please configure it."
    And the review session for that card should be paused.

  Scenario: User submits an empty answer
    Given I am in a review session and the front of a card is displayed
    When I submit an empty answer
    Then the application must not make a call to the AI service
    And I should see a message, such as "Answer cannot be empty. Please try again."
    And I must remain on the same card, with the input prompt ready for another attempt.
```

## Details & Notes

*   **Related PRD Epic:** AI-Powered Learning Session
*   **Related PRD Goal(s):**
    *   `2.1 Primary Goal`: This AI feedback loop is the core feature designed to make learning more effective and habitual.
*   **Dependencies:**
    *   `US003: Initiate Review Session and Display First Card`: This story builds directly on the state left by US003.
*   **UI/UX Considerations:**
    *   AI feedback, the user's answer, and the correct answer should be clearly labeled and formatted to be easily distinguishable in the terminal. Using colors or titles like `[AI GRADE]`, `[YOUR ANSWER]`, `[CORRECT ANSWER]` is recommended.
*   **Security Considerations:**
    *   The AI API key is sensitive information. It **must not** be hardcoded. It should be loaded securely from a configuration file (e.g., `.env`) or an environment variable that is not checked into version control.
*   **Integration:**
    *   This story introduces a critical dependency on an external AI API (e.g., OpenAI, Gemini, etc.).
    *   The prompt sent to the AI is a key part of this integration. An initial, simple prompt should be used, with the expectation that it will be configurable later (covered in a future story). For example: `Is the "user answer" a correct response to the "question" if the "correct answer" is this? Grade it as correct/incorrect and provide brief feedback.`
*   **Testing & QA:**
    *   Requires a mocked AI API client to simulate various responses:
        *   A successful grading response.
        *   A 5xx server error.
        *   A 4xx client error (e.g., invalid authentication).
        *   A network timeout.
*   **Note on State:** This story only covers submitting the answer and getting feedback. Updating the card's SRS data based on the AI's grade will be handled in a separate, subsequent user story.