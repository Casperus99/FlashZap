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

### [ ] Task 1.3: Configure the Basic FastAPI Application

We will create the main application file, which will be responsible for server configuration and startup.

1.  [ ] In the `src/flash_zap/web/` directory, create a file named `app.py`.
2.  [ ] In the `app.py` file, add the following code, which initializes the FastAPI application and configures the paths to templates and static files:

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

### [ ] Task 1.4: Create a Startup Script

We need a simple way to launch our new web application.

1.  [ ] In the project's root directory (next to `pyproject.toml`), create a new file named `run_web.py`.
2.  [ ] Fill it with the following content:

    ```python
    import uvicorn

    if __name__ == "__main__":
        uvicorn.run("src.flash_zap.web.app:app", host="0.0.0.0", port=8000, reload=True)
    ```

3.  [ ] **Verification:** Run the application with the command `python run_web.py` and open `http://127.0.0.1:8000` in your browser. You should see the welcome message in JSON format.

---

## Phase 2: Implementation of Actual Features

In this phase, we will implement the API endpoints and their corresponding HTML views to replicate the functionality of the existing TUI.

### [ ] Task 2.1: Implement the Main Menu View

We will create a home page that corresponds to the menu from `main_menu.py`.

1.  [ ] In the `src/flash_zap/web/app.py` file, modify the `/` endpoint:
    *   [ ] Remove the test `root` endpoint.
    *   [ ] Create a new `GET /` endpoint that will render the `main_menu.html` template.
    *   [ ] Use `Request` from FastAPI and the `templates` object to return a `TemplateResponse`.
2.  [ ] In the `src/flash_zap/web/templates/` directory, create a `main_menu.html` file.
3.  [ ] Fill `main_menu.html` with a basic HTML structure and add two links (for now, they can point to `#`):
    *   [ ] "Browse all flashcards"
    *   [ ] "Start a review session"

### [ ] Task 2.2: Implement the Flashcard Browsing View

We will create a page that displays a list of all flashcards, similar to `browse_view.py`.

1.  [ ] **API Endpoint:**
    *   [ ] In `src/flash_zap/web/`, create a new file `routes.py` next to `app.py` and import it into `app.py` using `app.include_router`.
    *   [ ] In `routes.py`, create a `GET /cards` endpoint.
    *   [ ] Inside this endpoint, use `card_manager.get_all_cards()` to fetch the flashcards from the database.
    *   [ ] Pass the list of flashcards to the `browse_view.html` template and return a `TemplateResponse`.
2.  [ ] **HTML Template:**
    *   [ ] In the `src/flash_zap/web/templates/` directory, create a `browse_view.html` file.
    *   [ ] Use a `for` loop in Jinja2 to iterate over the list of flashcards and display them in a table (or list), showing the `question` and `answer`.

### [ ] Task 2.3: Implement the Review Session

This is the most complex part. We will implement the review session logic.

1.  [ ] **Endpoint to Start a Session:**
    *   [ ] Create a `GET /review` endpoint that:
        *   [ ] Uses `review_session.start_session()` to get the cards due for review.
        *   [ ] If there are no cards, it displays an appropriate message.
        *   [ ] If there are cards, it redirects the user to the first card's page, e.g., `GET /review/card/{card_id}`.
2.  [ ] **Endpoint to Display a Single Card:**
    *   [ ] Create a `GET /review/card/{card_id}` endpoint that:
        *   [ ] Fetches the data for a specific card.
        *   [ ] Renders the `review_card_view.html` template, passing the card's data to it (only the question!).
3.  [ ] **Endpoint to Grade a Card:**
    *   [ ] Create a `POST /review/card/{card_id}` endpoint that will accept the user's answer and grade.
    *   [ ] Inside the endpoint:
        *   [ ] Get the user's answer from the form.
        *   [ ] Call `ai_grader.grade_answer()` (if used) or simply show the correct answer.
        *   [ ] Call `srs_engine.update_card()` to update the card's review interval.
        *   [ ] Find the ID of the next card in the session and redirect the user to `GET /review/card/{next_card_id}`. If it's the last card, redirect to a summary page.
4.  [ ] **HTML Templates:**
    *   [ ] Create `review_card_view.html`: it should contain a form with a field for the user's answer and grading buttons.
    *   [ ] Create `review_summary.html`: a page displayed after the session is complete.

---

## Phase 3: Final Touches and Cleanup

Finally, we will ensure the application is coherent and remove unnecessary code.

### [ ] Task 3.1: Interface Styling

Let's add a basic stylesheet to make the application look neat.

1.  [ ] In `src/flash_zap/web/static/`, create a `style.css` file.
2.  [ ] Add simple CSS rules to improve the appearance of tables, buttons, and the overall layout.
3.  [ ] Make sure the `style.css` file is included in the `<head>` of every HTML template.

### [ ] Task 3.2: Refactoring and Removing Old Code

Once the web interface is fully functional and tested, we can get rid of the old code.

1.  [ ] Delete the entire `src/flash_zap/tui/` directory.
2.  [ ] Review the `src/flash_zap/main.py` file and remove the code responsible for running the terminal interface. You can leave the file empty or delete it if it's no longer needed.
3.  [ ] Remove any no-longer-used dependencies from `pyproject.toml` (if there were any specific to the TUI).
4.  [ ] Update `README.md` to describe how to run the new web application (`python run_web.py`).

After completing these steps, the FlashZap application will have a fully functional, modern web interface. 