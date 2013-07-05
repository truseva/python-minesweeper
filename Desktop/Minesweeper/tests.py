import sys

import unittest

import main
import create_board
import gameplay
import tools
from tools import *
import settings


class BoardTest(unittest.TestCase):
    def setUp(self):
        self.board = create_board.Board()

    def tearDown(self):
        del self.board

    def test_attributes(self):
        self.assertIn('real_board', dir(self.board))
        self.assertIn('display_board', dir(self.board))
        self.assertIn('mine_ls', dir(self.board))

    def test_empty_display_board(self):
        for row in range(0, settings.ROWS):
            for column in range(0, settings.COLUMNS):
                self.assertEqual(
                    self.board.display_board[row][column], '')

    def test_mine_count(self):
        self.assertEqual(len(self.board.mine_ls), settings.MINES_COUNT)

    def test_real_board_mine_count(self):
        mine_ls = []
        real_board = self.board.real_board
        for row in range(0, settings.ROWS):
            for column in range(0, settings.COLUMNS):
                if real_board[row][column] == settings.MINE_SIGN:
                    element = (row, column)
                    mine_ls.append(element)
        self.assertEqual(len(mine_ls), settings.MINES_COUNT)

    def test_cell_mine_count(self):
        (row, column) = tools.rand()
        list = tools.neighbours(row, column)
        board = self.board.real_board
        m = settings.MINE_SIGN
        neighbours_mine = [(r, c) for (r, c) in list if board[r][c] == m]
        self.assertIn(board[row][column], [len(neighbours_mine), m])


class GameTest(unittest.TestCase):
    def setUp(self):
        self.game = gameplay.Game()

    def tearDown(self):
        del self.game

    def test_attributes(self):
        self.assertIn('board', dir(self.game))
        self.assertIn('real_board', dir(self.game))
        self.assertIn('display_board', dir(self.game))
        self.assertIn('mine_ls', dir(self.game))
        self.assertIn('status', dir(self.game))
        self.assertIn('revealed_ls', dir(self.game))
        self.assertIn('flagged_ls', dir(self.game))

    def test_initial_values(self):
        self.assertEqual(self.game.status, settings.GAME_STATUS['playing'])
        self.assertEqual(self.game.revealed_ls, [])
        self.assertEqual(self.game.flagged_ls, [])

    def test_flag(self):
        len_revealed = len(self.game.revealed_ls)
        len_flagged = len(self.game.flagged_ls)
        (row, column) = tools.rand()
        self.game.flag(row, column)
        revealed_values = [len_revealed - 1, len_revealed + 1]
        flagged_values = [len_flagged - 1, len_flagged + 1]
        self.assertIn(len(self.game.revealed_ls), revealed_values)
        self.assertIn(len(self.game.flagged_ls), flagged_values)

    def test_select(self):
        (row, column) = tools.rand()
        self.game.select(row, column)
        self.assertIn((row, column), self.game.revealed_ls)


if __name__ == '__main__':
    unittest.main()