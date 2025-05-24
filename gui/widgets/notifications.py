from PyQt5.QtWidgets import (QLabel, QMenu, QAction, 
                             QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QFrame, QScrollArea, QWidgetAction, QSizePolicy)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QCursor, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QSize, QPoint, pyqtSignal, QEvent
import os

class NotificationItem:
    """Class to represent a notification"""
    def __init__(self, title, message):
        self.title = title
        self.message = message
        self.read = False
    
    def mark_as_read(self):
        self.read = True

class NotificationLabel(QLabel):
    """Custom label for notification items"""
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWordWrap(True)
        # HTML content with classes for styling via QSS
        content = f"""<div>
            <span class="notification-title" style="font-weight:bold;color:#bd93f9;font-size:18px;">{title}</span><br>
            <span class="notification-message" style="color:#f8f8f2;font-size:18px">{message}</span>
        </div>"""
        self.setText(content)
        self.setObjectName("notificationItem")
        self.setProperty("class", "notificationItem")  # For QSS styling
        self.setMinimumWidth(200)

class ClickableNotificationBell(QLabel):
    """Clickable notification bell with badge counter"""
    notificationsCleared = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set object name for QSS styling
        self.setObjectName("notificationBell")
        
        # Set up the bell icon
        self.icon = QIcon("gui/widgets/resources/notification-bell.png")
        self.pixmap = self.icon.pixmap(32, 32)
        self.setPixmap(self.pixmap)
        self.setFixedSize(32, 32)
        
        # Make the label clickable
        self.setCursor(Qt.PointingHandCursor)
        
        # Notification list
        self.notifications = []
        
        # Create the custom notification menu
        self.menu = QMenu(self)
        self.menu.setObjectName("notificationMenu")
        
        # Badge counter
        self.unread_count = 0
        self.show_badge = False
        
        # Load QSS file if it exists
        self.load_styles()
    
    def load_styles(self):
        """Load styles from QSS file"""
        qss_path = os.path.join(os.path.dirname(__file__), "themes", "notifications.qss")
        if os.path.exists(qss_path):
            print(qss_path)
            with open(qss_path, "r") as f:
                stylesheet = f.read()
                # Apply stylesheet to the menu
                self.menu.setStyleSheet(stylesheet)
        else:
            print("not found")
        
    def add_notification(self, title, message):
        """Add a new notification to the list"""
        notification = NotificationItem(title, message)
        self.notifications.append(notification)
        self.unread_count += 1
        self.show_badge = True
        self.update()  # Redraw to show badge
        
    def update_menu(self):
        """Update the menu with current notifications"""
        # Clear existing menu items
        self.menu.clear()
        
        # Add header
        header = QLabel("Notifications")
        header.setObjectName("notificationHeader")
        header_action = QWidgetAction(self.menu)
        header_action.setDefaultWidget(header)
        self.menu.addAction(header_action)
        
        # Add notifications or "No new notifications" message
        if not self.notifications:
            no_notifications = QLabel("No new notifications")
            no_notifications.setObjectName("emptyNotification")
            no_action = QWidgetAction(self.menu)
            no_action.setDefaultWidget(no_notifications)
            self.menu.addAction(no_action)
        else:
            # Create container for notifications
            notifications_widget = QWidget()
            notifications_layout = QVBoxLayout(notifications_widget)
            notifications_layout.setSpacing(0)
            notifications_layout.setContentsMargins(0, 0, 0, 0)
            
            # Add all notifications
            for notification in self.notifications:
                notification_label = NotificationLabel(notification.title, notification.message)
                notifications_layout.addWidget(notification_label)
            
            # Add some padding at the bottom
            spacer = QWidget()
            spacer.setFixedHeight(5)
            notifications_layout.addWidget(spacer)
            
            # Set up scrollable area
            scroll_area = QScrollArea()
            scroll_area.setObjectName("notificationScrollArea")
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(notifications_widget)
            scroll_area.setFixedSize(300, min(350, max(100, len(self.notifications) * 70)))
            scroll_area.setFrameShape(QFrame.NoFrame)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            
            scroll_action = QWidgetAction(self.menu)
            scroll_action.setDefaultWidget(scroll_area)
            self.menu.addAction(scroll_action)
        
    def mousePressEvent(self, event):
        """Show the dropdown menu when the bell is clicked"""
        if event.button() == Qt.LeftButton:
            # Update the menu before showing it
            self.update_menu()
            
            # Show the menu below the bell icon
            self.menu.exec_(self.mapToGlobal(QPoint(0, self.height())))
            
            # Mark all notifications as read
            for notification in self.notifications:
                notification.mark_as_read()
            
            # Clear notifications list
            self.notifications.clear()
            
            # Reset counter and badge
            self.unread_count = 0
            self.show_badge = False
            self.update()  # Redraw to hide badge
            
            # Emit signal that notifications were cleared
            self.notificationsCleared.emit()
        else:
            super().mousePressEvent(event)
    
    def paintEvent(self, event):
        """Custom paint event to draw the badge"""
        super().paintEvent(event)
        
        if self.show_badge and self.unread_count > 0:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Draw red circle with border for better visibility
            badge_size = 16
            painter.setPen(QPen(QColor(180, 0, 0), 1))  # Darker red border
            painter.setBrush(QColor(255, 0, 0))  # Red fill
            painter.drawEllipse(self.width() - badge_size, 0, badge_size, badge_size)
            
            # Draw count text with improved visibility
            painter.setPen(QColor(255, 255, 255))  # White text
            painter.setFont(QFont("Arial", 8, QFont.Bold))
            
            # Handle different number lengths
            text = str(min(self.unread_count, 99))
            if self.unread_count > 99:
                text = "99+"
                
            text_width = painter.fontMetrics().horizontalAdvance(text)
            
            # Convert float coordinates to integers
            x_pos = int(self.width() - badge_size + (badge_size - text_width) / 2)
            y_pos = int(badge_size / 2 + 4)
            
            # Use integer coordinates for drawText
            painter.drawText(x_pos, y_pos, text)



if __name__ == "__main__":
    import sys
    
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Notification Bell Example")
            self.setGeometry(100, 100, 800, 600)
            
            # Create main widget and layout
            main_widget = QWidget()
            layout = QHBoxLayout(main_widget)
            
            # Add stretch to push the bell to the right
            layout.addStretch(1)
            
            # Add the notification bell
            self.bell_icon = ClickableNotificationBell()
            layout.addWidget(self.bell_icon)
            
            self.setCentralWidget(main_widget)
            
            # Add some sample notifications
            self.bell_icon.add_notification("New Message", "You received a new message from User123")
            self.bell_icon.add_notification("System Update", "Application update is available")
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())