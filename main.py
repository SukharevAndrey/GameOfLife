#!/usr/bin/env python3

import sys

from PyQt5.QtWidgets import QApplication
from mainwidget import MainWidget


def main():
    app = QApplication(sys.argv)
    w = MainWidget()
    w.setWindowTitle("Игра \"Жизнь\"")
    w.setFixedSize(w.geometry().width(), w.geometry().height())
    w.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())