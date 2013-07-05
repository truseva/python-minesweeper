import create_board
import tools
from tools import *
import settings


class Game:
    def __init__(self):
        self.board = create_board.Board()
        self.real_board = self.board.real_board
        self.display_board = self.board.display_board
        self.mine_ls = self.board.mine_ls
        self.status = settings.GAME_STATUS['playing']
        self.revealed_ls = []
        self.flagged_ls = []

    def select(self, row, column):
        if not self.is_revealed(row, column):
            self.open(row, column)
            if (len(self.revealed_ls) == settings.ROWS*settings.COLUMNS and
                    self.status != settings.GAME_STATUS['lost'] and
                    len(self.flagged_ls) == settings.MINES_COUNT):
                self.status = settings.GAME_STATUS['win']

    def flag(self, row, column):
        element = (row, column)
        if not self.is_revealed(row, column):
            self.display_board[row][column] = settings.FLAG_SIGN
            self.revealed_ls.append(element)
            self.flagged_ls.append(element)
            if (len(self.revealed_ls) == settings.ROWS*settings.COLUMNS and
                    self.status != settings.GAME_STATUS['lost'] and
                    len(self.flagged_ls) == settings.MINES_COUNT):
                self.status = settings.GAME_STATUS['win']
        else:
            if self.display_board[row][column] == settings.FLAG_SIGN:
                self.display_board[row][column] = ''
                self.revealed_ls.remove(element)
                self.flagged_ls.remove(element)

    def is_revealed(self, row, column):
        return self.display_board[row][column] != ''

    def is_flagged(self, row, column):
        return self.display_board[row][column] == settings.FLAG_SIGN

    def open(self, row, column):
        if (self.status == settings.GAME_STATUS['playing'] and
                not self.is_revealed(row, column)):
            cell = self.real_board[row][column]
            if cell == settings.MINE_SIGN:
                self.game_over()
            else:
                self.show(row, column)
                if cell == 0:
                    self.show_all(row, column)

    def game_over(self):
        for (row, column) in self.mine_ls:
            if not self.is_revealed(row, column):
                self.show(row, column)
        self.status = settings.GAME_STATUS['lost']

    def show(self, row, column):
        self.display_board[row][column] = self.real_board[row][column]
        element = (row, column)
        self.revealed_ls.append(element)

    def show_all(self, row, column):
        for (r, c) in tools.neighbours(row, column):
            if not self.is_revealed(r, c):
                self.open(r, c)