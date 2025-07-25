from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from flash_zap.core import card_manager
from flash_zap.core.review_session import ReviewSession
from flash_zap.services.import_service import import_cards_from_json
from flash_zap.config import SessionLocal
import uuid
import tempfile
import os
import logging

router = APIRouter()

# Initialize templates here to avoid circular import
templates = Jinja2Templates(directory="src/flash_zap/web/templates")

# Simple in-memory storage for active review sessions
active_sessions = {}


@router.get("/browse", response_class=HTMLResponse)
async def browse_form(request: Request):
    """Display form to enter card ID for browsing."""
    return templates.TemplateResponse(request=request, name="browse_form.html")


@router.get("/browse/{card_id}", response_class=HTMLResponse)
async def browse_card(request: Request, card_id: int):
    """Display a single card by ID with edit options."""
    db_session = SessionLocal()
    try:
        card = card_manager.get_card_by_id(db_session, card_id)
        return templates.TemplateResponse(
            request=request, 
            name="browse_card.html", 
            context={"card": card}
        )
    finally:
        db_session.close()


@router.post("/browse/{card_id}/edit-front")
async def edit_card_front(card_id: int, new_front: str = Form(...)):
    """Update the front of a card."""
    db_session = SessionLocal()
    try:
        card_manager.update_card_front(db_session, card_id, new_front)
        return RedirectResponse(url=f"/browse/{card_id}", status_code=302)
    finally:
        db_session.close()


@router.post("/browse/{card_id}/edit-back")
async def edit_card_back(card_id: int, new_back: str = Form(...)):
    """Update the back of a card."""
    db_session = SessionLocal()
    try:
        card_manager.update_card_back(db_session, card_id, new_back)
        return RedirectResponse(url=f"/browse/{card_id}", status_code=302)
    finally:
        db_session.close()


@router.post("/browse/{card_id}/edit-mastery")
async def edit_card_mastery(card_id: int, new_mastery_level: int = Form(...)):
    """Update the mastery level of a card."""
    db_session = SessionLocal()
    try:
        card_manager.update_card_mastery(db_session, card_id, new_mastery_level)
        return RedirectResponse(url=f"/browse/{card_id}", status_code=302)
    finally:
        db_session.close()


@router.get("/review", response_class=HTMLResponse)
async def start_review_session(request: Request):
    """Start or continue a review session."""
    db_session = SessionLocal()
    try:
        # Create a new review session
        review_session = ReviewSession(db_session)
        
        # Get the first card
        card = review_session.get_next_card()
        
        if not card:
            # No cards due for review
            return templates.TemplateResponse(
                request=request, 
                name="review_no_cards.html"
            )
        
        # Generate session ID and store the session
        session_id = str(uuid.uuid4())
        active_sessions[session_id] = review_session
        
        # Render the first card
        response = templates.TemplateResponse(
            request=request, 
            name="review_card.html", 
            context={
                "card": card,
                "remaining_count": review_session.remaining_cards_count
            }
        )
        response.set_cookie("session_id", session_id)
        return response
    finally:
        # Don't close the session yet as it's stored in review_session
        pass


@router.post("/review")
async def process_review_answer(request: Request, user_answer: str = Form(None), action: str = Form("submit_answer")):
    """Process user's answer or continue to next card."""
    # Get session ID from cookie
    session_id = request.cookies.get("session_id")
    
    if not session_id or session_id not in active_sessions:
        # Session not found, redirect to start
        return RedirectResponse(url="/review", status_code=302)
    
    review_session = active_sessions[session_id]
    
    if action == "continue":
        # Move to next card after feedback
        next_card = review_session.get_next_card()
        
        if next_card:
            # More cards to review
            return templates.TemplateResponse(
                request=request, 
                name="review_card.html", 
                context={
                    "card": next_card,
                    "remaining_count": review_session.remaining_cards_count
                }
            )
        else:
            # Session complete
            del active_sessions[session_id]
            return templates.TemplateResponse(
                request=request, 
                name="review_summary.html"
            )
    
    else:  # action == "submit_answer" or default
        current_card = review_session.get_next_card()
        
        if not current_card or not user_answer:
            # No card to grade, redirect to start
            return RedirectResponse(url="/review", status_code=302)
        
        try:
            # Grade the answer and update the card
            grade, feedback, old_mastery_level, new_mastery_level = review_session.grade_and_update_card(current_card, user_answer)
            


            # Show feedback but stay on same card
            return templates.TemplateResponse(
                request=request,
                name="review_card.html",
                context={
                    "card": current_card,
                    "remaining_count": review_session.remaining_cards_count,
                    "grade": grade,
                    "feedback": feedback,
                    "show_feedback": True,
                    "user_answer": user_answer,
                    "old_mastery_level": old_mastery_level,
                    "new_mastery_level": new_mastery_level
                }
            )
        except Exception as e:
            # Handle grading errors
            logging.error(f"Error in grade_and_update_card: {e}", exc_info=True)
            return templates.TemplateResponse(
                request=request,
                name="review_card.html",
                context={
                    "card": current_card,
                    "remaining_count": review_session.remaining_cards_count,
                    "error": "Grading service temporarily unavailable"
                }
            )


@router.get("/import", response_class=HTMLResponse)
async def import_form(request: Request):
    """Display form for JSON file upload."""
    return templates.TemplateResponse(request=request, name="import_form.html")


@router.post("/import")
async def process_import(request: Request, file: UploadFile = File(...)):
    """Process uploaded JSON file and import cards."""
    db_session = SessionLocal()
    try:
        # Read file content
        content = await file.read()
        
        # Save to temporary file (import_service expects file path)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write(content.decode('utf-8'))
            temp_path = temp_file.name
        
        try:
            # Call existing import service with file path
            import_cards_from_json(db_session, temp_path)
            
            # Success
            return templates.TemplateResponse(
                request=request, 
                name="import_result.html", 
                context={"success": True, "message": "Cards imported successfully!"}
            )
        except Exception as e:
            # Import failed
            return templates.TemplateResponse(
                request=request, 
                name="import_result.html", 
                context={"success": False, "message": f"Import failed: {str(e)}"}
            )
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    finally:
        db_session.close() 