from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFileDialog, QProgressBar,
    QMessageBox, QSpinBox, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import os
import cv2
import numpy as np
from PIL import Image
from utils.app_theme import AppTheme

def upscale_image(image_path, scale_factor, method='bicubic'):
    # Read image with PIL for better format support
    img = Image.open(image_path)
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    # Convert to numpy array
    img_array = np.array(img)
    # Convert from RGB to BGR for OpenCV
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    height, width = img_array.shape[:2]
    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)

    if method.lower() == 'bicubic':
        upscaled = cv2.resize(img_array, (new_width, new_height),
                            interpolation=cv2.INTER_CUBIC)
    elif method.lower() == 'lanczos':
        upscaled = cv2.resize(img_array, (new_width, new_height),
                            interpolation=cv2.INTER_LANCZOS4)
    elif method.lower() == 'edsr':
        # Use OpenCV's built-in EDSR model
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        path = os.path.join(os.path.dirname(__file__), 'models', 'EDSR_x2.pb')
        if not os.path.exists(path):
            raise FileNotFoundError("EDSR model file not found. Please download it first.")
        sr.readModel(path)
        sr.setModel("edsr", 2)  # 2x upscaling
        upscaled = sr.upsample(img_array)
        # If we need more than 2x, use additional bicubic scaling
        if scale_factor > 2:
            remaining_scale = scale_factor / 2
            upscaled = cv2.resize(upscaled, (new_width, new_height),
                                    interpolation=cv2.INTER_CUBIC)
    else:
        raise ValueError(f"Unknown upscaling method: {method}")

    # Convert back to RGB
    upscaled = cv2.cvtColor(upscaled, cv2.COLOR_BGR2RGB)
    return Image.fromarray(upscaled)

class ImageUpscaler(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme = AppTheme()
        self.setup_ui()
        self.preview_image = None

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Image Upscaler")
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

        # Scale Factor
        scale_layout = QHBoxLayout()
        scale_label = QLabel("Scale Factor:")
        scale_label.setStyleSheet("color: white;")
        self.scale_factor = QSpinBox()
        self.scale_factor.setRange(2, 8)
        self.scale_factor.setValue(2)
        self.scale_factor.setStyleSheet("""
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
        scale_layout.addWidget(scale_label)
        scale_layout.addWidget(self.scale_factor)
        controls_layout.addLayout(scale_layout)

        # Algorithm Selection
        algo_layout = QHBoxLayout()
        algo_label = QLabel("Algorithm:")
        algo_label.setStyleSheet("color: white;")
        self.algorithm = QComboBox()
        self.algorithm.addItems(["Bicubic", "Lanczos", "EDSR"])
        self.algorithm.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: white;
            }
            QComboBox:focus {
                border: 1px solid #4a90e2;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        algo_layout.addWidget(algo_label)
        algo_layout.addWidget(self.algorithm)
        controls_layout.addLayout(algo_layout)

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

        # Upscale Button
        upscale_btn = QPushButton("Upscale Image")
        upscale_btn.setStyleSheet("""
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
        upscale_btn.clicked.connect(self.upscale_image)
        controls_layout.addWidget(upscale_btn)

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
            self.preview_image = cv2.imread(image_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")

    def upscale_image(self):
        if self.preview_image is None:
            QMessageBox.warning(self, "Error", "Please select an image first!")
            return

        try:
            self.progress.show()
            self.progress.setValue(0)

            # Get parameters
            scale = self.scale_factor.value()
            algorithm = self.algorithm.currentText()

            # Process image
            self.progress.setValue(30)
            upscaled = upscale_image(self.image_path.text(), scale, algorithm)
            self.progress.setValue(70)

            # Save result
            input_path = self.image_path.text()
            base_name = os.path.splitext(input_path)[0]
            ext = os.path.splitext(input_path)[1]
            output_path = f"{base_name}_upscaled_{scale}x{ext}"
            upscaled.save(output_path)

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
                f"Image upscaled successfully!\nSaved as: {output_path}"
            )

        except Exception as e:
            self.progress.hide()
            QMessageBox.critical(self, "Error", f"Failed to upscale image: {str(e)}")
