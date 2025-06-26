import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QTimer, QTime

class PomodoroApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 60, 800, 600)
        self.setWindowTitle('Pomodoro')


        self.time = QTime(0, 30, 0, 0)

        # BUttons
        self.time_label = QLabel("label before userinput", self)
        self.test = QLineEdit(self)
        self.test.setPlaceholderText("H:MM")



        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.reset_button = QPushButton("Reset", self)


        ######### self-reminder: fix this later
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.time_label)
        self.layout.addWidget(self.test)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.reset_button)
        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.setInterval(10)  # 10ms = 0.01s (centésimos)
        self.timer.timeout.connect(self.update_display)


        # connectors
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.reset_button.clicked.connect(self.reset)




    def start(self):
        self.userinput = self.test.text()

        try:
            self.hours = int(self.userinput[0])
            self.minutes = int(self.userinput[2:4])
            self.time = QTime(self.hours, self.minutes, 0,  0)
            self.update_display()
        except:
            self.time_label.setText("invalid")
            return


        self.timer.start()
        self.test.clear()

    def stop(self):
        self.timer.stop()

    def reset(self):
        self.timer.stop()

        try:
            hours = int(self.userinput[0])
            minutes = int(self.userinput[2:4])
            self.time = QTime(hours, minutes, 0, 0)
        except:
            self.time = QTime(0, 30, 0, 0)

        self.update_display()

    def update_display(self):
        if self.time == QTime(0, 0, 0, 0):
            self.timer.stop()
            self.time_label.settext("time's up!")
        else:
            self.time_label.setText(self.time.toString("hh:mm:ss"))
            self.time = self.time.addMSecs(-10)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PomodoroApp()
    window.show()
    sys.exit(app.exec_())