import sys

from PyQt5.QtWidgets import QApplication

import graphic_interface


if __name__ == '__main__':
    app = QApplication(sys.argv)
    minesweeper = graphic_interface.Minesweeper()
    sys.exit(app.exec_())