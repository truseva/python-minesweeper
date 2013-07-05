from PyQt5.QtWidgets import (QTableWidget, QTableWidgetItem,
                             QPushButton, QWidget, QDialog, QLabel)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QRect

import gameplay
import artificial_inteligence
import tools
from tools import *
import settings


class MessageStatusDialog(QDialog):
    def __init__(self, status, parent=None):
        QDialog.__init__(self)
        self.setWindowTitle("Status Message")
        self.resize(200, 50)
        self.move(200, 50)
        self.status = QLabel(self)
        self.status.setGeometry(QRect(10, 10, 180, 30))
        font = QFont()
        font.setPointSize(16)
        self.status.setFont(font)
        self.status.setText(status)
        self.status.setAlignment(Qt.AlignCenter)


class Minesweeper(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        self.new_game_button = QPushButton("New Game", self)
        self.new_game_button.resize(self.new_game_button.sizeHint())
        self.new_game_button.move(
            settings.CELL_SIZE*settings.COLUMNS/2 - 55, 20)
        self.new_game_button.clicked.connect(self.new_game)
        self.demo_button = QPushButton("Demo", self)
        self.demo_button.resize(self.demo_button.sizeHint())
        self.demo_button.move(
            settings.CELL_SIZE*settings.COLUMNS/2 + 25, 20)
        self.demo_button.clicked.connect(self.demo)
        game = gameplay.Game()
        self.initTableUI(game)
        self.setWindowTitle("Minesweeper")
        self.resize(
            settings.CELL_SIZE*settings.COLUMNS + 40,
            settings.CELL_SIZE*settings.ROWS + 80)
        self.move(300, 100)
        self.show()

    def initTableUI(self, game):
        table = Table(game, self)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionMode(QTableWidget.NoSelection)
        for row in range(0, settings.ROWS):
            table.verticalHeader().resizeSection(
                row, settings.CELL_SIZE)
        for column in range(0, settings.COLUMNS):
            table.horizontalHeader().resizeSection(
                column, settings.CELL_SIZE)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionMode(QTableWidget.NoSelection)
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        table.resize(
            settings.CELL_SIZE*settings.COLUMNS + 3,
            settings.CELL_SIZE*settings.ROWS + 3)
        table.move(20, 60)
        self.table = table

    def new_game(self):
        self.table.game = gameplay.Game()
        self.table.refresh_data(self.table.game, self.table)

    def demo(self):
        self.demo = artificial_inteligence.Demo()
        self.demo.launch(self)

    def update(self, demo):
        self.table.game = demo.game
        self.table.refresh_data(self.table.game, self)
        if demo.game.status == settings.GAME_STATUS['playing']:
            self.popup("Move made.")

    def popup(self, status):
        self.dialog = MessageStatusDialog(status)
        self.dialog.exec_()


class Table(QTableWidget):
    def __init__(self, game, parent):
        QTableWidget.__init__(
            self, settings.ROWS, settings.COLUMNS, parent)
        self.parent = parent
        self.game = game
        self.refresh_data(game, parent)

    def refresh_data(self, game, parent):
        for row in range(0, settings.ROWS):
            for column in range(0, settings.COLUMNS):
                text = str(game.display_board[row][column])
                self.element = QTableWidgetItem(text)
                if text != '':
                    tools.visualize(self.element, text)
                self.setItem(row, column, self.element)
        if game.status != settings.GAME_STATUS['playing']:
            parent.popup(game.status)
        self.game.display_board = game.display_board

    def mouseReleaseEvent(self, event):
        (row, column) = (
            int(event.y()/settings.CELL_SIZE),
            int(event.x()/settings.CELL_SIZE))
        if event.button() == Qt.LeftButton:
            self.game.select(row, column)
        else:
            self.game.flag(row, column)
        self.refresh_data(self.game, self.parent)
        event.accept()