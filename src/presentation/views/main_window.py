from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTabWidget, QLabel, QFileDialog,
    QSpinBox, QLineEdit, QProgressBar, QMessageBox,
    QListWidget, QListWidgetItem, QCheckBox, QGroupBox, 
    QTextEdit, QRadioButton, QButtonGroup, QComboBox, QSlider
)
from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtCore import QUrl
from pathlib import Path
import os
from src.presentation.viewmodels.pdf_to_images_viewmodel import PDFToImagesViewModel
from src.presentation.viewmodels.images_to_pdf_viewmodel import ImagesToPDFViewModel
from src.presentation.viewmodels.docx_converter_viewmodel import DocxConverterViewModel
from src.presentation.viewmodels.excel_converter_viewmodel import ExcelConverterViewModel
from src.presentation.viewmodels.ppt_converter_viewmodel import PPTConverterViewModel
from src.presentation.viewmodels.image_resizer_viewmodel import ImageResizerViewModel
from src.presentation.viewmodels.background_remover_viewmodel import BackgroundRemoverViewModel
from src.presentation.viewmodels.image_upscaler_viewmodel import ImageUpscalerViewModel
from src.presentation.viewmodels.logo_converter_viewmodel import LogoConverterViewModel
from src.infrastructure.image_services.logo_converter import LogoConverter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HiEL Utility Tools")
        self.setMinimumSize(800, 600)
        
        # Set window icon
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        icon_path = os.path.join(BASE_DIR, 'assets', 'app_icon.ico')
        print(f"Icon path: {icon_path}")
        print(f"Icon exists: {os.path.exists(icon_path)}")
        print(f"BASE_DIR: {BASE_DIR}")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Initialize view models
        self.pdf_to_images_vm = PDFToImagesViewModel()
        self.pdf_to_images_vm.progress_updated.connect(self.update_progress)
        self.pdf_to_images_vm.conversion_completed.connect(self.conversion_completed)
        self.pdf_to_images_vm.error_occurred.connect(self.show_error)
        
        self.images_to_pdf_vm = ImagesToPDFViewModel()
        self.images_to_pdf_vm.conversion_completed.connect(self.images_to_pdf_completed)
        self.images_to_pdf_vm.error_occurred.connect(self.show_error)
        
        self.docx_converter_vm = DocxConverterViewModel()
        self.docx_converter_vm.conversion_completed.connect(self.docx_conversion_completed)
        self.docx_converter_vm.error_occurred.connect(self.show_error)
        
        self.excel_converter_vm = ExcelConverterViewModel()
        self.excel_converter_vm.conversion_completed.connect(self.excel_conversion_completed)
        self.excel_converter_vm.error_occurred.connect(self.show_error)
        
        self.ppt_converter_vm = PPTConverterViewModel()
        self.ppt_converter_vm.conversion_completed.connect(self.ppt_conversion_completed)
        self.ppt_converter_vm.error_occurred.connect(self.show_error)
        
        self.image_resizer_vm = ImageResizerViewModel()
        self.image_resizer_vm.resize_completed.connect(self.resize_completed)
        self.image_resizer_vm.android_resize_completed.connect(self.android_resize_completed)
        self.image_resizer_vm.error_occurred.connect(self.show_error)
        
        self.background_remover_vm = BackgroundRemoverViewModel()
        self.background_remover_vm.processing_completed.connect(self.background_removal_completed)
        self.background_remover_vm.error_occurred.connect(self.show_error)
        
        self.image_upscaler_vm = ImageUpscalerViewModel()
        self.image_upscaler_vm.processing_completed.connect(self.upscale_completed)
        self.image_upscaler_vm.error_occurred.connect(self.show_error)
        
        self.logo_converter_vm = LogoConverterViewModel()
        self.logo_converter_vm.error_occurred.connect(self.show_error)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Add Buy Me a Coffee button
        support_layout = QHBoxLayout()
        buy_coffee_btn = QPushButton("☕ Support the Project")
        buy_coffee_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFDD00;
                color: black;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FFAA00;
            }
        """)
        buy_coffee_btn.clicked.connect(self._open_buy_me_coffee)
        support_layout.addStretch()
        support_layout.addWidget(buy_coffee_btn)
        support_layout.addStretch()
        
        # Add support layout to main layout
        main_layout.addLayout(support_layout)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Add feature tabs
        self.setup_pdf_to_images_tab()
        self.setup_images_to_pdf_tab()
        self.setup_pdf_docx_tab()
        self.setup_pdf_excel_tab()
        self.setup_ppt_pdf_tab()
        self.setup_logo_resizer_tab()
        self.setup_android_logo_tab()
        self.setup_background_remover_tab()
        self.setup_image_upscaler_tab()
        self.setup_web_search_tab()
        
    def _open_buy_me_coffee(self):
        """
        Open Buy Me a Coffee page in the default web browser
        """
        try:
            url = QUrl("https://buymeacoffee.com/serhabdel")
            QDesktopServices.openUrl(url)
        except Exception as e:
            QMessageBox.warning(self, "Error", 
                f"Could not open support page. Please visit: https://buymeacoffee.com/serhabdel\n\nError: {str(e)}")
    
    def setup_pdf_to_images_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Input file selection
        input_group = QGroupBox("PDF File")
        input_layout = QVBoxLayout()
        
        file_layout = QHBoxLayout()
        self.pdf_input_path = QLineEdit()
        self.pdf_input_path.setPlaceholderText("Select PDF file...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(lambda: self.browse_file_with_target("PDF files (*.pdf)", self.pdf_input_path))
        file_layout.addWidget(self.pdf_input_path)
        file_layout.addWidget(browse_btn)
        input_layout.addLayout(file_layout)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Convert button
        convert_btn = QPushButton("Convert PDF to Images")
        convert_btn.clicked.connect(self.convert_pdf_to_images)
        layout.addWidget(convert_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        layout.addWidget(self.progress_bar)
        
        # Output preview area
        output_group = QGroupBox("Converted Images")
        output_layout = QVBoxLayout()
        self.output_images_list = QListWidget()
        output_layout.addWidget(self.output_images_list)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "PDF to Images")
    
    def convert_pdf_to_images(self):
        input_path = self.pdf_input_path.text()
        if not input_path:
            QMessageBox.warning(self, "Error", "Please select a PDF file")
            return
        
        # Reset UI
        self.progress_bar.setValue(0)
        self.output_images_list.clear()
        
        try:
            # Convert PDF to images
            self.pdf_to_images_vm.convert_pdf(input_path)
        except Exception as e:
            QMessageBox.critical(self, "Conversion Error", str(e))
    
    def update_progress(self, value: int):
        self.progress_bar.setValue(value)
    
    def conversion_completed(self, output_files):
        # Clear previous items
        self.output_images_list.clear()
        
        # Add converted image paths to the list
        for file_path in output_files:
            item = QListWidgetItem(os.path.basename(file_path))
            item.setToolTip(file_path)
            self.output_images_list.addItem(item)
        
        # Show success message
        QMessageBox.information(self, "Conversion Complete", f"Converted {len(output_files)} images")
    
    def show_error(self, message: str):
        QMessageBox.critical(self, "Error", message)
        self.progress_bar.setValue(0)
    
    def setup_images_to_pdf_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Image list
        self.image_list = QListWidget()
        layout.addWidget(QLabel("Selected Images:"))
        layout.addWidget(self.image_list)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Add images button
        add_images_btn = QPushButton("Add Images")
        add_images_btn.clicked.connect(self.add_images)
        buttons_layout.addWidget(add_images_btn)
        
        # Remove selected button
        remove_btn = QPushButton("Remove Selected")
        remove_btn.clicked.connect(self.remove_selected_images)
        buttons_layout.addWidget(remove_btn)
        
        # Clear all button
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.image_list.clear)
        buttons_layout.addWidget(clear_btn)
        
        layout.addLayout(buttons_layout)
        
        # Output file selection
        output_layout = QHBoxLayout()
        self.pdf_output_path = QLineEdit()
        self.pdf_output_path.setPlaceholderText("Select output PDF location (optional)...")
        browse_output_btn = QPushButton("Browse")
        browse_output_btn.clicked.connect(self.browse_pdf_output)
        output_layout.addWidget(self.pdf_output_path)
        output_layout.addWidget(browse_output_btn)
        layout.addLayout(output_layout)
        
        # Convert button
        convert_btn = QPushButton("Convert to PDF")
        convert_btn.clicked.connect(self.convert_images_to_pdf)
        layout.addWidget(convert_btn)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "Images to PDF")
    
    def add_images(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            str(Path.home()),
            "Image files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_paths:
            self.image_list.addItems(file_paths)
    
    def remove_selected_images(self):
        for item in self.image_list.selectedItems():
            self.image_list.takeItem(self.image_list.row(item))
    
    def browse_pdf_output(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF As",
            str(Path.home()),
            "PDF files (*.pdf)"
        )
        if file_path:
            if not file_path.lower().endswith('.pdf'):
                file_path += '.pdf'
            self.pdf_output_path.setText(file_path)
    
    def convert_images_to_pdf(self):
        image_paths = [
            self.image_list.item(i).text()
            for i in range(self.image_list.count())
        ]
        output_path = self.pdf_output_path.text() or None
        
        self.images_to_pdf_vm.convert_images(image_paths, output_path)
    
    def images_to_pdf_completed(self, output_path: str):
        QMessageBox.information(
            self,
            "Conversion Complete",
            f"Successfully created PDF: {output_path}"
        )
    
    def setup_pdf_docx_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Input file selection
        input_layout = QHBoxLayout()
        self.docx_input_path = QLineEdit()
        self.docx_input_path.setPlaceholderText("Select PDF or DOCX file...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(lambda: self.browse_file_with_target("Documents (*.pdf *.docx)", self.docx_input_path))
        input_layout.addWidget(self.docx_input_path)
        input_layout.addWidget(browse_btn)
        layout.addLayout(input_layout)
        
        # Output file selection
        output_layout = QHBoxLayout()
        self.docx_output_path = QLineEdit()
        self.docx_output_path.setPlaceholderText("Select output location (optional)...")
        browse_output_btn = QPushButton("Browse")
        browse_output_btn.clicked.connect(self.browse_docx_output)
        output_layout.addWidget(self.docx_output_path)
        output_layout.addWidget(browse_output_btn)
        layout.addLayout(output_layout)
        
        # Convert button
        convert_btn = QPushButton("Convert")
        convert_btn.clicked.connect(self.convert_docx)
        layout.addWidget(convert_btn)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "PDF DOCX")
    
    def browse_file_docx(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            str(Path.home()),
            "Documents (*.pdf *.docx)"
        )
        if file_path:
            self.docx_input_path.setText(file_path)
            # Update output path placeholder based on input type
            input_ext = Path(file_path).suffix.lower()
            output_ext = '.docx' if input_ext == '.pdf' else '.pdf'
            self.docx_output_path.setPlaceholderText(f"Select output {output_ext} location (optional)...")
    
    def browse_docx_output(self):
        input_path = self.docx_input_path.text()
        if not input_path:
            QMessageBox.warning(self, "Warning", "Please select an input file first")
            return
        
        input_ext = Path(input_path).suffix.lower()
        output_ext = '.docx' if input_ext == '.pdf' else '.pdf'
        filter_text = "Word Document (*.docx)" if output_ext == '.docx' else "PDF Document (*.pdf)"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save As",
            str(Path.home()),
            filter_text
        )
        if file_path:
            if not file_path.lower().endswith(output_ext):
                file_path += output_ext
            self.docx_output_path.setText(file_path)
    
    def convert_docx(self):
        self.docx_converter_vm.convert_file(
            self.docx_input_path.text(),
            self.docx_output_path.text() or None
        )
    
    def docx_conversion_completed(self, output_path: str):
        QMessageBox.information(
            self,
            "Conversion Complete",
            f"Successfully converted file: {output_path}"
        )
    
    def setup_pdf_excel_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Input file selection
        input_layout = QHBoxLayout()
        self.excel_input_path = QLineEdit()
        self.excel_input_path.setPlaceholderText("Select PDF file...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(lambda: self.browse_file_with_target("PDF files (*.pdf)", self.excel_input_path))
        input_layout.addWidget(self.excel_input_path)
        input_layout.addWidget(browse_btn)
        layout.addLayout(input_layout)
        
        # Options group
        options_group = QGroupBox("Conversion Options")
        options_layout = QVBoxLayout()
        
        # Pages option
        pages_layout = QHBoxLayout()
        pages_layout.addWidget(QLabel("Pages:"))
        self.pages_input = QLineEdit()
        self.pages_input.setPlaceholderText("e.g., 1-3 or 'all'")
        self.pages_input.setText("all")
        pages_layout.addWidget(self.pages_input)
        options_layout.addLayout(pages_layout)
        
        # Multiple tables option
        self.multiple_tables_cb = QCheckBox("Extract multiple tables per page")
        self.multiple_tables_cb.setChecked(True)
        options_layout.addWidget(self.multiple_tables_cb)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Output file selection
        output_layout = QHBoxLayout()
        self.excel_output_path = QLineEdit()
        self.excel_output_path.setPlaceholderText("Select output Excel location (optional)...")
        browse_output_btn = QPushButton("Browse")
        browse_output_btn.clicked.connect(self.browse_excel_output)
        output_layout.addWidget(self.excel_output_path)
        output_layout.addWidget(browse_output_btn)
        layout.addLayout(output_layout)
        
        # Convert button
        convert_btn = QPushButton("Convert to Excel")
        convert_btn.clicked.connect(self.convert_to_excel)
        layout.addWidget(convert_btn)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "PDF to Excel")
    
    def browse_excel_output(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Excel As",
            str(Path.home()),
            "Excel files (*.xlsx)"
        )
        if file_path:
            if not file_path.lower().endswith('.xlsx'):
                file_path += '.xlsx'
            self.excel_output_path.setText(file_path)
    
    def convert_to_excel(self):
        self.excel_converter_vm.convert_to_excel(
            input_path=self.excel_input_path.text(),
            output_path=self.excel_output_path.text() or None,
            pages=self.pages_input.text(),
            multiple_tables=self.multiple_tables_cb.isChecked()
        )
    
    def excel_conversion_completed(self, output_path: str):
        QMessageBox.information(
            self,
            "Conversion Complete",
            f"Successfully converted PDF to Excel: {output_path}"
        )
    
    def setup_ppt_pdf_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Input file selection
        input_layout = QHBoxLayout()
        self.ppt_input_path = QLineEdit()
        self.ppt_input_path.setPlaceholderText("Select PPT/PPTX or PDF file...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(lambda: self.browse_file_ppt())
        input_layout.addWidget(self.ppt_input_path)
        input_layout.addWidget(browse_btn)
        layout.addLayout(input_layout)
        
        # Output file selection
        output_layout = QHBoxLayout()
        self.ppt_output_path = QLineEdit()
        self.ppt_output_path.setPlaceholderText("Select output location (optional)...")
        browse_output_btn = QPushButton("Browse")
        browse_output_btn.clicked.connect(self.browse_ppt_output)
        output_layout.addWidget(self.ppt_output_path)
        output_layout.addWidget(browse_output_btn)
        layout.addLayout(output_layout)
        
        # Convert button
        convert_btn = QPushButton("Convert")
        convert_btn.clicked.connect(self.convert_ppt)
        layout.addWidget(convert_btn)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "PPT PDF")
    
    def browse_file_ppt(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            str(Path.home()),
            "Presentations (*.ppt *.pptx *.pdf)"
        )
        if file_path:
            self.ppt_input_path.setText(file_path)
            # Update output path placeholder based on input type
            input_ext = Path(file_path).suffix.lower()
            output_ext = '.pdf' if input_ext in ['.ppt', '.pptx'] else '.pptx'
            self.ppt_output_path.setPlaceholderText(f"Select output {output_ext} location (optional)...")
    
    def browse_ppt_output(self):
        input_path = self.ppt_input_path.text()
        if not input_path:
            QMessageBox.warning(self, "Warning", "Please select an input file first")
            return
        
        input_ext = Path(input_path).suffix.lower()
        output_ext = '.pdf' if input_ext in ['.ppt', '.pptx'] else '.pptx'
        filter_text = "PDF Document (*.pdf)" if output_ext == '.pdf' else "PowerPoint Presentation (*.pptx)"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save As",
            str(Path.home()),
            filter_text
        )
        if file_path:
            if not file_path.lower().endswith(output_ext):
                file_path += output_ext
            self.ppt_output_path.setText(file_path)
    
    def convert_ppt(self):
        self.ppt_converter_vm.convert_file(
            self.ppt_input_path.text(),
            self.ppt_output_path.text() or None
        )
    
    def ppt_conversion_completed(self, output_path: str):
        QMessageBox.information(
            self,
            "Conversion Complete",
            f"Successfully converted file: {output_path}"
        )
    
    def setup_logo_resizer_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Input file selection
        input_group = QGroupBox("Input Logo")
        input_layout = QVBoxLayout()
        
        file_layout = QHBoxLayout()
        self.logo_input_path = QLineEdit()
        self.logo_input_path.setPlaceholderText("Select 500x500 PNG file...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(lambda: self.browse_file_with_target("PNG files (*.png)", self.logo_input_path))
        file_layout.addWidget(self.logo_input_path)
        file_layout.addWidget(browse_btn)
        input_layout.addLayout(file_layout)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Conversion options
        options_group = QGroupBox("Conversion Options")
        options_layout = QVBoxLayout()
        
        # Preset selection
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Preset:"))
        self.logo_preset = QComboBox()
        logo_presets = {
            "Windows Icon (.ico)": {
                "description": "Multi-size Windows application icon"
            },
            "Web Favicon (.ico)": {
                "description": "Small icon for web browser tabs"
            }
        }
        self.logo_presets_data = logo_presets
        preset_names = list(logo_presets.keys())
        self.logo_preset.addItems(preset_names)
        preset_layout.addWidget(self.logo_preset)
        options_layout.addLayout(preset_layout)
        
        # Preset description
        self.preset_description = QLabel("Select a preset to convert 500x500 PNG to ICO")
        self.preset_description.setWordWrap(True)
        options_layout.addWidget(self.preset_description)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Convert button
        convert_btn = QPushButton("Convert Logo")
        convert_btn.clicked.connect(self.convert_logo)
        layout.addWidget(convert_btn)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "Logo to Icon")
    
    def convert_logo(self):
        input_path = self.logo_input_path.text()
        if not input_path:
            QMessageBox.warning(self, "Error", "Please select a PNG file")
            return
        
        try:
            result_path = self.logo_converter_vm.convert_logo(input_path)
            QMessageBox.information(self, "Conversion Complete", f"Icon saved to: {result_path}")
        except Exception as e:
            QMessageBox.critical(self, "Conversion Error", str(e))
    
    def setup_android_logo_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Input file selection
        input_layout = QHBoxLayout()
        self.android_logo_input_path = QLineEdit()
        self.android_logo_input_path.setPlaceholderText("Select image file (recommended: 512x512 PNG)...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(lambda: self.browse_image(self.android_logo_input_path))
        input_layout.addWidget(self.android_logo_input_path)
        input_layout.addWidget(browse_btn)
        layout.addLayout(input_layout)
        
        # Info text
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMaximumHeight(100)
        info_text.setText(
            "This will create the following Android icon sizes:\n"
            "- mipmap-mdpi: 48x48\n"
            "- mipmap-hdpi: 72x72\n"
            "- mipmap-xhdpi: 96x96\n"
            "- mipmap-xxhdpi: 144x144\n"
            "- mipmap-xxxhdpi: 192x192\n"
            "- Play Store: 512x512"
        )
        layout.addWidget(info_text)
        
        # Generate button
        generate_btn = QPushButton("Generate Android Icons")
        generate_btn.clicked.connect(self.generate_android_icons)
        layout.addWidget(generate_btn)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "Android Logo Generator")
    
    def browse_image(self, target: QLineEdit = None):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            str(Path.home()),
            "Image files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            if target is None:
                target = self.logo_input_path
            target.setText(file_path)
    
    def generate_android_icons(self):
        self.image_resizer_vm.create_android_icons(
            input_path=self.android_logo_input_path.text()
        )
    
    def setup_background_remover_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Input file selection
        input_layout = QHBoxLayout()
        self.bg_input_path = QLineEdit()
        self.bg_input_path.setPlaceholderText("Select image file...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(lambda: self.browse_image(self.bg_input_path))
        input_layout.addWidget(self.bg_input_path)
        input_layout.addWidget(browse_btn)
        layout.addLayout(input_layout)
        
        # Output file selection
        output_layout = QHBoxLayout()
        self.bg_output_path = QLineEdit()
        self.bg_output_path.setPlaceholderText("Select output location (optional)...")
        browse_output_btn = QPushButton("Browse")
        browse_output_btn.clicked.connect(self.browse_bg_output)
        output_layout.addWidget(self.bg_output_path)
        output_layout.addWidget(browse_output_btn)
        layout.addLayout(output_layout)
        
        # Process button
        process_btn = QPushButton("Remove Background")
        process_btn.clicked.connect(self.remove_background)
        layout.addWidget(process_btn)
        
        # Info text
        info_text = QLabel(
            "This tool is designed to remove backgrounds from images.\n"
            "The output will be saved as a PNG file with transparency."
        )
        info_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_text)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "Background Remover")
    
    def browse_bg_output(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image As",
            str(Path.home()),
            "PNG Image (*.png)"
        )
        if file_path:
            if not file_path.lower().endswith('.png'):
                file_path += '.png'
            self.bg_output_path.setText(file_path)
    
    def remove_background(self):
        self.background_remover_vm.remove_background(
            input_path=self.bg_input_path.text(),
            output_path=self.bg_output_path.text() or None
        )
    
    def background_removal_completed(self, output_path: str):
        QMessageBox.information(
            self,
            "Background Removal Complete",
            f"Successfully removed background: {output_path}"
        )
    
    def setup_image_upscaler_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Input file selection
        input_layout = QHBoxLayout()
        self.upscaler_input_path = QLineEdit()
        self.upscaler_input_path.setPlaceholderText("Select image file...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(lambda: self.browse_image(self.upscaler_input_path))
        input_layout.addWidget(self.upscaler_input_path)
        input_layout.addWidget(browse_btn)
        layout.addLayout(input_layout)
        
        # Scale factor selection
        scale_group = QGroupBox("Scale Factor")
        scale_layout = QHBoxLayout()
        
        self.scale_2x = QRadioButton("2x")
        self.scale_2x.setChecked(True)
        self.scale_4x = QRadioButton("4x")
        
        scale_layout.addWidget(self.scale_2x)
        scale_layout.addWidget(self.scale_4x)
        scale_group.setLayout(scale_layout)
        layout.addWidget(scale_group)
        
        # Output file selection
        output_layout = QHBoxLayout()
        self.upscaler_output_path = QLineEdit()
        self.upscaler_output_path.setPlaceholderText("Select output location (optional)...")
        browse_output_btn = QPushButton("Browse")
        browse_output_btn.clicked.connect(self.browse_upscaler_output)
        output_layout.addWidget(self.upscaler_output_path)
        output_layout.addWidget(browse_output_btn)
        layout.addLayout(output_layout)
        
        # Process button
        process_btn = QPushButton("Upscale Image")
        process_btn.clicked.connect(self.upscale_image)
        layout.addWidget(process_btn)
        
        # Info text
        info_text = QLabel(
            "This tool performs super-resolution to upscale images.\n"
            "2x will double the resolution, 4x will quadruple it."
        )
        info_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_text)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "Image Upscaler")
    
    def browse_upscaler_output(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image As",
            str(Path.home()),
            "Image files (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.upscaler_output_path.setText(file_path)
    
    def upscale_image(self):
        scale_factor = 4 if self.scale_4x.isChecked() else 2
        self.image_upscaler_vm.upscale_image(
            input_path=self.upscaler_input_path.text(),
            scale_factor=scale_factor,
            output_path=self.upscaler_output_path.text() or None
        )
    
    def upscale_completed(self, output_path: str):
        QMessageBox.information(
            self,
            "Upscaling Complete",
            f"Successfully upscaled image: {output_path}"
        )
    
    def setup_web_search_tab(self):
        pass
    
    def resize_completed(self, output_path: str):
        QMessageBox.information(
            self,
            "Resize Complete",
            f"Successfully resized image: {output_path}"
        )
    
    def android_resize_completed(self, output_paths: dict):
        message = "Successfully generated Android icons:\n\n"
        for density, path in output_paths.items():
            message += f"{density}: {path}\n"
        
        QMessageBox.information(
            self,
            "Android Icons Generated",
            message
        )
    
    def browse_file_with_target(self, file_filter: str, target: QLineEdit) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File", str(Path.home()), file_filter
        )
        if file_path:
            target.setText(file_path)