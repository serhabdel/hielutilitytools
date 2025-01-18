from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFileDialog, QProgressBar,
    QMessageBox, QSlider, QFrame
)
from PySide6.QtCore import Qt
import fitz
import os
from utils.app_theme import AppTheme

class PDFCompressor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme = AppTheme()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("PDF Compressor")
        title.setStyleSheet("font-size: 24px; color: white; margin-bottom: 20px;")
        layout.addWidget(title)

        # Content Frame
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background: #2d2d2d;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(15)

        # Input File
        input_label = QLabel("Select PDF")
        input_label.setStyleSheet("color: #888; font-size: 12px;")
        content_layout.addWidget(input_label)

        input_layout = QHBoxLayout()
        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("Choose PDF file...")
        self.input_path.setStyleSheet("""
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
        browse_btn = QPushButton("Browse")
        browse_btn.setStyleSheet("""
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
        browse_btn.clicked.connect(self.browse_input)
        input_layout.addWidget(self.input_path)
        input_layout.addWidget(browse_btn)
        content_layout.addLayout(input_layout)

        # Output File
        output_label = QLabel("Output Location")
        output_label.setStyleSheet("color: #888; font-size: 12px;")
        content_layout.addWidget(output_label)

        output_layout = QHBoxLayout()
        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Choose output location...")
        self.output_path.setStyleSheet(self.input_path.styleSheet())
        browse_output_btn = QPushButton("Browse")
        browse_output_btn.setStyleSheet(browse_btn.styleSheet())
        browse_output_btn.clicked.connect(self.browse_output)
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(browse_output_btn)
        content_layout.addLayout(output_layout)

        # Compression Quality
        quality_label = QLabel("Compression Quality")
        quality_label.setStyleSheet("color: #888; font-size: 12px;")
        content_layout.addWidget(quality_label)

        self.quality_value = QLabel("75%")
        self.quality_value.setStyleSheet("color: white; font-size: 14px;")
        content_layout.addWidget(self.quality_value)

        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setMinimum(1)
        self.quality_slider.setMaximum(100)
        self.quality_slider.setValue(75)
        self.quality_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #3d3d3d;
                height: 8px;
                background: #2d2d2d;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #4a90e2;
                border: none;
                width: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #357abd;
            }
        """)
        self.quality_slider.valueChanged.connect(self.update_quality_label)
        content_layout.addWidget(self.quality_slider)

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                text-align: center;
                background: #363636;
            }
            QProgressBar::chunk {
                background-color: #4a90e2;
            }
        """)
        self.progress.hide()
        content_layout.addWidget(self.progress)

        # Compress Button
        compress_btn = QPushButton("Compress")
        compress_btn.setStyleSheet("""
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
        compress_btn.clicked.connect(self.compress)
        content_layout.addWidget(compress_btn)

        layout.addWidget(content_frame)
        layout.addStretch()

    def update_quality_label(self):
        self.quality_value.setText(f"{self.quality_slider.value()}%")

    def browse_input(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select PDF File",
            "",
            "PDF files (*.pdf)"
        )
        if file_path:
            self.input_path.setText(file_path)
            if not self.output_path.text():
                # Auto-generate output path
                base_name = os.path.splitext(file_path)[0]
                self.output_path.setText(f"{base_name}_compressed.pdf")

    def browse_output(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Compressed PDF",
            "",
            "PDF files (*.pdf)"
        )
        if file_path:
            self.output_path.setText(file_path)

    def compress(self):
        input_path = self.input_path.text()
        output_path = self.output_path.text()
        quality = self.quality_slider.value()

        if not input_path or not output_path:
            QMessageBox.warning(self, "Error", "Please select both input and output files")
            return

        try:
            self.progress.show()
            self.progress.setValue(0)

            # Open the PDF
            pdf_document = fitz.open(input_path)
            total_pages = len(pdf_document)

            # Create a new PDF for compressed version
            compressed_pdf = fitz.open()

            for page_num in range(total_pages):
                # Get the page
                page = pdf_document[page_num]

                # Add page to new PDF
                new_page = compressed_pdf.new_page(width=page.rect.width, height=page.rect.height)

                # Get page contents as image
                pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))

                # Convert to image and back with compression
                img_data = pix.tobytes("png")
                new_page.insert_image(new_page.rect, stream=img_data, compression=quality/100)

                self.progress.setValue(int((page_num + 1) / total_pages * 100))

            # Save the compressed PDF
            compressed_pdf.save(output_path, garbage=4, deflate=True)
            compressed_pdf.close()
            pdf_document.close()

            self.progress.setValue(100)
            self.progress.hide()

            QMessageBox.information(
                self,
                "Success",
                f"PDF compressed successfully!\nOutput file: {output_path}"
            )

        except Exception as e:
            self.progress.hide()
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
