import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QAction, QTabWidget, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView

class WebBrowser(QMainWindow):
    """
    A simple web browser with a tabbed interface.
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PyQtWebEngine Browser")
        self.setGeometry(100, 100, 1000, 700)
        
        # Create the tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)
        
        # Connect signals for tab management
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        
        # Create navigation toolbar
        self.navigation_bar = QToolBar("Navigation")
        self.addToolBar(self.navigation_bar)
        
        # Navigation actions
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.back_to_tab)
        self.navigation_bar.addAction(back_btn)

        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.forward_on_tab)
        self.navigation_bar.addAction(forward_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.reload_tab)
        self.navigation_bar.addAction(reload_btn)
        
        stop_btn = QAction("Stop", self)
        stop_btn.triggered.connect(self.stop_tab)
        self.navigation_bar.addAction(stop_btn)

        # New tab button
        new_tab_btn = QAction("New Tab", self)
        new_tab_btn.triggered.connect(lambda: self.new_tab())
        self.navigation_bar.addAction(new_tab_btn)
        
        # Homepage button
        homepage_btn = QAction("Homepage", self)
        homepage_btn.triggered.connect(lambda: self.new_tab(QUrl('https://minimalbrowserhomepage.netlify.app/')))
        self.navigation_bar.addAction(homepage_btn)
        
        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navigation_bar.addWidget(self.url_bar)
        
        # Add the first tab
        self.new_tab(QUrl('https://minimalbrowserhomepage.netlify.app/'))
        
    def new_tab(self, qurl=None):
        """Adds a new tab with an optional URL."""
        if qurl is None:
            qurl = QUrl('https://minimalbrowserhomepage.netlify.app/')
            
        browser = QWebEngineView()
        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(index)
        
        browser.setUrl(qurl)
        
        # Connect signals for the new browser instance
        browser.urlChanged.connect(lambda url: self.update_url_bar(url, browser))
        browser.loadProgress.connect(lambda progress: self.update_progress(progress, browser))
        browser.titleChanged.connect(lambda title: self.tabs.setTabText(self.tabs.indexOf(browser), title))
    
    def navigate_to_url(self):
        """Loads the URL from the URL bar in the current tab."""
        current_browser = self.tabs.currentWidget()
        if current_browser:
            url_text = self.url_bar.text()
            if not url_text:
                return

            if not url_text.startswith(("http://", "https://")):
                url_text = "http://" + url_text
            
            current_browser.setUrl(QUrl(url_text))
            
    def close_current_tab(self, index):
        """Closes the current tab."""
        if self.tabs.count() < 2:
            return
            
        self.tabs.removeTab(index)
    
    def current_tab_changed(self, index):
        """Updates the UI when the current tab changes."""
        current_browser = self.tabs.currentWidget()
        if current_browser:
            self.update_url_bar(current_browser.url(), current_browser)
            self.setWindowTitle(current_browser.title())

    def update_url_bar(self, url, browser=None):
        """Updates the URL bar with the current page URL."""
        if browser != self.tabs.currentWidget():
            return
        
        self.url_bar.setText(url.toString())
        self.url_bar.setCursorPosition(0)

    def update_progress(self, progress, browser=None):
        """Updates the status bar with the loading progress."""
        if browser != self.tabs.currentWidget():
            return
            
        if progress < 100:
            self.statusBar().showMessage(f"Loading... {progress}%")
        else:
            self.statusBar().showMessage("Done", 2000)

    def back_to_tab(self):
        """Goes back in the current tab's history."""
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.back()
            
    def forward_on_tab(self):
        """Goes forward in the current tab's history."""
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.forward()

    def reload_tab(self):
        """Reloads the current tab."""
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.reload()

    def stop_tab(self):
        """Stops loading the current tab."""
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.stop()

# Main application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("PyQtWebEngine Browser")
    
    main_window = WebBrowser()
    main_window.show()
    
    sys.exit(app.exec_())

    sys.exit(app.exec_())


