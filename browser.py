import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QAction, QTabWidget, QMessageBox, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QFileDialog, QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineDownloadItem

class WebBrowser(QMainWindow):
    """
    A simple web browser with a tabbed interface, bookmarks, and downloads.
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PyQtWebEngine Browser")
        self.setGeometry(100, 100, 1000, 700)
        
        # Bookmarks data structure
        self.bookmarks = {}
        
        # tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)
        
        # tab management
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
        homepage_btn.triggered.connect(lambda: self.new_tab(QUrl('https://minimal-browser-simple-search-engine-code.onrender.com/')))
        self.navigation_bar.addAction(homepage_btn)
        
        # Bookmark actions
        add_bookmark_btn = QAction("Add Bookmark", self)
        add_bookmark_btn.triggered.connect(self.add_bookmark)
        self.navigation_bar.addAction(add_bookmark_btn)
        
        show_bookmarks_btn = QAction("Bookmarks", self)
        show_bookmarks_btn.triggered.connect(self.show_bookmarks_list)
        self.navigation_bar.addAction(show_bookmarks_btn)
        
        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navigation_bar.addWidget(self.url_bar)
        
        
        self.new_tab(QUrl('https://minimal-browser-simple-search-engine-code.onrender.com/'))
        
    def new_tab(self, qurl=None):
        """Adds a new tab with an optional URL."""
        if qurl is None:
            qurl = QUrl('https://minimal-browser-simple-search-engine-code.onrender.com/')
            
        browser = QWebEngineView()
       
        browser.setUrl(qurl)
        
        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(index)
        
        browser.urlChanged.connect(lambda url, browser=browser: self.update_url_bar(url, browser))
        browser.loadProgress.connect(lambda progress, browser=browser: self.update_progress(progress, browser))
        browser.titleChanged.connect(lambda title, browser=browser: self.tabs.setTabText(self.tabs.indexOf(browser), title))
        browser.iconChanged.connect(lambda icon, browser=browser: self.tabs.setTabIcon(self.tabs.indexOf(browser), icon))
    
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
    
    def add_bookmark(self):
        """Adds the current page to bookmarks."""
        current_browser = self.tabs.currentWidget()
        if current_browser:
            url = current_browser.url().toString()
            title = current_browser.title()
            if url not in self.bookmarks:
                self.bookmarks[url] = title
                QMessageBox.information(self, "Bookmark Added", f"Added '{title}' to bookmarks.")
            else:
                QMessageBox.warning(self, "Bookmark Exists", "This page is already bookmarked.")

    def show_bookmarks_list(self):
        """Displays a list of bookmarks."""
        # boookmarks window
        self.bookmark_window = QWidget()
        self.bookmark_window.setWindowTitle("Bookmarks")
        self.bookmark_window.setGeometry(200, 200, 400, 300)
        
        main_layout = QVBoxLayout()
        list_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        
        self.bookmark_list = QListWidget()
        
        for url, title in self.bookmarks.items():
            item = QListWidgetItem(f"{title} - {url}")
            item.setData(1, url)  
            self.bookmark_list.addItem(item)
            
        self.bookmark_list.itemClicked.connect(lambda item: self.open_bookmark(item.data(1)))
        
        delete_button = QPushButton("Delete Bookmark")
        delete_button.clicked.connect(self.delete_bookmark)
        
        button_layout.addStretch(1)
        button_layout.addWidget(delete_button)
        button_layout.addStretch(1)
        
        list_layout.addWidget(self.bookmark_list)
        
        main_layout.addLayout(list_layout)
        main_layout.addLayout(button_layout)
        
        self.bookmark_window.setLayout(main_layout)
        self.bookmark_window.show()

    def delete_bookmark(self):
        """Deletes the selected bookmark."""
        selected_item = self.bookmark_list.currentItem()
        if selected_item:
            url_to_delete = selected_item.data(1)
            del self.bookmarks[url_to_delete]
            self.bookmark_list.takeItem(self.bookmark_list.row(selected_item))
            QMessageBox.information(self, "Bookmark Deleted", "Bookmark has been successfully deleted.")
        else:
            QMessageBox.warning(self, "No Bookmark Selected", "Please select a bookmark to delete.")

    def open_bookmark(self, url):
        """Opens a bookmarked URL in a new tab."""
        self.new_tab(QUrl(url))
        
# Main application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Minimalist")
    
    main_window = WebBrowser()
    main_window.show()
    
    sys.exit(app.exec_())

