from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor, QLinearGradient, QBrush
from PySide6.QtCore import Qt

class AppTheme:
    TOKYO_NIGHT = "tokyo_night"
    SOLARIZED = "solarized"
    LIGHT = "light"
    DRACULA = "dracula"
    NORD = "nord"

    def __init__(self, theme_name=TOKYO_NIGHT):
        self.theme_name = theme_name
        self.themes = {
            self.TOKYO_NIGHT: {
                "background_dark": "#1a1b26",
                "background_mid": "#24283b",
                "background_light": "#2f334d",
                "accent_primary": "#7aa2f7",
                "accent_secondary": "#bb9af7",
                "accent_success": "#9ece6a",
                "text_color": "#a9b1d6",
                "muted_text": "#565f89",
                "border_color": "#2f334d",
                "tab_selected": "#7aa2f7",
                "tab_hover": "rgba(122, 162, 247, 0.1)",
                "sidebar_bg": "#1a1b26",
                "active_item_bg": "rgba(122, 162, 247, 0.1)",
                "active_item_text": "#7aa2f7",
                "hover_bg": "rgba(47, 51, 77, 0.8)"
            },
            self.SOLARIZED: {
                "background_dark": "#002b36",
                "background_mid": "#073642",
                "background_light": "#094352",
                "accent_primary": "#2aa198",
                "accent_secondary": "#268bd2",
                "accent_success": "#859900",
                "text_color": "#93a1a1",
                "muted_text": "#586e75",
                "border_color": "#094352",
                "tab_selected": "#2aa198",
                "tab_hover": "rgba(42, 161, 152, 0.1)",
                "sidebar_bg": "#002b36",
                "active_item_bg": "rgba(42, 161, 152, 0.1)",
                "active_item_text": "#2aa198",
                "hover_bg": "rgba(9, 67, 82, 0.8)"
            },
            self.LIGHT: {
                "background_dark": "#F8F9FD",
                "background_mid": "#FFFFFF",
                "background_light": "#F8F9FD",
                "accent_primary": "#2563EB",
                "accent_secondary": "#3B82F6",
                "accent_success": "#10B981",
                "text_color": "#64748B",
                "muted_text": "#94A3B8",
                "border_color": "#E2E8F0",
                "tab_selected": "#2563EB",
                "tab_hover": "rgba(37, 99, 235, 0.1)",
                "sidebar_bg": "#FFFFFF",
                "active_item_bg": "rgba(37, 99, 235, 0.1)",
                "active_item_text": "#2563EB",
                "hover_bg": "rgba(241, 245, 249, 0.8)"
            },
            self.DRACULA: {
                "background_dark": "#282a36",
                "background_mid": "#44475a",
                "background_light": "#6272a4",
                "accent_primary": "#bd93f9",
                "accent_secondary": "#ff79c6",
                "accent_success": "#50fa7b",
                "text_color": "#f8f8f2",
                "muted_text": "#6272a4",
                "border_color": "#44475a",
                "tab_selected": "#bd93f9",
                "tab_hover": "rgba(189, 147, 249, 0.1)",
                "sidebar_bg": "#282a36",
                "active_item_bg": "rgba(189, 147, 249, 0.1)",
                "active_item_text": "#bd93f9",
                "hover_bg": "rgba(68, 71, 90, 0.8)"
            },
            self.NORD: {
                "background_dark": "#2e3440",
                "background_mid": "#3b4252",
                "background_light": "#4c566a",
                "accent_primary": "#88c0d0",
                "accent_secondary": "#81a1c1",
                "accent_success": "#a3be8c",
                "text_color": "#e5e9f0",
                "muted_text": "#4c566a",
                "border_color": "#3b4252",
                "tab_selected": "#88c0d0",
                "tab_hover": "rgba(136, 192, 208, 0.1)",
                "sidebar_bg": "#2e3440",
                "active_item_bg": "rgba(136, 192, 208, 0.1)",
                "active_item_text": "#88c0d0",
                "hover_bg": "rgba(59, 66, 82, 0.8)"
            }
        }

    def apply_theme(self, app: QApplication):
        theme = self.themes[self.theme_name]
        palette = QPalette()

        # Create gradients
        main_gradient = QLinearGradient(0, 0, 0, 400)
        main_gradient.setColorAt(0.0, QColor(theme["background_dark"]))
        main_gradient.setColorAt(1.0, QColor(theme["background_mid"]))

        # Set color roles
        palette.setColor(QPalette.Window, QColor(theme["background_dark"]))
        palette.setBrush(QPalette.Window, QBrush(main_gradient))
        palette.setColor(QPalette.WindowText, QColor(theme["text_color"]))
        palette.setColor(QPalette.Base, QColor(theme["background_mid"]))
        palette.setColor(QPalette.AlternateBase, QColor(theme["background_light"]))
        palette.setColor(QPalette.ToolTipBase, QColor(theme["background_mid"]))
        palette.setColor(QPalette.ToolTipText, QColor(theme["text_color"]))
        palette.setColor(QPalette.Text, QColor(theme["text_color"]))
        palette.setColor(QPalette.Button, QColor(theme["accent_primary"]))
        palette.setColor(QPalette.ButtonText, QColor(theme["text_color"]))
        palette.setColor(QPalette.BrightText, QColor(theme["accent_success"]))
        palette.setColor(QPalette.Link, QColor(theme["accent_primary"]))
        palette.setColor(QPalette.Highlight, QColor(theme["accent_primary"]))
        palette.setColor(QPalette.HighlightedText, QColor(theme["text_color"]))

        # Disabled colors
        palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(theme["muted_text"]))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(theme["muted_text"]))
        palette.setColor(QPalette.Disabled, QPalette.Button, QColor(theme["background_mid"]))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(theme["muted_text"]))
        palette.setColor(QPalette.Disabled, QPalette.Base, QColor(theme["background_dark"]))

        # Apply the palette
        app.setPalette(palette)

        # Set the stylesheet for custom widgets
        app.setStyleSheet(f"""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme["background_dark"]},
                    stop:1 {theme["background_mid"]});
            }}

            QWidget {{
                background: transparent;
            }}

            QFrame {{
                background: {theme["sidebar_bg"]};
                border-radius: 8px;
                border: 1px solid {theme["border_color"]};
            }}

            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme["accent_primary"]},
                    stop:1 {theme["accent_secondary"]});
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                color: {theme["background_dark"]};
                font-weight: bold;
            }}

            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme["accent_secondary"]},
                    stop:1 {theme["accent_primary"]});
            }}

            QTabWidget {{
                background: transparent;
            }}

            QTabWidget::pane {{
                border: none;
                background: {theme["sidebar_bg"]};
                border-radius: 8px;
                margin-top: -1px;
            }}

            QTabBar {{
                background: transparent;
            }}

            QTabBar::tab {{
                background: transparent;
                color: {theme["muted_text"]};
                padding: 8px 20px;
                border: none;
                border-radius: 4px 4px 0 0;
                margin-right: 2px;
                font-weight: 500;
            }}

            QTabBar::tab:hover {{
                background: {theme["tab_hover"]};
                color: {theme["text_color"]};
            }}

            QTabBar::tab:selected {{
                color: {theme["tab_selected"]};
                border-bottom: 2px solid {theme["tab_selected"]};
                background: {theme["background_mid"]};
            }}

            QScrollBar:vertical {{
                border: none;
                background: {theme["background_dark"]};
                width: 8px;
                margin: 0px;
            }}

            QScrollBar::handle:vertical {{
                background: {theme["accent_primary"]};
                border-radius: 4px;
                min-height: 20px;
            }}

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}

            QLineEdit, QSpinBox, QComboBox {{
                background: {theme["background_dark"]};
                border: 1px solid {theme["border_color"]};
                border-radius: 4px;
                padding: 8px;
                color: {theme["text_color"]};
                selection-background-color: {theme["accent_primary"]};
            }}

            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
                border: 1px solid {theme["accent_primary"]};
            }}

            QLabel {{
                color: {theme["text_color"]};
            }}

            QCheckBox {{
                color: {theme["text_color"]};
                spacing: 8px;
            }}

            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {theme["accent_primary"]};
                border-radius: 4px;
                background: {theme["background_dark"]};
            }}

            QCheckBox::indicator:checked {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme["accent_primary"]},
                    stop:1 {theme["accent_secondary"]});
            }}

            QGroupBox {{
                border: 1px solid {theme["border_color"]};
                border-radius: 4px;
                margin-top: 1em;
                padding-top: 1em;
                color: {theme["text_color"]};
            }}

            QMenuBar {{
                background: transparent;
                color: {theme["text_color"]};
                padding: 4px;
            }}

            QMenuBar::item {{
                background: transparent;
                padding: 4px 12px;
                border-radius: 4px;
            }}

            QMenuBar::item:selected {{
                background: {theme["tab_hover"]};
            }}

            QMenu {{
                background: {theme["background_mid"]};
                border: 1px solid {theme["border_color"]};
                border-radius: 4px;
                padding: 4px;
            }}

            QMenu::item {{
                padding: 4px 20px;
                color: {theme["text_color"]};
            }}

            QMenu::item:selected {{
                background: {theme["tab_hover"]};
            }}
        """)

    def _get_button_text_color(self):
        if self.theme_name == self.LIGHT:
            return self.themes[self.theme_name]["background_dark"]
        return self.themes[self.theme_name]["background_dark"]
