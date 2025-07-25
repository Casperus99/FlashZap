from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Initialize the FastAPI application
app = FastAPI(title="FlashZap")

# Configure the path to static files (CSS, JS)
app.mount("/static", StaticFiles(directory="src/flash_zap/web/static"), name="static")

# Configure the Jinja2 template engine
templates = Jinja2Templates(directory="src/flash_zap/web/templates")

# Import and include routes
from flash_zap.web.routes import router
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def main_menu(request: Request):
    return templates.TemplateResponse(request=request, name="main_menu.html") 