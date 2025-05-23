from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QInputDialog, QVBoxLayout, QTextEdit, QDialog, QScrollArea, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QFontMetrics, QFont, QTextCursor, QTextCharFormat, QColor, QPixmap
import os
from docx import Document
import fitz
import pytesseract
from PIL import Image
import io

class DocxViewer(QDialog):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle(os.path.basename(file_path))
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QDialog {
                background: #0a0a0a;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search in document...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.05);
                color: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                font-size: 14px;
                padding: 8px 12px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Text area
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.text.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.03);
                color: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                font-size: 14px;
                font-family: 'Segoe UI', sans-serif;
                padding: 12px;
            }
        """)
        layout.addWidget(self.text)
        self.setLayout(layout)
        try:
            doc = Document(file_path)
            content = "\n\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            self.text.setText(content)
        except Exception as e:
            self.text.setText(f"Failed to load document: {e}")
        
        self.search_input.returnPressed.connect(self.search_text)

    def search_text(self):
        query = self.search_input.text()
        if not query:
            return
        cursor = self.text.textCursor()
        format = QTextCharFormat()
        format.setBackground(QColor("#ffb300"))
        # Clear previous formatting
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())
        cursor.clearSelection()
        # Highlight all matches
        doc = self.text.document()
        highlight_cursor = QTextCursor(doc)
        while not highlight_cursor.isNull() and not highlight_cursor.atEnd():
            highlight_cursor = doc.find(query, highlight_cursor)
            if not highlight_cursor.isNull():
                highlight_cursor.mergeCharFormat(format)

class PdfViewer(QDialog):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle(os.path.basename(file_path))
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QDialog {
                background: #0a0a0a;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search in PDF...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.05);
                color: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                font-size: 14px;
                padding: 8px 12px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Text area
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.text.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.03);
                color: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                font-size: 14px;
                font-family: 'Segoe UI', sans-serif;
                padding: 12px;
            }
        """)
        layout.addWidget(self.text)
        self.setLayout(layout)
        try:
            doc = fitz.open(file_path)
            self.pages = list(doc)
            content = []
            
            for page_num, page in enumerate(doc):
                text = page.get_text()
                if not text.strip():
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img_data = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_data))
                    text = pytesseract.image_to_string(img)
                    if text.strip():
                        content.append(f"[Page {page_num + 1} - Scanned Content]\n{text}")
                    else:
                        content.append(f"[Page {page_num + 1} - No text found]")
                else:
                    content.append(text)
            
            self.text.setText("\n\n".join(content))
        except Exception as e:
            self.text.setText(f"Failed to load PDF: {e}")
        self.search_input.returnPressed.connect(self.search_text)

    def search_text(self):
        query = self.search_input.text()
        if not query:
            return
        cursor = self.text.textCursor()
        format = QTextCharFormat()
        format.setBackground(QColor("#ffb300"))
        # Clear previous formatting
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())
        cursor.clearSelection()
        # Highlight all matches
        doc = self.text.document()
        highlight_cursor = QTextCursor(doc)
        while not highlight_cursor.isNull() and not highlight_cursor.atEnd():
            highlight_cursor = doc.find(query, highlight_cursor)
            if not highlight_cursor.isNull():
                highlight_cursor.mergeCharFormat(format)

class ImageViewer(QDialog):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle(os.path.basename(file_path))
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QDialog {
                background: #0a0a0a;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search in image text...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.05);
                color: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                font-size: 14px;
                padding: 8px 12px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Text area
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.text.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.03);
                color: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                font-size: 14px;
                font-family: 'Segoe UI', sans-serif;
                padding: 12px;
            }
        """)
        layout.addWidget(self.text)
        self.setLayout(layout)
        
        try:
            
            # Extract text from image
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)
            if text.strip():
                self.text.setText(text)
            else:
                self.text.setText("No text found in the image.")
        except Exception as e:
            self.text.setText(f"Failed to load image: {e}")
        
        self.search_input.returnPressed.connect(self.search_text)

    def search_text(self):
        query = self.search_input.text()
        if not query:
            return
        cursor = self.text.textCursor()
        format = QTextCharFormat()
        format.setBackground(QColor("#ffb300"))
        # Clear previous formatting
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())
        cursor.clearSelection()
        # Highlight all matches
        doc = self.text.document()
        highlight_cursor = QTextCursor(doc)
        while not highlight_cursor.isNull() and not highlight_cursor.atEnd():
            highlight_cursor = doc.find(query, highlight_cursor)
            if not highlight_cursor.isNull():
                highlight_cursor.mergeCharFormat(format)

class FileBox(QWidget):
    label_added = pyqtSignal(str, str)  # filename, label

    def __init__(self, filename, label_text=None, parent=None):
        super().__init__(parent)
        self.filename = filename
        self.label_text = label_text
        self.setFixedSize(160, 160)
        self.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
            }
            QWidget:hover {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        
        # File icon
        self.icon = QLabel("📄" if filename.lower().endswith('.pdf') else "📝")
        self.icon.setAlignment(Qt.AlignCenter)
        self.icon.setStyleSheet("""
            color: rgba(255, 255, 255, 0.7);
            font-size: 32px;
            padding-top: 16px;
        """)
        self.icon.setGeometry(0, 0, 160, 50)

        # File name
        self.label = QLabel(self)
        self.label.setFont(QFont("Segoe UI", 10))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9);
            font-size: 12px;
            padding: 8px;
        """)
        metrics = QFontMetrics(self.label.font())
        elided = metrics.elidedText(filename.split("/")[-1], Qt.ElideMiddle, 140)
        self.label.setText(elided)
        self.label.setToolTip(filename.split("/")[-1])
        self.label.setGeometry(0, 50, 160, 50)

        # Add label button
        self.add_label_btn = QPushButton("Add Label", self)
        self.add_label_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.9);
                border: none;
                border-radius: 8px;
                font-size: 11px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
            }
        """)
        self.add_label_btn.move(90, 110)
        self.add_label_btn.hide()
        self.add_label_btn.clicked.connect(self.prompt_label)

        # Label tag
        self.label_tag = QLabel(self)
        self.label_tag.setStyleSheet("""
            background: rgba(255, 179, 0, 0.2);
            color: #ffb300;
            border-radius: 6px;
            font-size: 11px;
            padding: 4px 8px;
        """)
        self.label_tag.move(10, 110)
        self.label_tag.hide()
        if label_text:
            self.set_label(label_text)

    def enterEvent(self, event):
        self.add_label_btn.show()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.add_label_btn.hide()
        super().leaveEvent(event)

    def prompt_label(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Add Label")
        dialog.setLabelText(f"Enter label for {self.filename.split('/')[-1]}")
        dialog.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
            }
            QLineEdit {
                color: rgba(255, 255, 255, 0.9);
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                font-size: 14px;
                padding: 8px;
            }
            QPushButton {
                color: rgba(255, 255, 255, 0.9);
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 8px;
                font-size: 14px;
                min-width: 80px;
                min-height: 32px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
            }
        """)
        ok = dialog.exec_()
        text = dialog.textValue()
        if ok and text:
            self.set_label(text)
            self.label_added.emit(self.filename, text)

    def set_label(self, text):
        self.label_tag.setText(text)
        self.label_tag.adjustSize()
        self.label_tag.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.filename.lower().endswith('.docx'):
                viewer = DocxViewer(self.filename, self)
                viewer.exec_()
            elif self.filename.lower().endswith('.pdf'):
                viewer = PdfViewer(self.filename, self)
                viewer.exec_()
            elif self.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
                viewer = ImageViewer(self.filename, self)
                viewer.exec_()
        super().mousePressEvent(event)

class FileList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.files = []
        self.labels = {}  # filename -> label
        self.box_size = 140
        self.layout = QGridLayout(self)
        self.layout.setSpacing(24)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.setStyleSheet("background: transparent;")

    def add_files(self, files):
        new_files = [f for f in files if f not in self.files]
        self.files.extend(new_files)
        self.clear()
        for idx, file in enumerate(self.files):
            row = idx // 3
            col = idx % 3
            label_text = self.labels.get(file)
            box = FileBox(file, label_text, self)
            box.label_added.connect(self.set_file_label)
            self.layout.addWidget(box, row, col)

    def set_file_label(self, filename, label):
        self.labels[filename] = label
        self.add_files([])  # Refresh UI

    def clear(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater() 