import re
from playwright.sync_api import Page, expect, Locator
from ui_testing.helpers.agree_to_cookies import agree_to_cookies


class CheckersPage:
    URL = 'https://www.gamesforthebrain.com/game/checkers/'

    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.locator('h1')
        self.restart_button = page.locator('a:has-text("Restart...")')
        self.message = page.locator('#message')
        self.no_of_pieces = 12

    def load(self) -> None:
        self.page.goto(self.URL)
        agree_to_cookies(self.page)
        expect(self.title).to_have_text('Checkers')

    def restart_game(self):
        self.restart_button.click()
        self.check_message('Select an orange piece to move.')
        self.no_of_pieces = 12
        current_no_of_pieces = self.page.locator('[src="you1.gif"]')
        expect(current_no_of_pieces).to_have_count(self.no_of_pieces)

    def select_piece_to_move(self, position: (int, int)):
        self.click_square(position)
        self.check_square_src_attribute(position, 'you2.gif')

    def click_destination_square(self, position: (int, int)):
        self.check_square_src_attribute(position, 'gray.gif')
        self.click_square(position)

    def check_piece_was_moved(self, initial_position, destination_position):
        self.check_square_src_attribute(initial_position, f'{self.URL}gray.gif')
        self.check_square_src_attribute(destination_position, 'you1.gif')

    def check_message(self, message: str):
        expect(self.message).to_have_text(message)

    def wait_computer_move(self):
        self.page.wait_for_load_state(state='domcontentloaded')
        self.message.locator('text=Make a move.').wait_for()

    def check_computer_got_piece(self, position):
        self.check_square_src_attribute(position, 'gray.gif')
        self.no_of_pieces -= 1
        current_no_of_pieces = self.page.locator('[src="you1.gif"]')
        expect(current_no_of_pieces).to_have_count(self.no_of_pieces)

    def check_square_src_attribute(self, position: (int, int), attribute_value: str):
        self.page.wait_for_load_state(state='domcontentloaded')
        expect(self.__square_at(*position)).to_have_attribute('src', attribute_value)

    def click_square(self, position: (int, int)):
        self.__square_at(*position).click()

    def __square_at(self, column_right_to_left: int, row_bottom_to_top: int) -> Locator:
        return self.page.locator(f'[name="space{column_right_to_left}{row_bottom_to_top}"]')


