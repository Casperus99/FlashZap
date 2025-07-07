"""
This module provides an AI-powered grading service using the Gemini API.
"""
import logging
import google.generativeai as genai
from flash_zap.config import settings
from flash_zap.core.exceptions import AIGraderError

# The Gemini client will automatically be configured with the API key
# from the GEMINI_API_KEY environment variable loaded by the settings.
genai.configure(api_key=settings.GEMINI_API_KEY)

def grade_answer(question: str, user_answer: str, correct_answer: str) -> tuple[str, str]:
    """
    Grades a user's answer against a correct answer using an AI model.

    Args:
        question: The question that was asked.
        user_answer: The answer provided by the user.
        correct_answer: The correct answer for the flashcard.

    Returns:
        A tuple containing the grade ("Correct" or "Incorrect") and feedback.

    Raises:
        AIGraderError: If the API call fails or the response is malformed.
    """
    model = genai.GenerativeModel(settings.AI_GRADER_MODEL_NAME)

    prompt = settings.AI_GRADER_PROMPT_TEMPLATE.format(
        question=question,
        correct_answer=correct_answer,
        user_answer=user_answer,
    )

    try:
        logging.info("Sending prompt to AI for grading.")
        logging.debug(f"AI Grader Prompt: {prompt}")
        generation_config = genai.GenerationConfig(temperature=0.1)
        response = model.generate_content(prompt, generation_config=generation_config)
        logging.info("Received response from AI.")
        logging.debug(f"AI Grader Response Text: {response.text}")
        
        lines = response.text.strip().split('\n')
        if len(lines) < 2 or not lines[0].startswith("Result:") or not lines[1].startswith("Feedback:"):
            raise AIGraderError("Malformed response from AI grader.")

        result = lines[0].replace("Result:", "").strip()
        feedback = lines[1].replace("Feedback:", "").strip()

        if result not in ["Correct", "Incorrect"]:
            raise AIGraderError(f"Unexpected result from AI grader: {result}")

        return result, feedback
    except Exception as e:
        logging.error("Error communicating with the AI grader.", exc_info=True)
        raise AIGraderError(f"An error occurred while grading the answer: {e}") 