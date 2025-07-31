import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from datetime import date


def test_browse_form_endpoint_returns_200(client: TestClient):
    """
    GIVEN: The FastAPI application is running.
    WHEN: A GET request is made to the /browse endpoint.
    THEN: The response should redirect to the browse list.
    """
    # WHEN
    response = client.get("/browse", follow_redirects=False)

    # THEN
    assert response.status_code == 302
    assert "/browse/list" in response.headers["location"]


def test_browse_redirects_to_list_view(client: TestClient):
    """
    GIVEN: The FastAPI application is running.
    WHEN: A GET request is made to /browse.
    THEN: The user should be redirected to the browse list view.
    """
    # WHEN
    response = client.get("/browse", follow_redirects=True)
    soup = BeautifulSoup(response.text, 'html.parser')

    # THEN
    assert response.status_code == 200
    # Should see the browse list page with card grid
    card_grid = soup.find(class_='card-grid')
    # Grid might be empty but should exist
    assert card_grid is not None or "No cards found" in response.text


@patch("flash_zap.web.routes.card_manager")
def test_browse_card_endpoint_calls_card_manager(mock_card_manager, client: TestClient):
    """
    GIVEN: A card ID and mocked card_manager.
    WHEN: A GET request is made to /browse/{card_id}.
    THEN: card_manager.get_card_by_id should be called with correct parameters.
    """
    # GIVEN
    card_id = 1
    mock_card = MagicMock()
    mock_card.id = 1
    mock_card.front = "Test Question"
    mock_card.back = "Test Answer"
    mock_card.mastery_level = 2
    mock_card.next_review_date = "2024-01-01"
    mock_card_manager.get_card_by_id.return_value = mock_card

    # WHEN
    response = client.get(f"/browse/{card_id}")

    # THEN
    mock_card_manager.get_card_by_id.assert_called_once()
    call_args = mock_card_manager.get_card_by_id.call_args[0]
    assert call_args[1] == card_id  # Second arg should be card_id


@patch("flash_zap.web.routes.card_manager")
def test_browse_card_endpoint_displays_card_details(mock_card_manager, client: TestClient):
    """
    GIVEN: A valid card ID and existing card.
    WHEN: A GET request is made to /browse/{card_id}.
    THEN: The HTML should display card details and edit options.
    """
    # GIVEN
    card_id = 1
    mock_card = MagicMock()
    mock_card.id = 1
    mock_card.front = "Test Question"
    mock_card.back = "Test Answer"
    mock_card.mastery_level = 2
    mock_card.next_review_date = "2024-01-01"
    mock_card_manager.get_card_by_id.return_value = mock_card

    # WHEN
    response = client.get(f"/browse/{card_id}")
    soup = BeautifulSoup(response.text, 'html.parser')

    # THEN
    assert response.status_code == 200
    assert "Test Question" in response.text
    assert "Test Answer" in response.text
    assert "2" in response.text  # mastery level


@patch("flash_zap.web.routes.card_manager")
def test_edit_card_front_endpoint_exists(mock_card_manager, client: TestClient):
    """
    GIVEN: A card ID and new front text.
    WHEN: A POST request is made to /browse/{card_id}/edit-front.
    THEN: The response should be successful and card_manager.update_card_front should be called.
    """
    # GIVEN
    card_id = 1
    new_front = "Updated Question"
    mock_card = MagicMock()
    mock_card_manager.update_card_front.return_value = mock_card

    # WHEN
    response = client.post(f"/browse/{card_id}/edit-front", data={"new_front": new_front})

    # THEN
    assert response.status_code in [200, 302]  # Success or redirect
    mock_card_manager.update_card_front.assert_called_once()


@patch("flash_zap.web.routes.card_manager")
def test_edit_card_back_endpoint_exists(mock_card_manager, client: TestClient):
    """
    GIVEN: A card ID and new back text.
    WHEN: A POST request is made to /browse/{card_id}/edit-back.
    THEN: The response should be successful and card_manager.update_card_back should be called.
    """
    # GIVEN
    card_id = 1
    new_back = "Updated Answer"
    mock_card = MagicMock()
    mock_card_manager.update_card_back.return_value = mock_card

    # WHEN
    response = client.post(f"/browse/{card_id}/edit-back", data={"new_back": new_back})

    # THEN
    assert response.status_code in [200, 302]  # Success or redirect
    mock_card_manager.update_card_back.assert_called_once()


@patch("flash_zap.web.routes.card_manager")
def test_edit_card_mastery_endpoint_exists(mock_card_manager, client: TestClient):
    """
    GIVEN: A card ID and new mastery level.
    WHEN: A POST request is made to /browse/{card_id}/edit-mastery.
    THEN: The response should be successful and card_manager.update_card_mastery should be called.
    """
    # GIVEN
    card_id = 1
    new_mastery = 1
    mock_card_manager.update_card_mastery.return_value = (MagicMock(), True)

    # WHEN
    response = client.post(f"/browse/{card_id}/edit-mastery", data={"new_mastery_level": new_mastery})

    # THEN
    assert response.status_code in [200, 302]  # Success or redirect
    mock_card_manager.update_card_mastery.assert_called_once()


# NEW BROWSE LIST TESTS
@patch("flash_zap.web.routes.card_manager")
def test_browse_list_endpoint_returns_200(mock_card_manager, client: TestClient):
    """
    GIVEN: A functioning FastAPI application.
    WHEN: A GET request is made to the /browse/list endpoint.
    THEN: The response should be 200 OK with browse list HTML.
    """
    # GIVEN
    mock_card_manager.get_all_cards_paginated.return_value = ([], 0, 1, 1)  # cards, total, page, total_pages
    
    # WHEN
    response = client.get("/browse/list")
    
    # THEN
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


@patch("flash_zap.web.routes.card_manager")
def test_browse_list_calls_card_manager_with_correct_pagination(mock_card_manager, client: TestClient):
    """
    GIVEN: A page parameter in query string.
    WHEN: A GET request is made to /browse/list with page parameter.
    THEN: card_manager.get_all_cards_paginated should be called with correct page and per_page.
    """
    # GIVEN
    mock_card_manager.get_all_cards_paginated.return_value = ([], 0, 2, 1)
    
    # WHEN
    response = client.get("/browse/list?page=2")
    
    # THEN
    mock_card_manager.get_all_cards_paginated.assert_called_once()
    call_args = mock_card_manager.get_all_cards_paginated.call_args
    args, kwargs = call_args
    assert args[1] == 2    # page number (positional)
    assert kwargs['per_page'] == 30   # per_page (keyword argument)


@patch("flash_zap.web.routes.card_manager")
def test_browse_list_displays_card_grid(mock_card_manager, client: TestClient):
    """
    GIVEN: Multiple cards in the database.
    WHEN: A GET request is made to /browse/list.
    THEN: The HTML should display cards in a grid with front, back, mastery level icons and next review date icons.
    """
    # GIVEN
    mock_cards = [
        MagicMock(id=1, front="Question 1", back="Answer 1", mastery_level=2, next_review_date=date(2024, 1, 15)),
        MagicMock(id=2, front="Question 2", back="Answer 2", mastery_level=3, next_review_date=date(2024, 1, 20)),
    ]
    mock_card_manager.get_all_cards_paginated.return_value = (mock_cards, 2, 1, 1)
    
    # WHEN
    response = client.get("/browse/list")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # THEN
    assert response.status_code == 200
    # Check for card grid container
    card_grid = soup.find(class_='card-grid')
    assert card_grid is not None
    
    # Check for individual cards
    card_divs = soup.find_all(class_='card-item')
    assert len(card_divs) == 2
    
    # Check first card content
    first_card = card_divs[0]
    assert "Question 1" in first_card.text
    assert "Answer 1" in first_card.text
    
    # Check for trophy icon (mastery level)
    trophy_icon = first_card.find(class_='trophy-icon')
    assert trophy_icon is not None
    
    # Check for calendar icon (next review date)
    calendar_icon = first_card.find(class_='calendar-icon')
    assert calendar_icon is not None


@patch("flash_zap.web.routes.card_manager")
def test_browse_list_card_items_link_to_card_details(mock_card_manager, client: TestClient):
    """
    GIVEN: Cards displayed in the browse list.
    WHEN: A card item is rendered in the list.
    THEN: Each card should be clickable and link to the card detail view.
    """
    # GIVEN
    mock_cards = [
        MagicMock(id=1, front="Question 1", back="Answer 1", mastery_level=2, next_review_date=date(2024, 1, 15)),
    ]
    mock_card_manager.get_all_cards_paginated.return_value = (mock_cards, 1, 1, 1)
    
    # WHEN
    response = client.get("/browse/list")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # THEN
    card_links = soup.find_all('a', href=lambda href: href and '/browse/' in href and '/browse/list' not in href)
    assert len(card_links) >= 1
    assert '/browse/1' in card_links[0]['href']


@patch("flash_zap.web.routes.card_manager")
def test_browse_list_truncates_long_text(mock_card_manager, client: TestClient):
    """
    GIVEN: A card with very long front and back text.
    WHEN: The card is displayed in the browse list.
    THEN: The text should be truncated to prevent layout issues.
    """
    # GIVEN
    long_text = "This is a very long question that should be truncated when displayed in the browse list view to prevent layout issues and keep the card grid clean and readable"
    mock_cards = [
        MagicMock(id=1, front=long_text, back=long_text, mastery_level=1, next_review_date=date(2024, 1, 15)),
    ]
    mock_card_manager.get_all_cards_paginated.return_value = (mock_cards, 1, 1, 1)
    
    # WHEN
    response = client.get("/browse/list")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # THEN
    card_item = soup.find(class_='card-item')
    # The text should be truncated (less than original length)
    displayed_text = card_item.text
    assert len(displayed_text) < len(long_text) * 2  # both front and back combined should be much shorter


@patch("flash_zap.web.routes.card_manager")
def test_browse_list_shows_pagination_controls(mock_card_manager, client: TestClient):
    """
    GIVEN: Multiple pages of cards exist.
    WHEN: A GET request is made to /browse/list.
    THEN: The HTML should display pagination controls with previous/next links.
    """
    # GIVEN
    mock_cards = [MagicMock(id=i, front=f"Q{i}", back=f"A{i}", mastery_level=1, next_review_date=date(2024, 1, 15)) for i in range(30)]
    mock_card_manager.get_all_cards_paginated.return_value = (mock_cards, 100, 1, 4)  # 100 total cards, page 1 of 4
    
    # WHEN
    response = client.get("/browse/list")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # THEN
    pagination = soup.find(class_='pagination')
    assert pagination is not None
    
    # Check for next page link when on first page
    next_link = soup.find('a', string=lambda text: text and 'Next' in text)
    assert next_link is not None
    assert 'page=2' in next_link['href']


@patch("flash_zap.web.routes.card_manager")
def test_browse_list_pagination_previous_link_on_second_page(mock_card_manager, client: TestClient):
    """
    GIVEN: Multiple pages of cards exist and user is on page 2.
    WHEN: A GET request is made to /browse/list?page=2.
    THEN: The HTML should display a previous page link.
    """
    # GIVEN
    mock_cards = [MagicMock(id=i, front=f"Q{i}", back=f"A{i}", mastery_level=1, next_review_date=date(2024, 1, 15)) for i in range(30)]
    mock_card_manager.get_all_cards_paginated.return_value = (mock_cards, 100, 2, 4)  # page 2 of 4
    
    # WHEN
    response = client.get("/browse/list?page=2")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # THEN
    prev_link = soup.find('a', string=lambda text: text and 'Previous' in text)
    assert prev_link is not None
    assert 'page=1' in prev_link['href']


@patch("flash_zap.web.routes.card_manager")
def test_browse_template_contains_remove_option(mock_card_manager, client: TestClient):
    """
    GIVEN: A valid card ID and existing card.
    WHEN: A GET request is made to /browse/{card_id}.
    THEN: The HTML should contain a red-colored remove card option.
    """
    # GIVEN
    card_id = 1
    mock_card = MagicMock()
    mock_card.id = 1
    mock_card.front = "Test Question"
    mock_card.back = "Test Answer"
    mock_card.mastery_level = 2
    mock_card.next_review_date = "2024-01-01"
    mock_card_manager.get_card_by_id.return_value = mock_card

    # WHEN
    response = client.get(f"/browse/{card_id}")
    soup = BeautifulSoup(response.text, 'html.parser')

    # THEN
    assert response.status_code == 200
    # Look for the remove card option link
    remove_link = soup.find('a', string=lambda text: text and 'Remove card' in text)
    assert remove_link is not None
    # Check if the link has red styling (either inline or class)
    assert 'color: red' in str(remove_link) or 'red' in remove_link.get('class', [])


@patch("flash_zap.web.routes.card_manager")
def test_remove_card_endpoint_deletes_card(mock_card_manager, client: TestClient):
    """
    GIVEN: A card ID and confirmation.
    WHEN: A POST request is made to /browse/{card_id}/remove with confirmation.
    THEN: The card_manager.delete_card should be called and redirect to browse.
    """
    # GIVEN
    card_id = 1
    mock_card_manager.delete_card.return_value = True

    # WHEN
    response = client.post(f"/browse/{card_id}/remove", data={"confirm": "yes"}, follow_redirects=False)

    # THEN
    assert response.status_code == 302  # Redirect after deletion
    mock_card_manager.delete_card.assert_called_once()
    call_args = mock_card_manager.delete_card.call_args[0]
    assert call_args[1] == card_id  # Second arg should be card_id


@patch("flash_zap.web.routes.card_manager")
def test_remove_card_endpoint_without_confirmation_redirects_back(mock_card_manager, client: TestClient):
    """
    GIVEN: A card ID without confirmation.
    WHEN: A POST request is made to /browse/{card_id}/remove without confirmation.
    THEN: The card should not be deleted and user redirected back to card.
    """
    # GIVEN
    card_id = 1

    # WHEN
    response = client.post(f"/browse/{card_id}/remove", data={}, follow_redirects=False)

    # THEN
    assert response.status_code == 302  # Redirect back
    mock_card_manager.delete_card.assert_not_called() 

# PAGE PERSISTENCE TESTS
@patch("flash_zap.web.routes.card_manager")
def test_card_detail_links_include_page_parameter(mock_card_manager, client: TestClient):
    """
    GIVEN: User is on page 2 of browse list.
    WHEN: Card links are rendered.
    THEN: Each card link should include the current page parameter.
    """
    # GIVEN
    mock_cards = [
        MagicMock(id=1, front="Question 1", back="Answer 1", mastery_level=2, next_review_date=date(2024, 1, 15)),
        MagicMock(id=2, front="Question 2", back="Answer 2", mastery_level=3, next_review_date=date(2024, 1, 20)),
    ]
    mock_card_manager.get_all_cards_paginated.return_value = (mock_cards, 100, 2, 4)  # page 2 of 4
    
    # WHEN
    response = client.get("/browse/list?page=2")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # THEN
    card_links = soup.find_all('a', href=lambda href: href and '/browse/' in href and '/browse/list' not in href)
    assert len(card_links) >= 1
    # All card links should include the page parameter
    for link in card_links:
        assert 'from_page=2' in link['href']


@patch("flash_zap.web.routes.card_manager")
def test_card_detail_view_accepts_from_page_parameter(mock_card_manager, client: TestClient):
    """
    GIVEN: A card detail URL with from_page parameter.
    WHEN: A GET request is made to /browse/{card_id}?from_page=3.
    THEN: The page should render successfully and include the from_page in context.
    """
    # GIVEN
    mock_card = MagicMock(id=1, front="Test Question", back="Test Answer", mastery_level=2, next_review_date=date(2024, 1, 15))
    mock_card_manager.get_card_by_id.return_value = mock_card
    
    # WHEN
    response = client.get("/browse/1?from_page=3")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # THEN
    assert response.status_code == 200
    # Check that the back link includes the correct page
    back_link = soup.find('a', string=lambda text: text and 'Back to Browse List' in text)
    assert back_link is not None
    assert 'page=3' in back_link['href']


@patch("flash_zap.web.routes.card_manager")
def test_card_detail_back_link_defaults_to_page_one_without_from_page(mock_card_manager, client: TestClient):
    """
    GIVEN: A card detail URL without from_page parameter.
    WHEN: A GET request is made to /browse/{card_id} (no from_page).
    THEN: The back link should default to page 1.
    """
    # GIVEN
    mock_card = MagicMock(id=1, front="Test Question", back="Test Answer", mastery_level=2, next_review_date=date(2024, 1, 15))
    mock_card_manager.get_card_by_id.return_value = mock_card
    
    # WHEN
    response = client.get("/browse/1")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # THEN
    assert response.status_code == 200
    back_link = soup.find('a', string=lambda text: text and 'Back to Browse List' in text)
    assert back_link is not None
    # Should link to page 1 (default) or no page parameter
    assert 'page=1' in back_link['href'] or back_link['href'] == '/browse/list'


@patch("flash_zap.web.routes.card_manager")
def test_edit_redirects_preserve_from_page_parameter(mock_card_manager, client: TestClient):
    """
    GIVEN: User edits a card from a specific page.
    WHEN: The edit form is submitted.
    THEN: The redirect should preserve the from_page parameter.
    """
    # GIVEN
    mock_card = MagicMock()
    mock_card_manager.update_card_front.return_value = mock_card
    
    # WHEN
    response = client.post("/browse/1/edit-front?from_page=3", data={"new_front": "Updated Question"}, follow_redirects=False)
    
    # THEN
    assert response.status_code == 302
    # Should redirect back to the card detail with from_page preserved
    assert 'from_page=3' in response.headers['location'] 

# NUMBERED PAGINATION TESTS
@patch("flash_zap.web.routes.card_manager")
def test_numbered_pagination_shows_page_numbers(mock_card_manager, client: TestClient):
    """
    GIVEN: Multiple pages of cards exist (e.g., 10 pages total).
    WHEN: A GET request is made to /browse/list?page=5.
    THEN: The HTML should display numbered page links around the current page.
    """
    # GIVEN
    mock_cards = [MagicMock(id=i, front=f"Q{i}", back=f"A{i}", mastery_level=1, next_review_date=date(2024, 1, 15)) for i in range(30)]
    mock_card_manager.get_all_cards_paginated.return_value = (mock_cards, 300, 5, 10)  # page 5 of 10
    
    # WHEN
    response = client.get("/browse/list?page=5")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # THEN
    assert response.status_code == 200
    pagination = soup.find(class_='pagination')
    assert pagination is not None
    
    # Should show numbered links
    page_links = pagination.find_all('a', href=lambda href: href and 'page=' in href)
    page_numbers = []
    for link in page_links:
        if link.text.isdigit():
            page_numbers.append(int(link.text))
    
    # Should have several page numbers around current page (5)
    assert len(page_numbers) >= 3  # At least a few page numbers
    assert 5 in page_numbers or any(abs(num - 5) <= 2 for num in page_numbers)  # Current page or nearby


@patch("flash_zap.web.routes.card_manager")
def test_current_page_is_highlighted_in_pagination(mock_card_manager, client: TestClient):
    """
    GIVEN: User is on page 3 of multiple pages.
    WHEN: The browse list is rendered.
    THEN: Page 3 should be visually highlighted (not a link).
    """
    # GIVEN
    mock_cards = [MagicMock(id=i, front=f"Q{i}", back=f"A{i}", mastery_level=1, next_review_date=date(2024, 1, 15)) for i in range(30)]
    mock_card_manager.get_all_cards_paginated.return_value = (mock_cards, 300, 3, 10)  # page 3 of 10
    
    # WHEN
    response = client.get("/browse/list?page=3")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # THEN
    pagination = soup.find(class_='pagination')
    assert pagination is not None
    
    # Current page should be highlighted (not a link)
    current_page_span = pagination.find('span', class_='current-page')
    assert current_page_span is not None
    assert '3' in current_page_span.text


@patch("flash_zap.web.routes.card_manager")
def test_page_numbers_link_to_correct_pages(mock_card_manager, client: TestClient):
    """
    GIVEN: Multiple pages exist.
    WHEN: Page numbers are rendered.
    THEN: Each page number should link to the correct page.
    """
    # GIVEN
    mock_cards = [MagicMock(id=i, front=f"Q{i}", back=f"A{i}", mastery_level=1, next_review_date=date(2024, 1, 15)) for i in range(30)]
    mock_card_manager.get_all_cards_paginated.return_value = (mock_cards, 300, 5, 10)  # page 5 of 10
    
    # WHEN
    response = client.get("/browse/list?page=5")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # THEN
    pagination = soup.find(class_='pagination')
    page_links = pagination.find_all('a', href=lambda href: href and 'page=' in href)
    
    for link in page_links:
        if link.text.isdigit():
            page_num = link.text
            expected_href = f"/browse/list?page={page_num}"
            assert link['href'] == expected_href


@patch("flash_zap.web.routes.card_manager")
def test_pagination_shows_ellipsis_for_many_pages(mock_card_manager, client: TestClient):
    """
    GIVEN: Many pages exist (e.g., 50 pages) and user is in the middle.
    WHEN: The browse list is rendered.
    THEN: Ellipsis (...) should be shown for skipped page ranges.
    """
    # GIVEN
    mock_cards = [MagicMock(id=i, front=f"Q{i}", back=f"A{i}", mastery_level=1, next_review_date=date(2024, 1, 15)) for i in range(30)]
    mock_card_manager.get_all_cards_paginated.return_value = (mock_cards, 1500, 25, 50)  # page 25 of 50
    
    # WHEN
    response = client.get("/browse/list?page=25")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # THEN
    pagination = soup.find(class_='pagination')
    assert pagination is not None
    
    # Should show ellipsis for skipped ranges
    ellipsis_spans = pagination.find_all('span', string='...')
    assert len(ellipsis_spans) >= 1  # At least one ellipsis
    
    # Should show first page and last page
    first_page_link = pagination.find('a', string='1')
    last_page_link = pagination.find('a', string='50')
    assert first_page_link is not None
    assert last_page_link is not None


@patch("flash_zap.web.routes.card_manager")
def test_pagination_first_page_special_case(mock_card_manager, client: TestClient):
    """
    GIVEN: User is on the first page.
    WHEN: The browse list is rendered.
    THEN: Should show pages 1,2,3... without left ellipsis.
    """
    # GIVEN
    mock_cards = [MagicMock(id=i, front=f"Q{i}", back=f"A{i}", mastery_level=1, next_review_date=date(2024, 1, 15)) for i in range(30)]
    mock_card_manager.get_all_cards_paginated.return_value = (mock_cards, 300, 1, 10)  # page 1 of 10
    
    # WHEN
    response = client.get("/browse/list?page=1")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # THEN
    pagination = soup.find(class_='pagination')
    # Should show pages starting from 1
    page_1_span = pagination.find('span', class_='current-page', string='1')
    assert page_1_span is not None
    
    # Should have links to pages 2, 3, etc.
    page_2_link = pagination.find('a', string='2')
    assert page_2_link is not None 