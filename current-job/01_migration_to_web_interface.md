# Migration Plan from Terminal to Web Interface

Below is a detailed, step-by-step plan to migrate the application's interface from a terminal-based UI (TUI) to a web-based interface. The goal is to replace the existing UI with a new web application based on FastAPI and Jinja2 templates, while maximizing the reuse of existing business logic.

## Phase 1: Web Project Initialization and API Layer Creation

In this phase, we will focus on preparing the foundation for the web application and exposing the existing business logic through a REST API.

### [x] Task 1.1: Update Project Dependencies

The necessary libraries to run the web application must be added to the project.

1.  [x] Open a terminal in the project's root directory.
2.  [x] Run the following command to install FastAPI, Uvicorn (application server), and Jinja2 (template engine):
    ```bash
    pip install fastapi "uvicorn[standard]" jinja2 aiofiles
    ```
3.  [x] Update the `pyproject.toml` file (or `requirements.txt`, if it exists) to reflect the new dependencies.

### [x] Task 1.2: Create Directory Structure for the Web Application

File organization is key. We will create a new directory structure dedicated to the web interface.

1.  [x] Inside the `src/flash_zap/` directory, create a new directory named `web`.
2.  [x] Inside `src/flash_zap/web/`, create the following subdirectories:
    *   [x] `templates`: This is where HTML (Jinja2) templates will be stored.
    *   [x] `static`: This is for static files, such as CSS or JavaScript.
3.  [x] Inside `src/flash_zap/web/`, create an empty `__init__.py` file.

### [x] Task 1.3: Configure the Basic FastAPI Application

We will create the main application file, which will be responsible for server configuration and startup.

1.  [x] In the `src/flash_zap/web/` directory, create a file named `app.py`.
2.  [x] In the `app.py` file, add the following code, which initializes the FastAPI application and configures the paths to templates and static files:

    ```python
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates

    # Initialize the FastAPI application
    app = FastAPI(title="FlashZap")

    # Configure the path to static files (CSS, JS)
    app.mount("/static", StaticFiles(directory="src/flash_zap/web/static"), name="static")

    # Configure the Jinja2 template engine
    templates = Jinja2Templates(directory="src/flash_zap/web/templates")

    @app.get("/")
    async def root():
        return {"message": "Welcome to FlashZap Web UI!"}
    ```

### [x] Task 1.4: Create a Startup Script

We need a simple way to launch our new web application.

1.  [x] In the project's root directory (next to `pyproject.toml`), create a new file named `run_web.py`.
2.  [x] Fill it with the following content:

    ```python
    import uvicorn

    if __name__ == "__main__":
        uvicorn.run("src.flash_zap.web.app:app", host="0.0.0.0", port=8000, reload=True)
    ```

3.  [x] **Verification:** Run the application with the command `python run_web.py` and open `http://127.0.0.1:8000` in your browser. You should see the welcome message in JSON format.

---

## Phase 2: Implementation of Actual Features

In this phase, we will implement the API endpoints and their corresponding HTML views to replicate the functionality of the existing TUI.

### [x] Task 2.1: Implement the Main Menu View

We will create a home page that corresponds to the menu from `main_menu.py`.

1.  [x] In the `src/flash_zap/web/app.py` file, modify the `/` endpoint:
    *   [x] Remove the test `root` endpoint.
    *   [x] Create a new `GET /` endpoint that will render the `main_menu.html` template.
    *   [x] Use `Request` from FastAPI and the `templates` object to return a `TemplateResponse`.
2.  [x] In the `src/flash_zap/web/templates/` directory, create a `main_menu.html` file.
3.  [x] Fill `main_menu.html` with a basic HTML structure and add links to match the terminal menu:
    *   [x] "Start a review session" → `/review`
    *   [x] "Import Flashcards from JSON" → `/import`
    *   [x] "Browse Cards" → `/browse`

### [x] Task 2.2: Implement the Flashcard Browsing View

We will create a page that allows viewing and editing a single flashcard by ID, similar to `browse_view.py`.

1.  [x] **API Endpoint:**
    *   [x] In `src/flash_zap/web/`, create a new file `routes.py` next to `app.py` and import it into `app.py` using `app.include_router`.
    *   [x] In `routes.py`, create a `GET /browse` endpoint that displays a form to enter a card ID.
    *   [x] Create a `GET /browse/{card_id}` endpoint that fetches a single card using `card_manager.get_card_by_id()`.
    *   [x] Create `POST /browse/{card_id}/edit` endpoints to handle editing card front, back, and mastery level using existing `card_manager` functions.
2.  [x] **HTML Templates:**
    *   [x] In the `src/flash_zap/web/templates/` directory, create a `browse_form.html` file with a form to enter card ID.
    *   [x] Create a `browse_card.html` file that displays the card details and edit options, similar to the terminal interface.

### [x] Task 2.3: Implement the Review Session

This is the most complex part. We will implement the review session logic using a session-based approach.

1.  [x] **Session Management:**
    *   [x] Create a `GET /review` endpoint that:
        *   [x] Creates a new `ReviewSession` instance and stores it in the web session/memory.
        *   [x] Gets the first card using `session.get_next_card()`.
        *   [x] If there are no cards, displays the "no cards due" message.
        *   [x] If there are cards, renders the `review_card.html` template with the card question.
2.  [x] **Answer Processing:**
    *   [x] Create a `POST /review` endpoint that:
        *   [x] Retrieves the current review session from memory.
        *   [x] Gets the user's answer from the form.
        *   [x] Calls `session.grade_and_update_card()` to process the answer and update the card.
        *   [x] Displays the grade and feedback.
        *   [x] Gets the next card using `session.get_next_card()`.
        *   [x] If there are more cards, renders the next card. If finished, redirects to summary.
3.  [x] **Session Storage:**
    *   [x] Use FastAPI's session middleware or a simple in-memory store to maintain the ReviewSession instance across requests.
4.  [x] **HTML Templates:**
    *   [x] Create `review_card.html`: displays the card question and answer form.
    *   [x] Create `review_feedback.html`: shows grading results and "continue" button.
    *   [x] Create `review_summary.html`: displayed when the session is complete.

### [x] Task 2.4: Implement JSON Import

We will create a web interface for importing flashcards from JSON files, matching the terminal functionality.

1.  [x] **API Endpoints:**
    *   [x] Create a `GET /import` endpoint that displays a file upload form.
    *   [x] Create a `POST /import` endpoint that:
        *   [x] Accepts the uploaded JSON file.
        *   [x] Uses the existing `import_service.import_cards_from_json()` function.
        *   [x] Displays success/error messages and returns to the main menu.
2.  [x] **HTML Template:**
    *   [x] Create `import_form.html`: displays a file upload form with instructions.
    *   [x] Create `import_result.html`: shows import results (success/error messages) with a "back to menu" button.

---

## Phase 3: Final Touches and Cleanup

Finally, we will ensure the application is coherent and remove unnecessary code.

### [x] Task 3.1: Interface Styling

Let's add a basic stylesheet to make the application look neat.

1.  [x] In `src/flash_zap/web/static/`, create a `style.css` file.
2.  [x] Add simple CSS rules to improve the appearance of tables, buttons, and the overall layout.
3.  [x] Make sure the `style.css` file is included in the `<head>` of every HTML template.

### [x] Task 3.2: Refactoring and Removing Old Code

Once the web interface is fully functional and tested, we can get rid of the old code.

1.  [x] Delete the entire `src/flash_zap/tui/` directory.
2.  [x] Review the `src/flash_zap/main.py` file and remove the code responsible for running the terminal interface. You can leave the file empty or delete it if it's no longer needed.
3.  [x] Remove any no-longer-used dependencies from `pyproject.toml` (if there were any specific to the TUI).
4.  [x] Update `README.md` to describe how to run the new web application (`python run_web.py`).

After completing these steps, the FlashZap application will have a fully functional, modern web interface. 