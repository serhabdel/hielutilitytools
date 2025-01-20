from pathlib import Path
from typing import List, Optional, Union, Callable
import fitz  # PyMuPDF
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import sys
import shutil
from src.domain.interfaces.file_converter import FileConverter

class PDFToImageConverter(FileConverter):
    def __init__(self):
        pass

    def convert(self, 
                input_path: Union[str, Path], 
                output_path: Optional[Union[str, Path]] = None,
                progress_callback: Optional[Callable[[int], None]] = None,
                **kwargs) -> List[str]:
        try:
            input_path = Path(input_path)
            if not input_path.exists():
                raise FileNotFoundError(f"PDF file not found: {input_path}")
            
            # Simplified: Use a single default DPI
            dpi = 300
            fmt = kwargs.get('fmt', 'png')
            thread_count = min(os.cpu_count() or 1, 4)
            
            if output_path is None:
                output_path = input_path.parent / f"{input_path.stem}_images"
            output_path = Path(output_path)
            output_path.mkdir(parents=True, exist_ok=True)

            pdf_document = fitz.open(str(input_path))
            total_pages = pdf_document.page_count
            converted_images = []

            for page_num in range(total_pages):
                page = pdf_document[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
                
                # Generate output filename
                output_filename = output_path / f"page_{page_num + 1}.{fmt}"
                
                # Save the image
                pix.save(str(output_filename))
                converted_images.append(str(output_filename))
                
                # Update progress if callback is provided
                if progress_callback:
                    progress_callback(int((page_num + 1) / total_pages * 100))
            
            pdf_document.close()
            return converted_images

        except Exception as e:
            raise RuntimeError(f"PDF to Images conversion failed: {e}")