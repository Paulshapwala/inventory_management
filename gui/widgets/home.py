import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QStackedLayout, QFrame, QSizePolicy, QSlider)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from glob_widgets import NavigationWidget, load_theme

class HomeWidget(QWidget):    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("homeWidget")
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Set base styling for all text
        self.setStyleSheet("""
            QLabel {
                color: #f8f8f2;
            }
            QWidget#homeWidget {
                background-color: #282a36;
            }
        """)
        
        # Header section
        header_layout = QHBoxLayout()
        greeting_label = QLabel("Morning, James")
        greeting_label.setFont(QFont("Arial", 24, QFont.Bold))
        
        toggle_layout = QHBoxLayout()
        toggle_layout.setSpacing(10)
        
        toggle_label = QLabel("Turned Disabled")
        toggle_label.setFont(QFont("Arial", 16))
        
        # Custom toggle slider that matches Dracula theme
        toggle_slider = QSlider(Qt.Horizontal)
        toggle_slider.setFixedSize(70, 26)
        toggle_slider.setRange(0, 1)
        toggle_slider.setValue(0)  # Default to disabled
        toggle_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #44475a;
                height: 20px;
                background: #44475a;
                margin: 0px;
                border-radius: 10px;
            }
            QSlider::handle:horizontal {
                background: #ff79c6;
                border: 1px solid #ff79c6;
                width: 24px;
                height: 24px;
                margin: -2px 0px;
                border-radius: 12px;
            }
        """)
        
        toggle_layout.addWidget(toggle_label)
        toggle_layout.addWidget(toggle_slider)
        toggle_layout.setAlignment(Qt.AlignRight)
        
        header_layout.addWidget(greeting_label)
        header_layout.addLayout(toggle_layout)
        main_layout.addLayout(header_layout)
        
        main_layout.addSpacing(30)
        
        # Notifications section
        notifications_label = QLabel("🔔 Notifications")
        notifications_label.setFont(QFont("Arial", 18, QFont.Bold))
        main_layout.addWidget(notifications_label)
        
        no_notifications = QLabel("No new notifications")
        no_notifications.setFont(QFont("Arial", 14))
        no_notifications.setStyleSheet("color: #bd93f9;")
        main_layout.addWidget(no_notifications)
        
        main_layout.addSpacing(20)
        
        # Stock Overview section
        stock_frame = QFrame()
        stock_frame.setFrameShape(QFrame.StyledPanel)
        stock_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #44475a;
                border-radius: 8px;
                background-color: #383a59;
            }
            QLabel {
                color: #f8f8f2;
            }
        """)
        
        stock_layout = QVBoxLayout(stock_frame)
        
        # Stock header with sell button
        stock_header = QHBoxLayout()
        stock_title = QLabel("Stock Overviow")
        stock_title.setFont(QFont("Arial", 20, QFont.Bold))
        
        sell_btn = QPushButton("Sell")
        sell_btn.setFixedSize(100, 40)
        sell_btn.setStyleSheet("""
            QPushButton {
                background-color: #50fa7b;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                color: #282a36;
            }
            QPushButton:hover {
                background-color: #5af78e;
            }
            QPushButton:pressed {
                background-color: #46e66e;
            }
        """)
        
        stock_header.addWidget(stock_title)
        stock_header.addStretch()
        stock_header.addWidget(sell_btn)
        stock_layout.addLayout(stock_header)
        
        stock_layout.addSpacing(10)
        
        # Stock color
        color_label = QLabel("Black")
        color_label.setFont(QFont("Arial", 16))
        # Adding some Dracula-themed styling
        color_label.setStyleSheet("color: #8be9fd;")
        stock_layout.addWidget(color_label)
        
        # Stock details with report button
        details_layout = QHBoxLayout()
        body_label = QLabel("Sold body:")
        body_label.setFont(QFont("Arial", 16))
        
        price_label = QLabel("72.000/=")
        price_label.setFont(QFont("Arial", 16, QFont.Bold))
        price_label.setStyleSheet("color: #f1fa8c;")  # Yellow for price
        
        report_btn = QPushButton("Report")
        report_btn.setFixedSize(100, 40)
        report_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff79c6;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                color: #282a36;
            }
            QPushButton:hover {
                background-color: #ff92d0;
            }
            QPushButton:pressed {
                background-color: #ea6cb0;
            }
        """)
        
        details_layout.addWidget(body_label)
        details_layout.addWidget(price_label)
        details_layout.addStretch()
        details_layout.addWidget(report_btn)
        stock_layout.addLayout(details_layout)
        
        main_layout.addWidget(stock_frame)
        main_layout.addStretch()
        
        self.setLayout(main_layout)


class InventoryApp(QMainWindow):
    """Main inventory application window with Dracula theme"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory")
        self.resize(900, 600)
        
        # Set window style with Dracula theme colors
        self.setStyleSheet("""
            QMainWindow {
                background-color: #282a36;
                color: #f8f8f2;
            }
            QWidget {
                background-color: #282a36;
                color: #f8f8f2;
            }
            QToolTip {
                background-color: #44475a;
                color: #f8f8f2;
                border: 1px solid #6272a4;
            }
        """)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create central widget
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar navigation
        self.navigation = NavigationWidget()
        self.navigation.setFixedWidth(200)
        
        # Create stacked layout for different pages
        self.stacked_layout = QStackedLayout()
        
        # Create different page widgets
        self.home_widget = HomeWidget()
        
        # Create placeholder widgets with proper theming
        self.stock_widget = QWidget()
        self.stock_widget.setStyleSheet("background-color: #282a36;")
        stock_layout = QVBoxLayout(self.stock_widget)
        stock_layout.addWidget(QLabel("Stock Page - Coming Soon"))
        stock_layout.addStretch()
        
        self.sold_widget = QWidget()
        self.sold_widget.setStyleSheet("background-color: #282a36;")
        sold_layout = QVBoxLayout(self.sold_widget)
        sold_layout.addWidget(QLabel("Sold Page - Coming Soon"))
        sold_layout.addStretch()
        
        self.reports_widget = QWidget()
        self.reports_widget.setStyleSheet("background-color: #282a36;")
        reports_layout = QVBoxLayout(self.reports_widget)
        reports_layout.addWidget(QLabel("Reports Page - Coming Soon"))
        reports_layout.addStretch()
        
        self.settings_widget = QWidget()
        self.settings_widget.setStyleSheet("background-color: #282a36;")
        inventor_layout = QVBoxLayout(self.settings_widget)
        inventor_layout.addWidget(QLabel("Inventor Page - Coming Soon"))
        inventor_layout.addStretch()
        
        # Add widgets to stacked layout
        self.stacked_layout.addWidget(self.home_widget)
        self.stacked_layout.addWidget(self.stock_widget)
        self.stacked_layout.addWidget(self.sold_widget)
        self.stacked_layout.addWidget(self.reports_widget)
        self.stacked_layout.addWidget(self.settings_widget)
        
        # Create container for stacked layout
        stacked_container = QWidget()
        stacked_container.setLayout(self.stacked_layout)
        
        # Connect navigation buttons to stacked layout switching
        self.navigation.home_btn.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(0))
        self.navigation.stock_btn.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(1))
        self.navigation.sold_btn.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(2))
        self.navigation.reports_btn.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(3))
        self.navigation.settings_btn.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(4))
        
        # Make buttons exclusive
        button_group = [
            self.navigation.home_btn,
            self.navigation.stock_btn,
            self.navigation.sold_btn,
            self.navigation.reports_btn,
            self.navigation.settings_btn
        ]
        
        for button in button_group:
            button.clicked.connect(lambda checked, btn=button: self.make_exclusive(btn, button_group))
        
        # Add widgets to main layout
        main_layout.addWidget(self.navigation)
        main_layout.addWidget(stacked_container, 1)
        
        self.setCentralWidget(central_widget)
    
    def make_exclusive(self, clicked_button, button_group):
        """Makes navigation buttons act like radio buttons"""
        for button in button_group:
            if button != clicked_button:
                button.setChecked(False)
            else:
                button.setChecked(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(load_theme(r"gui/widgets/themes/dracula.qss"))
    # Set application-wide palette based on Dracula theme
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(40, 42, 54))           # Background
    palette.setColor(QPalette.WindowText, QColor(248, 248, 242))    # Text
    palette.setColor(QPalette.Base, QColor(68, 71, 90))             # Input fields
    palette.setColor(QPalette.AlternateBase, QColor(56, 58, 89))    # Alternate bg
    palette.setColor(QPalette.ToolTipBase, QColor(68, 71, 90))      # Tooltip bg
    palette.setColor(QPalette.ToolTipText, QColor(248, 248, 242))   # Tooltip text
    palette.setColor(QPalette.Text, QColor(248, 248, 242))          # Text fields
    palette.setColor(QPalette.Button, QColor(68, 71, 90))           # Buttons
    palette.setColor(QPalette.ButtonText, QColor(248, 248, 242))    # Button text
    palette.setColor(QPalette.BrightText, QColor(255, 121, 198))    # Bright text (pink)
    palette.setColor(QPalette.Link, QColor(139, 233, 253))          # Links (cyan)
    palette.setColor(QPalette.Highlight, QColor(189, 147, 249))     # Selection bg (purple)
    palette.setColor(QPalette.HighlightedText, QColor(40, 42, 54))  # Selection text
    app.setPalette(palette)
    
    # Create and show window
    window = InventoryApp()
    window.show()
    
    sys.exit(app.exec_())