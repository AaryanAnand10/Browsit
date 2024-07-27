import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import *

class HoverSidebar(QWidget):
    def __init__(self, parent, width, extended_width):
        super().__init__(parent)
        self.normal_width = width
        self.extended_width = extended_width
        self.setFixedWidth(10)
        self.setMaximumWidth(250)
        
        self.layout = QVBoxLayout()

        self.title_label = QLabel("Notes", self)
        self.title_label.setFont(QFont("Courier", 16, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #FFFFFF; margin-bottom: 5px;")  # White text color and margin
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)
        
        self.note_area = QTextEdit(self)
        self.note_area.setPlaceholderText("Take notes here...")
        self.note_area.setStyleSheet("background-color: #555555; color: #FFFFFF; border: none;")
        self.layout.addWidget(self.note_area)
        
        self.setLayout(self.layout)

        # Enable hover events
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)

    def event(self, event):
        if event.type() == QEvent.Type.HoverEnter:
            self.setFixedWidth(self.extended_width)
        elif event.type() == QEvent.Type.HoverLeave:
            self.setFixedWidth(self.normal_width)
        return super().event(event)

    def set_normal_width(self, width):
        self.normal_width = width
        self.setFixedWidth(self.normal_width)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL and press Enter")
        self.url_bar.setFixedHeight(30)  # Increase the height of the URL bar
        self.url_bar.setMinimumWidth(300)  # Optional: Set a minimum width for the URL bar

        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # Set up the toolbar and add the URL bar
        navbar = QToolBar("Navigation")
        self.addToolBar(navbar)

        self.go_btn = QPushButton("Go")
        self.go_btn.clicked.connect(self.navigate_to_url)
        navbar.addWidget(self.go_btn)

        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        navbar.addWidget(self.url_bar)

        # Set the main window properties
        self.setWindowTitle("Browsit")
        self.setGeometry(100, 100, 1920, 1080)
        self.setStyleSheet("""
            QMainWindow {
                background-image: url(images/eagan-hsu-sdewdKGHl5A-unsplash.jpg);
                background-repeat: no-repeat;
                background-position: center;
            }
        """)  # Change background to the image
        self.showMaximized()

        # Create shortcuts for navigating back and forward
        self.shortcutPrevPage = QShortcut(QKeySequence("Alt+Left"), self)
        self.shortcutPrevPage.activated.connect(self.navigate_back)

        self.shortcutForwPage = QShortcut(QKeySequence("Alt+Right"), self)
        self.shortcutForwPage.activated.connect(self.navigate_forward)

        self.shortcutUrlFocus = QShortcut(QKeySequence("Ctrl+/"), self)
        self.shortcutUrlFocus.activated.connect(self.focus_url_bar)

        self.shortcutNewTab = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcutNewTab.activated.connect(self.add_new_tab)

        # Create the Ctrl + W shortcut for closing the current tab
        self.shortcutCloseTab = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcutCloseTab.activated.connect(self.close_current_tab)

        # Create the central widget and set layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
       
        self.initUI()

        # Connect returnPressed signals
        self.text_input.returnPressed.connect(self.perform_search)

    def initUI(self):
        # Create the main layout
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.brows_layout = QHBoxLayout(self.central_widget)
        self.brows_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        

        # Create the Browsit label
        browsit_label = QLabel("Browsit...", self)
        browsit_label.setFont(QFont("Courier", 25))  # Smaller font size
        browsit_label.setStyleSheet("color: #FFFFFF;")  # White text color
        browsit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        browsit_label.setMargin(5)
        browsit_label.setGeometry(1640, 30, 30, 30)
        # main_layout.addWidget(browsit_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.brows_layout.addWidget(browsit_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Create the text input area
        input_container = QWidget(self)
        input_container.setFixedSize(600, 40)  # Smaller size
        input_container.setStyleSheet("background-color: #000000; border-radius: 15px;")

        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(25, 12, 25, 12)  # Adjust margins

        self.text_input = QLineEdit(input_container)
        self.text_input.setStyleSheet("color: #ffffff;")
        self.text_input.setFont(QFont("Courier", 12, QFont.Weight.Bold))  # Smaller font size
        input_layout.addWidget(self.text_input)
        
        self.go_button = QPushButton("GO", input_container)
        self.go_button.setFont(QFont("Courier", 7, QFont.Weight.Bold, italic=True))  # Smaller font size
        self.go_button.setStyleSheet("color: #FFFFFF;")  # White text color
        self.go_button.clicked.connect(self.perform_search)
        input_layout.addWidget(self.go_button)

        # main_layout.addWidget(input_container, alignment=Qt.AlignmentFlag.AlignCenter)
        self.brows_layout.addWidget(input_container, alignment=Qt.AlignmentFlag.AlignCenter)

        self.brows_layout.setContentsMargins(0, 20, 0, 0)

        main_layout.addLayout(self.brows_layout)

        # Create the tab widget for web pages
        self.tab_widget = QTabWidget(self)
        main_layout.addWidget(self.tab_widget)

        # Add the first empty tab with a default web view
        self.add_new_tab()
        
        # Add buttons to the icons container layout
        # # Create round button B
        # round_button2 = QPushButton("B", self)
        # round_button2.setGeometry(1640, 30, 30, 30)  # Place on the leftmost side, same height as round_button1
        # round_button2.setFont(QFont("Courier", 8, QFont.Weight.Bold, italic=True))  # Smaller font size
        # round_button2.setStyleSheet("color: #FFFFFF;")  # White text color

        # Create the Chrome button
        self.chrome_button = QPushButton(self)
        self.chrome_button.setIcon(QIcon("HackathonPrep/google.jpeg"))
        self.chrome_button.setIconSize(QSize(30, 30))  # Set the icon size to match the button size
        self.chrome_button.setGeometry(1500, 67, 30, 30)  # Align horizontally below round_button2
        self.chrome_button.setCheckable(True)
        self.chrome_button.setFixedSize(40, 40)  # Same size as round_button2
        self.chrome_button.setStyleSheet("background-color: none;")

        # Create the Duck button
        self.duck_button = QPushButton(self)
        self.duck_button.setIcon(QIcon("HackathonPrep/ddgico.jpg"))
        self.duck_button.setIconSize(QSize(30, 30))  # Set the icon size to match the button size
        self.duck_button.setGeometry(1620, 67, 30, 30)  # Align horizontally below round_button2
        self.duck_button.setCheckable(True)
        self.duck_button.setFixedSize(40, 40)  # Same size as round_button2
        self.duck_button.setStyleSheet("background-color: none;")
        
        # Create the Yahoo button
        self.yahoo_button = QPushButton(self)
        self.yahoo_button.setIcon(QIcon("HackathonPrep/yahoo.jpeg"))
        self.yahoo_button.setIconSize(QSize(30, 30))  # Set the icon size to match the button size
        self.yahoo_button.setGeometry(1560, 67, 30, 30)  # Align horizontally below round_button2
        self.yahoo_button.setCheckable(True)
        self.yahoo_button.setFixedSize(40, 40)  # Same size as round_button2
        self.yahoo_button.setStyleSheet("background-color: none;")

        # Show the buttons
        # round_button2.show()
        self.chrome_button.show()
        self.yahoo_button.show()
        self.duck_button.show()

        # Create and add the sidebar
        self.sidebar = HoverSidebar(self, width=10, extended_width=250)
        self.sidebar.setStyleSheet("background-color: rgba(51, 51, 51, 150);")  # Translucent background
        self.sidebar.setFixedHeight(self.height())
        self.sidebar.move(0, 0)
        self.sidebar.show()

    def close_current_tab(self):
        current_index = self.tab_widget.currentIndex()
        if current_index != -1:
            self.tab_widget.removeTab(current_index)


    def add_new_tab(self, url=None):
        web_view = QWebEngineView(self)
        if url:
            web_view.setUrl(QUrl(url))
        else:
            web_view.setUrl(QUrl(""))
        self.tab_widget.addTab(web_view, "New Tab")
        self.tab_widget.setCurrentWidget(web_view)

    def perform_search(self):
        query = self.text_input.text() or self.url_bar.text()
        if not query:
            return
        search_url1 = f"https://www.google.com/search?q={query}"
        search_url2 = f"https://search.yahoo.com/search?p={query}"
        search_url3 = f"https://duckduckgo.com/?q={query}"

        if self.chrome_button.isChecked():
            self.add_new_tab(search_url1)
        elif self.yahoo_button.isChecked():
            self.add_new_tab(search_url2)   
        elif self.duck_button.isChecked():
            self.add_new_tab(search_url3)
        else:
            self.add_new_tab(search_url1)
        
    def navigate_back(self):
        current_tab = self.tab_widget.currentWidget()
        if isinstance(current_tab, QWebEngineView):
            current_tab.back()

    def navigate_forward(self):
        current_tab = self.tab_widget.currentWidget()
        if isinstance(current_tab, QWebEngineView):
            current_tab.forward()

    def navigate_home(self):
        self.add_new_tab("")

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("https://"):
            url = "https://" + url
        self.add_new_tab(url)

    def focus_url_bar(self):
        self.url_bar.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())