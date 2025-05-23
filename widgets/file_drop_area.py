from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QFont, QColor

class FileDropArea(QWidget):
    files_dropped = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setFixedSize(500, 300)
        self.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.03);
                border: 2px dashed rgba(255, 255, 255, 0.1);
                border-radius: 20px;
            }
            QWidget:hover {
                background: rgba(255, 255, 255, 0.05);
                border: 2px dashed rgba(255, 255, 255, 0.2);
            }
        """)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(16)

        # Upload icon (up arrow)
        self.arrow = QLabel("↑")
        self.arrow.setAlignment(Qt.AlignCenter)
        self.arrow.setStyleSheet("""
            color: rgba(255, 255, 255, 0.7);
            font-size: 48px;
            font-weight: bold;
        """)
        self.arrow.setFont(QFont("Segoe UI", 48, QFont.Bold))
        layout.addWidget(self.arrow)

        # Main text
        self.text = QLabel("Drag and drop your documents here")
        self.text.setAlignment(Qt.AlignCenter)
        self.text.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9);
            font-size: 24px;
            font-family: 'Segoe UI', sans-serif;
            font-weight: 500;
        """)
        layout.addWidget(self.text)

        # Subtext
        self.subtext = QLabel("or click to browse files")
        self.subtext.setAlignment(Qt.AlignCenter)
        self.subtext.setStyleSheet("""
            color: rgba(255, 255, 255, 0.5);
            font-size: 16px;
            font-family: 'Segoe UI', sans-serif;
        """)
        layout.addWidget(self.subtext)

        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            self.setStyleSheet("""
                QWidget {
                    background: rgba(255, 255, 255, 0.08);
                    border: 2px dashed rgba(255, 255, 255, 0.3);
                    border-radius: 20px;
                }
            """)
            event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.03);
                border: 2px dashed rgba(255, 255, 255, 0.1);
                border-radius: 20px;
            }
            QWidget:hover {
                background: rgba(255, 255, 255, 0.05);
                border: 2px dashed rgba(255, 255, 255, 0.2);
            }
        """)
        super().dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent):
        self.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.03);
                border: 2px dashed rgba(255, 255, 255, 0.1);
                border-radius: 20px;
            }
            QWidget:hover {
                background: rgba(255, 255, 255, 0.05);
                border: 2px dashed rgba(255, 255, 255, 0.2);
            }
        """)
        files = [u.toLocalFile() for u in event.mimeData().urls() if u.isLocalFile()]
        if len(files) > 15:
            files = files[:15]
        self.files_dropped.emit(files)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            files, _ = QFileDialog.getOpenFileNames(
                self,
                "Select up to 15 files",
                "",
                "Documents (*.pdf *.docx *.jpg *.jpeg *.png *.bmp *.tiff);;All Files (*)"
            )
            if len(files) > 15:
                files = files[:15]
            if files:
                self.files_dropped.emit(files) 