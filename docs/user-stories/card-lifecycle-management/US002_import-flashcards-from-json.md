# US002: Import Flashcards from JSON

**As a:** User
**I want to:** Import a set of flashcards from a local JSON file
**So that:** I can quickly populate my collection with new study material without manual entry.

## Acceptance Criteria

```gherkin
Feature: Import Flashcards from JSON file

  Scenario: Successful import of a valid JSON file
    Given I have selected the "Import from JSON" option in the main menu
    And I provide the path to a valid JSON file "cards.json"
    And "cards.json" contains a list of dictionaries, each with "front" and "back" keys
    And the "front" and "back" values are strings of 200 characters or less
    When the application processes the file
    Then the new flashcards should be added to the database
    And I should see a success message on the terminal, like "Successfully imported 15 cards."

  Scenario: User provides a path to a non-existent file
    Given I have selected the "Import from JSON" option in the main menu
    When I provide a path to a file that does not exist
    Then the application should not add any cards
    And I should see an error message on the terminal, like "Error: File not found at path 'non_existent_file.json'."

  Scenario: The JSON file is malformed or not a list
    Given I have selected the "Import from JSON" option in the main menu
    And I provide the path to a JSON file "malformed.json"
    And "malformed.json" contains invalid JSON or is not a list of objects
    When the application processes the file
    Then the application should not add any cards
    And I should see an error message on the terminal, like "Error: Invalid JSON format. Expected a list of objects."

  Scenario: A dictionary in the JSON file is missing a required key
    Given I have selected the "Import from JSON" option in the main menu
    And I provide the path to a JSON file "missing_keys.json"
    And the file contains a list with a dictionary missing the "back" key
    When the application processes the file
    Then the application should not add any cards from the invalid entry
    And I should see an error message on the terminal detailing the issue, like "Error: Invalid record found. Each card must have 'front' and 'back' keys."

  Scenario: A flashcard's content exceeds the character limit
    Given I have selected the "Import from JSON" option in the main menu
    And I provide the path to a JSON file "too_long.json"
    And the file contains a card where the "front" text is over 200 characters long
    When the application processes the file
    Then the application should not add the oversized card
    And I should see an error message on the terminal, like "Error: Card content exceeds 200 character limit."

```

## Details & Notes

*   **Related PRD Epic:** Card Lifecycle Management
*   **Dependencies:** US001: Main Menu Navigation
*   **UI/UX Considerations:** The user will be prompted for the file path directly in the terminal after selecting the import option.
*   **Security Considerations:** The application should handle file path inputs safely to prevent path traversal issues, even if it's a local application.
*   **Testing & QA:** Requires test JSON files for all valid and invalid scenarios described in the Acceptance Criteria. 