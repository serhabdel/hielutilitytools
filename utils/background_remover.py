from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QFileDialog, QProgressBar,
    QMessageBox, QSpinBox, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import os
from rembg import remove
from PIL import Image
import io

class BackgroundRemover(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.preview_image = None

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Background Remover")
        title.setStyleSheet("font-size: 24px; color: white; margin-bottom: 20px;")
        layout.addWidget(title)

        # Main content layout
        content_layout = QHBoxLayout()

        # Left side - Controls
        controls_layout = QVBoxLayout()

        # Image Input
        input_group = QVBoxLayout()
        input_label = QLabel("Select Image")
        input_label.setStyleSheet("color: #888; font-size: 12px;")
        input_group.addWidget(input_label)

        image_layout = QHBoxLayout()
        self.image_path = QLineEdit()
        self.image_path.setPlaceholderText("Choose an image file...")
        self.image_path.setStyleSheet("""
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
        browse_btn.clicked.connect(self.browse_image)
        image_layout.addWidget(self.image_path)
        image_layout.addWidget(browse_btn)
        input_group.addLayout(image_layout)
        controls_layout.addLayout(input_group)

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
        controls_layout.addWidget(self.progress)

        # Remove Background Button
        remove_btn = QPushButton("Remove Background")
        remove_btn.setStyleSheet("""
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
        remove_btn.clicked.connect(self.remove_background)
        controls_layout.addWidget(remove_btn)

        controls_layout.addStretch()
        content_layout.addLayout(controls_layout)

        # Right side - Preview
        preview_layout = QVBoxLayout()
        preview_label = QLabel("Preview")
        preview_label.setStyleSheet("color: #888; font-size: 12px;")
        preview_layout.addWidget(preview_label)

        self.preview = QLabel()
        self.preview.setStyleSheet("""
            QLabel {
                background: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
            }
        """)
        self.preview.setMinimumSize(300, 300)
        self.preview.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(self.preview)
        content_layout.addLayout(preview_layout)

        layout.addLayout(content_layout)

    def browse_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.image_path.setText(file_path)
            self.load_preview(file_path)

    def load_preview(self, image_path):
        try:
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(
                300, 300,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.preview.setPixmap(scaled_pixmap)
            self.preview_image = Image.open(image_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")

    def remove_background(self):
        if not self.preview_image:
            QMessageBox.warning(self, "Error", "Please select an image first!")
            return

        try:
            self.progress.show()
            self.progress.setValue(0)

            # Process image
            self.progress.setValue(30)
            
            # Remove background
            output = remove(self.preview_image)
            self.progress.setValue(70)

            # Save result
            input_path = self.image_path.text()
            output_path = os.path.splitext(input_path)[0] + "_no_bg.png"
            output.save(output_path)

            # Update preview
            pixmap = QPixmap(output_path)
            scaled_pixmap = pixmap.scaled(
                300, 300,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.preview.setPixmap(scaled_pixmap)

            self.progress.setValue(100)
            self.progress.hide()

            QMessageBox.information(
                self,
                "Success",
                f"Background removed successfully!\nSaved as: {output_path}"
            )

        except Exception as e:
            self.progress.hide()
            QMessageBox.critical(self, "Error", f"Failed to remove background: {str(e)}")
