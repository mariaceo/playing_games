import requests
from cerberus import Validator
from assertpy import assert_that
from api_testing.src.api_clients.deck_api_client import DeckApiClient, deck_schema, Card

deckClient = DeckApiClient()


def test_deck_of_cards_apis():
    # Create a deck of cards
    deck, response = deckClient.create_new()
    deck_id = deck.deck_id
    initial_no_of_cards = deck.remaining
    validator = Validator(deck_schema)
    is_valid = validator.validate(response.body)

    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(deck.shuffled).is_false()
    assert_that(deck.remaining).is_equal_to(52)
    assert_that(len(deck_id)).is_greater_than(0)

    # Shuffle the deck
    deck, response = deckClient.reshuffle(deck_id)
    is_valid = validator.validate(response.body)

    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(deck.shuffled).is_true()
    assert_that(deck.remaining).is_equal_to(52)

    # Draw 3 cards from deck
    cards_to_draw = 3
    cards, response = deckClient.draw_cards_from_deck(deck_id, cards_to_draw)
    latest_no_of_cards = initial_no_of_cards - cards_to_draw

    assert_that(len(cards)).is_equal_to(3)
    assert_that(response.body['remaining']).is_equal_to(latest_no_of_cards)

    # Make 2 piles with 5 cards each from deck
    pile_one = 'pile_one'
    pile_two = 'pile_two'
    cards_pile_one, r = deckClient.draw_cards_from_deck(deck_id, 5)
    piles, response = deckClient.add_cards_to_pile(deck_id, pile_one, cards_pile_one)
    latest_no_of_cards -= 5

    assert_that(response.body['remaining']).is_equal_to(latest_no_of_cards)
    assert_that(len(piles)).is_equal_to(1)
    assert_that(piles[pile_one]['remaining']).is_equal_to(5)

    cards_pile_two, r = deckClient.draw_cards_from_deck(deck_id, 5)
    piles, response = deckClient.add_cards_to_pile(deck_id, pile_two, cards_pile_two)
    latest_no_of_cards -= 5

    assert_that(response.body['remaining']).is_equal_to(latest_no_of_cards)
    assert_that(len(piles)).is_equal_to(2)
    assert_that(piles[pile_one]['remaining']).is_equal_to(5)
    assert_that(piles[pile_two]['remaining']).is_equal_to(5)

    # List the cards in pile1 and pile2
    piles, cards, response = deckClient.show_cards_from_pile(deck_id, pile_one)
    assert_that(response.body['remaining']).is_equal_to(latest_no_of_cards)
    assert_that(len(piles)).is_equal_to(2)
    assert_that(piles[pile_one]['remaining']).is_equal_to(5)
    assert_that(cards).is_equal_to(cards_pile_one)

    piles, cards, response = deckClient.show_cards_from_pile(deck_id, pile_two)
    assert_that(response.body['remaining']).is_equal_to(latest_no_of_cards)
    assert_that(len(piles)).is_equal_to(2)
    assert_that(piles[pile_two]['remaining']).is_equal_to(5)
    assert_that(cards).is_equal_to(cards_pile_two)

    # shuffle pile1
    response = deckClient.shuffle_cards_from_pile(deck_id, pile_one)
    assert_that(response.body['remaining']).is_equal_to(latest_no_of_cards)
    assert_that(len(piles)).is_equal_to(2)
    assert_that(piles[pile_one]['remaining']).is_equal_to(5)
    assert_that(piles[pile_two]['remaining']).is_equal_to(5)

    # draw 2 cards from pile1
    piles, cards, response = deckClient.draw_cards_from_pile(deck_id, pile_one, 2)
    assert_that(len(piles)).is_equal_to(2)
    assert_that(len(cards)).is_equal_to(2)
    assert_that(piles[pile_one]['remaining']).is_equal_to(5-2)
    assert_that(piles[pile_two]['remaining']).is_equal_to(5)

    # draw 3 cards from pile2
    piles, cards, response = deckClient.draw_cards_from_pile(deck_id, pile_two, 3)
    assert_that(len(piles)).is_equal_to(2)
    assert_that(len(cards)).is_equal_to(3)
    assert_that(piles[pile_one]['remaining']).is_equal_to(5-2)
    assert_that(piles[pile_two]['remaining']).is_equal_to(5-3)
