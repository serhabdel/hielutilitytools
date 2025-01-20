from pathlib import Path
from typing import List, Optional, Union
import img2pdf
from PIL import Image
from src.domain.interfaces.file_converter import FileConverter

class ImagesToPDFConverter(FileConverter):
    def convert(self, 
                input_path: Union[str, Path, List[str], List[Path]], 
                output_path: Optional[Union[str, Path]] = None,
                **kwargs) -> str:
        """
        Convert images to PDF.
        
        Args:
            input_path: Path to image file or list of image paths
            output_path: Optional output PDF path
            **kwargs: Additional parameters
        
        Returns:
            Path to the generated PDF file
        """
        # Handle input paths
        if isinstance(input_path, (str, Path)):
            input_paths = [Path(input_path)]
        else:
            input_paths = [Path(p) for p in input_path]
        
        # Validate input files
        for path in input_paths:
            if not path.exists():
                raise FileNotFoundError(f"Image file not found: {path}")
            if path.suffix.lower() not in ['.png', '.jpg', '.jpeg', '.bmp']:
                raise ValueError(f"Unsupported image format: {path}")
        
        # Create output path if not specified
        if output_path is None:
            # Use the first image's name as base
            output_path = input_paths[0].parent / f"{input_paths[0].stem}_combined.pdf"
        output_path = Path(output_path)
        
        # Convert images to PDF
        with open(str(output_path), "wb") as f:
            # Convert images to RGB if necessary
            image_files = []
            for img_path in input_paths:
                with Image.open(img_path) as img:
                    if img.mode != 'RGB':
                        rgb_img = img.convert('RGB')
                        temp_path = img_path.parent / f"temp_{img_path.name}"
                        rgb_img.save(temp_path)
                        image_files.append(temp_path)
                    else:
                        image_files.append(img_path)
            
            # Create PDF
            f.write(img2pdf.convert([str(p) for p in image_files]))
            
            # Clean up temporary files
            for path in image_files:
                if path.name.startswith('temp_'):
                    path.unlink()
        
        return str(output_path) 