from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QFileDialog, QProgressBar,
    QMessageBox, QSpinBox, QComboBox, QCheckBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
import os
from PIL import Image

class LogoResizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.preview_image = None

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Logo Resizer")
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

        # Size Options
        size_group = QVBoxLayout()
        size_label = QLabel("Size Options")
        size_label.setStyleSheet("color: #888; font-size: 12px;")
        size_group.addWidget(size_label)

        # Preset sizes
        self.size_preset = QComboBox()
        self.size_preset.addItems([
            "Custom Size",
            "16x16 - Favicon",
            "32x32 - Windows Icon",
            "48x48 - App Icon",
            "64x64 - Desktop Icon",
            "128x128 - Mac Icon",
            "256x256 - High-DPI Icon",
            "512x512 - App Store Icon"
        ])
        self.size_preset.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: white;
            }
            QComboBox:hover {
                border: 1px solid #4a90e2;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 8px;
            }
        """)
        self.size_preset.currentIndexChanged.connect(self.on_preset_changed)
        size_group.addWidget(self.size_preset)

        # Custom size inputs
        size_inputs = QHBoxLayout()
        
        width_layout = QVBoxLayout()
        width_label = QLabel("Width")
        width_label.setStyleSheet("color: white;")
        width_layout.addWidget(width_label)
        self.width_input = QSpinBox()
        self.width_input.setRange(1, 9999)
        self.width_input.setValue(128)
        self.width_input.setStyleSheet("""
            QSpinBox {
                padding: 5px;
                background: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: white;
            }
        """)
        width_layout.addWidget(self.width_input)
        size_inputs.addLayout(width_layout)

        height_layout = QVBoxLayout()
        height_label = QLabel("Height")
        height_label.setStyleSheet("color: white;")
        height_layout.addWidget(height_label)
        self.height_input = QSpinBox()
        self.height_input.setRange(1, 9999)
        self.height_input.setValue(128)
        self.height_input.setStyleSheet("""
            QSpinBox {
                padding: 5px;
                background: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: white;
            }
        """)
        height_layout.addWidget(self.height_input)
        size_inputs.addLayout(height_layout)
        
        size_group.addLayout(size_inputs)

        # Maintain aspect ratio
        self.maintain_aspect = QCheckBox("Maintain Aspect Ratio")
        self.maintain_aspect.setChecked(True)
        self.maintain_aspect.setStyleSheet("""
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
        size_group.addWidget(self.maintain_aspect)
        controls_layout.addLayout(size_group)

        # Output Format
        format_group = QVBoxLayout()
        format_label = QLabel("Output Format")
        format_label.setStyleSheet("color: #888; font-size: 12px;")
        format_group.addWidget(format_label)

        self.format_combo = QComboBox()
        self.format_combo.addItems(["PNG", "JPEG", "ICO", "WEBP"])
        self.format_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: white;
            }
            QComboBox:hover {
                border: 1px solid #4a90e2;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 8px;
            }
        """)
        format_group.addWidget(self.format_combo)
        controls_layout.addLayout(format_group)

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

        # Resize Button
        resize_btn = QPushButton("Resize Logo")
        resize_btn.setStyleSheet("""
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
        resize_btn.clicked.connect(self.resize_image)
        controls_layout.addWidget(resize_btn)

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
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp *.ico *.webp)"
        )
        if file_path:
            self.image_path.setText(file_path)
            self.load_preview(file_path)

    def load_preview(self, image_path):
        try:
            self.preview_image = Image.open(image_path)
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(
                300, 300,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.preview.setPixmap(scaled_pixmap)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")

    def on_preset_changed(self, index):
        if index == 0:  # Custom Size
            return
        
        size = int(self.size_preset.currentText().split('x')[0])
        self.width_input.setValue(size)
        self.height_input.setValue(size)

    def resize_image(self):
        if not self.preview_image:
            QMessageBox.warning(self, "Error", "Please select an image first!")
            return

        try:
            self.progress.show()
            self.progress.setValue(0)

            # Get target size
            width = self.width_input.value()
            height = self.height_input.value()

            # Resize image
            if self.maintain_aspect.isChecked():
                self.preview_image.thumbnail((width, height), Image.Resampling.LANCZOS)
                resized_image = self.preview_image
            else:
                resized_image = self.preview_image.resize(
                    (width, height),
                    Image.Resampling.LANCZOS
                )

            self.progress.setValue(50)

            # Save with selected format
            output_format = self.format_combo.currentText()
            input_path = self.image_path.text()
            output_path = os.path.splitext(input_path)[0] + f"_resized.{output_format.lower()}"

            if output_format == "ICO":
                resized_image.save(output_path, format="ICO", sizes=[(width, height)])
            else:
                resized_image.save(output_path, format=output_format)

            self.progress.setValue(100)
            self.progress.hide()

            QMessageBox.information(
                self,
                "Success",
                f"Image resized successfully!\nSaved as: {output_path}"
            )

        except Exception as e:
            self.progress.hide()
            QMessageBox.critical(self, "Error", f"Failed to resize image: {str(e)}")