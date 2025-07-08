# FlashZap User Manual

## 1. Introduction

Welcome to FlashZap!

FlashZap is a powerful, terminal-based flashcard application designed for learners who want to achieve deep, long-term knowledge retention. It goes beyond traditional flashcard apps by using an AI-powered grading system to provide objective, actionable feedback on your open-ended answers.

Stop wondering if you *really* know the answer. FlashZap's AI will tell you, helping you identify and fix knowledge gaps effectively.

## 2. Getting Started

Follow these steps to get FlashZap up and running on your system.

### 2.1. Prerequisites

*   **Python:** Version 3.9 or higher.

### 2.2. Installation

_(TODO: Add installation instructions here. For now, we assume you have the project set up and can run it from the source.)_

### 2.3. Configuration

Before you can run the application, you need to configure a few settings.

1.  **Create a `.env` file:** In the root directory of the project, create a file named **.env**.

2.  **Add your API Key:** Open the **.env** file and add the following line, replacing `YOUR_API_KEY_HERE` with your actual Gemini API key:

    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

    > **Security Note:** Your API key is a secret. The **.env** file is included in the project's **.gitignore** to prevent you from accidentally committing it to source control. Do not share this key.

3.  **Database:** FlashZap uses a simple **SQLite** database by default, which requires no extra setup. The database file (`flashzap.db`) will be created automatically. If you are an advanced user, you can switch to another database like **PostgreSQL** by setting the `DATABASE_URL` in your **.env** file (see "Advanced Topics / Customization").

## 3. How to Use the Application

### 3.1. Running the Application

Once configured, you can start FlashZap by running the following command from the root of the project directory:

```bash
python -m src.flash_zap
```

You will be greeted by the main menu, which is your central hub for all actions. Use the number keys to navigate.

### 3.2. Importing Flashcards

Before you can start a review session, you need to import some cards.

1.  Select option `2` from the main menu.
2.  The application will prompt you to enter the path to a JSON file.

**JSON File Format:**
Your JSON file must be an array of objects, where each object represents a single flashcard and contains `front` and `back` keys (max 200 characters each).

**Example `my_cards.json` file:**
```json
[
  {
    "front": "What is the command to initialize a new Git repository?",
    "back": "git init"
  },
  {
    "front": "What does the 'SOLID' acronym stand for in software design?",
    "back": "Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion"
  }
]
```
A success or error message will be shown upon completion.

### 3.3. The Review Session

This is the core of FlashZap.

1.  Select option `1` from the main menu to begin. If no cards are due, the app will let you know.
2.  The "front" of a card is displayed. Type your answer and press Enter.
3.  The app shows a `Grading...` status while the AI evaluates your answer.
4.  The results are displayed:
    *   **Grade:** `Correct` or `Incorrect`.
    *   **Feedback:** A short explanation from the AI.
    *   **Mastery Level:** Shows how the card's mastery has been updated.

**Important Feature: Intelligent Incorrect Card Handling**
When your answer is graded as `Incorrect`, FlashZap handles it intelligently to optimize your learning.
*   If the card's mastery level drops to `0`, it will be moved to the back of your current session's deck. This gives you a "second chance" to review it after attempting all other due cards.
*   If the mastery level is still above `0`, the card is removed from the current session and rescheduled for its next review based on its new, lower mastery level.

### 3.4. Browse and View a Specific Flashcard

A new "Browse Cards" option has been added to the main menu, allowing you to look up the details of any specific flashcard in your collection without starting a review session.

1.  **Select "Browse Cards"**: From the main menu, choose the new "Browse Cards" option.
2.  **Enter Card ID**: You will be prompted to enter the numerical ID of the card you want to view.
3.  **View Details**: If the card exists, the application will display its full details:
    *   ID
    *   Front (the question or prompt)
    *   Back (the answer or information)
    *   Mastery Level
    *   Next Review Date

Once the card's details are displayed, an "Edit Options" menu will appear below them. This menu allows you to modify the card directly.

**Editing a Card:**
After a card's details are shown, you can choose one of the following options by pressing the corresponding number key:

1.  **Edit front**: Displays the current front text and then prompts you to enter the new text.
2.  **Edit back**: Displays the current back text and then prompts you to enter the new text.
3.  **Lower mastery level**: Shows the current mastery level and then allows you to manually reduce it. You will be prompted for a new level, which must be a number and cannot be higher than the card's current level. This is useful if you feel you don't know a card as well as its current level suggests.
4.  **Cancel**: Exits the edit menu and returns you to the main menu.

After performing an edit, a confirmation message will be displayed. Press any key to return to the edit menu to make other changes if needed.

If you enter an ID for a card that does not exist, a "Card not found" message will be displayed. If you enter a non-numeric value for the ID, an "Invalid ID. Please enter a number." message will be shown. After either message, press any key to return to the main menu.

## 4. Advanced Topics / Customization

You can customize FlashZap's behavior by editing your **.env** file or the **src/flash_zap/config.py** file.

### 4.1. Changing the Database

To use a different database like PostgreSQL, update the `DATABASE_URL` in your **.env** file. Make sure you have the appropriate database driver installed (e.g., `psycopg2-binary` for PostgreSQL).

**Example for PostgreSQL:**
```
DATABASE_URL="postgresql://user:password@localhost/flashzap_db"
```

### 4.2. Customizing the AI

The AI's behavior can be tweaked in **config.py**:
*   `AI_GRADER_MODEL_NAME`: Experiment with different Gemini models.
*   `AI_GRADER_PROMPT_TEMPLATE`: Modify the prompt to change how the AI grades answers.

## 5. Troubleshooting / FAQ

*   **Question:** Why do some incorrect cards reappear in my session while others don't?
*   **Answer:** This is part of the intelligent review process. If a card's mastery level drops to zero after an incorrect answer, it will reappear in the same session for immediate reinforcement. If you still have some mastery over the card (level > 0), it is simply rescheduled for its next review date, allowing you to focus on the material you know least well. 