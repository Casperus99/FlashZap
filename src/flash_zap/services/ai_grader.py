"""
This module provides an AI-powered grading service using the Gemini API.
"""
import google.generativeai as genai
from flash_zap.config import settings
from flash_zap.core.exceptions import AIGraderError

# The Gemini client will automatically be configured with the API key
# from the GEMINI_API_KEY environment variable loaded by the settings.
genai.configure(api_key=settings.GEMINI_API_KEY)

def grade_answer(user_answer: str, correct_answer: str) -> tuple[str, str]:
    """
    Grades a user's answer against a correct answer using an AI model.

    Args:
        user_answer: The answer provided by the user.
        correct_answer: The correct answer for the flashcard.

    Returns:
        A tuple containing the grade ("Correct" or "Incorrect") and feedback.

    Raises:
        AIGraderError: If the API call fails or the response is malformed.
    """
    model = genai.GenerativeModel(settings.AI_GRADER_MODEL_NAME)

    prompt = f"""
    You are an AI assistant for a flashcard application. Your task is to evaluate a user's answer to a flashcard question.

    The user was given the front of a flashcard and provided an answer. You need to compare their answer to the correct answer (the back of the flashcard) and determine if it is "Correct" or "Incorrect".

    - **Correct**: The user's answer is semantically equivalent to the correct answer. Minor differences in phrasing are acceptable.
    - **Incorrect**: The user's answer is wrong.

    Provide a brief, encouraging, and helpful feedback message.

    **Correct Answer:** "{correct_answer}"
    **User's Answer:** "{user_answer}"

    **Output format:**
    Result: [Correct/Incorrect]
    Feedback: [Your feedback here]
    """

    try:
        response = model.generate_content(prompt)
        
        lines = response.text.strip().split('\n')
        if len(lines) < 2 or not lines[0].startswith("Result:") or not lines[1].startswith("Feedback:"):
            raise AIGraderError("Malformed response from AI grader.")

        result = lines[0].replace("Result:", "").strip()
        feedback = lines[1].replace("Feedback:", "").strip()

        if result not in ["Correct", "Incorrect"]:
            raise AIGraderError(f"Unexpected result from AI grader: {result}")

        return result, feedback
    except Exception as e:
        raise AIGraderError(f"An error occurred while grading the answer: {e}") 