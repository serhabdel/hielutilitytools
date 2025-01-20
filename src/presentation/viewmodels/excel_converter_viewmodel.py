from PySide6.QtCore import QObject, Signal
from pathlib import Path
from src.infrastructure.file_services.excel_converter import PDFToExcelConverter

class ExcelConverterViewModel(QObject):
    conversion_completed = Signal(str)  # Output file path
    error_occurred = Signal(str)  # Error message
    
    def __init__(self):
        super().__init__()
        self._converter = PDFToExcelConverter()
    
    def convert_to_excel(self, 
                        input_path: str, 
                        output_path: str = None,
                        pages: str = 'all',
                        multiple_tables: bool = True) -> None:
        """
        Convert PDF tables to Excel.
        
        Args:
            input_path: Path to the PDF file
            output_path: Optional output Excel file path
            pages: Pages to convert (e.g., '1-3' or 'all')
            multiple_tables: Whether to extract multiple tables per page
        """
        try:
            # Validate input
            if not input_path:
                raise ValueError("Please select a PDF file")
            
            input_path = Path(input_path)
            if not input_path.exists():
                raise FileNotFoundError(f"File not found: {input_path}")
            
            if input_path.suffix.lower() != '.pdf':
                raise ValueError("Selected file must be a PDF")
            
            # Convert to Excel
            output_file = self._converter.convert(
                input_path=input_path,
                output_path=output_path if output_path else None,
                pages=pages,
                multiple_tables=multiple_tables
            )
            
            self.conversion_completed.emit(output_file)
            
        except Exception as e:
            self.error_occurred.emit(str(e)) 