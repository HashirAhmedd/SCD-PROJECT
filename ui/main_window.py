from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from widgets.file_drop_area import FileDropArea
from widgets.file_list import FileList

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Document Manager")
        self.setStyleSheet("""
            QWidget {
                background-color: #0a0a0a;
                color: #ffffff;
            }
        """)
        self.setMinimumSize(900, 700)

        # Outer vertical layout
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(40, 40, 40, 40)
        outer_layout.setSpacing(32)

        # Title
        title = QLabel("Document Manager")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #ffffff; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        outer_layout.addWidget(title)

        # Center drop area horizontally
        drop_area_row = QHBoxLayout()
        drop_area_row.addStretch(1)
        self.drop_area = FileDropArea(self)
        drop_area_row.addWidget(self.drop_area)
        drop_area_row.addStretch(1)
        outer_layout.addLayout(drop_area_row)

        # Center file list horizontally
        file_list_row = QHBoxLayout()
        file_list_row.addStretch(1)
        self.file_list = FileList(self)
        file_list_row.addWidget(self.file_list)
        file_list_row.addStretch(1)
        outer_layout.addLayout(file_list_row)
        outer_layout.addStretch(1)

        self.setLayout(outer_layout)
        self.drop_area.files_dropped.connect(self.file_list.add_files) 