import pytest

from playwright.sync_api import Page

from ui_testing.src.pages.checkers_page import CheckersPage


def test_checkers(
        page: Page,
        checkers_page: CheckersPage) -> None:

    # start a new game by restarting
    checkers_page.load()

    checkers_page.restart_game()
    initial_position = (4, 2)

    # Make your first move
    first_move_position = (5, 3)
    checkers_page.select_piece_to_move(initial_position)
    checkers_page.click_destination_square(first_move_position)
    checkers_page.check_piece_was_moved(initial_position, first_move_position)

    # Let computer move
    checkers_page.wait_computer_move()

    # Click invalid square when having to make a move
    checkers_page.click_square(initial_position)
    checkers_page.check_message('Click on your orange piece, then click where you want to move it.')

    # Make your second move
    second_move_position = (4, 4)
    checkers_page.select_piece_to_move(first_move_position)
    checkers_page.click_destination_square(second_move_position)

    # Let computer take your piece
    checkers_page.wait_computer_move()

    # Make sure your piece is taken
    checkers_page.check_computer_got_piece(second_move_position)

    # Start a new game
    checkers_page.restart_game()


