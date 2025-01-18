from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog, QProgressBar
from PySide6.QtCore import Qt

class BaseTool(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)
        self.setLayout(self.layout)

    def create_title(self, text):
        title = QLabel(text)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 16px;
        """)
        return title

    def create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 14px; margin-bottom: 4px;")
        return label

    def create_button(self, text, primary=True):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(40)
        
        if primary:
            btn.setProperty("class", "primary")
        else:
            btn.setProperty("class", "secondary")
            
        self.update_button_style(btn)
        return btn

    def create_browse_button(self):
        btn = QPushButton("Browse")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedSize(100, 40)
        btn.setProperty("class", "secondary")
        self.update_button_style(btn)
        return btn

    def create_input(self, placeholder=""):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setFixedHeight(40)
        self.update_input_style(input_field)
        return input_field

    def create_progress_bar(self):
        progress = QProgressBar()
        progress.setFixedHeight(8)
        progress.setTextVisible(False)
        self.update_progress_style(progress)
        return progress

    def update_theme(self):
        if hasattr(self.main_window, 'theme'):
            theme = self.main_window.theme.themes[self.main_window.theme.theme_name]
            
            # Update widget background
            self.setStyleSheet(f"""
                QWidget {{
                    background: {theme["background_dark"]};
                    color: {theme["text_color"]};
                }}
            """)
            
            # Update all buttons
            for btn in self.findChildren(QPushButton):
                self.update_button_style(btn)
            
            # Update all inputs
            for input_field in self.findChildren(QLineEdit):
                self.update_input_style(input_field)
            
            # Update all progress bars
            for progress in self.findChildren(QProgressBar):
                self.update_progress_style(progress)

    def update_button_style(self, button):
        if not hasattr(self.main_window, 'theme'):
            return
            
        theme = self.main_window.theme.themes[self.main_window.theme.theme_name]
        
        if button.property("class") == "primary":
            button.setStyleSheet(f"""
                QPushButton {{
                    background: {theme["accent_primary"]};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 0 24px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background: {theme["accent_secondary"]};
                }}
                QPushButton:disabled {{
                    background: {theme["muted_text"]};
                }}
            """)
        else:
            button.setStyleSheet(f"""
                QPushButton {{
                    background: {theme["background_light"]};
                    color: {theme["text_color"]};
                    border: 1px solid {theme["border_color"]};
                    border-radius: 8px;
                    padding: 0 24px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background: {theme["hover_bg"]};
                    border-color: {theme["accent_primary"]};
                    color: {theme["accent_primary"]};
                }}
                QPushButton:disabled {{
                    background: {theme["background_mid"]};
                    color: {theme["muted_text"]};
                    border-color: {theme["border_color"]};
                }}
            """)

    def update_input_style(self, input_field):
        if not hasattr(self.main_window, 'theme'):
            return
            
        theme = self.main_window.theme.themes[self.main_window.theme.theme_name]
        
        input_field.setStyleSheet(f"""
            QLineEdit {{
                background: {theme["background_light"]};
                color: {theme["text_color"]};
                border: 1px solid {theme["border_color"]};
                border-radius: 8px;
                padding: 0 16px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border-color: {theme["accent_primary"]};
            }}
            QLineEdit:disabled {{
                background: {theme["background_mid"]};
                color: {theme["muted_text"]};
            }}
        """)

    def update_progress_style(self, progress):
        if not hasattr(self.main_window, 'theme'):
            return
            
        theme = self.main_window.theme.themes[self.main_window.theme.theme_name]
        
        progress.setStyleSheet(f"""
            QProgressBar {{
                background: {theme["background_light"]};
                border: none;
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background: {theme["accent_primary"]};
                border-radius: 4px;
            }}
        """)

    def browse_file(self, input_field, file_types="All Files (*.*)"):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "", file_types)
        if file_name:
            input_field.setText(file_name)

    def browse_save_file(self, input_field, file_types="All Files (*.*)"):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", file_types)
        if file_name:
            input_field.setText(file_name)

    def browse_directory(self, input_field):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            input_field.setText(directory)