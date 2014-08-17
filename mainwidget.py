from PyQt5 import uic

from PyQt5.QtCore import QTimer, QDir
from PyQt5.QtWidgets import QWidget, QFileDialog
from gamewidget import GameWidget
from life import Life


class MainWidget(QWidget):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        uic.loadUi('form.ui', self)

        self.game = GameWidget()
        self.game.life = Life(self.fieldSize.value(), self.fieldSize.value())
        self.game.timer = QTimer(self)
        self.game.timer.setInterval(self.evolutionSpeed.value())
        self.game.timer.timeout.connect(self.game.evolve)
        self.b_chance = self.blackChance.value()
        self.gameLayout.addWidget(self.game)

        self.startButton.clicked.connect(self.game.startGame)
        self.stopButton.clicked.connect(self.game.stopGame)
        self.clearButton.clicked.connect(self.game.clearGame)

        self.loadGameButton.clicked.connect(self.loadGame)
        self.saveGameButton.clicked.connect(self.saveGame)
        self.stateSelection.currentIndexChanged[str].connect(self.selectFigure)

        self.randomFillButton.clicked.connect(self.fillRandom)

        self.wrapping.stateChanged.connect(self.game.toggleWrap)
        self.fieldSize.editingFinished.connect(self.changeWorldSize)
        self.evolutionSpeed.valueChanged.connect(self.game.setSpeed)

    def fillRandom(self):
        self.game.randomFill(self.blackChance.value() / 100.0)

    def changeWorldSize(self):
        new_m = self.fieldSize.value()
        self.game.life.extend_world(new_m - self.game.life.m, new_m - self.game.life.m)
        self.game.update()

    def _load_from_file(self, filename):
        self.game.life.populate_from_file(filename)
        self.fieldSize.setValue(self.game.life.m)
        if self.game.life.wrap == True:
            self.wrapping.setChecked(True)
            self.game.life.wrap = True
        else:
            self.wrapping.setChecked(False)
            self.game.life.wrap = False

    def loadGame(self):
        self.game.stopGame()
        filename = QFileDialog.getOpenFileName(self, 'Загрузить состояние игры', QDir.homePath(),
                                               'Файлы игры \"Жизнь\" (*.life)')
        if len(filename[0]) > 1:
            self._load_from_file(filename[0])
        self.game.startGame()

    def saveGame(self):
        self.game.stopGame()
        filename = QFileDialog.getSaveFileName(self, 'Сохранить текущее состояние игры', QDir.homePath(),
                                               'Файлы игры \"Жизнь\" (*.life)')
        if len(filename[0]) > 1:
            self.game.life.save_to_file(filename[0])
        self.game.startGame()

    def selectFigure(self, fig_name):
        self.game.stopGame()
        if fig_name == "Gosper's Glider Gun":
            self._load_from_file('patterns/glider_gun.life')
        elif fig_name == "Pulsar":
            self._load_from_file('patterns/pulsar.life')
        else:
            self.game.life.clear_world()
        self.game.update()