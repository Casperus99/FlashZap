import subprocess
import sys
import time
import httpx
import pytest
import os

@pytest.mark.skipif(not os.path.exists("run_web.py"), reason="run_web.py not created yet")
def test_run_web_script_starts_server():
    """
    GIVEN: The run_web.py script exists.
    WHEN: The script is executed with python.
    THEN: The FastAPI server starts and is accessible.
    """
    # GIVEN
    script_path = "run_web.py"
    python_executable = sys.executable
    
    # WHEN
    # Run the script as a separate process
    process = subprocess.Popen([python_executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Give the server a moment to start
    time.sleep(3)

    # THEN
    try:
        # Check if the process is still running and the server is responsive
        assert process.poll() is None, f"Server process terminated prematurely. stderr: {process.stderr.read().decode()}"

        with httpx.Client() as client:
            response = client.get("http://127.0.0.1:8000/")
        
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to FlashZap Web UI!"}

    finally:
        # Clean up the server process
        process.terminate()
        process.wait() 