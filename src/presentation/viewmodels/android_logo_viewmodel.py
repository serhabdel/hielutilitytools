from PySide6.QtCore import QObject, Signal
from pathlib import Path
from src.infrastructure.image_services.android_logo_generator import AndroidLogoGenerator


class AndroidLogoViewModel(QObject):
    progress_updated = Signal(int)  # Progress percentage (0-100)
    generation_completed = Signal(dict)  # Dictionary of generated paths
    error_occurred = Signal(str)  # Error message
    
    def __init__(self):
        super().__init__()
        self._generator = AndroidLogoGenerator()
    
    def generate_android_icons(self, input_path: str, output_dir: str = None) -> None:
        """
        Generate Android app icons from input image.
        
        Args:
            input_path: Path to input image file
            output_dir: Optional output directory path
        """
        try:
            if not input_path:
                raise ValueError("Please select an image file")
            
            input_path = Path(input_path)
            if not input_path.exists():
                raise FileNotFoundError(f"File not found: {input_path}")
            
            # Convert image to Android icons with progress tracking
            output_paths = self._generator.generate_icons(
                input_path=input_path,
                output_base_dir=output_dir,
                progress_callback=self.progress_updated.emit
            )
            
            # Emit completion signal with output paths
            self.generation_completed.emit(output_paths)
            
        except Exception as e:
            error_msg = f"Android Icon Generation Error: {str(e)}"
            self.error_occurred.emit(error_msg)
