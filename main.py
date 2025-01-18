import sys
import os
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTabWidget, QLabel, QFrame, QSizePolicy, QScrollArea,
    QMenu, QMenuBar
)
from PySide6.QtGui import QIcon, QFont, QPalette, QColor
from PySide6.QtCore import Qt, QSize
from shiboken6 import Shiboken  # Add this import if not present

from utils.app_theme import AppTheme
from utils.localization import localization
from utils.pdf_converter import PDFConverter
from utils.pdf_to_docx import PDFtoDocx
from utils.pdf_to_excel import PDFtoExcel
from utils.pdf_compressor import PDFCompressor
from utils.ppt_converter import PPTConverter
from utils.web_scraper import WebScraper
from utils.images_to_pdf import ImagesToPDF
from utils.logo_resizer import LogoResizer
from utils.android_logo_resizer import AndroidLogoResizer
from utils.background_remover import BackgroundRemover
from utils.image_upscaler import ImageUpscaler

class ToolButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        
        # Create layout for icon and text
        layout = QHBoxLayout()
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)
        self.setLayout(layout)
        
        # Add icon (you can customize these based on the button type)
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(18, 18)
        layout.addWidget(self.icon_label)
        
        # Add text
        self.text_label = QLabel(text)
        self.text_label.setStyleSheet("background: transparent;")
        layout.addWidget(self.text_label)
        
        # Add spacer
        layout.addStretch()
        
        # Set initial style
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                border: none;
                border-radius: 8px;
                color: #64748B;
                background: transparent;
                font-size: 14px;
                font-weight: 500;
                padding: 0;
                margin: 2px 8px;
            }
            QPushButton:hover {
                background: rgba(241, 245, 249, 0.8);
            }
            QPushButton:checked {
                background: rgba(37, 99, 235, 0.1);
                color: #2563EB;
                font-weight: 600;
            }
            QLabel {
                background: transparent;
                border: none;
            }
        """)

    def showEvent(self, event):
        super().showEvent(event)
        self.updateStyle()

    def updateStyle(self):
        try:
            window = self.window()
            if window and hasattr(window, 'theme'):
                theme = window.theme.themes[window.theme.theme_name]
                base_style = f"""
                    QPushButton {{
                        text-align: left;
                        border: none;
                        border-radius: 8px;
                        color: {theme["text_color"]};
                        background: transparent;
                        font-size: 14px;
                        font-weight: 500;
                        padding: 0;
                        margin: 2px 8px;
                    }}
                    QPushButton:hover {{
                        background: {theme["hover_bg"]};
                        color: {theme["text_color"]};
                    }}
                    QPushButton:checked {{
                        background: {theme["active_item_bg"]};
                        color: {theme["active_item_text"]};
                        font-weight: 600;
                    }}
                    QLabel {{
                        background: transparent;
                        border: none;
                    }}
                """
                self.setStyleSheet(base_style)
        except Exception:
            pass

class CategoryWidget(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 8, 0, 8)
        self.layout.setSpacing(2)

        # Create header with icon and text
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 0, 20, 0)
        header_layout.setSpacing(8)
        
        self.header = QLabel(title)
        self.header.setStyleSheet("""
            color: #94A3B8; 
            font-size: 12px; 
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 8px 0;
            background: transparent;
        """)
        header_layout.addWidget(self.header)
        header_layout.addStretch()
        
        self.layout.addLayout(header_layout)

        # Create content layout
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(2)
        self.layout.addLayout(self.content_layout)

    def add_tool(self, tool_button):
        self.content_layout.addWidget(tool_button)

class Sidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(260)
        self.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
            QPushButton#coffee_btn {
                background: #FFDD00;
                color: #000000;
                border: none;
                border-radius: 8px;
                padding: 0 16px;
                font-weight: 600;
            }
            QPushButton#coffee_btn:hover {
                background: #FFE838;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 16)
        layout.setSpacing(32)

        # Add logo and title
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(8, 0, 0, 0)
        title_layout.setSpacing(12)
        
        logo_label = QLabel("🛠️")
        logo_label.setStyleSheet("font-size: 24px; background: transparent;")
        title_layout.addWidget(logo_label)
        
        title = QLabel("Converter")
        title.setStyleSheet("font-size: 20px; font-weight: 600; color: #1E293B; background: transparent;")
        title_layout.addWidget(title)
        
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # Create scrollable area for categories
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                width: 8px;
                background: transparent;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #CBD5E1;
                min-height: 24px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        # Create widget to hold categories
        categories_widget = QWidget()
        categories_widget.setStyleSheet("background: transparent;")
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

        # Add Buy Me a Coffee button
        coffee_btn = QPushButton("☕ Buy Me a Coffee")
        coffee_btn.setObjectName("coffee_btn")
        coffee_btn.setCursor(Qt.PointingHandCursor)
        coffee_btn.setFixedHeight(40)
        coffee_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://buymeacoffee.com/serhabdel")))
        layout.addWidget(coffee_btn)

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
        
        # Set application icon
        icon = QIcon("assets/app_icon.ico")
        self.setWindowIcon(icon)
        QApplication.instance().setWindowIcon(icon)

        # Initialize theme first
        self.theme = AppTheme(AppTheme.TOKYO_NIGHT)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create sidebar
        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)

        # Create main content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        main_layout.addWidget(content_widget)

        # Create tab widget for tool content
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        content_layout.addWidget(self.tab_widget)

        # Create theme menu
        menubar = self.menuBar()
        theme_menu = menubar.addMenu("Theme")
        theme_menu.setStyleSheet(f"""
            QMenu {{
                background: {self.theme.themes[self.theme.theme_name]["background_mid"]};
                color: {self.theme.themes[self.theme.theme_name]["text_color"]};
                border: 1px solid {self.theme.themes[self.theme.theme_name]["border_color"]};
                padding: 8px 0;
            }}
            QMenu::item {{
                padding: 8px 24px;
                margin: 0;
            }}
            QMenu::item:selected {{
                background: {self.theme.themes[self.theme.theme_name]["hover_bg"]};
                color: {self.theme.themes[self.theme.theme_name]["accent_primary"]};
            }}
        """)
        
        # Add theme actions
        tokyo_action = theme_menu.addAction("Tokyo Night")
        tokyo_action.triggered.connect(lambda: self.change_theme(AppTheme.TOKYO_NIGHT))
        
        solarized_action = theme_menu.addAction("Solarized Dark")
        solarized_action.triggered.connect(lambda: self.change_theme(AppTheme.SOLARIZED))
        
        light_action = theme_menu.addAction("Solarized Light")
        light_action.triggered.connect(lambda: self.change_theme(AppTheme.LIGHT))

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

        # Apply theme after all widgets are created
        self.apply_theme()

        # Show initial tool
        self.sidebar.pdf_converter_btn.click()

    def add_tool_tab(self, name, tool_class):
        # Check if tab already exists
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == name:
                self.tab_widget.setCurrentIndex(i)
                return

        # Create new tab
        tab = tool_class(self)
        index = self.tab_widget.addTab(tab, name)
        self.tab_widget.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tab_widget.count() > 1:  # Keep at least one tab open
            self.tab_widget.removeTab(index)

    def change_theme(self, theme_name):
        self.theme = AppTheme(theme_name)
        self.apply_theme()

    def apply_theme(self):
        theme = self.theme.themes[self.theme.theme_name]
        
        # Apply theme to the application
        self.theme.apply_theme(QApplication.instance())
        
        # Update menubar style
        menubar_style = f"""
            QMenuBar {{
                background: {theme["background_mid"]};
                color: {theme["text_color"]};
                border: none;
                border-bottom: 1px solid {theme["border_color"]};
                padding: 4px 8px;
            }}
            QMenuBar::item {{
                background: transparent;
                padding: 8px 12px;
                margin: 0;
                border-radius: 4px;
            }}
            QMenuBar::item:selected {{
                background: {theme["hover_bg"]};
                color: {theme["accent_primary"]};
            }}
            QMenuBar::item:pressed {{
                background: {theme["background_dark"]};
                color: {theme["accent_primary"]};
            }}
            QMenu {{
                background: {theme["background_mid"]};
                color: {theme["text_color"]};
                border: 1px solid {theme["border_color"]};
                padding: 8px 0;
            }}
            QMenu::item {{
                padding: 8px 24px;
                margin: 0;
            }}
            QMenu::item:selected {{
                background: {theme["hover_bg"]};
                color: {theme["accent_primary"]};
            }}
        """
        self.menuBar().setStyleSheet(menubar_style)
        
        # Update tab widget style
        tab_style = f"""
            QTabWidget::pane {{
                border: none;
                background: {theme["background_dark"]};
            }}
            QTabBar::tab {{
                background: {theme["background_mid"]};
                color: {theme["text_color"]};
                border: none;
                padding: 8px 24px;
                margin: 0;
                min-width: 120px;
            }}
            QTabBar::tab:selected {{
                color: {theme["accent_primary"]};
                background: {theme["background_dark"]};
                border-bottom: 2px solid {theme["accent_primary"]};
            }}
            QTabBar::tab:hover:!selected {{
                background: {theme["tab_hover"]};
            }}
            QTabBar::close-button {{
                image: url(close.png);
                padding: 4px;
            }}
            QTabBar::close-button:hover {{
                background: {theme["hover_bg"]};
                border-radius: 4px;
            }}
        """
        self.tab_widget.setStyleSheet(tab_style)
        
        # Update main window style
        self.setStyleSheet(f"""
            QMainWindow {{
                background: {theme["background_dark"]};
            }}
        """)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use Fusion style for better gradient support

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()