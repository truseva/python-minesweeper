import gameplay
import tools
from tools import *
import settings


class Demo:
    def __init__(self):
        self.game = gameplay.Game()

    def launch(self, minesweeper):
        self.initial_move(minesweeper)
        while self.game.status == settings.GAME_STATUS['playing']:
            obvious_move = self.obvious_move(minesweeper)
            counter = settings.MINES_COUNT/2
            while (counter and
                   self.game.status == settings.GAME_STATUS['playing']):
                obvious_move = self.obvious_move(minesweeper)
                counter -= 1
            self.chance_move(minesweeper)

    def initial_move(self, minesweeper):
        (row, column) = tools.rand()
        self.game.select(row, column)
        minesweeper.update(self)

    def chance_move(self, minesweeper):
        (row, column) = tools.rand()
        while ((row, column) in self.game.revealed_ls and
               self.game.status == settings.GAME_STATUS['playing']):
            (row, column) = tools.rand()
        self.game.select(row, column)
        minesweeper.update(self)

    def obvious_move(self, minesweeper):
        old_board = self.game.display_board
        obvious_safe_space = True
        while (obvious_safe_space and
               self.game.status == settings.GAME_STATUS['playing']):
            obvious_safe_space = self.select_obvious_safe_space(minesweeper)
            obvious_mine = True
            while (obvious_mine and
                   self.game.status == settings.GAME_STATUS['playing']):
                obvious_mine = self.flag_obvious_mine(minesweeper)
        return old_board != self.game.display_board

    def flag_obvious_mine(self, minesweeper):
        result = False
        for (row, column) in self.game.revealed_ls:
            neighbour_ls = tools.neighbours(row, column)
            revealed_ls = self.game.revealed_ls
            flagged_ls = self.game.flagged_ls
            n_revealed = [n for n in neighbour_ls if n in revealed_ls]
            m_revealed = [n for n in n_revealed if n in flagged_ls]
            mine_count = self.game.display_board[row][column]
            spaces_left = len(neighbour_ls) - len(n_revealed) + len(m_revealed)
            if spaces_left == mine_count:
                for neighbour in neighbour_ls:
                    if neighbour not in n_revealed:
                        (row, column) = neighbour
                        self.game.flag(row, column)
                        minesweeper.update(self)
                        result = True
        return result

    def select_obvious_safe_space(self, minesweeper):
        result = False
        for (row, column) in self.game.revealed_ls:
            neighbour_ls = tools.neighbours(row, column)
            revealed_ls = self.game.revealed_ls
            flagged_ls = self.game.flagged_ls
            n_revealed = [n for n in neighbour_ls if n in revealed_ls]
            m_revealed = [n for n in n_revealed if n in flagged_ls]
            mine_count = self.game.display_board[row][column]
            if len(m_revealed) == mine_count:
                for neighbour in neighbour_ls:
                    if neighbour not in n_revealed:
                        (row, column) = neighbour
                        self.game.select(row, column)
                        minesweeper.update(self)
                        result = True
        return result