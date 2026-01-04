import sys
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QGraphicsView,
    QGraphicsScene, QGraphicsPixmapItem, QWidget, QHBoxLayout
)
from PySide6.QtGui import QPixmap, QBrush
from PySide6.QtCore import Qt


DATA_FILE = "data/season_2026.json"
PITCH_IMG = "assets/pitch/pitch.png"


class PlayerItem(QGraphicsPixmapItem):
    def __init__(self, name):
        pix = QPixmap(30, 30)
        pix.fill(Qt.white)
        super().__init__(pix)
        self.name = name
        self.setFlag(self.ItemIsMovable)
        self.setFlag(self.ItemIsSelectable)


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grêmio Lineup Editor")

        # Load data
        with open(DATA_FILE, encoding="utf-8-sig") as f:
            self.data = json.load(f)

        # Scene / View
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        # Pitch
        pitch = QGraphicsPixmapItem(QPixmap(PITCH_IMG))
        self.scene.addItem(pitch)
        self.scene.setSceneRect(pitch.boundingRect())

        # Roster list
        self.roster = QListWidget()
        for p in self.data["roster"]:
            self.roster.addItem(p["nome"])

        self.roster.itemDoubleClicked.connect(self.add_player)

        # Layout
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(self.roster, 1)
        layout.addWidget(self.view, 4)

        self.setCentralWidget(container)

    def add_player(self, item):
        player = PlayerItem(item.text())
        player.setPos(200, 200)
        self.scene.addItem(player)

        # remove from roster
        self.roster.takeItem(self.roster.row(item))


app = QApplication(sys.argv)
window = Editor()
window.resize(1000, 600)
window.show()
sys.exit(app.exec())
