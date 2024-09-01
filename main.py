from PyQt6.QtWidgets import QApplication, QMainWindow
from player import Music_Player
import sys

app = QApplication(sys.argv)
window = Music_Player()
window.show()
app.exec()