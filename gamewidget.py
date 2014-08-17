from PyQt5.QtCore import QRectF, pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtGui import QPainter, QColor


class GameWidget(QWidget):
    stopIteration = pyqtSignal()

    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        self.life = None
        self.timer = None
        self.b_chance = None

        self.stopIteration.connect(self.iterationEnd)

    @property
    def cellWidth(self):
        return self.width() / self.life.n

    @property
    def cellHeight(self):
        return self.height() / self.life.m

    def startGame(self):
        self.timer.start()
        self.update()

    def iterationEnd(self):
        self.update()
        self.timer.stop()
        QMessageBox.information(self, 'Game Over',
                                'Дальнейшие состояния будут бесконечно повторяться.\nИгра остановлена.', QMessageBox.Ok)

    def stopGame(self):
        self.timer.stop()

    def clearGame(self):
        self.life.clear_world()
        self.stopGame()
        self.update()

    def evolve(self):
        if not self.life.evolve():
            self.stopIteration.emit()
        else:
            self.update()

    def randomFill(self, b_chance):
        self.life.clear_world()
        self.life.random_populate(1 - b_chance, b_chance)
        self.update()

    def toggleWrap(self):
        self.life.toggle_wrapping()
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        self.paintBackground(p)
        self.paintField(p)

    def setSpeed(self, msec):
        self.timer.setInterval(1000 / msec)

    def getCellColor(self, i, j):
        lt = self.life.lifetime[i, j]
        R, G, B = 0, 0, 0
        lamda = 20
        if 0 <= lt <= 10:
            R = (lt / lamda) * 255
            G = 255
        elif 10 < lt <= 20:
            G = (1 - (lt - 10) / lamda) * 255
            R = 255
        elif 20 < lt <= 30:
            R = (1 - (lt - 20) / lamda) * 255
        return QColor(R, G, B)

    def paintBackground(self, p):
        r = QRectF(0, 0, self.width(), self.height())
        p.fillRect(r, QColor(255, 255, 255))

    def paintField(self, p):
        for i in range(self.life.m):
            for j in range(self.life.n):
                if self.life.world[i, j]:
                    left = self.cellWidth * j
                    top = self.cellHeight * i
                    r = QRectF(left, top, self.cellWidth, self.cellHeight)
                    p.fillRect(r, self.getCellColor(i, j))

    def mousePressEvent(self, e):
        i = e.y() // self.cellHeight
        j = e.x() // self.cellWidth
        self.life.world[i, j] = 0 if self.life.world[i, j] == 1 else 1
        self.update()

    def mouseMoveEvent(self, e):
        i = e.y() // self.cellHeight
        j = e.x() // self.cellWidth
        if i < 0 or i >= self.life.n or j < 0 or j >= self.life.m:
            return
        if not self.life.world[i, j]:
            self.life.world[i, j] = 1
            self.update()