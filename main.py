import sys, os
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QHBoxLayout
from PyQt5.QtCore import QTimer, QTime



class Database:
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        db = os.path.join(path, 'pomodoro.db')
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS datetime_test (
                study_session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50),
                activity VARCHAR(50),
                time INT    
            );
        ''')
        self.conn.commit()

    def insert_table(self, inputdata):
        self.cursor.execute('''
            INSERT INTO datetime_test (name, activity, time)
            VALUES (?, ?, ?)
        ''', (inputdata['name'], inputdata['activity'], inputdata['time'])) 
        self.conn.commit()
    
    def get_last_entries(self):
        self.cursor.execute('''
            SELECT name, activity, time FROM datetime_test
            ORDER BY study_session_id DESC LIMIT 10
        ''')
        return self.cursor.fetchall()

class PomodoroApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 60, 300, 300)
        self.setWindowTitle('Pomodoro')
        
        
        self.db = Database()
        self.time = QTime(0, 30, 0, 0)

        self.widgets()
        self.layouts()
        self.timer()
        self.connectors()
        self.normal_theme()
        self.update_entry_list()
        
        self.is_paused = False
        self.inputcount = 0
        self.inputdata = {}


    def widgets(self):
        self.time_label = QLabel("label before userinput", self)
        self.test = QLineEdit(self)
        self.test.setPlaceholderText("Your name")


        self.start_button = QPushButton("Start", self)
        self.pause_button = QPushButton("Pause", self)
        self.reset_button = QPushButton("Reset", self)
        self.theme_button = QPushButton("⚙️")
        self.theme_button.setFixedSize(25, 25)

        self.entry_list = QListWidget(self)
        self.entry_list.setFixedHeight(180)
        self.entry_list.setFixedWidth(250)


    def layouts(self):
        ######### kinda fixed?
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        list_layout = QVBoxLayout()
        buttons_layout = QVBoxLayout()

        list_layout.addWidget(self.entry_list)

        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.pause_button)
        buttons_layout.addWidget(self.reset_button)

        top_layout.addLayout(list_layout)
        top_layout.addLayout(buttons_layout)

        main_layout.addWidget(self.time_label)
        main_layout.addWidget(self.theme_button)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.test)

        self.setLayout(main_layout)


    def timer(self):
        self.timer = QTimer(self)
        self.timer.setInterval(10)  # 10ms = 0.01s (centésimos)
        self.timer.timeout.connect(self.update_display)

    def connectors(self):
        self.start_button.clicked.connect(self.start)
        self.pause_button.clicked.connect(self.stop)
        self.reset_button.clicked.connect(self.reset)

    def normal_theme(self):
        self.setStyleSheet("""QLabel {
                font-size: 25px;
                color: #333;
                font-weight: bold;
                padding: 5px;
            }""")
    
    def dark_theme(self):
        pass

    def start(self):
    
            if self.is_paused:
                self.timer.start()
                self.is_paused = False
                self.time_label.setText(self.time.toString("hh:mm:ss"))
                return
            
            self.userinput = self.test.text().strip()

            if self.inputcount == 0:
                self.inputdata['name'] = self.userinput
                self.test.setPlaceholderText('What are you studying? ')
                self.test.clear()
                self.inputcount += 1
            
            elif self.inputcount == 1:
                self.inputdata['activity'] = self.userinput
                self.test.setPlaceholderText('H:MM')
                self.test.clear()
                self.inputcount += 1
            
            elif self.inputcount == 2: 
                try:
                    self.hours = int(self.userinput[0])
                    self.minutes = int(self.userinput[2:4])
                    self.time = QTime(self.hours, self.minutes, 0,  0)
                    self.inputdata['time'] = (self.hours * 60) + self.minutes
                    self.update_display()
                    print(self.inputdata) ###### kv check
                
                except:
                    self.time_label.setText("invalid")
                    return

                self.timer.start()
                #db
                self.db.insert_table(self.inputdata)
        

    def stop(self):
        self.timer.stop()
        self.is_paused = True

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
            self.time_label.setText("time's up!")
        else:
            self.time_label.setText(self.time.toString("hh:mm:ss"))
            self.time = self.time.addMSecs(-10)

    def update_entry_list(self):
        entries = self.db.get_last_entries()
        self.entry_list.clear()
        for e in entries:
            self.entry_list.addItem(f"{e[0]} - {e[1]} ({e[2]} min)")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PomodoroApp()
    window.show()
    sys.exit(app.exec_())


## to do
# add diff page to check entries from sql
# restrict user input
# set up dark theme