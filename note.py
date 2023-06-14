from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sqlite3
import shutil
import os
from os.path import exists


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Load the UI
        uic.loadUi("ui/main.ui", self)
        self.show()

        # Load list of notes on sidebar
        self.loadNotesTitle()

        self.currentlyLoadedTitle = ""
        self.isNewNote = True

        self.actionQuit.triggered.connect(exit)
        self.actionSave.triggered.connect(self.saveNote)
        self.actionDelete.triggered.connect(self.deleteNote)
        self.actionNew.triggered.connect(self.newNote)
        self.actionBackup.triggered.connect(self.backupNote)
        self.actionImport.triggered.connect(self.importNote)

        # Loads note from title list when double clicked
        self.notesTitleListWidget.itemDoubleClicked.connect(self.loadNotes)

    def saveNote(self):
        conn = sqlite3.connect("notelist.db")
        c = conn.cursor()

        itemTitle = self.textBoxTitle.text()
        itemContent = self.textBoxContent.toPlainText()
        items = [itemTitle, itemContent]

        if not itemTitle.strip():
            errorMessage1 = QMessageBox()
            errorMessage1.setText("Note needs a title")
            errorMessage1.exec_()
            return 0

        # If it is a new note the title needs to be unique
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
        # If is not a new note then delete old note with same title and replace
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
        try:
            noteToDeleteTitle = self.notesTitleListWidget.currentItem().text()
            conn = sqlite3.connect("notelist.db")
            c = conn.cursor()

            c.execute('DELETE FROM noteList WHERE title = ?',
                      (noteToDeleteTitle,))

            conn.commit()
            conn.close()
        except:
            errorMessage = QMessageBox()
            errorMessage.setText("No note selected")
            errorMessage.exec_()

        self.loadNotesTitle()

    def newNote(self):

        self.isNewNote = True

        self.textBoxTitle.setText("")
        self.textBoxContent.setPlainText("")

        currentSelectedNote = self.notesTitleListWidget.currentRow()

        try:
            # This line deselects the note in the title list
            self.notesTitleListWidget.item(
                currentSelectedNote).setSelected(False)
        except:
            # If no note is selected then do nothing
            pass

    def backupNote(self):
        filePath = QFileDialog.getSaveFileName(self)
        filePath = filePath[0]

        # Append filetype to file path if it doesnt already contain
        if filePath[-3:] != ".db":
            filePath += ".db"

        shutil.copy("notelist.db", filePath)

    def importNote(self):

        if exists("notelist.db"):
            warningMessage = QMessageBox()
            warningMessage.setText(
                "Importing notes will overwrite current notes")
            warningMessage.setStandardButtons(
                QMessageBox.Ok | QMessageBox.Cancel)
            warningMessage.buttonClicked.connect(self.importNoteConfirmed)
            warningMessage.exec_()

    def importNoteConfirmed(self, i):

        if i.text() == "OK":

            # Get File Name
            filePath = QFileDialog.getOpenFileName()
            filePath = filePath[0]
            currentPath = os.getcwd()

            # Copy backup to current directory
            shutil.copy(filePath, currentPath)
            # gets just the file name
            filePath = filePath.split("/")
            newFilePath = filePath[-1]
            # renames file
            os.rename(newFilePath, "notelist.db")
            self.loadNotesTitle()
        else:
            pass

    def loadNotes(self):

        self.isNewNote = False
        noteToLoad = self.notesTitleListWidget.currentItem().text()
        conn = sqlite3.connect("notelist.db")
        c = conn.cursor()

        c.execute("SELECT * FROM noteList WHERE title = ?", (noteToLoad,))
        databaseValues = c.fetchall()

        conn.commit()
        conn.close()

        # database values if a tuple so needs to get the first value, id counts
        # as 0 index
        self.textBoxContent.setPlainText(databaseValues[0][2])
        self.textBoxTitle.setText(databaseValues[0][1])
        self.currentlyLoadedTitle = databaseValues[0][1]

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
