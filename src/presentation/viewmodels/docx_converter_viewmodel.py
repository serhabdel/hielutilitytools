from PySide6.QtCore import QObject, Signal
from pathlib import Path
from src.infrastructure.file_services.docx_converter import DocxConverter

class DocxConverterViewModel(QObject):
    conversion_completed = Signal(str)  # Output file path
    error_occurred = Signal(str)  # Error message
    
    def __init__(self):
        super().__init__()
        self._converter = DocxConverter()
    
    def convert_file(self, input_path: str, output_path: str = None) -> None:
        """
        Convert between PDF and DOCX formats.
        
        Args:
            input_path: Path to the input file
            output_path: Optional output file path
        """
        try:
            # Validate input
            if not input_path:
                raise ValueError("Please select a file")
            
            input_path = Path(input_path)
            if not input_path.exists():
                raise FileNotFoundError(f"File not found: {input_path}")
            
            if input_path.suffix.lower() not in ['.pdf', '.docx']:
                raise ValueError("Selected file must be PDF or DOCX")
            
            # Convert file
            output_file = self._converter.convert(
                input_path=input_path,
                output_path=output_path if output_path else None
            )
            
            self.conversion_completed.emit(output_file)
            
        except Exception as e:
            self.error_occurred.emit(str(e)) 