from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Load the UI
        uic.loadUi("ui/main.ui", self)
        self.show()


app = QApplication([])
widget = QtWidgets.QStackedWidget()
mainwidow = MainWindow()
widget.addWidget(mainwidow)
widget.setWindowTitle("Note Taking App")
widget.show()
app.exec_()
