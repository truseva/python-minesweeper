from PyQt5.QtGui import QFont, QColor

from random import randrange

import settings


font_numbers = QFont()
font_numbers.setPointSize(settings.FONT_POINT_SIZE)
font_numbers.setFamily(settings.FONT_FAMILY_NUMBERS)

font_objects = QFont()
font_objects.setPointSize(settings.FONT_POINT_SIZE)
font_objects.setFamily(settings.FONT_FAMILY_OBJECTS)


def neighbours(row, column):
    if row == 0 and column == 0:
        return [(1, 0), (1, 1), (0, 1)]
    if row == 0 and column == settings.COLUMNS-1:
        return [
            (0, settings.COLUMNS-2),
            (1, settings.COLUMNS-2),
            (1, settings.COLUMNS-1)
        ]
    if row == settings.ROWS-1 and column == 0:
        return [
            (settings.ROWS-2, 0),
            (settings.ROWS-2, 1),
            (settings.ROWS-1, 1)
        ]
    if row == settings.ROWS-1 and column == settings.COLUMNS-1:
        return [
            (settings.ROWS-2, settings.COLUMNS-1),
            (settings.ROWS-2, settings.COLUMNS-2),
            (settings.ROWS-1, settings.COLUMNS-2)
        ]
    if row == 0:
        return [
            (0, column-1),
            (1, column-1),
            (1, column),
            (1, column+1),
            (0, column+1)
        ]
    if row == settings.ROWS-1:
        return [
            (settings.ROWS-1, column-1),
            (settings.ROWS-2, column-1),
            (settings.ROWS-2, column),
            (settings.ROWS-2, column+1),
            (settings.ROWS-1, column+1)
        ]
    if column == 0:
        return [
            (row-1, 0),
            (row-1, 1),
            (row, 1),
            (row+1, 1),
            (row+1, 0)
        ]
    if column == settings.COLUMNS-1:
        return [
            (row-1, settings.COLUMNS-1),
            (row-1, settings.COLUMNS-2),
            (row, settings.COLUMNS-2),
            (row+1, settings.COLUMNS-2),
            (row+1, settings.COLUMNS-1)
        ]
    return [
        (row-1, column-1),
        (row-1, column),
        (row-1, column+1),
        (row, column-1),
        (row, column+1),
        (row+1, column-1),
        (row+1, column),
        (row+1, column+1)
    ]


def rand():
    row = randrange(0, settings.ROWS)
    column = randrange(0, settings.COLUMNS)
    return row, column


def visualize(item, text):
    item.setTextAlignment(0x0080 | 0x0004)
    (red, green, blue) = settings.COLORS[text]
    item.setForeground(QColor(red, green, blue))
    color = settings.GRAY_SHADE
    item.setBackground(QColor(color, color, color))
    if text in [settings.MINE_SIGN, settings.FLAG_SIGN]:
        item.setFont(font_objects)
    else:
        item.setFont(font_numbers)