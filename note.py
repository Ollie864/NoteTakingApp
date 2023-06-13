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

        self.currentlyLoadedTitle = ""
        self.isNewNote = True

        self.actionQuit.triggered.connect(exit)
        self.actionSave.triggered.connect(self.saveNote)

    def saveNote(self):
        conn = sqlite3.connect("notelist.db")
        c = conn.cursor()

        itemTitle = self.textBoxTitle.text()
        itemContent = self.textBoxContent.toPlainText()
        items = [itemTitle, itemContent]

        if itemTitle == "":
            errorMessage1 = QMessageBox()
            errorMessage1.setText("Note needs a title")
            errorMessage1.exec_()
            return 0

        if self.isNewNote:
            # Check if note with the same title exists in database
            check = c.execute(
                'SELECT title FROM noteList WHERE title = ?', (itemTitle,))
            checkValue = c.fetchone()
            if checkValue:
                errorMessage = QMessageBox()
                errorMessage.setText("Note with that name already exists")
                errorMessage.exec_()
            else:
                c.execute("""INSERT INTO noteList (title, content)
                      VALUES (?, ?)
                      """, items)
        else:
            # Delete old note and save new one in its place
            c.execute("DELETE FROM noteList WHERE title = ?",
                      (self.currentlyLoadedTitle,))
            c.execute("""INSERT INTO noteList (title, content)
                      VALUES (?, ?)
                      """, items)

        self.currentlyLoadedTitle = itemTitle
        conn.commit()
        conn.close()
        self.loadNotesTitle()

    def deleteNote(self):
        pass

    def newNote(self):
        pass

    def backupNote(self):
        pass

    def loadNotes(self):
        pass

    def loadNotesTitle(self):
        self.notesTitleListWidget.clear()
        conn = sqlite3.connect("notelist.db")
        c = conn.cursor()

        c.execute("SELECT title FROM noteList")

        databaseTitles = c.fetchall()
        conn.commit()
        conn.close()

        # loop through and add to
        for i in databaseTitles:
            self.notesTitleListWidget.addItem(str(i[0]))


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
