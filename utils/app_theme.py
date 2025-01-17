from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor, QLinearGradient, QBrush
from PySide6.QtCore import Qt

class EnterpriseTheme:
    @staticmethod
    def apply_theme(app: QApplication):
        # Create the base palette
        palette = QPalette()
        
        # Tokyo Night colors
        background_dark = "#1a1b26"     # Darkest background
        background_mid = "#24283b"      # Mid background
        background_light = "#2f3549"    # Light background
        accent_primary = "#7aa2f7"      # Bright blue
        accent_secondary = "#bb9af7"    # Purple
        accent_success = "#9ece6a"      # Green
        text_color = "#c0caf5"          # Light blue text
        muted_text = "#565f89"          # Muted text
        border_color = "#292e42"        # Border color
        
        # Create gradients
        main_gradient = QLinearGradient(0, 0, 0, 400)
        main_gradient.setColorAt(0.0, QColor(background_dark))
        main_gradient.setColorAt(0.5, QColor(background_mid))
        main_gradient.setColorAt(1.0, QColor(background_light))
        
        accent_gradient = QLinearGradient(0, 0, 0, 40)
        accent_gradient.setColorAt(0.0, QColor(accent_primary))
        accent_gradient.setColorAt(1.0, QColor(accent_secondary))

        disabled_gradient = QLinearGradient(0, 0, 0, 40)
        disabled_gradient.setColorAt(0.0, QColor(muted_text))
        disabled_gradient.setColorAt(1.0, QColor(background_mid))

        # Set color roles
        palette.setColor(QPalette.Window, QColor(background_dark))
        palette.setBrush(QPalette.Window, QBrush(main_gradient))
        palette.setColor(QPalette.WindowText, QColor(text_color))
        palette.setColor(QPalette.Base, QColor(background_mid))
        palette.setColor(QPalette.AlternateBase, QColor(background_light))
        palette.setColor(QPalette.ToolTipBase, QColor(background_mid))
        palette.setColor(QPalette.ToolTipText, QColor(text_color))
        palette.setColor(QPalette.Text, QColor(text_color))
        palette.setColor(QPalette.Button, QColor(accent_primary))
        palette.setColor(QPalette.ButtonText, QColor(text_color))
        palette.setColor(QPalette.BrightText, QColor(accent_success))
        palette.setColor(QPalette.Link, QColor(accent_primary))
        palette.setColor(QPalette.Highlight, QColor(accent_primary))
        palette.setColor(QPalette.HighlightedText, QColor(text_color))

        # Disabled colors
        palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(muted_text))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(muted_text))
        palette.setColor(QPalette.Disabled, QPalette.Button, QColor(background_mid))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(muted_text))
        palette.setColor(QPalette.Disabled, QPalette.Base, QColor(background_dark))

        # Apply the palette
        app.setPalette(palette)

        # Set the stylesheet for custom widgets
        app.setStyleSheet(f"""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {background_dark},
                    stop:0.5 {background_mid},
                    stop:1 {background_light});
            }}
            
            QWidget {{
                background: transparent;
            }}
            
            QFrame {{
                background: rgba(26, 27, 38, 180);
                border-radius: 8px;
                border: 1px solid {border_color};
            }}
            
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {accent_primary},
                    stop:1 {accent_secondary});
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                color: {text_color};
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {accent_secondary},
                    stop:1 {accent_primary});
            }}
            
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {accent_secondary},
                    stop:0.5 {accent_primary},
                    stop:1 {accent_secondary});
            }}
            
            QPushButton:disabled {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {background_mid},
                    stop:1 {background_dark});
                color: {muted_text};
            }}
            
            QLineEdit, QSpinBox, QComboBox {{
                background: rgba(36, 40, 59, 180);
                border: 1px solid {border_color};
                border-radius: 4px;
                padding: 8px;
                color: {text_color};
            }}
            
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
                border: 1px solid {accent_primary};
                background: rgba(36, 40, 59, 220);
            }}
            
            QProgressBar {{
                border: 1px solid {border_color};
                border-radius: 4px;
                text-align: center;
                background: rgba(36, 40, 59, 180);
            }}
            
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {accent_primary},
                    stop:1 {accent_secondary});
            }}
            
            QScrollBar:vertical {{
                border: none;
                background: rgba(36, 40, 59, 180);
                width: 10px;
                margin: 0;
            }}
            
            QScrollBar::handle:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {accent_primary},
                    stop:1 {accent_secondary});
                min-height: 20px;
                border-radius: 5px;
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            
            QTabWidget::pane {{
                border: none;
                background: transparent;
            }}
            
            QTabBar::tab {{
                background: rgba(36, 40, 59, 180);
                color: {text_color};
                padding: 8px 16px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }}
            
            QTabBar::tab:selected {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {accent_primary},
                    stop:1 {accent_secondary});
            }}
            
            QTabBar::tab:hover:!selected {{
                background: rgba(122, 162, 247, 120);
            }}
            
            QCheckBox {{
                spacing: 8px;
                color: {text_color};
            }}
            
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {accent_primary};
                border-radius: 4px;
                background: rgba(36, 40, 59, 180);
            }}
            
            QCheckBox::indicator:checked {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {accent_primary},
                    stop:1 {accent_secondary});
            }}
            
            QLabel {{
                color: {text_color};
            }}
            
            QGroupBox {{
                border: 1px solid {border_color};
                border-radius: 4px;
                margin-top: 1em;
                padding-top: 1em;
                color: {text_color};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }}
            
            QMenuBar {{
                background: transparent;
                color: {text_color};
            }}
            
            QMenuBar::item {{
                background: transparent;
                padding: 4px 12px;
            }}
            
            QMenuBar::item:selected {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {accent_primary},
                    stop:1 {accent_secondary});
                border-radius: 4px;
            }}
            
            QMenu {{
                background: {background_mid};
                border: 1px solid {border_color};
                border-radius: 4px;
            }}
            
            QMenu::item {{
                padding: 8px 32px;
                color: {text_color};
            }}
            
            QMenu::item:selected {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {accent_primary},
                    stop:1 {accent_secondary});
            }}
            
            QToolTip {{
                background: {background_mid};
                border: 1px solid {border_color};
                border-radius: 4px;
                padding: 4px;
                color: {text_color};
            }}
        """)
