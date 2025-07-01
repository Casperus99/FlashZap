## Description

This task list is generated based on the user story: US004: Update Card Review Schedule After AI Grading.

### Notes

- The core logic will be implemented within an `SRS_Engine` service or class.
- The `SRS_Engine` will require access to the application's configuration to retrieve the mastery level intervals.
- All sub-tasks are designed as test cases to follow a Test-Driven Development (TDD) workflow.
- **Testing Strategy:** This will be a two-layered approach. First, fast unit tests will be created for the `SRSEngine` in a new test file (`test_srs_engine.py`) to validate its core logic in isolation. Second, an integration test will be added to the existing `test_review_session.py` to ensure the `ReviewSession` correctly calls the `SRSEngine` after a grade is received.

## Tasks

- [x] 1.0 Create the `SRSEngine` Service Structure
  > **File to create:** `src/flash_zap/services/srs_engine.py`
  > - **Action:** Create a new class `SRSEngine` that takes the SRS intervals from the config as a dependency.
  >
  > **File to create:** `tests/test_services/test_s_engine.py`
  > - **Action:** Create a new test file for the `SRSEngine` service.
  - [x] 1.1 Create a new file `src/flash_zap/services/srs_engine.py`.
  - [x] 1.2 Implement a basic `SRSEngine` class structure within the new file.
- [x] 2.0 Implement Card Promotion Logic
  > **File to modify:** `src/flash_zap/services/srs_engine.py`
  > - **Method to create:** `promote_card(self, card)`
  > - **Action:** This method will increase the card's mastery level by one, up to the maximum level, and calculate the next review date based on the corresponding interval.
  - [x] 2.1 Test that providing a "Correct" grade for a card at mastery level 0 advances it to level 1 and sets the correct `next_review_date`.
  - [x] 2.2 Test that providing a "Correct" grade for a card at an intermediate mastery level (e.g., level 2) advances it to the next level (level 3) and updates the `next_review_date` accordingly.
  - [x] 2.3 Test that providing a "Correct" grade for a card already at the maximum mastery level keeps it at the maximum level and updates the `next_review_date`.
- [x] 3.0 Implement Card Demotion Logic
  > **File to modify:** `src/flash_zap/services/srs_engine.py`
  > - **Method to create:** `demote_card(self, card)`
  > - **Action:** This method will decrease the card's mastery level by one, down to the minimum level (0), and calculate the next review date.
  - [x] 3.1 Test that providing an "Incorrect" grade for a card at an intermediate mastery level (e.g., level 4) demotes it to the previous level (level 3) and updates the `next_review_date`.
  - [x] 3.2 Test that providing an "Incorrect" grade for a card at mastery level 1 demotes it to level 0 and updates the `next_review_date`.
  - [x] 3.3 Test that providing an "Incorrect" grade for a card at mastery level 0 keeps it at level 0 and updates the `next_review_date`.
- [x] 4.0 Integrate `SRSEngine` into the Review Session
  > **File to modify:** `src/flash_zap/core/review_session.py`
  > - **Method to modify:** `handle_grading_result(self, card, grade)` (or similar existing method)
  > - **Action:** Import `SRSEngine`. After receiving a grade from the `AIGrader`, call the appropriate `SRSEngine` method (`promote_card` or `demote_card`) based on the result to update the card's state.
  - [x] 4.1 Test that the `ReviewSession` class correctly calls the `SRSEngine` to update a card's schedule after a grade is received from the `AIGrader`. 