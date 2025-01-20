from PySide6.QtCore import QObject, Signal
from pathlib import Path
from src.infrastructure.file_services.pdf_converter import PDFToImageConverter

class PDFToImagesViewModel(QObject):
    progress_updated = Signal(int)
    conversion_completed = Signal(list)
    error_occurred = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._converter = PDFToImageConverter()
    
    def convert_pdf(self, input_path: str) -> None:
        try:
            if not input_path:
                raise ValueError("Please select a PDF file")
            
            input_path = Path(input_path)
            if not input_path.exists():
                raise FileNotFoundError(f"File not found: {input_path}")
            
            if not input_path.suffix.lower() == '.pdf':
                raise ValueError("Selected file is not a PDF")
            
            # Convert PDF to images with progress tracking
            output_files = self._converter.convert(
                input_path=input_path,
                progress_callback=self.progress_updated.emit
            )
            
            # Emit conversion completed signal with output files
            self.conversion_completed.emit(output_files)
        
        except Exception as e:
            # Emit error signal if conversion fails
            error_msg = f"PDF to Images Conversion Error: {str(e)}"
            self.error_occurred.emit(error_msg)
