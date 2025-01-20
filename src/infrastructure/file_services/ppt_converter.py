from pathlib import Path
from typing import Optional, Union
import comtypes.client
import win32com.client
from pptx import Presentation
from src.domain.interfaces.file_converter import FileConverter

class PPTConverter(FileConverter):
    def convert(self, 
                input_path: Union[str, Path], 
                output_path: Optional[Union[str, Path]] = None,
                **kwargs) -> str:
        """
        Convert between PPT/PPTX and PDF formats.
        
        Args:
            input_path: Path to the input file (PPT/PPTX or PDF)
            output_path: Optional output file path
            **kwargs: Additional parameters
        
        Returns:
            Path to the converted file
        """
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"File not found: {input_path}")
        
        input_format = input_path.suffix.lower()
        if input_format not in ['.ppt', '.pptx', '.pdf']:
            raise ValueError(f"Unsupported file format: {input_format}")
        
        # Determine output format and path
        is_to_pdf = input_format in ['.ppt', '.pptx']
        output_format = '.pdf' if is_to_pdf else '.pptx'
        
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}{output_format}"
        else:
            output_path = Path(output_path)
            if not output_path.suffix.lower() == output_format:
                output_path = output_path.with_suffix(output_format)
        
        if is_to_pdf:
            # PPT/PPTX to PDF
            powerpoint = win32com.client.Dispatch("Powerpoint.Application")
            try:
                deck = powerpoint.Presentations.Open(str(input_path.absolute()))
                deck.SaveAs(str(output_path.absolute()), 32)  # 32 is the PDF format code
                deck.Close()
            finally:
                powerpoint.Quit()
        else:
            # PDF to PPTX (Note: This is a placeholder as direct PDF to PPT conversion
            # is complex and might require OCR or third-party services)
            raise NotImplementedError("PDF to PPT conversion not yet implemented")
        
        return str(output_path) 