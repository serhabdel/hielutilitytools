from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFileDialog, QProgressBar,
    QMessageBox, QFrame, QSpinBox, QComboBox, QCheckBox
)
from PySide6.QtCore import Qt
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
from urllib.parse import urljoin, urlparse
from utils.app_theme import AppTheme

class WebScraper(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme = AppTheme()
        self.setup_ui()
        self.driver = None
        self.visited_content = {}

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Web Content Converter")
        title.setStyleSheet("font-size: 24px; color: white; margin-bottom: 20px;")
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

        # URL Input
        url_label = QLabel("Website URL")
        url_label.setStyleSheet("color: #888; font-size: 12px;")
        content_layout.addWidget(url_label)

        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter website URL...")
        self.url_input.setStyleSheet("""
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
        url_layout.addWidget(self.url_input)
        content_layout.addLayout(url_layout)

        # Output Directory (Optional)
        output_layout = QHBoxLayout()
        self.use_custom_output = QCheckBox("Custom Output Directory")
        self.use_custom_output.setStyleSheet("""
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
        output_layout.addWidget(self.use_custom_output)
        content_layout.addLayout(output_layout)

        # Output Directory Widget
        self.output_widget = QWidget()
        output_widget_layout = QVBoxLayout(self.output_widget)
        output_widget_layout.setContentsMargins(0, 0, 0, 0)

        output_label = QLabel("Output Directory")
        output_label.setStyleSheet("color: #888; font-size: 12px;")
        output_widget_layout.addWidget(output_label)

        path_layout = QHBoxLayout()
        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Choose output location...")
        self.output_path.setStyleSheet(self.url_input.styleSheet())
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
        browse_btn.clicked.connect(self.browse_output)
        path_layout.addWidget(self.output_path)
        path_layout.addWidget(browse_btn)
        output_widget_layout.addLayout(path_layout)

        content_layout.addWidget(self.output_widget)
        self.output_widget.hide()

        self.use_custom_output.toggled.connect(self.output_widget.setVisible)

        # Options
        options_label = QLabel("Options")
        options_label.setStyleSheet("color: #888; font-size: 12px;")
        content_layout.addWidget(options_label)

        # Output Format
        format_layout = QHBoxLayout()
        format_label = QLabel("Output Format:")
        format_label.setStyleSheet("color: white;")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Markdown", "HTML"])
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
                border-top: 5px solid #4a90e2;
                margin-right: 8px;
            }
        """)
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()
        content_layout.addLayout(format_layout)

        # Depth Control
        depth_layout = QHBoxLayout()
        depth_label = QLabel("Crawl Depth:")
        depth_label.setStyleSheet("color: white;")
        self.depth_spin = QSpinBox()
        self.depth_spin.setMinimum(0)
        self.depth_spin.setMaximum(5)
        self.depth_spin.setValue(0)
        self.depth_spin.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                background: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: white;
            }
            QSpinBox:hover {
                border: 1px solid #4a90e2;
            }
        """)
        depth_layout.addWidget(depth_label)
        depth_layout.addWidget(self.depth_spin)
        depth_layout.addStretch()
        content_layout.addLayout(depth_layout)

        # Additional Options
        self.wait_load = QCheckBox("Wait for JavaScript content")
        self.wait_load.setStyleSheet("""
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
        content_layout.addWidget(self.wait_load)

        self.single_file = QCheckBox("Save all content in a single file")
        self.single_file.setStyleSheet(self.wait_load.styleSheet())
        content_layout.addWidget(self.single_file)

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

        # Convert Button
        convert_btn = QPushButton("Convert")
        convert_btn.setStyleSheet("""
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
        convert_btn.clicked.connect(self.start_conversion)
        content_layout.addWidget(convert_btn)

        layout.addWidget(content_frame)
        layout.addStretch()

    def browse_output(self):
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            ""
        )
        if dir_path:
            self.output_path.setText(dir_path)

    def initialize_selenium(self):
        if self.driver is None and self.wait_load.isChecked():
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )

    def cleanup_selenium(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def get_page_content(self, url):
        if self.wait_load.isChecked():
            self.driver.get(url)
            time.sleep(2)  # Wait for JavaScript content
            return self.driver.page_source
        else:
            response = requests.get(url)
            return response.text

    def convert_to_markdown(self, html_content):
        return markdownify(html_content, heading_style="ATX")

    def clean_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.decompose()
        # Make all links absolute
        for a in soup.find_all('a', href=True):
            a['href'] = urljoin(self.base_url, a['href'])
        # Make all images absolute
        for img in soup.find_all('img', src=True):
            img['src'] = urljoin(self.base_url, img['src'])
        return str(soup)

    def get_links(self, url, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        base_url = urlparse(url).scheme + "://" + urlparse(url).netloc
        links = []

        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)

            # Only include links from the same domain
            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                links.append(full_url)

        return list(set(links))  # Remove duplicates

    def crawl_and_convert(self, url, depth, visited=None):
        if visited is None:
            visited = set()

        if depth < 0 or url in visited:
            return

        visited.add(url)
        try:
            html_content = self.get_page_content(url)

            # Store content based on format
            if self.format_combo.currentText() == "Markdown":
                content = self.convert_to_markdown(html_content)
            else:  # HTML
                content = self.clean_html(html_content)

            if self.single_file.isChecked():
                # Add to content dictionary with URL as key
                self.visited_content[url] = content
            else:
                # Save individual file
                output_dir = self.get_output_directory()
                filename = os.path.join(
                    output_dir,
                    f"{urlparse(url).path.strip('/').replace('/', '_') or 'index'}"
                    f".{'md' if self.format_combo.currentText() == 'Markdown' else 'html'}"
                )
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)

            # Crawl linked pages if depth > 0
            if depth > 0:
                links = self.get_links(url, html_content)
                for link in links:
                    self.crawl_and_convert(link, depth - 1, visited)

        except Exception as e:
            print(f"Error processing {url}: {str(e)}")

    def get_default_output_dir(self):
        # Get the domain name from the URL
        domain = urlparse(self.url_input.text()).netloc
        # Create a sanitized folder name
        folder_name = domain.replace('.', '_')
        # Get the user's documents folder
        documents_dir = os.path.expanduser('~/Documents')
        # Create the converter output directory
        converter_dir = os.path.join(documents_dir, 'Converter')
        # Create the web content directory
        web_content_dir = os.path.join(converter_dir, 'WebContent')
        # Create the final output directory with timestamp
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join(web_content_dir, f'{folder_name}_{timestamp}')
        return output_dir

    def get_output_directory(self):
        if self.use_custom_output.isChecked():
            return self.output_path.text()
        return self.get_default_output_dir()

    def save_single_file(self, output_dir):
        format_type = self.format_combo.currentText()
        filename = os.path.join(
            output_dir,
            f"website_content.{'md' if format_type == 'Markdown' else 'html'}"
        )

        with open(filename, 'w', encoding='utf-8') as f:
            if format_type == "HTML":
                # Create a proper HTML document
                f.write('<!DOCTYPE html>\n<html>\n<head>\n')
                f.write('<meta charset="UTF-8">\n')
                f.write(f'<title>Scraped Content from {self.base_url}</title>\n')
                f.write('</head>\n<body>\n')

            # Write content for each URL
            for url, content in self.visited_content.items():
                if format_type == "Markdown":
                    f.write(f"\n\n## Content from {url}\n\n")
                else:  # HTML
                    f.write(f'\n<h2>Content from {url}</h2>\n')
                f.write(content)

            if format_type == "HTML":
                f.write('\n</body>\n</html>')

    def start_conversion(self):
        url = self.url_input.text()

        if not url:
            QMessageBox.warning(self, "Error", "Please enter a URL")
            return

        if self.use_custom_output.isChecked() and not self.output_path.text():
            QMessageBox.warning(self, "Error", "Please select output directory")
            return

        try:
            self.progress.show()
            self.progress.setValue(0)

            # Get output directory (either custom or default)
            output_dir = self.get_output_directory()

            # Create output directory structure
            os.makedirs(output_dir, exist_ok=True)

            # Store base URL for making absolute links
            self.base_url = url

            # Clear previous content if using single file
            if self.single_file.isChecked():
                self.visited_content.clear()

            # Initialize Selenium if needed
            self.initialize_selenium()

            # Start crawling and converting
            self.crawl_and_convert(url, self.depth_spin.value())

            # Save single file if selected
            if self.single_file.isChecked():
                self.save_single_file(output_dir)

            self.progress.setValue(100)
            self.progress.hide()

            QMessageBox.information(
                self,
                "Success",
                f"Website content converted successfully!\nOutput directory: {output_dir}"
            )

        except Exception as e:
            self.progress.hide()
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

        finally:
            self.cleanup_selenium()

    def closeEvent(self, event):
        self.cleanup_selenium()
        super().closeEvent(event)
