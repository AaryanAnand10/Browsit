from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(2)  # Initial width of the sidebar
        self.setMinimumWidth(2)  # Set minimum width to initial width
        self.setMaximumWidth(2)  # Initial maximum width

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.animation = QPropertyAnimation(self, b"maximumWidth")
        self.animation.setDuration(300)

    def enterEvent(self, event):
        self.animateSidebar(expand=True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animateSidebar(expand=False)
        super().leaveEvent(event)

    def animateSidebar(self, expand):
        if expand:
            self.animation.setEndValue(150)  # Expand to maximum width
        else:
            self.animation.setEndValue(2)  # Collapse to initial width
        self.animation.start()


class MyWebBrowser(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MyWebBrowser, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        self.setWindowTitle("Web Browser")
        self.showMaximized()

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL and press Enter")
        self.url_bar.setFixedHeight(30)  # Increase the height of the URL bar
        self.url_bar.setMinimumWidth(
            300
        )  # Optional: Set a minimum width for the URL bar
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        navbar = QToolBar()
        self.addToolBar(navbar)

        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        navbar.addWidget(self.url_bar)

        self.go_btn = QPushButton("Go")
        self.go_btn.clicked.connect(self.navigate_to_url)
        navbar.addWidget(self.go_btn)

        self.back_btn = QPushButton("<")
        self.back_btn.clicked.connect(self.browser.back)
        navbar.addWidget(self.back_btn)

        self.forward_btn = QPushButton(">")
        self.forward_btn.clicked.connect(self.browser.forward)
        navbar.addWidget(self.forward_btn)

        self.reload_btn = QPushButton("Reload")
        self.reload_btn.clicked.connect(self.browser.reload)
        navbar.addWidget(self.reload_btn)

        shortcutPrevPage = QKeySequence(Qt.ALT + Qt.Key_Left)
        self.shortcutPrevPage = QShortcut(shortcutPrevPage, self)
        self.shortcutPrevPage.activated.connect(self.browser.back)

        shortcutForwPage = QKeySequence(Qt.ALT + Qt.Key_Right)
        self.shortcutForwPage = QShortcut(shortcutForwPage, self)
        self.shortcutForwPage.activated.connect(self.browser.forward)

        shortcutJumpSearch = QKeySequence(Qt.CTRL + Qt.Key_Slash)
        self.shortcutJumpSearch = QShortcut(shortcutJumpSearch, self)
        self.shortcutJumpSearch.activated.connect(self.focus_url_bar)

        self.sidebar = Sidebar()

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def focus_url_bar(self):
        self.url_bar.setFocus()

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("https://"):
            url = "https://" + url
        self.browser.setUrl(QUrl(url))


app = QApplication([])
main_window = MyWebBrowser()
main_window.show()
app.exec_()
