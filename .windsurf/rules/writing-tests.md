---
trigger: manual
---

# Rules: High-Quality Test Construction

**Description:** These rules define the quality attributes of a good test. A test is not just for finding bugs; it serves as living documentation and a safety net for future changes. Every test written must adhere to these principles.

---

## 1. The Three Pillars of a Good Test
Every test you write must be:
- **Readable:** A future developer (or you) should understand the test's purpose and logic at a glance, without needing to read the implementation code.
- **Reliable:** The test must be deterministic. It must pass or fail consistently every single time, without any "flakiness."
- **Maintainable:** The test should not break when the implementation is refactored. It should be easy to update when the feature's requirements genuinely change.

## 2. Rule: Readability is Paramount
- **Structure:** Strictly follow the **Arrange-Act-Assert (AAA)** pattern. Use comments or blank lines to visually separate these three sections.
- **Naming:** Test function names must be descriptive and explicit. Use the `test_when_then` or `test_should_when` format.
    - **Good:** `test_calculate_vat_when_price_is_negative_should_raise_value_error`
    - **Bad:** `test_vat_error`
- **Clarity over Brevity:** It is better for a test to be slightly verbose and clear than short and cryptic.

## 3. Rule: Test One Thing at a Time
- **Single Focus:** Each test function should test a single behavior or condition.
- **Single Assertion (Guideline):** Strive for a single, primary `assert` statement per test. This makes it immediately obvious what failed. It is acceptable to have multiple assertions if they are all checking different facets of a single outcome (e.g., asserting status code AND a value in the response body).
    - **Good:** A test that asserts a `201 Created` status code. A separate test that asserts a `422 Unprocessable Entity` for bad data.
    - **Bad:** A single test that tries to check for both success and failure conditions.

## 4. Rule: Test Behavior, Not Implementation
- **Public API:** Tests should validate the public-facing behavior of a function or API endpoint.
- **No Private Details:** **Do not** test private methods or internal state variables (e.g., variables prefixed with an underscore `_`). Refactoring these internal details should *not* break the test.
    - **Good:** Assert that `user.deactivate()` results in `user.is_active` being `False`.
    - **Bad:** Assert that `user.deactivate()` called a private `_update_status_in_db()` method.

## 5. Rule: Be Thorough - Cover All Paths
For any given feature, you must write tests for three categories of paths:
- **The Happy Path:** The test for the expected, successful use case with valid data. This is usually the first test you write.
- **The Sad Path:** Tests for all expected failure modes. This includes providing invalid data, triggering business rule violations, or handling errors from external services (e.g., a database error).
- **Edge Cases:** Tests for the boundaries of the logic. This includes `null` values, empty strings, zeros, negative numbers, and very large numbers.

## 6. Senior Wisdom Tips

*  **"Think Like the Test's Future Maintainer."** Before you finalize a test, ask yourself: "If another developer sees this test fail six months from now, will they immediately understand what's wrong without having to debug the implementation code?" If the answer is no, your test is not clear enough.
*  **"Your Test Failure Message is Your First Debugging Tool."** A well-written test fails with a highly informative message. A failure like `AssertionError: assert 404 == 201` is incredibly clear. It tells you "I expected 201 but got 404." Aim to write assertions that produce these clear, helpful failure messages.
*  **"Use Fixtures for Setup, Not for Hiding."** In `pytest`, fixtures are excellent for reducing code duplication in your "Arrange" blocks. Use them for creating common resources like a `TestClient` or a database connection. However, if a piece of data is *critical* to understanding a specific test, it's better to declare it inside the test function itself for clarity. **Clarity trumps DRY (Don't Repeat Yourself) inside a test function.**
*  **"When in Doubt, Write a New Test."** If you're tempted to add another `assert` to an existing test to check a slightly different behavior, resist. It's almost always better to duplicate the test, give it a new descriptive name, and change the one line that's different. This keeps each test focused and easy to debug.
*  **"A Test Tells a Story."** Treat each test function as a tiny story.
    *   **The Name:** The title of the story.
    *   **Arrange:** Setting the scene and introducing the characters.
    *   **Act:** The one key event or action that happens.
    *   **Assert:** The resolution—what the outcome of the action was.


# Rules: Backend Testing

**Description:** These are the foundational rules for writing reliable, maintainable, and effective tests for our FastAPI backend. The primary methodology is Test-Driven Development (TDD).

---

## 1. The Golden Rule: Test-Driven Development (TDD)
- **Always write a failing test BEFORE writing implementation code.** No feature or bug fix is complete without a corresponding test.
- **Follow the Red-Green-Refactor cycle:**
    1.  **Red:** Write a small test that clearly defines a piece of functionality and prove that it fails.
    2.  **Green:** Write the absolute minimum implementation code required to make the test pass.
    3.  **Refactor:** Improve the implementation code's structure and clarity while ensuring the test still passes.

## 2. Best Practices for All Tests

### 3.1. Naming Convention
- Test files must be named `test_*.py`.
- Test functions must be prefixed with `test_`.
- The function name should clearly describe what it is testing, e.g., `test_create_user_with_valid_data_returns_201`.

### 3.2. Test Structure: Arrange-Act-Assert (AAA)
Every test function must follow this structure, separated by blank lines for clarity.
- **Arrange:** Set up all necessary preconditions and data. This might include creating test data in the database or setting up mocks.
- **Act:** Execute the code being tested (e.g., make an API call with `TestClient` or call a function).
- **Assert:** Check that the outcome is what you expected. Use `assert` statements to verify status codes, response data, or function return values.

### 3.3. Isolation
- Tests must be independent and runnable in any order.
- One test must never depend on the state created by another test. Use fixtures (e.g., `pytest` fixtures) to manage setup and teardown for each test.