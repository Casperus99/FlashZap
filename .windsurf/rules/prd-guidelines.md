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

### 1. Introduction / Overview

*   **Purpose:** To provide a brief, high-level summary of the product and the problem it solves.
*   **What it should consist of:**
    *   A concise statement of what the product is.
    *   The primary problem the product aims to solve for its users.
    *   The core value proposition.
*   **Why it's important:** Sets the stage and immediately orients the reader (and AI) to the product's fundamental purpose.
*   **Instruction to AI:**
    *   Ensure this section clearly answers: What is this product? What main problem does it solve? What's its unique benefit?
    *   For example: 'Project Scribe is a web application designed to help solo developers efficiently manage and collaborate on project documentation with AI assistance. It solves the problem of disorganized, outdated, or insufficient documentation in solo-led projects by providing structured templates and AI-powered generation and maintenance tools. Its core value is enabling faster development cycles and better long-term project maintainability through intelligent documentation.' Rewrite to be as clear and impactful as this example.

### 2. Vision Statement

*   **Purpose:** To articulate the long-term desired future state or impact of the product.
*   **What it should consist of:**
    *   An aspirational, forward-looking statement.
    *   What the product aims to become or achieve in the long run.
*   **Why it's important:** Provides a guiding star for all product decisions and helps maintain focus on the bigger picture.
*   **Instruction to AI:**
    *   This section should paint a picture of the product's ultimate aspiration.
    *    For example: 'Our vision for Project Scribe is to become the indispensable AI-first documentation companion for every solo innovator, transforming documentation from a chore into a strategic accelerator for software creation.' Verify the existing statement is aspirational and long-term focused, or propose a revision.

### 3. Target Audience / User Personas

*   **Purpose:** To clearly define who the product is for.
*   **What it should consist of:**
    *   Detailed descriptions of primary (and potentially secondary) user personas.
    *   Include: demographics (if relevant), needs, pain points, motivations, technical proficiency, and how they might interact with the product.
*   **Why it's important:** All product decisions should be made with the target user in mind. This section ensures a shared understanding of who that is.
*   **Example (Instruction to AI):**
    *   "For each persona, ensure it includes: Name, Role/Archetype, Key Goals (related to the product), Frustrations/Pain Points (that the product solves), and a brief Scenario of Use. *For example: 'Persona: Alex, the Solo SaaS Developer. Goals: Quickly bootstrap new projects, maintain clear documentation for future self or potential collaborators, minimize time spent on non-coding tasks. Frustrations: Documentation quickly becomes outdated; context switching between code and docs is inefficient.'* If personas are vague, suggest adding these details."

### 4. Key Features / Epics

*   **Purpose:** To list and briefly describe the major functionalities or modules of the product.
*   **What it should consist of:**
    *   A high-level list of core features (often called "Epics" in Agile).
    *   A brief (1-2 sentence) description for each, explaining its value to the user or its purpose.
    *   (Optional) High-level prioritization (e.g., Must-have, Should-have, Could-have).
*   **Why it's important:** Outlines the "What" of the product at a high level, forming the basis for more detailed User Stories later.
*   **Example (Instruction to AI):**
    *   "Ensure this is a list of *major* capabilities, not granular tasks. *For example: '1. AI-Powered Documentation Generation: Users can generate initial drafts of PRDs, User Stories, and technical specs based on high-level inputs. 2. Real-time Documentation Sync: Changes in linked code repositories can trigger suggestions for documentation updates. 3. Collaborative Editing (Future): Allows multiple users to work on documentation simultaneously.'* Check if descriptions clearly state the value/purpose. If prioritization is missing and seems beneficial, suggest adding it."

### 5. Additional Functional Requirements

*   **Purpose:** To detail other necessary functional requirements that support the main epics, cut across multiple features, or provide important secondary value. This section captures functionalities that aren't large enough to be an epic but are crucial for a complete product experience.
*   **What it should consist of:**
    *   A list of supporting functionalities.
    *   Examples include: Search, User Profile Management, Notification System, User Onboarding Tour, Integrations with specific third-party tools, Admin Panels, Reporting/Analytics.
    *   Each item should have a brief description of its purpose and scope.
*   **Why it's important:** This ensures that "smaller" but often complex and critical features are not forgotten during high-level planning. Forgetting a robust search or a notification system can negatively impact the user experience and lead to scope creep later.
*   **Instruction to AI:**
    *   Review the list to ensure these are genuine supporting features, not core epics in disguise. A core epic delivers a primary piece of the value proposition; a supporting feature enables or enhances that experience.
    *   For example: For "Project Scribe", *'AI-Powered Documentation Generation'* is a **Key Feature/Epic**. *'Full-Text Search within Documents'* is an **Additional Functional Feature**.
    *   If a major capability is listed here, suggest moving it to the "Key Features / Epics" section. If the section is empty but the product implies the need for things like search or user settings, suggest adding them here.

### 6. Non-functional Requirements

*   **Purpose:** To define the quality attributes, constraints, and operational characteristics of the system. This section describes *how well* the system should perform its functions, rather than *what* functions it performs.
*   **What it should consist of:**
    *   A list of requirements categorized by type. Common categories include:
        *   **Performance:** Response times, load capacity (e.g., "Page loads in under 2 seconds," "System supports 100 concurrent users").
        *   **Security:** Authentication, data encryption, access control (e.g., "All user data at rest must be encrypted with AES-256").
        *   **Scalability:** How the system will handle growth (e.g., "The architecture must support horizontal scaling to accommodate a 10x user increase over one year").
        *   **Usability / Accessibility:** Ease of use, and compliance with standards like WCAG (e.g., "The UI must be navigable using only a keyboard").
        *   **Reliability:** Uptime, data integrity, error handling (e.g., "The service must maintain 99.9% uptime").
*   **Why it's important:** Non-functional requirements are critical for user satisfaction, technical feasibility, and long-term success. They directly influence architectural decisions, development effort, and infrastructure costs.
*   **Instruction to AI:**
    *   Ensure requirements in this section are specific, measurable, and testable where possible. Vague statements should be flagged.
    *   For example, change *'The application should be fast'* to *'Performance: AI-generated document drafts must be produced in under 10 seconds for a standard PRD template.'*
    *   If this section is missing or sparse, suggest its creation and propose standard categories (Performance, Security, Reliability) as a starting point, explaining why they are crucial for defining the product's quality and guiding the technical team.

## Final Check for AI Agent

*   After revising, reread the entire PRD. Does it tell a coherent story?
*   Is it clear *why* this product should be built and *what* it fundamentally aims to do?
*   Are there any internal contradictions or ambiguities?
*   Is the language professional, clear, and engaging?