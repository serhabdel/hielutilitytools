from pathlib import Path
from typing import Optional, Union, Callable
import logging
import os

from pdf2docx import Converter
from docx2pdf import convert
from src.domain.interfaces.file_converter import FileConverter

class DocxConverter(FileConverter):
    def __init__(self, 
                 log_level: int = logging.INFO):
        """
        Initialize DocxConverter with logging options.
        
        Args:
            log_level: Logging level for conversion process
        """
        logging.basicConfig(level=log_level, 
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def convert(self, 
                input_path: Union[str, Path], 
                output_path: Optional[Union[str, Path]] = None,
                progress_callback: Optional[Callable[[int, str], None]] = None,
                **kwargs) -> str:
        """
        Convert PDF to DOCX or DOCX to PDF with enhanced features.
        
        Args:
            input_path: Path to input file
            output_path: Optional path for output file
            progress_callback: Optional callback for tracking conversion progress
            **kwargs: Additional conversion parameters
        
        Returns:
            Path to the converted file
        """
        try:
            input_path = Path(input_path)
            if not input_path.exists():
                raise FileNotFoundError(f"File not found: {input_path}")
            
            input_format = input_path.suffix.lower()
            if input_format not in ['.pdf', '.docx']:
                raise ValueError(f"Unsupported file format: {input_format}")
            
            output_format = '.docx' if input_format == '.pdf' else '.pdf'
            if output_path is None:
                output_path = input_path.parent / f"{input_path.stem}{output_format}"
            else:
                output_path = Path(output_path)
                if not output_path.suffix.lower() == output_format:
                    output_path = output_path.with_suffix(output_format)
            
            if input_format == '.pdf':
                output_path = self._convert_pdf_to_docx(input_path, output_path, progress_callback)
            else:
                output_path = self._convert_docx_to_pdf(input_path, output_path)
            
            self.logger.info(f"Conversion completed: {input_path} -> {output_path}")
            return str(output_path)
        
        except Exception as e:
            self.logger.error(f"Conversion error: {e}")
            raise

    def _convert_pdf_to_docx(self, 
                               input_path: Path, 
                               output_path: Path, 
                               progress_callback: Optional[Callable[[int, str], None]] = None) -> Path:
        """
        Convert PDF to DOCX using pdf2docx library.
        
        Args:
            input_path: Path to input PDF
            output_path: Path to output DOCX
            progress_callback: Optional callback for tracking progress
        
        Returns:
            Path to the generated DOCX file
        """
        try:
            # Initialize converter
            cv = Converter(str(input_path))
            
            # Convert PDF to DOCX
            cv.convert(str(output_path), start=0, end=None)
            
            # Close the converter
            cv.close()
            
            # Optional progress tracking
            if progress_callback:
                progress_callback(100, "PDF to DOCX conversion complete")
            
            return output_path
        
        except Exception as e:
            self.logger.error(f"PDF to DOCX conversion failed: {e}")
            raise

    def _convert_docx_to_pdf(self, input_path: Path, output_path: Path) -> Path:
        """
        Convert DOCX to PDF with error handling.
        
        Args:
            input_path: Path to input DOCX
            output_path: Path to output PDF
        
        Returns:
            Path to the generated PDF file
        """
        try:
            convert(str(input_path), str(output_path))
            return output_path
        except Exception as e:
            self.logger.error(f"DOCX to PDF conversion failed: {e}")
            raise