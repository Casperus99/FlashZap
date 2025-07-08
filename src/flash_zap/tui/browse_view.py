import readchar

from flash_zap.core.card_manager import (
    get_card_by_id,
    update_card_front,
    update_card_back,
    update_card_mastery,
)
from flash_zap.utils.terminal import clear_screen


def show_card_view(session):
    """Shows a detailed view of a single card for viewing or editing."""
    clear_screen()
    try:
        card_id_str = input("Enter the ID of the card you want to view: ")
        card_id = int(card_id_str)
        card = get_card_by_id(session, card_id)

        if card:
            while True:
                clear_screen()
                print("--- Card Details ---")
                print(f"ID: {card.id}")
                print(f"Front: {card.front}")
                print(f"Back: {card.back}")
                print(f"Mastery Level: {card.mastery_level}")
                print(f"Next Review: {card.next_review_date}")
                print("--------------------")

                print("\n--- Edit Options ---")
                print("1. Edit front")
                print("2. Edit back")
                print("3. Lower mastery level")
                print("4. Cancel")
                print("--------------------")

                choice = readchar.readkey()

                if choice == "1":
                    clear_screen()
                    print(f"Current front: {card.front}")
                    new_front = input("Enter the new text for the front: ")
                    update_card_front(session, card.id, new_front)
                    card.front = new_front
                    print("Card front updated successfully.")
                    print("\nPress any key to continue...")
                    readchar.readkey()
                elif choice == "2":
                    clear_screen()
                    print(f"Current back: {card.back}")
                    new_back = input("Enter the new text for the back: ")
                    update_card_back(session, card.id, new_back)
                    card.back = new_back
                    print("Card back updated successfully.")
                    print("\nPress any key to continue...")
                    readchar.readkey()
                elif choice == "3":
                    clear_screen()
                    print(f"Current mastery level: {card.mastery_level}")
                    new_mastery_level_str = input("Enter the new mastery level: ")
                    try:
                        new_mastery_level = int(new_mastery_level_str)
                        if new_mastery_level <= card.mastery_level:
                            update_card_mastery(
                                session, card.id, new_mastery_level
                            )
                            card.mastery_level = new_mastery_level
                            print("Mastery level updated successfully.")
                        else:
                            print(
                                "New mastery level cannot be higher than the current one."
                            )
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                    print("\nPress any key to continue...")
                    readchar.readkey()
                elif choice == "4":
                    break
        else:
            print("Card not found.")
            print("\nPress any key to return to the main menu...")
            readchar.readkey()

    except ValueError:
        print("Invalid ID. Please enter a number.")
        print("\nPress any key to return to the main menu...")
        readchar.readkey() 