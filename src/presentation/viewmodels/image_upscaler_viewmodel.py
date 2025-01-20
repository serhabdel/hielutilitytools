from PySide6.QtCore import QObject, Signal
from pathlib import Path
from src.infrastructure.image_services.image_upscaler import ImageUpscaler

class ImageUpscalerViewModel(QObject):
    processing_completed = Signal(str)  # Output file path
    error_occurred = Signal(str)  # Error message
    
    def __init__(self):
        super().__init__()
        self._processor = ImageUpscaler()
    
    def upscale_image(self, 
                     input_path: str, 
                     scale_factor: int = 2,
                     output_path: str = None) -> None:
        """
        Upscale an image using super-resolution.
        
        Args:
            input_path: Path to the input image
            scale_factor: Upscaling factor (2 or 4)
            output_path: Optional output path
        """
        try:
            # Validate input
            if not input_path:
                raise ValueError("Please select an image")
            
            input_path = Path(input_path)
            if not input_path.exists():
                raise FileNotFoundError(f"File not found: {input_path}")
            
            if not input_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp']:
                raise ValueError("Selected file must be an image")
            
            if scale_factor not in [2, 4]:
                raise ValueError("Scale factor must be 2 or 4")
            
            # Process image
            output_file = self._processor.process(
                input_path=input_path,
                output_path=output_path,
                scale_factor=scale_factor
            )
            
            self.processing_completed.emit(output_file)
            
        except Exception as e:
            self.error_occurred.emit(str(e)) 