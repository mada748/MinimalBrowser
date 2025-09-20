import sys
import os
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInfo, QWebEngineUrlRequestInterceptor
from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QAction, QMessageBox, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QStackedWidget, QDockWidget, QFileDialog, QProgressBar, QLabel



 

class AdBlockerInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ad_domains = [
            # Juicy ad list
            "static.xx.fbcdn.net",
            "scontent.xx.fna.fbcdn.net",
            "cdn.taboola.com",
            "cdn.outbrain.com",
            "rtb.criteo.com",
            "contextual.media.net",
            "aax-us-east.amazon-adsystem.com",
            "googleads.g.doubleclick.net",
            "www.googletagservices.com",
            "www.google-analytics.com",
            "adservice.google.com",
            "ad.doubleclick.net",
            "afs.googlesyndication.com",
            "stats.g.doubleclick.net",
            "m.doublecklick.net",
            "static.doublecklick.net",
            "meadiavisor.doubleclick.net",
            "ads30.adcolony.com",
            "adc3.adconoly.com",
            "events3alt.adcolony.com",
            "wd.adcolony.com",
            "static.media.net",
            "media.net",
            "adtago.s3.amazonaws.com",
            "https://bat.bing.com/bat.js",
            "https://static.ads-twitter.com/uwt.js",
            "https://connect.facebook.net/en_US/fbevents.js",
            "analyticsengine.s3.amazonaws.com",
            "analytics.s3.amazonaws.com",
            "advice-ads.s3.amazonaws.com",
            "advice-ads.s3.amazonaws.com",
            "pagead2.googleadservices.com",
            "adc3-launch.adcolony.com",
            "static.doubleclick.net",
            "m.doubleclick.net",
            "mediavisor.doubleclick.net",
            "analytics.google.com",
            "adm.hotjar.com",
            "click.googleanalytics.com",
            "pagead2.googlesyndication.com",
            "google-analytics.com",
            "ssl.google-analytics.com",
            "identify.hotjar.com",
            "insights.hotjar.com",
            "script.hotjar.com",
            "surveys.hotjar.com",
            "careers.hotjar.com",
            "cdn.mouseflow.com",
            "o2.mouseflow.com",
            "freshmarketer.com",
            "claritybt.freshmarketer.com",
            "fwtracks.freshmarketer.com",
            "cdn-test.mouseflow.com",
            "stats.wp.com",
            "luckyorange.com",
            "api.luckyorange.com",
            "realtime.luckyorange.com",
            "cdn.luckyorange.com",
            "w1.luckyorange.com",
            "upload.luckyorange.net",
            "cs.luckyorange.net",
            "settings.luckyorange.net",
            "notify.bugsnag.com",
            "sessions.bugsnag.com",
            "api.bugsnag.com",
            "app.bugsnag.com",
            "browser.sentry-cdn.com",
            "app.getsentry.com",
            "tools.mouseflow.com",
            "pixel.facebook.com",
            "an.facebook.com",
            "static.ads-twitter.com",
            "ads-api.twitter.com",
            "ads.linkedin.com",
            "analytics.pointdrive.linkedin.com",
            "ads.pinterest.com",
            "log.pinterest.com",
            "analytics.pinterest.com",
            "trk.pinterest.com",
            "events.reddit.com",
            "events.redditmedia.com",
            "ads.youtube.com",
            "ads-api.tiktok.com",
            "analytics.tiktok.com",
            "ads-sg.tiktok.com",
            "analytics-sg.tiktok.com",
            "business-api.tiktok.com",
            "ads.tiktok.com",
            "log.byteoversea.com",
            "ads.yahoo.com",
            "analytics.yahoo.com",
            "geo.yahoo.com",
            "udcm.yahoo.com",
            "analytics.query.yahoo.com",
            "partnerads.ysm.yahoo.com",
            "log.fc.yahoo.com",
            "gemini.yahoo.com",
            "adtech.yahooinc.com",
            "appmetrica.yandex.ru",
            "adfstat.yandex.ru",
            "metrika.yandex.ru",
            "adfox.yandex.ru",
            "auction.unityads.unity3d.com",
            "webview.unityads.unity3d.com",
            "config.unityads.unity3d.com",
            "adserver.unityads.unity3d.com",
            "iot-eu-logser.realme.com",
            "iot-logser.realme.com",
            "bdapi-ads.realmemobile.com",
            "bdapi-in-ads.realmemobile.com",
            "api.ad.xiaomi.com",
            "data.mistat.xiaomi.com",
            "data.mistat.india.xiaomi.com",
            "data.mistat.rus.xiaomi.com",
            "sdkconfig.ad.xiaomi.com",
            "sdkconfig.ad.intl.xiaomi.com",
            "tracking.rus.miui.com",
            "adsfs.oppomobile.com",
            "adx.ads.oppomobile.com",
            "ck.ads.oppomobile.com",
            "data.ads.oppomobile.com",
            "metrics.data.hicloud.com",
            "metrics2.data.hicloud.com",
            "grs.hicloud.com",
            "logservice.hicloud.com",
            "logservice1.hicloud.com",
            "logbak.hicloud.com",
            "iadsdk.apple.com",
            "metrics.icloud.com",
            "metrics.mzstatic.com",
            "api-adservices.apple.com",
            "books-analytics-events.apple.com",
            "weather-analytics-events.apple.com",
            "notes-analytics-events.apple.com",
            "samsungads.com",
            "smetrics.samsung.com",
            "samsung-com.112.2o7.net",
            "analytics-api.samsunghealthcn.com",
            "widgets.pinterest.com",
            "extmaps-api.yandex.net",
            "advretising.yandex.ru",
            "offerwall.yandex.net",
            "udc.yahoo.com",
            "advretising.yahoo.com",
            "advertising.apple.com"
        ]
    # adblocker logic btw
    def interceptRequest(self, info: QWebEngineUrlRequestInfo):# the code works who the dablocker says if you are X ad domain im gonna shoot
        url = info.requestUrl().host()
        if any(ad_domain in url for ad_domain in self.ad_domains):# since the site doesn't respond it checks if he needs to shoot
            print("AdBlocker: Blocking request to", url)# and if yes it shoots
            info.block(True)

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PyQtWebEngine Browser")
        self.setGeometry(100, 100, 1000, 700)
        
        self.bookmarks = {}
        
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
        self.profile.setPersistentStoragePath(os.path.join(os.path.expanduser('~'), '.minimal_browser_data'))
        
        self.interceptor = AdBlockerInterceptor(self.profile)
        self.profile.setUrlRequestInterceptor(self.interceptor)

        # Connecting downloading stuff do not matter
        self.profile.downloadRequested.connect(self.handle_download_requested)

        self.web_view_stack = QStackedWidget()
        self.setCentralWidget(self.web_view_stack)

        self.sidebar_dock = QDockWidget("Tabs", self)
        self.sidebar_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sidebar_dock)
        self.sidebar_dock.setFixedWidth(200)

        sidebar_content_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_content_widget)

        self.tab_list_widget = QListWidget()
        self.tab_list_widget.itemClicked.connect(self.select_tab_from_sidebar)
        
        new_tab_btn_sidebar = QPushButton("New Tab")
        new_tab_btn_sidebar.clicked.connect(lambda: self.new_tab())
        
        remove_tab_btn_sidebar = QPushButton("Remove Tab")
        remove_tab_btn_sidebar.clicked.connect(self.remove_current_tab)

        button_layout = QHBoxLayout()
        button_layout.addWidget(new_tab_btn_sidebar)
        button_layout.addWidget(remove_tab_btn_sidebar)

        sidebar_layout.addWidget(self.tab_list_widget)
        sidebar_layout.addLayout(button_layout)
        
        # - buttons and navigation -

        # navigation bar
        self.sidebar_dock.setWidget(sidebar_content_widget)
        self.navigation_bar = QToolBar("Navigation")
        self.addToolBar(self.navigation_bar)
        
        # back
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.back_to_tab)
        self.navigation_bar.addAction(back_btn)
        
        # going forward (only works if you pressed self.back_to_tab)
        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.forward_on_tab)
        self.navigation_bar.addAction(forward_btn)
        
        # realoading
        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.reload_tab)
        self.navigation_bar.addAction(reload_btn)
        
        # stop loading
        stop_btn = QAction("Stop", self)
        stop_btn.triggered.connect(self.stop_tab)
        self.navigation_bar.addAction(stop_btn)

        # Sidebar 
        toggle_sidebar_btn = QAction("Toggle Sidebar", self)
        toggle_sidebar_btn.triggered.connect(self.sidebar_dock.toggleViewAction().trigger)
        self.navigation_bar.addAction(toggle_sidebar_btn)
        
        # homepage
        homepage_btn = QAction("Homepage", self)
        homepage_btn.triggered.connect(lambda: self.new_tab(QUrl('https://minimalbrowserhomepage.netlify.app/')))
        self.navigation_bar.addAction(homepage_btn)
        
        # Bookmarking (what term is even this)
        add_bookmark_btn = QAction("Add Bookmark", self)
        add_bookmark_btn.triggered.connect(self.add_bookmark)
        self.navigation_bar.addAction(add_bookmark_btn)
        
        # Bookmarks 
        show_bookmarks_btn = QAction("Bookmarks", self)
        show_bookmarks_btn.triggered.connect(self.show_bookmarks_list)
        self.navigation_bar.addAction(show_bookmarks_btn)
        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navigation_bar.addWidget(self.url_bar)
        
        # - New tab stuff -

        
        self.new_tab(QUrl('https://minimalbrowserhomepage.netlify.app/'))
        
    def new_tab(self, qurl=None):
        if qurl is None:
            qurl = QUrl('https://minimalbrowserhomepage.netlify.app/')
        
        browser = QWebEngineView()
        browser.setUrl(qurl)
        
        index = self.web_view_stack.addWidget(browser)
        
        item = QListWidgetItem("New Tab")
        self.tab_list_widget.addItem(item)

        
        self.web_view_stack.setCurrentIndex(index)
        self.tab_list_widget.setCurrentItem(item)
        
        browser.urlChanged.connect(lambda url, browser=browser: self.update_url_bar(url, browser))
        browser.loadProgress.connect(lambda progress, browser=browser: self.update_progress(progress, browser))
        browser.titleChanged.connect(lambda title, browser=browser: self.tab_list_widget.item(self.web_view_stack.indexOf(browser)).setText(title))
        browser.iconChanged.connect(lambda icon, browser=browser: self.tab_list_widget.item(self.web_view_stack.indexOf(browser)).setIcon(icon))
        
    # - Removing tab stuff (work in progress) -   
    def remove_current_tab(self):
        if self.web_view_stack.count() < 2:
            QMessageBox.information(self, "Tab Menager", "Last tab closed extiting with code 0...")
            SHUTDOWN = True
            exit()
            return

        current_index = self.web_view_stack.currentIndex()
        
        widget_to_remove = self.web_view_stack.widget(current_index)
        self.web_view_stack.removeWidget(widget_to_remove)
        widget_to_remove.deleteLater()
        
        self.tab_list_widget.takeItem(current_index)
        
        if self.web_view_stack.count() > 0:
            if current_index >= self.web_view_stack.count():
                new_index = self.web_view_stack.count() - 1
            else:
                new_index = current_index
            self.web_view_stack.setCurrentIndex(new_index)
            self.tab_list_widget.setCurrentRow(new_index)

    def select_tab_from_sidebar(self, item):
        index = self.tab_list_widget.row(item)
        self.web_view_stack.setCurrentIndex(index)
        current_browser = self.web_view_stack.currentWidget()
        if current_browser:
            self.update_url_bar(current_browser.url(), current_browser)
            self.setWindowTitle(current_browser.title())
    
    def navigate_to_url(self):
        self.Httpwarning()
        current_browser = self.web_view_stack.currentWidget()
        if current_browser:
            url_text = self.url_bar.text()
            if not url_text:
                return

            if not url_text.startswith(("http://", "https://")):
                url_text = "http://" + url_text
            
            current_browser.setUrl(QUrl(url_text))

    def Httpwarning(self):
        current_browser = self.web_view_stack.currentWidget()
        try:
            current_browser.setUrl(QUrl(url_text))
        except UnboundLocalError:
            print("SiteProtection: ERROR 984 - UnBound Local Error")
            return            
        url_text = self.url.bar.text()
        if not url_text:
                        print("SiteProtection: ERROR 657 - unable to check url")
                        return


        if self.url_text.startwith("http://"):
            QMessageBox.warning(self, "Insecure Connection", "The site", url_text, "is not safe and it may track or steal your data.")
            print("SteProtection: Warning user conneecting to insecure site", url_text)
        

    def close_current_tab(self, index):
        if self.web_view_stack.count() < 2:
            return
            
        widget_to_remove = self.web_view_stack.widget(index)
        self.web_view_stack.removeWidget(widget_to_remove)
        widget_to_remove.deleteLater()
        
        self.tab_list_widget.takeItem(index)

    def current_tab_changed(self, index):
        current_browser = self.web_view_stack.currentWidget()
        if current_browser:
            self.update_url_bar(current_browser.url(), current_browser)
            self.setWindowTitle(current_browser.title())

    def update_url_bar(self, url, browser=None):
        if browser != self.web_view_stack.currentWidget():
            return
        
        self.url_bar.setText(url.toString())
        self.url_bar.setCursorPosition(0)

    def update_progress(self, progress, browser=None):
        if browser != self.web_view_stack.currentWidget():
            return
        
        if progress < 100:
            self.statusBar().showMessage(f"Loading... {progress}%")
        else:
            self.statusBar().showMessage("Done", 2000)

    def back_to_tab(self):
        current_browser = self.web_view_stack.currentWidget()
        if current_browser:
            current_browser.back()
            
    def forward_on_tab(self):
        current_browser = self.web_view_stack.currentWidget()
        if current_browser:
            current_browser.forward()

    def reload_tab(self):
        current_browser = self.web_view_stack.currentWidget()
        if current_browser:
            current_browser.reload()

    def stop_tab(self):
        current_browser = self.web_view_stack.currentWidget()
        if current_browser:
            current_browser.stop()
    
    def add_bookmark(self):
        current_browser = self.web_view_stack.currentWidget()
        if current_browser:
            url = current_browser.url().toString()
            title = current_browser.title()
            if url not in self.bookmarks:
                self.bookmarks[url] = title
                QMessageBox.information(self, "Bookmark Added", f"Added '{title}' to bookmarks.")
            else:
                QMessageBox.warning(self, "Bookmark Exists", "This page is already bookmarked.")

    def show_bookmarks_list(self):
        self.bookmark_window = QWidget()
        self.bookmark_window.setWindowTitle("Bookmarks")
        self.bookmark_window.setGeometry(200, 200, 400, 300)
        
        main_layout = QVBoxLayout()
        list_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        
        self.bookmark_list = QListWidget()
        
        for url, title in self.bookmarks.items():
            item = QListWidgetItem(f"{title} - {url}")
            item.setData(0, url)
            self.bookmark_list.addItem(item)
        
        self.bookmark_list.itemDoubleClicked.connect(self.open_bookmark)
        
        list_layout.addWidget(self.bookmark_list)
        main_layout.addLayout(list_layout)
        
        self.bookmark_window.setLayout(main_layout)
        self.bookmark_window.show()

    def open_bookmark(self, item):
        url = item.data(0)
        self.new_tab(QUrl(url))

    def handle_download_requested(self, download):
        suggested_filename = download.downloadFileName()
        
        # Ask user where to save
        path, _ = QFileDialog.getSaveFileName(self, "Save File", suggested_filename)
        if path:
            download.setPath(path)
            download.accept()

            # Create a download widget
            download_widget = QWidget()
            layout = QVBoxLayout(download_widget)
            label = QLabel(f"Downloading: {os.path.basename(path)}")
            progress_bar = QProgressBar()
            progress_bar.setValue(0)
            layout.addWidget(label)
            layout.addWidget(progress_bar)
            
            # Add to download window
            if not hasattr(self, 'download_window') or not self.download_window:
                self.download_window = QWidget()
                self.download_window.setWindowTitle("Downloads")
                self.download_window.setGeometry(300, 300, 400, 300)
                self.download_layout = QVBoxLayout(self.download_window)
                self.download_window.setLayout(self.download_layout)

            self.download_layout.addWidget(download_widget)
            self.download_window.show()

            # Update progress
            download.downloadProgress.connect(lambda received, total: self.update_download_progress(progress_bar, received, total))
            download.finished.connect(lambda: self.download_finished(download, progress_bar, label))
        else:
            download.cancel()

    def update_download_progress(self, progress_bar, received, total):
        if total > 0:
            progress = int((received / total) * 100)
            progress_bar.setValue(progress)

    def download_finished(self, download, progress_bar, label):
        if download.state() == download.DownloadCompleted:
            label.setText(f"Download completed: {os.path.basename(download.path())}")
            print("Download", {os.path.basename(download.path())}, "In", {download.path()})
            QMessageBox.information(self, "Download Completed", f"File saved to:\n{download.path()}")
        elif download.state() == download.DownloadCancelled:
            label.setText("Download cancelled.")
        elif download.state() == download.DownloadInterrupted:
            label.setText("Download interrupted.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Minimalist")
    
    main_window = WebBrowser()
    main_window.show()
    
    sys.exit(app.exec_())
    
    sys.exit(app.exec_())
    sys.exit(app.exec_())



