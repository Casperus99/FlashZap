from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Initialize the FastAPI application
app = FastAPI(title="FlashZap")

# Configure the path to static files (CSS, JS)
app.mount("/static", StaticFiles(directory="src/flash_zap/web/static"), name="static")

# Configure the Jinja2 template engine
templates = Jinja2Templates(directory="src/flash_zap/web/templates")

@app.get("/")
async def root():
    return {"message": "Welcome to FlashZap Web UI!"} 