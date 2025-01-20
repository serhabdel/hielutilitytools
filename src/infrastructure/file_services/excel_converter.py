from pathlib import Path
from typing import Optional, Union, List
import tabula
import pandas as pd
import fitz  # PyMuPDF
from src.domain.interfaces.file_converter import FileConverter

class PDFToExcelConverter(FileConverter):
    def convert(self, 
                input_path: Union[str, Path], 
                output_path: Optional[Union[str, Path]] = None,
                **kwargs) -> str:
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"PDF file not found: {input_path}")
        
        if input_path.suffix.lower() != '.pdf':
            raise ValueError("Input file must be a PDF")
        
        pages = kwargs.get('pages', 'all')
        output_path = self._get_output_path(input_path, output_path)
        
        tables: List[pd.DataFrame] = []
        
        # Try PyMuPDF first
        try:
            pdf_doc = fitz.open(str(input_path))
            for page_num in range(pdf_doc.page_count):
                page = pdf_doc[page_num]
                found_tables = page.get_tables()
                
                if found_tables:
                    for table in found_tables:
                        if len(table) > 0 and len(table[0]) > 0:
                            df = pd.DataFrame(table[1:], columns=table[0])
                            tables.append(df)

            pdf_doc.close()
        except Exception:
            pass

        # If no tables found, try tabula as fallback
        if not tables:
            try:
                tables.extend(tabula.read_pdf(
                    str(input_path),
                    pages=pages,
                    multiple_tables=True,
                    guess=True,
                    lattice=True,
                    stream=True
                ))
            except Exception:
                pass
        
        if not tables:
            raise ValueError("No tables found in the PDF")
        
        # Write tables to Excel with formatting
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for i, df in enumerate(tables, 1):
                sheet_name = f"Table_{i}"
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Auto-adjust column widths
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).apply(len).max(),
                        len(str(col))
                    )
                    worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
        
        return str(output_path)
    
    def _get_output_path(self, input_path: Path, output_path: Optional[Union[str, Path]]) -> Path:
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}.xlsx"
        output_path = Path(output_path)
        if output_path.suffix.lower() != '.xlsx':
            output_path = output_path.with_suffix('.xlsx')
        return output_path