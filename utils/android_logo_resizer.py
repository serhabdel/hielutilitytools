from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QFileDialog, QProgressBar,
    QMessageBox, QFrame, QCheckBox
)
from PySide6.QtCore import Qt
from PIL import Image
import os

class AndroidLogoResizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sizes = {
            'mipmap-hdpi': (72, 72),
            'mipmap-mdpi': (48, 48),
            'mipmap-xhdpi': (96, 96),
            'mipmap-xxhdpi': (144, 144),
            'mipmap-xxxhdpi': (192, 192),
            'drawable-mdpi': (48, 48),
            'drawable-hdpi': (72, 72),
            'drawable-xhdpi': (96, 96),
            'drawable-xxhdpi': (144, 144),
            'drawable-xxxhdpi': (192, 192)
        }
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Android Logo Resizer")
        title.setStyleSheet("font-size: 24px; color: white;")
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
        input_label = QLabel("Select Logo (500x500 recommended)")
        input_label.setStyleSheet("color: #888; font-size: 12px;")
        content_layout.addWidget(input_label)

        input_layout = QHBoxLayout()
        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("Choose logo file...")
        self.input_path.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background: #363636;
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

        # Output Directory
        output_label = QLabel("Output Directory")
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

        # Options
        options_label = QLabel("Options")
        options_label.setStyleSheet("color: #888; font-size: 12px;")
        content_layout.addWidget(options_label)

        self.create_mipmap = QCheckBox("Create mipmap directories")
        self.create_mipmap.setChecked(True)
        self.create_mipmap.setStyleSheet("""
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
        content_layout.addWidget(self.create_mipmap)

        self.create_drawable = QCheckBox("Create drawable directories")
        self.create_drawable.setChecked(True)
        self.create_drawable.setStyleSheet(self.create_mipmap.styleSheet())
        content_layout.addWidget(self.create_drawable)

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

        # Generate Button
        generate_btn = QPushButton("Generate Icons")
        generate_btn.setStyleSheet("""
            QPushButton {
                padding: 12px;
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
        generate_btn.clicked.connect(self.generate_icons)
        content_layout.addWidget(generate_btn)

        layout.addWidget(content_frame)
        layout.addStretch()

    def browse_input(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Logo File",
            "",
            "Image files (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.input_path.setText(file_path)

    def browse_output(self):
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            ""
        )
        if dir_path:
            self.output_path.setText(dir_path)

    def generate_icons(self):
        input_path = self.input_path.text()
        output_dir = self.output_path.text()

        if not input_path or not output_dir:
            QMessageBox.warning(self, "Error", "Please select both input file and output directory")
            return

        try:
            self.progress.show()
            self.progress.setValue(0)

            # Filter sizes based on checkboxes
            selected_sizes = {}
            if self.create_mipmap.isChecked():
                selected_sizes.update({k: v for k, v in self.sizes.items() if k.startswith('mipmap')})
            if self.create_drawable.isChecked():
                selected_sizes.update({k: v for k, v in self.sizes.items() if k.startswith('drawable')})

            if not selected_sizes:
                QMessageBox.warning(self, "Error", "Please select at least one directory type")
                self.progress.hide()
                return

            # Create output directory
            os.makedirs(output_dir, exist_ok=True)

            # Open and process the image
            with Image.open(input_path) as img:
                total_items = len(selected_sizes)
                for i, (folder, size) in enumerate(selected_sizes.items()):
                    # Create the folder
                    folder_path = os.path.join(output_dir, folder)
                    os.makedirs(folder_path, exist_ok=True)

                    # Resize the image
                    resized_img = img.resize(size, Image.Resampling.LANCZOS)

                    # Save as ic_launcher.png
                    output_name = 'ic_launcher.png'
                    resized_img.save(os.path.join(folder_path, output_name))

                    # Update progress
                    self.progress.setValue(int((i + 1) / total_items * 100))

            self.progress.setValue(100)
            self.progress.hide()

            QMessageBox.information(
                self,
                "Success",
                "Android icons generated successfully!"
            )

        except Exception as e:
            self.progress.hide()
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
