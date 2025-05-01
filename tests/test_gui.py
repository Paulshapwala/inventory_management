
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QStackedLayout, QFrame, QSizePolicy, QSlider)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        settings = self.create_nav_button("settings",r"gui/widgets/resources/settings.png")
        centralWidget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(settings)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def create_nav_button(self, text, icon):
        """icon: path to the icon"""
        btn = QPushButton(text, self)
        btn.setIcon(QIcon(icon))
        btn.setCheckable(True)
        btn.setMinimumHeight(60)
        return btn

app = QApplication(sys.argv)
window = mainWindow()
window.show()
app.exec()