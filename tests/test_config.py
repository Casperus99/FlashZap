import os
from unittest.mock import patch

import pytest


def test_config_loads_gemini_api_key():
    """
    Tests that the Settings class correctly loads the GEMINI_API_KEY
    from environment variables.
    """
    # Arrange
    api_key = "test-api-key"
    with patch.dict(os.environ, {"GEMINI_API_KEY": api_key}):
        # Import inside the context manager to avoid collection-time errors
        from flash_zap.config import Settings
        # Act
        settings = Settings()
        # Assert
        assert settings.GEMINI_API_KEY == api_key


def test_ai_grader_model_name_default_and_override():
    """
    Tests that AI_GRADER_MODEL_NAME has a correct default and can be
    overridden by an environment variable.
    """
    # Arrange
    # Import inside the context manager to avoid collection-time errors
    from flash_zap.config import Settings
    
    # Act (Default)
    # We need to provide a dummy value for the required GEMINI_API_KEY
    with patch.dict(os.environ, {"GEMINI_API_KEY": "dummy-key"}):
        settings_default = Settings()

    # Assert (Default)
    assert settings_default.AI_GRADER_MODEL_NAME == "gemini-2.5-flash-lite-preview-06-17"

    # Arrange (Override)
    model_name = "test-model-name"
    with patch.dict(os.environ, {"AI_GRADER_MODEL_NAME": model_name, "GEMINI_API_KEY": "dummy-key"}):
        # Act (Override)
        settings_override = Settings()
    
    # Assert (Override)
    assert settings_override.AI_GRADER_MODEL_NAME == model_name 