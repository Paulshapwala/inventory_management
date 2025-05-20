"""This module contains globally applied widgets"""

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QListWidget, QFrame
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QPainter
from PyQt5.QtCore import Qt, QPoint, QRect, QSize

def load_theme(path):
        with open(path, "r") as f:
            return f.read()


class NavigationWidget(QWidget):    
    def __init__(self):
        super().__init__()
        self.setObjectName("navigationWidget")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # navigation buttons
        buttons = []
        self.home_btn = self.create_nav_button("Home", r"gui/widgets/resources/home-button.png")
        buttons.append(self.home_btn)
        self.stock_btn = self.create_nav_button("Stock", r"gui/widgets/resources/box.png")
        buttons.append(self.stock_btn)
        self.sold_btn = self.create_nav_button("Sold", r"gui/widgets/resources/dollar.png")
        buttons.append(self.sold_btn)
        self.reports_btn = self.create_nav_button("Reports", r"gui/widgets/resources/analysis.png")
        buttons.append(self.reports_btn)
        self.settings_btn = self.create_nav_button("Settings",r"gui/widgets/resources/settings.png")
        buttons.append(self.settings_btn)
        
        #home is default
        self.home_btn.setChecked(True)
        for button in buttons:
             layout.addWidget(button)
        
        layout.addStretch()
        
        self.setLayout(layout)
        
    def create_nav_button(self, text, icon_path):
        """
    Creates a styled navigation button with an icon and label.

    Parameters:
        text (str): The text label to display on the button.
        icon_path (str): File path to the icon image (e.g., PNG, SVG).

    Returns:
        QPushButton: A QPushButton instance with the specified text and icon.
    """
        btn = QPushButton(text, self)
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(32,32))
        btn.setCheckable(True)
        btn.setMinimumHeight(100)
        return btn
