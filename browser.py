import os
import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QAction
from PyQt6.QtWebEngineCore import (
    QWebEngineProfile,
    QWebEngineUrlRequestInfo,
    QWebEngineUrlRequestInterceptor,
)
from PyQt6.QtWebEngineWidgets import (
    QWebEngineView,
)
from PyQt6.QtWidgets import (
    QApplication,
    QDockWidget,
    QFileDialog,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


class AdBlockerInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ad_domains = [
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
            "advertising.apple.com",
        ]

    def interceptRequest(self, info: QWebEngineUrlRequestInfo):
        url = info.requestUrl().host()
        if any(ad_domain in url for ad_domain in self.ad_domains):
            print("AdBlocker: Blocking request to", url)
            info.block(True)


class DevToolsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Developer Tools")
        self.setGeometry(150, 150, 800, 600)
        self.dev_tools_view = QWebEngineView()
        self.setCentralWidget(self.dev_tools_view)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
        self.main_browser = parent

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F12 and self.main_browser:
            self.main_browser.toggle_dev_tools()
        super().keyPressEvent(event)

    def closeEvent(self, event):
        if self.main_browser and self.main_browser.dev_tools_window.isVisible():
            self.main_browser.toggle_dev_tools()
        event.ignore()


class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 WebEngine Browser")
        self.setGeometry(100, 100, 1000, 700)

        self.bookmarks = {}

        # PyQt6: Accessing the profile
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies
        )
        self.profile.setPersistentStoragePath(
            os.path.join(os.path.expanduser("~"), ".minimal_browser_data")
        )

        self.interceptor = AdBlockerInterceptor(self.profile)
        self.profile.setUrlRequestInterceptor(self.interceptor)
        self.profile.downloadRequested.connect(self.handle_download_requested)

        self.web_view_stack = QStackedWidget()
        self.setCentralWidget(self.web_view_stack)

        self.sidebar_dock = QDockWidget("Tabs", self)
        self.sidebar_dock.setFeatures(
            QDockWidget.DockWidgetFeature.NoDockWidgetFeatures
        )
        # PyQt6: Enum scoping changed
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar_dock)
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

        self.sidebar_dock.setWidget(sidebar_content_widget)
        self.navigation_bar = QToolBar("Navigation")
        self.addToolBar(self.navigation_bar)

        # Navigation Actions
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

        toggle_sidebar_btn = QAction("Toggle Sidebar", self)
        toggle_sidebar_btn.triggered.connect(
            self.sidebar_dock.toggleViewAction().trigger
        )
        self.navigation_bar.addAction(toggle_sidebar_btn)

        homepage_btn = QAction("Homepage", self)
        homepage_btn.triggered.connect(
            lambda: self.new_tab(
                QUrl("https://minimalsite-zeta.vercel.app/API/homepage")
            )
        )
        self.navigation_bar.addAction(homepage_btn)

        add_bookmark_btn = QAction("Add Bookmark", self)
        add_bookmark_btn.triggered.connect(self.add_bookmark)
        self.navigation_bar.addAction(add_bookmark_btn)

        show_bookmarks_btn = QAction("Bookmarks", self)
        show_bookmarks_btn.triggered.connect(self.show_bookmarks_list)
        self.navigation_bar.addAction(show_bookmarks_btn)

        self.dev_tools_action = QAction("Toggle DevTools", self)
        self.dev_tools_action.triggered.connect(self.toggle_dev_tools)
        self.dev_tools_action.setShortcut(Qt.Key.Key_F12)
        self.addAction(self.dev_tools_action)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navigation_bar.addWidget(self.url_bar)

        self.dev_tools_window = DevToolsWindow(self)
        self.new_tab(QUrl("https://minimalsite-zeta.vercel.app/API/homepage"))

    def new_tab(self, qurl=None):
        if qurl is None:
            qurl = QUrl("https://minimalsite-zeta.vercel.app/API/homepage")

        browser = QWebEngineView()
        browser.setUrl(qurl)

        index = self.web_view_stack.addWidget(browser)
        item = QListWidgetItem("New Tab")
        self.tab_list_widget.addItem(item)

        self.web_view_stack.setCurrentIndex(index)
        self.tab_list_widget.setCurrentItem(item)

        browser.urlChanged.connect(lambda url, b=browser: self.update_url_bar(url, b))
        browser.loadProgress.connect(lambda p, b=browser: self.update_progress(p, b))
        browser.titleChanged.connect(lambda t, b=browser: self.update_tab_title(t, b))
        browser.iconChanged.connect(lambda i, b=browser: self.update_tab_icon(i, b))

        self.web_view_stack.currentChanged.connect(self.current_tab_changed)

    def update_tab_title(self, title, browser):
        index = self.web_view_stack.indexOf(browser)
        if index != -1:
            self.tab_list_widget.item(index).setText(title)

    def update_tab_icon(self, icon, browser):
        index = self.web_view_stack.indexOf(browser)
        if index != -1:
            self.tab_list_widget.item(index).setIcon(icon)

    def toggle_dev_tools(self):
        current_browser = self.web_view_stack.currentWidget()
        if not current_browser:
            return

        if self.dev_tools_window.isVisible():
            current_browser.page().setDevToolsPage(None)
            self.dev_tools_window.hide()
            current_browser.setFocus()
        else:
            current_browser.page().setDevToolsPage(
                self.dev_tools_window.dev_tools_view.page()
            )
            self.dev_tools_window.show()
            self.dev_tools_window.activateWindow()

    def remove_current_tab(self):
        if self.web_view_stack.count() < 2:
            QMessageBox.information(
                self, "Action Denied", "Cannot close the last remaining tab."
            )
            return

        current_index = self.web_view_stack.currentIndex()
        widget_to_remove = self.web_view_stack.widget(current_index)

        if self.dev_tools_window.isVisible():
            self.toggle_dev_tools()

        self.web_view_stack.removeWidget(widget_to_remove)
        widget_to_remove.deleteLater()
        self.tab_list_widget.takeItem(current_index)

    def select_tab_from_sidebar(self, item):
        index = self.tab_list_widget.row(item)
        self.web_view_stack.setCurrentIndex(index)

    def navigate_to_url(self):
        current_browser = self.web_view_stack.currentWidget()
        if current_browser:
            url_text = self.url_bar.text()
            if not url_text:
                return

            self.Httpwarning(url_text)

            if not url_text.startswith(("http://", "https://")):
                url_text = "https://duckduckgo.com/?q=" + url_text

            current_browser.setUrl(QUrl(url_text))

    def Httpwarning(self, url_text):
        if url_text.startswith("http://"):
            QMessageBox.warning(
                self, "Insecure Connection", f"The site {url_text} is not secure."
            )

    def current_tab_changed(self, index):
        current_browser = self.web_view_stack.currentWidget()
        if current_browser:
            self.update_url_bar(current_browser.url(), current_browser)
            self.setWindowTitle(current_browser.title())
            if self.dev_tools_window.isVisible():
                current_browser.page().setDevToolsPage(
                    self.dev_tools_window.dev_tools_view.page()
                )

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
        if self.web_view_stack.currentWidget():
            self.web_view_stack.currentWidget().back()

    def forward_on_tab(self):
        if self.web_view_stack.currentWidget():
            self.web_view_stack.currentWidget().forward()

    def reload_tab(self):
        if self.web_view_stack.currentWidget():
            self.web_view_stack.currentWidget().reload()

    def stop_tab(self):
        if self.web_view_stack.currentWidget():
            self.web_view_stack.currentWidget().stop()

    def add_bookmark(self):
        cb = self.web_view_stack.currentWidget()
        if cb:
            url = cb.url().toString()
            if url not in self.bookmarks:
                self.bookmarks[url] = cb.title()
                QMessageBox.information(self, "Bookmark Added", "Saved!")

    def show_bookmarks_list(self):
        self.bookmark_window = QWidget()
        self.bookmark_window.setWindowTitle("Bookmarks")
        layout = QVBoxLayout(self.bookmark_window)
        self.bookmark_list = QListWidget()
        for url, title in self.bookmarks.items():
            item = QListWidgetItem(f"{title} - {url}")
            item.setData(Qt.ItemDataRole.UserRole, url)  # PyQt6 uses ItemDataRole
            self.bookmark_list.addItem(item)
        self.bookmark_list.itemDoubleClicked.connect(self.open_bookmark)
        layout.addWidget(self.bookmark_list)
        self.bookmark_window.show()

    def open_bookmark(self, item):
        url = item.data(Qt.ItemDataRole.UserRole)
        self.new_tab(QUrl(url))
        self.bookmark_window.close()

    # downloads
    def handle_download_requested(self, download):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save File", download.downloadFileName()
        )
        if path:
            download.setDownloadDirectory(os.path.dirname(path))
            download.setDownloadFileName(os.path.basename(path))
            download.accept()

        else:
            download.cancel()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Minimalist PyQt6")
    main_window = WebBrowser()
    main_window.show()
    sys.exit(app.exec())
