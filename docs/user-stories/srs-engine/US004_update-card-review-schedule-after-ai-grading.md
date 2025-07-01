# US004: Update Card Review Schedule After AI Grading

**As a:** User
**I want to:** Have the system automatically update a card's next review date after it has been graded by the AI
**So that:** My study schedule is continuously optimized based on my performance, ensuring I review material at the most effective intervals for long-term retention.

## Acceptance Criteria

```gherkin
Feature: SRS Card Scheduling

  Scenario: Advancing a card's mastery level on a correct answer
    Given A flashcard is at mastery level 2 (e.g., a 3-day review interval)
    And I am in a review session for that card
    When I submit an answer that the AI grades as "Correct"
    Then The card's mastery level should be advanced to 3 (e.g., a 7-day interval)
    And The card's next_review_date should be updated to today's date plus the interval for mastery level 3.

  Scenario: Decreasing a card's mastery level on an incorrect answer
    Given A flashcard is at mastery level 4 (e.g., a 14-day review interval)
    And I am in a review session for that card
    When I submit an answer that the AI grades as "Incorrect"
    Then The card's mastery level should be decreased to 3 (e.g., a 7-day interval)
    And The card's next_review_date should be updated to today's date plus the interval for mastery level 3.
```

## Details & Notes

*   **Related PRD Epic:** Spaced Repetition System (SRS) Engine
*   **Related PRD Goal(s):** P1: Core Learning Habit Formation
*   **Dependencies:** `US003_review-due-flashcard-with-ai-evaluation.md`
*   **Note:** This story assumes the existence of a configurable list of intervals corresponding to mastery levels (e.g., [1, 3, 7, 14] days). The implementation of *how* to configure that schedule is out of scope and will be handled in a subsequent story.
*   **Note:** The binary grade values from the AI service ("Correct", "Incorrect") will be mapped to the scheduling actions (promote, demote) within the SRS Engine. 