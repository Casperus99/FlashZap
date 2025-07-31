import uvicorn
from src.flash_zap.logger import setup_logging

if __name__ == "__main__":
    # Initialize logging for the web server
    setup_logging()
    
    # Configure uvicorn to not interfere with our logging
    uvicorn.run(
        "src.flash_zap.web.app:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_config=None,  # Disable uvicorn's logging config
        access_log=False  # Disable uvicorn access logs that might interfere
    ) 