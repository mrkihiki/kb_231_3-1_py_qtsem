from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl


class VideoMessageBox(QDialog):
    def __init__(self, parent=None, title="Видео", text="", video_url=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(700, 800)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(text))

        if video_url:
            self.webview = QWebEngineView()
            self.webview.setUrl(QUrl(video_url))
            layout.addWidget(self.webview)
