from flash_zap.models.card import Card

def get_card_by_id(session, card_id):
    """
    Retrieves a card from the database by its ID.
    """
    return session.query(Card).filter_by(id=card_id).first()

def update_card_front(session, card_id, new_front):
    """
    Updates the front of a card.
    """
    card = get_card_by_id(session, card_id)
    if card:
        card.front = new_front
        session.commit()
    return card

def update_card_back(session, card_id, new_back):
    """
    Updates the back of a card.
    """
    card = get_card_by_id(session, card_id)
    if card:
        card.back = new_back
        session.commit()
    return card

def update_card_mastery(session, card_id, new_mastery_level):
    """
    Updates the mastery level of a card, ensuring the new level is not higher than the current one.
    """
    card = get_card_by_id(session, card_id)
    if card:
        if new_mastery_level <= card.mastery_level:
            card.mastery_level = new_mastery_level
            session.commit()
            return card, True
        else:
            return card, False
    return None, False


def delete_card(session, card_id):
    """
    Deletes a card from the database by its ID.
    Returns True if the card was successfully deleted, False otherwise.
    """
    card = get_card_by_id(session, card_id)
    if card:
        session.delete(card)
        session.commit()
        return True
    return False 


def get_all_cards_paginated(session, page=1, per_page=30):
    """
    Retrieves cards from the database with pagination.
    
    Args:
        session: Database session
        page: Page number (1-based)
        per_page: Number of cards per page
        
    Returns:
        tuple: (cards, total_count, current_page, total_pages)
    """
    # Calculate offset
    offset = (page - 1) * per_page
    
    # Get total count
    total_count = session.query(Card).count()
    
    # Calculate total pages
    total_pages = (total_count + per_page - 1) // per_page  # Ceiling division
    
    # Get cards for current page
    cards = session.query(Card).offset(offset).limit(per_page).all()
    
    return cards, total_count, page, total_pages 