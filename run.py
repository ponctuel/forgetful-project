import sys
import random
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QTabWidget,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtNetwork import (
    QNetworkAccessManager,
    QNetworkRequest,
    QNetworkCookie,
    QNetworkCookieJar,
)
from PyQt5.QtCore import QUrl, QDateTime

class WebBrowser(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Forgetful Browser")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(
            """
            background-color: #121212;
            color: white;
            border: none;
            font-size: 16px;
            """
        )

        self.tabWidget = QTabWidget(self)
        self.setCentralWidget(self.tabWidget)
        self.tabWidget.setStyleSheet(
            """
            QTabWidget::pane { border: none; }
            QTabWidget::tab-bar { alignment: center; }
            QTabBar::tab {
                background-color: #1e1e1e;
                color: white;
                border: none;
                padding: 10px 20px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
            QTabBar::tab:selected {
                background-color: #343434;
            }
            """
        )

        self.newTabButton = QPushButton("+", self)
        self.newTabButton.setStyleSheet(
            """
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            """
        )
        self.tabWidget.setCornerWidget(self.newTabButton)
        self.newTabButton.clicked.connect(self.newTab)

        self.tabs = []

        self.newTab()

    def newTab(self):
        webView = WebView(self)
        index = self.tabWidget.addTab(webView, "New Tab")
        self.tabWidget.setCurrentIndex(index)
        self.tabs.append(webView)

    def closeEvent(self, event):
        for widget in self.tabs:
            widget.deleteLater()
        event.accept()

class WebView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.urlLineEdit = QLineEdit(self)
        self.urlLineEdit.setStyleSheet(
            """
            background-color: #343434;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            """
        )
        layout.addWidget(self.urlLineEdit)

        self.urlLineEdit.returnPressed.connect(self.openLink)

        goButton = QPushButton("Go", self)
        goButton.setStyleSheet(
            """
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            """
        )
        layout.addWidget(goButton)
        goButton.clicked.connect(self.openLink)

        self.webView = QWebEngineView(self)
        layout.addWidget(self.webView)

        self.userAgents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
            # Ajout de plus d'user agents pour plus d'anonymat
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
        ]

        self.manager = QNetworkAccessManager(self)

    def openLink(self):
        url = self.urlLineEdit.text()
        try:
            request = QNetworkRequest(QUrl(url))
            request.setRawHeader(b"User-Agent", random.choice(self.userAgents).encode())
            self.manager.get(request)
            self.webView.load(QUrl(url))
            self.resetCookies()
        except Exception as e:
            print("Erreur:", e)

    def resetCookies(self):
        cookie_jar = self.manager.cookieJar()
        if cookie_jar is not None:
            cookies = cookie_jar.allCookies()
            for cookie in cookies:
                cookie.setExpirationDate(QDateTime.currentDateTime().addYears(-1))
                cookie_jar.setCookie(cookie)

        # Effacer les cookies de session
        self.manager.cookieJar().deleteCookie(QNetworkCookie("SID"))
        self.manager.cookieJar().deleteCookie(QNetworkCookie("SSID"))
        self.manager.cookieJar().deleteCookie(QNetworkCookie("HSID"))
        self.manager.cookieJar().deleteCookie(QNetworkCookie("SAPISID"))
        self.manager.cookieJar().deleteCookie(QNetworkCookie("APISID"))
        self.manager.cookieJar().deleteCookie(QNetworkCookie(b"NID", b""))
        self.manager.cookieJar().deleteCookie(QNetworkCookie(b"OTZ", b""))
        self.manager.cookieJar().deleteCookie(QNetworkCookie(b"1P_JAR", b""))
        self.manager.cookieJar().deleteCookie(QNetworkCookie(b"CONSENT", b""))
        self.manager.cookieJar().deleteCookie(QNetworkCookie(b"SIDCC", b""))


    def closeEvent(self, event):
        self.clearSessionData()
        event.accept()

    def clearSessionData(self):
        self.webView.page().profile().clearHttpCache()
        self.webView.page().profile().clearAllVisitedLinks()
        self.webView.page().profile().clearVisitedLinks()
        self.webView.page().profile().clearHttpAuthenticationCache()
        self.webView.page().profile().clearCache()
        self.webView.page().profile().deleteAllScripts()
        self.webView.page().profile().deleteAllWebStorage()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(
        """
        QMainWindow {
            background-color: #121212;
            color: white;
            font-size: 16px;
        }
        QLineEdit {
            background-color: #343434;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
        }
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QTabWidget::pane {
            border: none;
        }
        QTabWidget::tab-bar {
            alignment: center;
        }
        QTabBar::tab {
            background-color: #1e1e1e;
            color: white;
            border: none;
            padding: 10px 20px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }
        QTabBar::tab:selected {
            background-color: #343434;
        }
        """
    )
    browser = WebBrowser()
    browser.show()
    sys.exit(app.exec_())
