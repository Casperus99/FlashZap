import uvicorn
from src.flash_zap.logger import setup_logging

if __name__ == "__main__":
    # Initialize logging for the web server
    setup_logging()
    uvicorn.run("src.flash_zap.web.app:app", host="127.0.0.1", port=8000, reload=True) 