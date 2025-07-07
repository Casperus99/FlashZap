import readchar
from flash_zap.core.card_manager import get_card_by_id

def show_card_view(session):
    """Prompts user for a card ID and displays the card details."""
    card_id_str = input("Enter the ID of the card you want to view: ")

    try:
        card_id = int(card_id_str)
        card = get_card_by_id(session, card_id)

        if card:
            print("--- Card Details ---")
            print(f"ID: {card.id}")
            print(f"Front: {card.front}")
            print(f"Back: {card.back}")
            print(f"Mastery Level: {card.mastery_level}")
            print(f"Next Review: {card.next_review_date}")
            print("--------------------")
        else:
            print("Card not found.")

    except ValueError:
        print("Invalid ID. Please enter a number.")
    
    # Wait for user to press a key before returning
    print("\nPress any key to return to the main menu...")
    readchar.readkey()

    # The rest of the view logic, including the final "press enter" prompt,
    # will be implemented in subsequent tasks. 