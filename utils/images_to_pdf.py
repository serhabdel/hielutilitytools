from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QListWidget, QFileDialog, QMessageBox,
    QLineEdit
)
from PySide6.QtCore import Qt
from PIL import Image
import os
from .base_tool import BaseTool

class ImagesToPDF(BaseTool):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.images = []
        self.setup_ui()

    def setup_ui(self):
        # Images list
        self.layout.addWidget(QLabel("Selected Images:"))
        self.listbox = QListWidget()
        self.listbox.setStyleSheet("""
            QListWidget {
                background: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-radius: 2px;
            }
            QListWidget::item:selected {
                background: #4a90e2;
            }
        """)
        self.layout.addWidget(self.listbox)

        # Buttons
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Add Images")
        self.remove_btn = QPushButton("Remove Selected")
        self.clear_btn = QPushButton("Clear All")
        
        for btn in [self.add_btn, self.remove_btn, self.clear_btn]:
            btn.setFixedHeight(36)
            btn.setStyleSheet("""
                QPushButton {
                    background: #4a90e2;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background: #357abd;
                }
                QPushButton:pressed {
                    background: #2d6da3;
                }
            """)
            btn_layout.addWidget(btn)
        
        self.layout.addLayout(btn_layout)

        # Output file
        self.layout.addWidget(QLabel("Output PDF:"))
        output_layout = QHBoxLayout()
        
        self.output_path = QLineEdit()
        self.output_path.setStyleSheet("""
            QLineEdit {
                background: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: white;
                padding: 8px;
            }
        """)
        output_layout.addWidget(self.output_path)
        
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setFixedHeight(36)
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background: #4a90e2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: #357abd;
            }
            QPushButton:pressed {
                background: #2d6da3;
            }
        """)
        output_layout.addWidget(self.browse_btn)
        
        self.layout.addLayout(output_layout)

        # Convert button
        self.convert_btn = QPushButton("Convert to PDF")
        self.convert_btn.setFixedHeight(36)
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background: #4a90e2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #357abd;
            }
            QPushButton:pressed {
                background: #2d6da3;
            }
        """)
        self.layout.addWidget(self.convert_btn)

        # Connect signals
        self.add_btn.clicked.connect(self.add_images)
        self.remove_btn.clicked.connect(self.remove_selected)
        self.clear_btn.clicked.connect(self.clear_all)
        self.browse_btn.clicked.connect(self.browse_output)
        self.convert_btn.clicked.connect(self.convert_to_pdf)

        self.layout.addStretch()

    def add_images(self):
        # Get initial directory from last selected image if available
        initial_dir = ""
        if self.images:
            initial_dir = os.path.dirname(self.images[-1])
            
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            initial_dir,
            "Image files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)"
        )
        if files:
            self.images.extend(files)
            self.update_listbox()
            
            # Auto-set output path if not set
            if not self.output_path.text() and len(self.images) > 0:
                first_image = os.path.basename(self.images[0])
                suggested_name = os.path.splitext(first_image)[0] + "_combined.pdf"
                # Use the same directory as the first image
                suggested_path = os.path.join(os.path.dirname(self.images[0]), suggested_name)
                self.output_path.setText(suggested_path)

    def remove_selected(self):
        selected_items = self.listbox.selectedItems()
        for item in selected_items:
            row = self.listbox.row(item)
            self.images.pop(row)
            self.listbox.takeItem(row)

    def clear_all(self):
        self.images.clear()
        self.listbox.clear()

    def update_listbox(self):
        self.listbox.clear()
        for img in self.images:
            self.listbox.addItem(os.path.basename(img))

    def browse_output(self):
        # Get initial directory from first image if available
        initial_dir = ""
        if self.images:
            initial_dir = os.path.dirname(self.images[0])
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF",
            os.path.join(initial_dir, self.output_path.text() or "combined.pdf"),
            "PDF files (*.pdf)"
        )
        if file_path:
            self.output_path.setText(file_path)

    def convert_to_pdf(self):
        if not self.images:
            QMessageBox.critical(self, "Error", "Please add at least one image")
            return

        output_path = self.output_path.text()
        if not output_path:
            QMessageBox.critical(self, "Error", "Please specify output PDF file")
            return

        try:
            # Open first image
            images = [Image.open(self.images[0])]
            # Convert and append other images
            images.extend([Image.open(img).convert('RGB') for img in self.images[1:]])
            
            # Save as PDF
            images[0].save(
                output_path, 
                "PDF", 
                save_all=True,
                append_images=images[1:],
                resolution=100.0
            )

            QMessageBox.information(
                self,
                "Success",
                f"Images combined into PDF successfully!\nOutput file: {output_path}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")