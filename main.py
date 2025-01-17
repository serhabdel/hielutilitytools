import sys
import os

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTabWidget, QLabel, QFrame, QSizePolicy, QScrollArea
)
from PySide6.QtGui import QIcon, QFont, QPalette, QColor
from PySide6.QtCore import Qt, QSize
from shiboken6 import Shiboken  # Add this import if not present

from utils.app_theme import EnterpriseTheme
from utils.localization import localization
from utils.pdf_converter import PDFConverter
from utils.pdf_to_docx import PDFtoDocx
from utils.pdf_to_excel import PDFtoExcel
from utils.logo_resizer import LogoResizer
from utils.android_logo_resizer import AndroidLogoResizer
from utils.background_remover import BackgroundRemover
from utils.image_upscaler import ImageUpscaler
from utils.pdf_compressor import PDFCompressor
from utils.ppt_converter import PPTConverter
from utils.web_scraper import WebScraper
from utils.images_to_pdf import ImagesToPDF

class ToolButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                color: white;
                background: transparent;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            QPushButton:checked {
                background: #4a90e2;
            }
        """)

class CategoryWidget(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        header = QLabel(title)
        header.setStyleSheet("color: #888; font-size: 12px; padding: 8px 16px;")
        layout.addWidget(header)
        
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(2)
        layout.addLayout(self.content_layout)
        
    def add_tool(self, tool_button):
        self.content_layout.addWidget(tool_button)

class Sidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(250)
        self.setStyleSheet("""
            QFrame {
                background: #1e1e1e;
                border-right: 1px solid #333;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(24)
        
        # Add logo or title
        title = QLabel("Converter")
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        # Create scrollable area for categories
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #2d2d2d;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #666;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        # Create widget to hold categories
        categories_widget = QWidget()
        categories_layout = QVBoxLayout(categories_widget)
        categories_layout.setContentsMargins(0, 0, 0, 0)
        categories_layout.setSpacing(24)
        
        # PDF Tools category
        pdf_category = CategoryWidget("PDF Tools")
        self.pdf_converter_btn = ToolButton("PDF to Images")
        self.pdf_to_docx_btn = ToolButton("PDF to DOCX")
        self.pdf_to_excel_btn = ToolButton("PDF to Excel")
        self.pdf_compressor_btn = ToolButton("PDF Compressor")
        self.ppt_converter_btn = ToolButton("PPT Converter")
        pdf_category.add_tool(self.pdf_converter_btn)
        pdf_category.add_tool(self.pdf_to_docx_btn)
        pdf_category.add_tool(self.pdf_to_excel_btn)
        pdf_category.add_tool(self.pdf_compressor_btn)
        pdf_category.add_tool(self.ppt_converter_btn)
        categories_layout.addWidget(pdf_category)
        
        # Image Tools category
        image_category = CategoryWidget("Image Tools")
        self.logo_resizer_btn = ToolButton("Logo Resizer")
        self.android_logo_btn = ToolButton("Android Logo Resizer")
        self.bg_remover_btn = ToolButton("Background Remover")
        self.img_upscaler_btn = ToolButton("Image Upscaler")
        self.images_to_pdf_btn = ToolButton("Images to PDF")
        image_category.add_tool(self.logo_resizer_btn)
        image_category.add_tool(self.android_logo_btn)
        image_category.add_tool(self.bg_remover_btn)
        image_category.add_tool(self.img_upscaler_btn)
        image_category.add_tool(self.images_to_pdf_btn)
        categories_layout.addWidget(image_category)
        
        # Web Tools category
        web_category = CategoryWidget("Web Tools")
        self.web_scraper_btn = ToolButton("Web Content Converter")
        web_category.add_tool(self.web_scraper_btn)
        categories_layout.addWidget(web_category)

        categories_layout.addStretch()
        scroll_area.setWidget(categories_widget)
        layout.addWidget(scroll_area)

class ToolTab(QWidget):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        if name == "PDF to Images":
            layout.addWidget(PDFConverter(self))
        elif name == "PDF to DOCX":
            layout.addWidget(PDFtoDocx(self))
        elif name == "PDF to Excel":
            layout.addWidget(PDFtoExcel(self))
        elif name == "Logo Resizer":
            layout.addWidget(LogoResizer(self))
        elif name == "Android Logo Resizer":
            layout.addWidget(AndroidLogoResizer(self))
        elif name == "Background Remover":
            layout.addWidget(BackgroundRemover(self))
        elif name == "Image Upscaler":
            layout.addWidget(ImageUpscaler(self))
        elif name == "PDF Compressor":
            layout.addWidget(PDFCompressor(self))
        elif name == "PPT Converter":
            layout.addWidget(PPTConverter(self))
        elif name == "Web Content Converter":
            layout.addWidget(WebScraper(self))
        elif name == "Images to PDF":
            layout.addWidget(ImagesToPDF(self))
        else:
            # Placeholder for other tools
            header = QLabel(name)
            header.setStyleSheet("font-size: 24px; color: #fff; padding: 20px;")
            layout.addWidget(header)
            
            content = QLabel("Tool content will be here")
            content.setAlignment(Qt.AlignCenter)
            content.setStyleSheet("color: #888; font-size: 16px;")
            layout.addWidget(content)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hiel Utility Tools")
        self.setMinimumSize(1200, 800)
        
        # Apply theme
        self.theme = EnterpriseTheme()
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Create tab widget for tool content
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #2d2d2d;
            }
            QTabBar::tab {
                background: #1e1e1e;
                color: #888;
                padding: 8px 16px;
                border: none;
                border-right: 1px solid #333;
            }
            QTabBar::tab:selected {
                background: #2d2d2d;
                color: white;
            }
            QTabBar::close-button {
                image: url(close.png);
            }
            QTabBar::close-button:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        main_layout.addWidget(self.tab_widget)
        
        # Connect buttons
        self.sidebar.pdf_converter_btn.clicked.connect(lambda: self.add_tool_tab("PDF to Images", PDFConverter))
        self.sidebar.pdf_to_docx_btn.clicked.connect(lambda: self.add_tool_tab("PDF to DOCX", PDFtoDocx))
        self.sidebar.pdf_to_excel_btn.clicked.connect(lambda: self.add_tool_tab("PDF to Excel", PDFtoExcel))
        self.sidebar.logo_resizer_btn.clicked.connect(lambda: self.add_tool_tab("Logo Resizer", LogoResizer))
        self.sidebar.android_logo_btn.clicked.connect(lambda: self.add_tool_tab("Android Logo Resizer", AndroidLogoResizer))
        self.sidebar.bg_remover_btn.clicked.connect(lambda: self.add_tool_tab("Background Remover", BackgroundRemover))
        self.sidebar.pdf_compressor_btn.clicked.connect(lambda: self.add_tool_tab("PDF Compressor", PDFCompressor))
        self.sidebar.ppt_converter_btn.clicked.connect(lambda: self.add_tool_tab("PPT Converter", PPTConverter))
        self.sidebar.img_upscaler_btn.clicked.connect(lambda: self.add_tool_tab("Image Upscaler", ImageUpscaler))
        self.sidebar.web_scraper_btn.clicked.connect(lambda: self.add_tool_tab("Web Content Converter", WebScraper))
        self.sidebar.images_to_pdf_btn.clicked.connect(lambda: self.add_tool_tab("Images to PDF", ImagesToPDF))
        
        # Show initial tool
        self.sidebar.pdf_converter_btn.click()
    
    def add_tool_tab(self, name, tool_class):
        # Check if tab already exists
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == name:
                self.tab_widget.setCurrentIndex(i)
                return
        
        # Create new tab
        tool_widget = tool_class(self)
        index = self.tab_widget.addTab(tool_widget, name)
        self.tab_widget.setCurrentIndex(index)
    
    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use Fusion style for better gradient support
    
    # Apply the enterprise theme
    enterprise_theme = EnterpriseTheme()
    enterprise_theme.apply_theme(app)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()