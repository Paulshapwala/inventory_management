import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QPushButton,QStackedLayout, QLabel,
                              QMainWindow, QTextEdit, QVBoxLayout, QWidget, 
                              QHBoxLayout, QGridLayout)

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Store")


# app = QApplication(sys.argv)       
# window = mainWindow()
# window.show()
# app.exec()