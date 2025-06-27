# Product Requirements Document: FlashZap

*   **Version:** 0.1
*   **Author:** Kacper Nowakowski

## **1. Introduction / Overview**

FlashZap is a personal, terminal-based flashcard application designed for developers and lifelong learners. It addresses the primary limitation of traditional study tools—the subjective and inconsistent self-grading of open-ended questions. By leveraging an AI-powered grading system, FlashZap provides objective feedback on user answers, eliminating cognitive burden and ensuring a more effective learning process. Its core value is enabling deeper, long-term knowledge retention through an efficient, responsive, and objective study experience.

## **2. Vision Statement**

Our vision is to seamlessly integrate deep learning into daily life, transforming it from a chore into a consistent, empowering habit. By pioneering AI-evaluated, open-ended questions within a robust Spaced Repetition System, FlashZap will serve as a personal knowledge engine. We believe in technology that augments human intellect, using AI as a collaborative partner to help us learn faster, remember longer, and maintain our cognitive edge in an ever-evolving world.

## **3. Target Audience / User Personas**

**Primary Persona: Alex, the Polymath Developer**

*   **Archetype:** A mid-level to senior software developer who is passionate about continuous learning, both within and outside of their professional domain. They view knowledge acquisition as a core part of their identity.

*   **Key Goals:**
    *   To build a durable, long-term knowledge base across diverse subjects (e.g., a new programming language, system design principles, a foreign language, historical facts).
    *   To efficiently integrate learning into a busy schedule, making consistent daily progress.
    *   To move beyond superficial understanding and achieve true mastery of concepts.

*   **Frustrations / Pain Points:**
    *   **Inefficient Recall:** Forgetting concepts learned just weeks or months ago, requiring time-consuming relearning.
    *   **Tool Friction:** Existing flashcard apps feel clunky, are slow to use, or don't handle complex, open-ended questions well.
    *   **Subjectivity:** The nagging feeling that "I think I know this" isn't a reliable measure of true understanding.
    *   **Context Switching:** The hassle of creating and managing flashcards feels like a separate, time-consuming task that pulls them away from actual learning.

*   **Scenario of Use:**
    *   It's 8:00 AM. Before diving into his workday, Alex opens his terminal and runs `flashzap review`. The app presents his first due card: "Explain the difference between `git merge` and `git rebase`." He types out his detailed answer. The AI grades it as "Mostly Correct," highlighting that he missed a key nuance about commit history. He makes a mental note, feeling the concept solidify, and moves to the next card, this one about a Spanish vocabulary word. In 15 minutes, he has completed his daily review, feeling accomplished and ready to start his day.

## **4. Epics**

### **4.1 Epic: Card Lifecycle Management**

*   **Priority:** Must-Have
*   **Description:** This epic covers the entire process of populating the application with learning material. The core functionality is the ability to import flashcards into the local PostgreSQL database. From the main terminal menu, the user will select an "Import Flashcards" option. The application will then prompt for a file path. The user provides the path to a JSON file containing an array of card objects. The system will parse this file and persist the new cards in the database.

### **4.2 Epic: AI-Powered Learning Session**

*   **Priority:** Must-Have
*   **Description:** This epic represents the primary user activity: the interactive study session. The user will initiate a session by selecting a "Review" option from the main menu. The application will then present the front of a card that is due for review according to the SRS schedule. The user types their answer in the terminal. This answer, along with the correct answer from the card's back, is sent to an external AI service for evaluation. The AI's grade and feedback are displayed to the user before the application proceeds to the next due card.

### **4.3 Epic: Spaced Repetition System (SRS) Engine**

*   **Priority:** Must-Have
*   **Description:** This epic encompasses the underlying logic that powers the learning schedule. The system will implement an SRS algorithm to track the user's performance on each card and calculate the optimal date for the next review. A crucial part of this epic is configurability. The user must be able to easily modify the SRS parameters, specifically the sequence of time intervals (e.g., 1 day, 3 days, 7 days, etc.) that determine a card's review schedule.

## **5. Additional Functional Requirements**

*(To be defined)*

## **6. Non-functional Requirements**

### **6.1 Performance**

*   **UI Responsiveness:** All terminal user interface (TUI) interactions, such as navigating menus or flipping cards, must render in under 100ms to feel instantaneous.
*   **AI Grading Latency:** The AI grading process should not exceed 3 seconds to maintain a fluid review session. The UI should indicate that grading is in progress.

### **6.2 Data Persistence & Reliability**

*   **Database:** All user data, including cards and review history, will be stored in a local PostgreSQL database to ensure data integrity and durability.
*   **Backup:** The user is responsible for backing up the PostgreSQL database using standard database tools. The application will not provide an automated backup feature in the initial version.

### **6.3 Security**

*   **API Key Storage:** The external AI service API key must not be hardcoded. It will be managed via a `.env` file, which will be included in the `.gitignore` file to prevent accidental commits.

### **6.4 Configurability**

*   **SRS Parameters:** The Spaced Repetition System intervals will be configurable via a `config.py` file, allowing the user to easily tailor the learning schedule.