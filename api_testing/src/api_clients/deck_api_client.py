from dataclasses import dataclass

import requests
from assertpy import assert_that
from dataclasses_json import dataclass_json, Undefined

from api_testing.src.api_clients.base_api_client import BaseAPIClient
from api_testing.src.config.environment import BASE_URI
from api_testing.src.helpers.requests import APIRequest


@dataclass_json
@dataclass
class Deck:
    success: bool
    deck_id: str
    shuffled: bool
    remaining: int


@dataclass_json
@dataclass
class Card:
    image: str
    value: str
    suit: str
    code: str


deck_schema = {
    "success": {'type': 'boolean'},
    "deck_id": {'type': 'string',
                # 'regex': '[^A-Za-z0-9]'
                },
    "shuffled": {'type': 'boolean'},
    "remaining": {'type': 'integer', 'min': 10, 'max': 54}
}


class DeckApiClient(BaseAPIClient):
    def __init__(self):
        super().__init__()

        self.request = APIRequest()
        self.base_url = BASE_URI
        self.new_deck_endpoint = f'{BASE_URI}/new/'

    @staticmethod
    def __deck_reshuffle_endpoint(deck_id: str, remaining: bool = True):
        if remaining:
            return f'{BASE_URI}/{deck_id}/shuffle/?remaining=true'
        else:
            return f'{BASE_URI}/{deck_id}/shuffle/'

    @staticmethod
    def __deck_draw_cards_from_deck_endpoint(deck_id: str, no_of_cards: int):
        return f'{BASE_URI}/{deck_id}/draw/?count={no_of_cards}'

    @staticmethod
    def __add_cards_to_pile_endpoint(deck_id: str, pile_name: str, cards: []):
        endpoint = f'{BASE_URI}/{deck_id}/pile/{pile_name}/add/?cards='
        for card in cards:
            endpoint += f'{card.code},'
        return endpoint[:-1]

    @staticmethod
    def __show_cards_from_pile_endpoint(deck_id: str, pile_name: str):
        return f'{BASE_URI}/{deck_id}/pile/{pile_name}/list/'

    @staticmethod
    def __shuffle_cards_from_pile_endpoint(deck_id: str, pile_name: str):
        return f'{BASE_URI}/{deck_id}/pile/{pile_name}/shuffle/'

    @staticmethod
    def __deck_draw_cards_from_pile_endpoint(deck_id: str, pile_name: str, no_of_cards: int):
        return f'{BASE_URI}/{deck_id}/pile/{pile_name}/draw/?count={no_of_cards}'

    def create_new(self):
        response = self.request.post(self.new_deck_endpoint)
        assert_that(response.status_code).is_equal_to(requests.codes.ok)
        assert_that(response.body['success']).is_true()
        return Deck.from_dict(response.body), response

    def reshuffle(self, deck_id: str, remaining: bool = True):
        response = self.request.post(self.__deck_reshuffle_endpoint(deck_id, remaining))
        assert_that(response.status_code).is_equal_to(requests.codes.ok)
        assert_that(response.body['success']).is_true()
        assert_that(response.body['deck_id']).is_equal_to(deck_id)
        return Deck.from_dict(response.body), response

    def draw_cards_from_deck(self, deck_id: str, no_of_cards_to_draw: int):
        response = self.request.get(self.__deck_draw_cards_from_deck_endpoint(deck_id, no_of_cards_to_draw))
        assert_that(response.status_code).is_equal_to(requests.codes.ok)
        assert_that(response.body['success']).is_true()
        assert_that(response.body['deck_id']).is_equal_to(deck_id)
        cards = [Card.from_dict(card) for card in response.body['cards']]
        return cards, response

    def add_cards_to_pile(self, deck_id: str, pile_name: str, cards: []):
        response = self.request.get(self.__add_cards_to_pile_endpoint(deck_id, pile_name, cards))
        assert_that(response.status_code).is_equal_to(requests.codes.ok)
        assert_that(response.body['success']).is_true()
        assert_that(response.body['deck_id']).is_equal_to(deck_id)
        piles = response.body['piles']
        return piles, response

    def show_cards_from_pile(self, deck_id: str, pile_name: str):
        response = self.request.get(self.__show_cards_from_pile_endpoint(deck_id, pile_name))
        assert_that(response.status_code).is_equal_to(requests.codes.ok)
        assert_that(response.body['success']).is_true()
        assert_that(response.body['deck_id']).is_equal_to(deck_id)
        piles = response.body['piles']
        cards = [Card.from_dict(card) for card in piles[pile_name]['cards']]
        return piles, cards, response

    def shuffle_cards_from_pile(self, deck_id: str, pile_name: str):
        response = self.request.get(self.__shuffle_cards_from_pile_endpoint(deck_id, pile_name))
        assert_that(response.status_code).is_equal_to(requests.codes.ok)
        assert_that(response.body['success']).is_true()
        assert_that(response.body['deck_id']).is_equal_to(deck_id)
        return response

    def draw_cards_from_pile(self, deck_id: str, pile_name: str, no_of_cards_to_draw: int):
        response = self.request.get(self.__deck_draw_cards_from_pile_endpoint(deck_id, pile_name, no_of_cards_to_draw))
        assert_that(response.status_code).is_equal_to(requests.codes.ok)
        assert_that(response.body['success']).is_true()
        assert_that(response.body['deck_id']).is_equal_to(deck_id)
        piles = response.body['piles']
        cards = [Card.from_dict(card) for card in response.body['cards']]
        return piles, cards, response

