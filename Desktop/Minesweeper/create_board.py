import tools
from tools import *
import settings


class Board:
    def __init__(self):
        rows = settings.ROWS
        columns = settings.COLUMNS
        self.real_board = [
            [0 for column in range(0, columns)] for row in range(0, rows)
        ]
        self.display_board = [
            ['' for column in range(0, columns)] for row in range(0, rows)
        ]
        self.mine_ls = []
        self.mine_generator()
        self.find_mines()
        self.fill()

    def __str__(self):
        print_result = '\n'
        for row in self.real_board:
            print_result += str(row) + '\n'
        print_result += '\n' + str(self.mine_ls) + '\n'
        return print_result

    def mine_generator(self):
        counter = settings.MINES_COUNT
        while counter:
            row, column = tools.rand()
            while self.is_mine(row, column):
                row, column = tools.rand()
            self.real_board[row][column] = settings.MINE_SIGN
            counter -= 1

    def is_mine(self, row, column):
        return self.real_board[row][column] == settings.MINE_SIGN

    def find_mines(self):
        mine_ls = []
        for row in range(0, settings.ROWS):
            for column in range(0, settings.COLUMNS):
                if self.is_mine(row, column):
                    mine_ls.append((row, column))
        self.mine_ls = mine_ls

    def fill(self):
        for (row, column) in self.mine_ls:
            self.call(row, column)

    def call(self, row, column):
        for (r, c) in tools.neighbours(row, column):
            self.replace(r, c)

    def replace(self, row, column):
        if not self.is_mine(row, column):
            self.real_board[row][column] += 1


if __name__ == '__main__':
    new_board = Board()
    print(new_board)