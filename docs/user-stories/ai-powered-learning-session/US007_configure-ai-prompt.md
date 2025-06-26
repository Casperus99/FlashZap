# US007: Configure AI Prompt via File

**As a:** User
**I want to:** Define the prompt template sent to the AI in a configuration file
**So that:** I can experiment with different instructions to improve the quality and accuracy of the AI's grading and feedback.

## Acceptance Criteria

```gherkin
Feature: AI Prompt Configuration

  Scenario: Application uses a custom prompt from a valid configuration file
    Given a configuration file exists at '~/.config/srs-app/config.json'
    And the file contains a key `ai_prompt_template` with a custom prompt string
    And the prompt string contains placeholders like {question}, {user_answer}, and {correct_answer}
    When I submit an answer to a card during a review session
    Then the application must construct the final prompt sent to the AI service by replacing the placeholders with the actual card data
    And the AI's response should be based on this custom instruction set.

  Scenario: Application uses the default prompt when the key is missing from the config file
    Given a configuration file exists but does not contain the `ai_prompt_template` key
    When the application prepares to send a request to the AI service
    Then it must not crash
    And it must use a hardcoded, default prompt template for the AI request.

  Scenario: Application handles an invalid data type for the prompt template
    Given the configuration file contains the `ai_prompt_template` key, but its value is not a string (e.g., it's a number or an array)
    When the application starts
    Then it must log a clear warning to the console, such as "Warning: 'ai_prompt_template' is not a valid string. Using default prompt."
    And it must fall back to using the hardcoded, default prompt for all subsequent AI requests.

  Scenario: Placeholder replacement in the prompt works correctly
    Given the `ai_prompt_template` is "Critique this: {user_answer}. The right answer is {correct_answer}."
    And the current card's front (question) is "What is the capital of France?"
    And the correct answer is "Paris"
    And my submitted answer is "Lyon"
    When the application sends the request to the AI
    Then the exact payload sent to the AI must contain the formatted string "Critique this: Lyon. The right answer is Paris."
```

## Details & Notes

*   **Related PRD Epic:** AI-Powered Learning Session
*   **Related PRD Goal(s):** This directly supports the core solution of having a more efficient and objective learning experience by allowing fine-tuning of the AI grader.
*   **Dependencies:**
    *   This feature modifies the behavior of `US004: Submit Answer for AI Grading`.
    *   It can share the same configuration file mechanism as `US006: Configure SRS Intervals`.
*   **UI/UX Considerations:**
    *   Configuration is handled by the user directly editing the configuration file. Clear documentation on available placeholders (`{question}`, `{user_answer}`, `{correct_answer}`) is essential.
*   **Security Considerations:**
    *   While the prompt itself is not sensitive, the configuration file it resides in may also contain the AI API key, which must be handled securely.
*   **Integration:**
    *   This directly impacts the payload sent to the external AI API.
*   **Testing & QA:**
    *   Unit tests should focus on the prompt formatting logic: ensuring placeholders are correctly replaced.
    *   Tests must verify the fallback behavior to the default prompt when the config is missing, malformed, or has an invalid data type.
*   **Note:** The application should read the configuration file on startup. A single `config.json` can be used for both SRS intervals and the AI prompt template.