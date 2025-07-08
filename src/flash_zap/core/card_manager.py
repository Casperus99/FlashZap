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