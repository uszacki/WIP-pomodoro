import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QPushButton)

class PomodoroApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 60, 800, 600)
        self.button = QPushButton('Button test')

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.button)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = PomodoroApp()
    widget.show()
    sys.exit(app.exec())