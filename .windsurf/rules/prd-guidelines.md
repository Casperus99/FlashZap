---
trigger: manual
---

# Guidelines to PRD maintenance

## General Instructions

1.  **Clarity and Conciseness:** Use clear, unambiguous language. Avoid jargon where possible, or define it if necessary. Be concise but thorough.
2.  **Consistency:** Ensure terminology is consistent throughout the PRD and with other project documents.
3.  **Audience:** Remember the PRD is for strategic understanding. While technical details might be hinted at, the primary focus is on product vision, user needs, and business goals.
4.  **Actionability (Implicit):** While not a task list, the PRD should provide enough clarity for epics and high-level features to be derived from it.
5.  **Structure:** Adhere to the section structure outlined below. If sections are missing, propose their creation. If content is misplaced, suggest moving it to the appropriate section.

## PRD Section Breakdown and Instructions

Below are the standard sections that should be present in the PRD. For each section, I've described its purpose, what it should contain, why it's important, and examples to guide your rewriting/editing.

---

### 1. Introduction / Overview

*   **Purpose:** To provide a brief, high-level summary of the product and the problem it solves.
*   **What it should consist of:**
    *   A concise statement of what the product is.
    *   The primary problem the product aims to solve for its users.
    *   The core value proposition.
*   **Why it's important:** Sets the stage and immediately orients the reader (and AI) to the product's fundamental purpose.
*   **Example (Instruction to AI):**
    *   "Ensure this section clearly answers: What is this product? What main problem does it solve? What's its unique benefit? *For example: 'Project Scribe is a web application designed to help solo developers efficiently manage and collaborate on project documentation with AI assistance. It solves the problem of disorganized, outdated, or insufficient documentation in solo-led projects by providing structured templates and AI-powered generation and maintenance tools. Its core value is enabling faster development cycles and better long-term project maintainability through intelligent documentation.'* Rewrite to be as clear and impactful as this example."

### 2. Vision Statement

*   **Purpose:** To articulate the long-term desired future state or impact of the product.
*   **What it should consist of:**
    *   An aspirational, forward-looking statement.
    *   What the product aims to become or achieve in the long run.
*   **Why it's important:** Provides a guiding star for all product decisions and helps maintain focus on the bigger picture.
*   **Example (Instruction to AI):**
    *   "This section should paint a picture of the product's ultimate aspiration. *For example: 'Our vision for Project Scribe is to become the indispensable AI-first documentation companion for every solo innovator, transforming documentation from a chore into a strategic accelerator for software creation.'* Verify the existing statement is aspirational and long-term focused, or propose a revision."

### 3. Goals and Objectives

*   **Purpose:** To define specific, measurable, achievable, relevant, and time-bound (SMART) goals for the product.
*   **What it should consist of:**
    *   Business goals (e.g., market share, revenue, user acquisition).
    *   Product goals (e.g., specific user outcomes, feature adoption rates).
    *   Potentially, project goals (e.g., initial release milestones).
*   **Why it's important:** Provides concrete targets against which success can be measured and helps prioritize efforts.
*   **Example (Instruction to AI):**
    *   "Check if goals are SMART. If not, rephrase them. *For example, instead of 'Get many users,' revise to: 'Acquire 100 active beta users within 3 months of soft launch.' Or, for a product goal: 'Achieve a 75% completion rate for the initial documentation setup wizard by Q4.'* Ensure there's a mix of business and product-focused goals."

### 4. Target Audience / User Personas

*   **Purpose:** To clearly define who the product is for.
*   **What it should consist of:**
    *   Detailed descriptions of primary (and potentially secondary) user personas.
    *   Include: demographics (if relevant), needs, pain points, motivations, technical proficiency, and how they might interact with the product.
*   **Why it's important:** All product decisions should be made with the target user in mind. This section ensures a shared understanding of who that is.
*   **Example (Instruction to AI):**
    *   "For each persona, ensure it includes: Name, Role/Archetype, Key Goals (related to the product), Frustrations/Pain Points (that the product solves), and a brief Scenario of Use. *For example: 'Persona: Alex, the Solo SaaS Developer. Goals: Quickly bootstrap new projects, maintain clear documentation for future self or potential collaborators, minimize time spent on non-coding tasks. Frustrations: Documentation quickly becomes outdated; context switching between code and docs is inefficient.'* If personas are vague, suggest adding these details."

### 5. Key Features / Epics

*   **Purpose:** To list and briefly describe the major functionalities or modules of the product.
*   **What it should consist of:**
    *   A high-level list of core features (often called "Epics" in Agile).
    *   A brief (1-2 sentence) description for each, explaining its value to the user or its purpose.
    *   (Optional) High-level prioritization (e.g., Must-have, Should-have, Could-have).
*   **Why it's important:** Outlines the "What" of the product at a high level, forming the basis for more detailed User Stories later.
*   **Example (Instruction to AI):**
    *   "Ensure this is a list of *major* capabilities, not granular tasks. *For example: '1. AI-Powered Documentation Generation: Users can generate initial drafts of PRDs, User Stories, and technical specs based on high-level inputs. 2. Real-time Documentation Sync: Changes in linked code repositories can trigger suggestions for documentation updates. 3. Collaborative Editing (Future): Allows multiple users to work on documentation simultaneously.'* Check if descriptions clearly state the value/purpose. If prioritization is missing and seems beneficial, suggest adding it."

### 6. Assumptions

*   **Purpose:** To list any assumptions being made that could impact the product's design, development, or success.
*   **What it should consist of:**
    *   Technical assumptions (e.g., "Users will have reliable internet access").
    *   Market assumptions (e.g., "There is a significant market of solo developers willing to pay for this tool").
    *   User behavior assumptions (e.g., "Users are comfortable using AI-assisted tools").
*   **Why it's important:** Makes implicit beliefs explicit. If an assumption proves false, it may require a pivot in strategy.
*   **Example (Instruction to AI):**
    *   "Review this section for clarity and impact. *For example: 'We assume users are familiar with Markdown for basic document formatting.' or 'We assume an existing LLM API (e.g., OpenAI) will be available and cost-effective for core AI features.'* Ensure assumptions are distinct from requirements."

### 7. Constraints / Scope (Out of Scope)

*   **Purpose:** To define limitations, boundaries, and things explicitly *not* being built (at least initially).
*   **What it should consist of:**
    *   Technical constraints (e.g., "Must be deployable on AWS," "Initial version will only support English").
    *   Resource constraints (e.g., "Development by a single developer").
    *   Explicitly out-of-scope features (e.g., "Mobile application is out of scope for V1," "Direct integration with project management tools other than GitHub/GitLab Issues is not planned").
*   **Why it's important:** Manages expectations and prevents scope creep. Clearly defining what's *not* included is as important as defining what *is*.
*   **Example (Instruction to AI):**
    *   "Ensure this section clearly delineates boundaries. *For example: 'Constraint: The initial version must be a web application accessible via modern browsers; native desktop apps are out of scope.' or 'Out of Scope for V1: Real-time collaborative editing with multiple cursors.'* Look for opportunities to make these statements more precise."

### 8. Success Metrics / KPIs (Key Performance Indicators)

*   **Purpose:** To define how the success of the product (and the achievement of its goals) will be measured.
*   **What it should consist of:**
    *   Specific, measurable metrics.
    *   Link these back to the Goals and Objectives section.
    *   Examples: User acquisition rate, active user count (daily/monthly), feature adoption rate, conversion rate (e.g., free to paid), user satisfaction scores (e.g., NPS), task completion rates.
*   **Why it's important:** Provides objective ways to track progress and make data-driven decisions. If you can't measure it, you can't improve it.
*   **Example (Instruction to AI):**
    *   "Metrics should be quantifiable. *For example: 'Monthly Active Users (MAU): Target 500 MAU within 6 months post-launch.' or 'Feature Adoption: 60% of registered users utilize the AI-powered User Story generation feature at least once within their first month.'* Ensure metrics align with the stated goals."

### 9. Release Criteria / Milestones (Optional but Recommended)

*   **Purpose:** To outline high-level conditions or feature sets that define a releasable version of the product (e.g., MVP, V1, V2).
*   **What it should consist of:**
    *   A list of key features or capabilities that must be complete for a specific release.
    *   Potentially, quality or performance benchmarks.
*   **Why it's important:** Provides clarity on what constitutes a "done" version for a particular stage of development.
*   **Example (Instruction to AI):**
    *   "If present, ensure release criteria are clear and tied to features. *For example: 'MVP Release Criteria: 1. User registration and login. 2. Ability to create and edit PRD documents using a Markdown editor. 3. Basic AI assistance for generating PRD sections (Introduction, User Personas).' or 'V1 Release Criteria: All MVP features + AI-assisted User Story generation with Gherkin ACs + GitHub Issue integration.'* If this section is missing, you might suggest its addition if the PRD implies different release phases."

---

## Final Check for AI Agent

*   After revising, reread the entire PRD. Does it tell a coherent story?
*   Is it clear *why* this product should be built and *what* it fundamentally aims to do?
*   Are there any internal contradictions or ambiguities?
*   Is the language professional, clear, and engaging?