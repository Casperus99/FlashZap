import pytest
from unittest.mock import patch, MagicMock

from flash_zap.services.ai_grader import grade_answer
from flash_zap.core.exceptions import AIGraderError

@patch('flash_zap.services.ai_grader.genai.GenerativeModel')
def test_grade_answer_returns_correct_for_positive_ai_response(mock_generative_model):
    """
    Tests if grade_answer returns 'Correct' for a positive AI response.
    """
    # Arrange
    mock_model_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Result: Correct\nFeedback: Great job!"
    mock_model_instance.generate_content.return_value = mock_response
    mock_generative_model.return_value = mock_model_instance

    user_answer = "The capital of France is Paris."
    correct_answer = "Paris is the capital of France."

    # Act
    result, feedback = grade_answer(user_answer, correct_answer)

    # Assert
    assert result == "Correct"
    assert feedback == "Great job!"
    mock_model_instance.generate_content.assert_called_once()

@patch('flash_zap.services.ai_grader.genai.GenerativeModel')
def test_grade_answer_returns_incorrect_for_negative_ai_response(mock_generative_model):
    """
    Tests if grade_answer returns 'Incorrect' for a negative AI response.
    """
    # Arrange
    mock_model_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Result: Incorrect\nFeedback: Not quite, try again."
    mock_model_instance.generate_content.return_value = mock_response
    mock_generative_model.return_value = mock_model_instance

    user_answer = "The capital of France is Lyon."
    correct_answer = "Paris is the capital of France."

    # Act
    result, feedback = grade_answer(user_answer, correct_answer)

    # Assert
    assert result == "Incorrect"
    assert feedback == "Not quite, try again."
    mock_model_instance.generate_content.assert_called_once()

@patch('flash_zap.services.ai_grader.genai.GenerativeModel')
def test_grade_answer_raises_custom_exception_on_api_failure(mock_generative_model):
    """
    Tests if grade_answer raises AIGraderError on API failure.
    """
    # Arrange
    mock_model_instance = MagicMock()
    mock_model_instance.generate_content.side_effect = Exception("API is down")
    mock_generative_model.return_value = mock_model_instance

    user_answer = "any answer"
    correct_answer = "any correct answer"

    # Act & Assert
    with pytest.raises(AIGraderError, match="An error occurred while grading the answer: API is down"):
        grade_answer(user_answer, correct_answer)

    mock_model_instance.generate_content.assert_called_once() 