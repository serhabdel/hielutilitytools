from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFileDialog, QProgressBar,
    QMessageBox, QCheckBox, QSpinBox
)
from PySide6.QtCore import Qt
import os
import tabula
import pandas as pd
from utils.app_theme import AppTheme

class PDFtoExcel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme = AppTheme()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("PDF to Excel Converter")
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

        # Output File
        output_group = QVBoxLayout()
        output_label = QLabel("Output Excel File (Optional)")
        output_label.setStyleSheet("color: #888; font-size: 12px;")
        output_group.addWidget(output_label)

        output_layout = QHBoxLayout()
        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Default: Same location as PDF")
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

        # Options
        options_group = QVBoxLayout()
        options_label = QLabel("Conversion Options")
        options_label.setStyleSheet("color: #888; font-size: 12px;")
        options_group.addWidget(options_label)

        # Page Range
        range_layout = QHBoxLayout()
        range_label = QLabel("Page Range:")
        range_label.setStyleSheet("color: white;")
        range_layout.addWidget(range_label)

        self.start_page = QSpinBox()
        self.start_page.setMinimum(1)
        self.start_page.setStyleSheet("""
            QSpinBox {
                padding: 5px;
                background: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: white;
            }
        """)
        range_layout.addWidget(self.start_page)

        range_layout.addWidget(QLabel("to"))

        self.end_page = QSpinBox()
        self.end_page.setMinimum(1)
        self.end_page.setStyleSheet("""
            QSpinBox {
                padding: 5px;
                background: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: white;
            }
        """)
        range_layout.addWidget(self.end_page)
        range_layout.addStretch()
        options_group.addLayout(range_layout)

        # Additional Options
        self.guess_cells = QCheckBox("Guess Cell Boundaries")
        self.guess_cells.setChecked(True)
        self.guess_cells.setStyleSheet("""
            QCheckBox {
                color: white;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #4a90e2;
                border-radius: 4px;
                background: #2d2d2d;
            }
            QCheckBox::indicator:checked {
                background: #4a90e2;
            }
        """)
        options_group.addWidget(self.guess_cells)

        self.multiple_tables = QCheckBox("Extract Multiple Tables")
        self.multiple_tables.setChecked(True)
        self.multiple_tables.setStyleSheet("""
            QCheckBox {
                color: white;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #4a90e2;
                border-radius: 4px;
                background: #2d2d2d;
            }
            QCheckBox::indicator:checked {
                background: #4a90e2;
            }
        """)
        options_group.addWidget(self.multiple_tables)
        layout.addLayout(options_group)

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
        convert_btn = QPushButton("Convert to Excel")
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
            # Auto-set output path
            excel_path = os.path.splitext(file_path)[0] + '.xlsx'
            self.output_path.setText(excel_path)

    def browse_output(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Excel File", "", "Excel Files (*.xlsx)"
        )
        if file_path:
            if not file_path.endswith('.xlsx'):
                file_path += '.xlsx'
            self.output_path.setText(file_path)

    def convert_pdf(self):
        pdf_path = self.pdf_path.text()
        if not pdf_path:
            QMessageBox.warning(self, "Error", "Please select a PDF file first!")
            return

        output_path = self.output_path.text()
        if not output_path:
            output_path = os.path.splitext(pdf_path)[0] + '.xlsx'

        try:
            self.progress.show()
            self.progress.setRange(0, 0)  # Indeterminate progress

            # Extract tables from PDF
            tables = tabula.read_pdf(
                pdf_path,
                pages=f"{self.start_page.value()}-{self.end_page.value()}",
                multiple_tables=self.multiple_tables.isChecked(),
                guess=self.guess_cells.isChecked()
            )

            # If only one table was found, convert it to a list
            if isinstance(tables, pd.DataFrame):
                tables = [tables]

            # Create Excel writer
            with pd.ExcelWriter(output_path) as writer:
                for i, table in enumerate(tables):
                    sheet_name = f"Table_{i+1}" if len(tables) > 1 else "Sheet1"
                    table.to_excel(writer, sheet_name=sheet_name, index=False)

            self.progress.hide()
            QMessageBox.information(
                self,
                "Success",
                f"PDF successfully converted to Excel!\nSaved as: {output_path}"
            )

        except Exception as e:
            self.progress.hide()
            QMessageBox.critical(self, "Error", f"Conversion failed: {str(e)}")
