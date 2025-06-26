# US002: Import Flashcards from JSON File

**As a:** User
**I want to:** Import a set of flashcards from a local JSON file
**So that:** I can quickly populate my knowledge base with new learning material.

## Acceptance Criteria

```gherkin
Feature: Card Import

  Scenario: Successfully import a well-formatted JSON file
    Given I am at the main menu in the terminal application
    And I have a JSON file named "cards.json" at "/path/to/my/cards.json"
    And "cards.json" contains a valid array of flashcard objects, each with a "front" and "back" key
    When I select the "Import Flashcards" option
    And I provide the full path "/path/to/my/cards.json"
    Then the application should parse the file
    And for each object in the file, a new card should be created in the database
    And I should see a success message in the terminal, like "Successfully imported 15 cards."
    And I should be returned to the main menu.

  Scenario: Attempt to import a file that does not exist
    Given I am at the main menu in the terminal application
    When I select the "Import Flashcards" option
    And I provide a path "/path/to/nonexistent-file.json" that does not exist
    Then the application should not import any cards
    And I should see an error message, like "Error: File not found at the specified path."
    And I should be returned to the main menu (or the import prompt).

  Scenario: Attempt to import a file with invalid JSON format
    Given I am at the main menu in the terminal application
    And I have a file "bad.json" at "/path/to/bad.json" that contains malformed JSON
    When I select the "Import Flashcards" option
    And I provide the path to "bad.json"
    Then the application should not import any cards
    And I should see an error message, like "Error: Failed to parse JSON. Please check the file format."
    And I should be returned to the main menu.

  Scenario: Attempt to import a file where a card object is missing a required key
    Given I am at the main menu in the terminal application
    And I have a valid JSON file "incomplete.json" where one or more objects are missing the "front" or "back" key
    When I select the "Import Flashcards" option
    And I provide the path to "incomplete.json"
    Then the application should reject the entire import
    And I should see a specific error message, like "Error: Import failed. Card at index 4 is missing required key: 'front'."
    And no cards from that file should be saved to the database.
```

## Details & Notes

*   **Related PRD Epic:** Card Lifecycle Management
*   **Related PRD Goal(s):** 2.2 Knowledge Base Expansion
*   **Dependencies:** **US001: Main Menu Navigation**
*   **UI/UX Considerations:** The interaction should be a simple prompt-response flow within the terminal.
*   **Note on Card Structure:** The JSON file must contain a single array of objects. Each object in the array MUST contain a `front` (string) and a `back` (string) key. The backend will handle the creation of SRS-related fields with default values.