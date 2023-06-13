from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Load the UI
        uic.loadUi("ui/main.ui", self)
        self.show()


# Initialise the database
conn = sqlite3.connect("notelist.db")
c = conn.cursor()
c.execute("""CREATE TABLE if not exists noteList(
    id INTEGER PRIMARY KEY,
    title text,
    content text)
          """)
conn.commit()
conn.close()

app = QApplication([])
widget = QtWidgets.QStackedWidget()
mainwidow = MainWindow()
widget.addWidget(mainwidow)
widget.setWindowTitle("Note Taking App")
widget.show()
app.exec_()
