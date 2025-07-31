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
    logging.info(f"Browsing card ID {card_id}")
    
    db_session = SessionLocal()
    try:
        card = card_manager.get_card_by_id(db_session, card_id)
        if card:
            logging.info(f"Successfully retrieved card ID {card_id} for browsing")
        else:
            logging.warning(f"Card ID {card_id} not found")
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
    logging.info(f"Updating front text for card ID {card_id}")
    
    db_session = SessionLocal()
    try:
        card_manager.update_card_front(db_session, card_id, new_front)
        logging.info(f"Successfully updated front text for card ID {card_id}")
        return RedirectResponse(url=f"/browse/{card_id}", status_code=302)
    except Exception as e:
        logging.error(f"Error updating front text for card ID {card_id}: {e}", exc_info=True)
        raise
    finally:
        db_session.close()


@router.post("/browse/{card_id}/edit-back")
async def edit_card_back(card_id: int, new_back: str = Form(...)):
    """Update the back of a card."""
    logging.info(f"Updating back text for card ID {card_id}")
    
    db_session = SessionLocal()
    try:
        card_manager.update_card_back(db_session, card_id, new_back)
        logging.info(f"Successfully updated back text for card ID {card_id}")
        return RedirectResponse(url=f"/browse/{card_id}", status_code=302)
    except Exception as e:
        logging.error(f"Error updating back text for card ID {card_id}: {e}", exc_info=True)
        raise
    finally:
        db_session.close()


@router.post("/browse/{card_id}/edit-mastery")
async def edit_card_mastery(card_id: int, new_mastery_level: int = Form(...)):
    """Update the mastery level of a card."""
    logging.info(f"Updating mastery level for card ID {card_id} to level {new_mastery_level}")
    
    db_session = SessionLocal()
    try:
        card_manager.update_card_mastery(db_session, card_id, new_mastery_level)
        logging.info(f"Successfully updated mastery level for card ID {card_id} to level {new_mastery_level}")
        return RedirectResponse(url=f"/browse/{card_id}", status_code=302)
    except Exception as e:
        logging.error(f"Error updating mastery level for card ID {card_id}: {e}", exc_info=True)
        raise
    finally:
        db_session.close()


@router.post("/browse/{card_id}/remove")
async def remove_card(card_id: int, confirm: str = Form(None)):
    """Remove a card after confirmation."""
    logging.info(f"Card removal requested for card ID {card_id} with confirmation: {confirm}")
    
    db_session = SessionLocal()
    try:
        if confirm == "yes":
            card_manager.delete_card(db_session, card_id)
            logging.info(f"Successfully deleted card ID {card_id}")
            return RedirectResponse(url="/browse", status_code=302)
        else:
            # No confirmation, redirect back to card
            logging.info(f"Card removal cancelled for card ID {card_id} - no confirmation")
            return RedirectResponse(url=f"/browse/{card_id}", status_code=302)
    except Exception as e:
        logging.error(f"Error deleting card ID {card_id}: {e}", exc_info=True)
        raise
    finally:
        db_session.close()


@router.get("/review", response_class=HTMLResponse)
async def start_review_session(request: Request):
    """Start or continue a review session."""
    logging.info("Starting new review session")
    
    db_session = SessionLocal()
    try:
        # Create a new review session
        review_session = ReviewSession(db_session)
        
        # Get the first card
        card = review_session.get_next_card()
        
        if not card:
            # No cards due for review
            logging.info("No cards due for review - showing no cards page")
            return templates.TemplateResponse(
                request=request, 
                name="review_no_cards.html"
            )
        
        # Generate session ID and store the session
        session_id = str(uuid.uuid4())
        active_sessions[session_id] = review_session
        
        logging.info(f"Review session created with {review_session.remaining_cards_count} cards. Session ID: {session_id[:8]}...")
        
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
    
    # Get session ID from cookie
    session_id = request.cookies.get("session_id")
    session_short_id = session_id[:8] + "..." if session_id else "unknown"
    
    logging.info(f"Processing review action '{action}' for session {session_short_id}")
    
    if not session_id or session_id not in active_sessions:
        # Session not found, redirect to start
        logging.warning(f"Review session {session_short_id} not found - redirecting to start")
        return RedirectResponse(url="/review", status_code=302)
    
    review_session = active_sessions[session_id]
    
    if action == "continue":
        # Move to next card after feedback
        logging.info(f"Continuing to next card in session {session_short_id}")
        next_card = review_session.get_next_card()
        
        if next_card:
            # More cards to review
            logging.info(f"Showing next card (ID: {next_card.id}) - {review_session.remaining_cards_count} cards remaining")
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
            logging.info(f"Review session {session_short_id} completed - all cards reviewed")
            return templates.TemplateResponse(
                request=request, 
                name="review_summary.html"
            )
    
    else:  # action == "submit_answer" or default
        current_card = review_session.get_next_card()
        
        if not current_card or not user_answer:
            # No card to grade, redirect to start
            logging.warning(f"No card to grade or missing answer in session {session_short_id}")
            return RedirectResponse(url="/review", status_code=302)
        
        logging.info(f"Grading answer for card ID {current_card.id} in session {session_short_id}")
        
        try:
            # Grade the answer and update the card
            grade, feedback, old_mastery_level, new_mastery_level = review_session.grade_and_update_card(current_card, user_answer)
            
            logging.info(f"Card ID {current_card.id} graded as '{grade}' - mastery level {old_mastery_level} → {new_mastery_level}")

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
            logging.error(f"Error grading card ID {current_card.id} in session {session_short_id}: {e}", exc_info=True)
            return templates.TemplateResponse(
                request=request,
                name="review_card.html",
                context={
                    "card": current_card,
                    "remaining_count": review_session.remaining_cards_count,
                    "error": "Grading service temporarily unavailable"
                }
            )


@router.get("/add-cards", response_class=HTMLResponse)
async def add_cards_form(request: Request):
    """Display comprehensive form for adding flashcards."""
    return templates.TemplateResponse(request=request, name="add_cards.html")


@router.post("/add-cards")
async def process_add_cards(request: Request):
    """Process card addition (manual or JSON import)."""
    from flash_zap.models.card import Card
    
    logging.info("POST /add-cards endpoint called - starting card processing")
    
    db_session = SessionLocal()
    try:
        # Get form data and files
        form = await request.form()
        
        # Check if this is a file upload (JSON import)
        if "json_file" in form and form["json_file"].filename:
            # Handle JSON import
            json_file = form["json_file"]
            
            try:
                # Read and parse JSON content
                content = await json_file.read()
                import json
                cards_data = json.loads(content.decode('utf-8'))
                
                # Validate JSON structure
                if not isinstance(cards_data, list):
                    raise ValueError("JSON must be a list of card objects")
                
                for card in cards_data:
                    if not isinstance(card, dict) or "front" not in card or "back" not in card:
                        raise ValueError("Each card must have 'front' and 'back' fields")
                
                # Return template with imported cards as editable forms
                return templates.TemplateResponse(
                    request=request,
                    name="add_cards.html",
                    context={
                        "imported_cards": cards_data,
                        "show_imported_form": True
                    }
                )
                
            except json.JSONDecodeError:
                return templates.TemplateResponse(
                    request=request,
                    name="add_cards.html",
                    context={"error": "Invalid JSON file format"}
                )
            except ValueError as e:
                return templates.TemplateResponse(
                    request=request,
                    name="add_cards.html",
                    context={"error": str(e)}
                )
        else:
            # Handle manual card creation
            logging.info("Starting manual card creation process.")
            
            # Extract card pairs from form data
            cards_to_create = []
            i = 0
            while f"front_{i}" in form and f"back_{i}" in form:
                front = form[f"front_{i}"].strip()
                back = form[f"back_{i}"].strip()
                
                # Skip empty pairs
                if front and back:
                    cards_to_create.append({"front": front, "back": back})
                    logging.debug(f"Prepared card {len(cards_to_create)}: '{front}' -> '{back}'")
                i += 1
            
            logging.info(f"Found {len(cards_to_create)} valid card pairs to create.")
            
            # Validate we have at least one card
            if not cards_to_create:
                logging.warning("No valid card pairs found in form data.")
                # Return to form with error
                return templates.TemplateResponse(
                    request=request,
                    name="add_cards.html",
                    context={"error": "Please fill in at least one complete card pair."}
                )
            
            # Create cards in database
            logging.info("Creating cards in database.")
            for i, card_data in enumerate(cards_to_create, 1):
                new_card = Card(
                    front=card_data["front"],
                    back=card_data["back"],
                    mastery_level=0
                )
                db_session.add(new_card)
                logging.debug(f"Added card {i} to database session.")
            
            db_session.commit()
            logging.info(f"Successfully saved {len(cards_to_create)} cards to the database.")
            
            # Redirect to success page
            return RedirectResponse(url="/", status_code=302)
    
    except Exception as e:
        logging.error(f"Error in process_add_cards: {e}", exc_info=True)
        db_session.rollback()
        return templates.TemplateResponse(
            request=request,
            name="add_cards.html",
            context={"error": f"An error occurred: {str(e)}"}
        )
    finally:
        db_session.close()


@router.get("/import", response_class=HTMLResponse)
async def import_form(request: Request):
    """Display form for JSON file upload."""
    return templates.TemplateResponse(request=request, name="import_form.html")


@router.post("/import")
async def process_import(request: Request, file: UploadFile = File(...)):
    """Process uploaded JSON file and import cards."""
    logging.info(f"Starting JSON import process for file: {file.filename}")
    
    db_session = SessionLocal()
    try:
        # Read file content
        content = await file.read()
        logging.info(f"Successfully read {len(content)} bytes from uploaded file")
        
        # Save to temporary file (import_service expects file path)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write(content.decode('utf-8'))
            temp_path = temp_file.name
        
        try:
            # Call existing import service with file path
            logging.info("Calling import service to process cards")
            import_cards_from_json(db_session, temp_path)
            
            logging.info("JSON import completed successfully")
            # Success
            return templates.TemplateResponse(
                request=request, 
                name="import_result.html", 
                context={"success": True, "message": "Cards imported successfully!"}
            )
        except Exception as e:
            # Import failed
            logging.error(f"JSON import failed: {e}", exc_info=True)
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