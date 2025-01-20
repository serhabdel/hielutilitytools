from pathlib import Path
from typing import Optional, Union, Tuple, Callable
from rembg import remove, new_session
from PIL import Image
import io
from src.domain.interfaces.image_processor import ImageProcessor

class BackgroundRemover(ImageProcessor):
    def __init__(self):
        self.session = new_session("u2net")  # Cache the model for better performance
    
    def process(self, 
                input_path: Union[str, Path],
                output_path: Optional[Union[str, Path]] = None,
                size: Optional[Tuple[int, int]] = None,
                progress_callback: Optional[Callable[[int], None]] = None,
                **kwargs) -> str:
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Image file not found: {input_path}")
        
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}_nobg.png"
        output_path = Path(output_path)
        
        if progress_callback:
            progress_callback(10)  # Model loading
        
        # Load and preprocess image
        with Image.open(input_path) as input_img:
            # Convert to RGBA if needed
            if input_img.mode != 'RGBA':
                input_img = input_img.convert('RGBA')
            
            if progress_callback:
                progress_callback(30)  # Image preprocessing
            
            # Apply background removal with additional options
            output_img = remove(
                input_img,
                session=self.session,
                alpha_matting=kwargs.get('alpha_matting', True),
                alpha_matting_foreground_threshold=kwargs.get('foreground_threshold', 240),
                alpha_matting_background_threshold=kwargs.get('background_threshold', 10),
                alpha_matting_erode_size=kwargs.get('erode_size', 10)
            )
            
            if progress_callback:
                progress_callback(80)  # Background removal complete
            
            # Post-process and save
            if size:
                output_img = output_img.resize(size, Image.Resampling.LANCZOS)
            
            # Optimize output
            with io.BytesIO() as bio:
                output_img.save(bio, 
                              format='PNG',
                              optimize=True,
                              quality=kwargs.get('quality', 95))
                with open(output_path, 'wb') as f:
                    f.write(bio.getvalue())
            
            if progress_callback:
                progress_callback(100)
            
            return str(output_path)