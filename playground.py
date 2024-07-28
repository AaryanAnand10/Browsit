# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# import sys

# class Window(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("QHBoxLayout Example")
#         # Create a QHBoxLayout instance
#         layout = QHBoxLayout()
        
#         # Create buttons
#         left_button = QPushButton("Left-Most")
#         center_button = QPushButton("Center")
#         right_button = QPushButton("Right-Most")
        
#         # Set size policies to give proportional sizes
#         left_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
#         center_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
#         right_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
#         # Add widgets to the layout with stretch factors
#         layout.addWidget(left_button, 1)
#         layout.addWidget(center_button, 1)
#         layout.addWidget(right_button, 1)
        
#         # Set the layout on the application's window
#         self.setLayout(layout)
#         self.showMaximized()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Window()
#     window.show()
#     sys.exit(app.exec_())

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import browser as br

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QHBoxLayout Example")
        # Create a QHBoxLayout instance
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Center the layout within the window
        
        # Create buttons
        left_button = QPushButton("Google Search Engine")
        center_button = QPushButton("Center")
        right_button = QPushButton("Right-Most")
        
        # Set the fixed size for square buttons
        button_size = 380  # Size of the square buttons (you can adjust this value)
        left_button.setFixedSize(button_size, button_size)
        center_button.setFixedSize(button_size, button_size)
        right_button.setFixedSize(button_size, button_size)
        
        # Set size policies to ensure the buttons are square
        left_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        center_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        right_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Add widgets to the layout with stretch factors
        layout.addWidget(left_button)
        layout.addWidget(center_button)
        layout.addWidget(right_button)
        
        # Set the layout on the application's window
        self.setLayout(layout)
        self.showMaximized()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
