import sys
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QAction, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QTabWidget, QMainWindow

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PyQtWebEngine Browser")
        self.setGeometry(100, 100, 1000, 700)
        
        
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        
        
        self.navigation_bar = QToolBar("Navigation")
        self.addToolBar(self.navigation_bar)
        
        # Back button
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.browser.back)
        self.navigation_bar.addAction(back_btn)

        # Forward button
        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.browser.forward)
        self.navigation_bar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        self.navigation_bar.addAction(reload_btn)
        
        # Stop button
        stop_btn = QAction("Stop", self)
        stop_btn.triggered.connect(self.browser.stop)
        self.navigation_bar.addAction(stop_btn)
        

        DuckDuckGo_btn = QAction("Homepage", self)
        self.navigation_bar.addAction(DuckDuckGo_btn)


        

        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navigation_bar.addWidget(self.url_bar)
        
        
        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.loadProgress.connect(self.update_progress)
        self.browser.titleChanged.connect(self.setWindowTitle)
        DuckDuckGo_btn.triggered.connect(lambda: self.browser.setUrl(QUrl('https://minimalbrowserhomepage.netlify.app/')))
        
        
        self.browser.setUrl(QUrl("https://minimalbrowserhomepage.netlify.app/"))

    def navigate_to_url(self):
        """Loads the URL from the URL bar."""
        url = self.url_bar.text()
        
        if not url:
            return

        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        
        self.browser.setUrl(QUrl(url))
    

    def update_url_bar(self, url):
        """Updates the URL bar with the current page URL."""
        self.url_bar.setText(url.toString())
        self.url_bar.setCursorPosition(0) 

    def update_progress(self, progress):
        """Updates the status bar with the loading progress."""
        if progress < 100:
            self.statusBar().showMessage(f"Loading... {progress}%")
        else:
            self.statusBar().showMessage("Done", 2000) 

# Main application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("PyQtWebEngine Browser")
    
    main_window = WebBrowser()
    main_window.show()
    

    sys.exit(app.exec_())

