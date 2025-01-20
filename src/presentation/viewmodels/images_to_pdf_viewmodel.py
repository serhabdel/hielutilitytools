from PySide6.QtCore import QObject, Signal
from pathlib import Path
from typing import List
from src.infrastructure.file_services.images_to_pdf_converter import ImagesToPDFConverter

class ImagesToPDFViewModel(QObject):
    conversion_completed = Signal(str)  # Output PDF path
    error_occurred = Signal(str)  # Error message
    
    def __init__(self):
        super().__init__()
        self._converter = ImagesToPDFConverter()
    
    def convert_images(self, image_paths: List[str], output_path: str = None) -> None:
        """
        Convert images to PDF.
        
        Args:
            image_paths: List of paths to image files
            output_path: Optional output PDF path
        """
        try:
            # Validate input
            if not image_paths:
                raise ValueError("Please select at least one image")
            
            # Convert images to PDF
            output_file = self._converter.convert(
                input_path=image_paths,
                output_path=output_path if output_path else None
            )
            
            self.conversion_completed.emit(output_file)
            
        except Exception as e:
            self.error_occurred.emit(str(e)) 