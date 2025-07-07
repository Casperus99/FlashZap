from flash_zap.models.card import Card

def get_card_by_id(session, card_id):
    """
    Retrieves a card from the database by its ID.
    """
    return session.query(Card).filter_by(id=card_id).first() 