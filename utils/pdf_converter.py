from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFileDialog, QSpinBox,
    QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt
import os
import fitz
from utils.app_theme import AppTheme

class PDFConverter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme = AppTheme()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("PDF to Images Converter")
        title.setStyleSheet("font-size: 24px; color: white; margin-bottom: 20px;")
        layout.addWidget(title)

        # PDF Input
        input_group = QVBoxLayout()
        input_label = QLabel("Select PDF File")
        input_label.setStyleSheet("color: #888; font-size: 12px;")
        input_group.addWidget(input_label)

        pdf_layout = QHBoxLayout()
        self.pdf_path = QLineEdit()
        self.pdf_path.setPlaceholderText("Choose a PDF file...")
        self.pdf_path.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: white;
            }
            QLineEdit:focus {
                border: 1px solid #4a90e2;
            }
        """)
        browse_pdf_btn = QPushButton("Browse")
        browse_pdf_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background: #4a90e2;
                border: none;
                border-radius: 4px;
                color: white;
            }
            QPushButton:hover {
                background: #357abd;
            }
        """)
        browse_pdf_btn.clicked.connect(self.browse_pdf)
        pdf_layout.addWidget(self.pdf_path)
        pdf_layout.addWidget(browse_pdf_btn)
        input_group.addLayout(pdf_layout)
        layout.addLayout(input_group)

        # Output Folder
        output_group = QVBoxLayout()
        output_label = QLabel("Output Folder (Optional)")
        output_label.setStyleSheet("color: #888; font-size: 12px;")
        output_group.addWidget(output_label)

        output_layout = QHBoxLayout()
        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Default: Same as PDF location")
        self.output_path.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: white;
            }
            QLineEdit:focus {
                border: 1px solid #4a90e2;
            }
        """)
        browse_output_btn = QPushButton("Browse")
        browse_output_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background: #4a90e2;
                border: none;
                border-radius: 4px;
                color: white;
            }
            QPushButton:hover {
                background: #357abd;
            }
        """)
        browse_output_btn.clicked.connect(self.browse_output)
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(browse_output_btn)
        output_group.addLayout(output_layout)
        layout.addLayout(output_group)

        # DPI Setting
        dpi_group = QVBoxLayout()
        dpi_label = QLabel("DPI (Dots Per Inch)")
        dpi_label.setStyleSheet("color: #888; font-size: 12px;")
        dpi_group.addWidget(dpi_label)

        self.dpi = QSpinBox()
        self.dpi.setRange(72, 600)
        self.dpi.setValue(300)
        self.dpi.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                background: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: white;
            }
            QSpinBox:focus {
                border: 1px solid #4a90e2;
            }
        """)
        dpi_group.addWidget(self.dpi)
        layout.addLayout(dpi_group)

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                text-align: center;
                background: #2d2d2d;
            }
            QProgressBar::chunk {
                background-color: #4a90e2;
            }
        """)
        self.progress.hide()
        layout.addWidget(self.progress)

        # Convert Button
        convert_btn = QPushButton("Convert PDF to Images")
        convert_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                background: #4a90e2;
                border: none;
                border-radius: 4px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #357abd;
            }
        """)
        convert_btn.clicked.connect(self.convert_pdf)
        layout.addWidget(convert_btn)

        layout.addStretch()

    def browse_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select PDF File", "", "PDF Files (*.pdf)"
        )
        if file_path:
            self.pdf_path.setText(file_path)

    def browse_output(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Output Folder"
        )
        if folder_path:
            self.output_path.setText(folder_path)

    def convert_pdf(self):
        pdf_path = self.pdf_path.text()
        if not pdf_path:
            QMessageBox.warning(self, "Error", "Please select a PDF file first!")
            return

        output_path = self.output_path.text()
        if not output_path:
            output_path = os.path.dirname(pdf_path)

        try:
            self.progress.show()
            doc = fitz.open(pdf_path)
            total_pages = doc.page_count
            self.progress.setMaximum(total_pages)

            for page_num in range(total_pages):
                page = doc[page_num]
                pix = page.get_pixmap(dpi=self.dpi.value())
                output_file = os.path.join(
                    output_path,
                    f"page_{page_num + 1}.png"
                )
                pix.save(output_file)
                self.progress.setValue(page_num + 1)

            doc.close()
            self.progress.hide()
            QMessageBox.information(
                self,
                "Success",
                f"Successfully converted {total_pages} pages to images!"
            )

        except Exception as e:
            self.progress.hide()
            QMessageBox.critical(self, "Error", f"Conversion failed: {str(e)}")
