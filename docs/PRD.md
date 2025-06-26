# Product Requirements Document: FlashZap

*   **Version:** 0.1
*   **Author:** Kacper Nowakowski

## **1. Introduction / Overview**

### **1.1 The Problem**

Traditional digital flashcard applications are often insufficient for deep, long-term learning. Their primary limitations are a lack of robust Spaced Repetition System (SRS) algorithms and, more critically, an inability to effectively handle open-ended questions. Current solutions force the user to self-grade their answers, which can be subjective, inconsistent, and a cognitive burden that detracts from the learning process itself.

### **1.2 The Solution**

This document outlines the requirements for a personal, terminal-based flashcard application designed to create a more efficient and objective learning experience. The application will leverage a configurable SRS algorithm to schedule card reviews optimally. Its core feature is an AI-powered grading system that evaluates the user's open-ended answers against the correct answer, providing objective feedback and eliminating the need for manual self-assessment.

### **1.3 Target User**

The initial and primary user is a software developer who is a lifelong learner, aiming to enhance memory and build knowledge across a wide variety of domains—from technical subjects like programming languages to general knowledge topics like health and languages.

## **2. Goals / Objectives**

### **2.1 Primary Goal**

The primary goal of this application is to establish a consistent and efficient daily learning habit for the user. The tool should be compelling and effective enough to be integrated into the user's regular routine.

### **2.2 Key Objectives & Success Metrics**

Success for this application will be measured by the following key objectives:

*   **Review Cadence:** The user successfully reviews an average of at least 100 flashcards per day.
*   **Knowledge Base Expansion:** The user adds an average of at least 20 new flashcards per week.

### **2.3 Non-Functional Goals**

*   **Performance:** The application's terminal user interface (TUI) must be highly responsive. All user interactions, from navigating cards to submitting answers, should feel instantaneous to ensure a fluid and frustration-free experience.

---

## **3. Epics**

### **3.1 Epic: Card Lifecycle Management**

This epic covers the entire process of populating the application with learning material. The core functionality is the ability to import flashcards into the local PostgreSQL database. From the main terminal menu, the user will select an "Import Flashcards" option. The application will then prompt for a file path. The user provides the path to a JSON file containing an array of card objects. The system will parse this file and persist the new cards in the database.

### **3.2 Epic: AI-Powered Learning Session**

This epic represents the primary user activity: the interactive study session. The user will initiate a session by selecting a "Review" option from the main menu. The application will then present the front of a card that is due for review according to the SRS schedule. The user types their answer in the terminal. This answer, along with the correct answer from the card's back, is sent to an external AI service for evaluation. The AI's grade and feedback are displayed to the user before the application proceeds to the next due card.

### **3.3 Epic: Spaced Repetition System (SRS) Engine**

This epic encompasses the underlying logic that powers the learning schedule. The system will implement an SRS algorithm to track the user's performance on each card and calculate the optimal date for the next review. A crucial part of this epic is configurability. The user must be able to easily modify the SRS parameters, specifically the sequence of time intervals (e.g., 1 day, 3 days, 7 days, etc.) that determine a card's review schedule.