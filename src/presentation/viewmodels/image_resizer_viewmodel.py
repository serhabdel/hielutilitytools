from PySide6.QtCore import QObject, Signal
from pathlib import Path
from src.infrastructure.image_services.image_resizer import ImageResizer

class ImageResizerViewModel(QObject):
    resize_completed = Signal(str)
    android_resize_completed = Signal(dict)
    progress_updated = Signal(int)
    error_occurred = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._resizer = ImageResizer()
    
    def resize_image(self, input_path: str, width: int, height: int, 
                    output_path: str = None, maintain_aspect: bool = True,
                    color_mode: str = 'RGBA', quality: int = 95,
                    resample: str = 'lanczos') -> None:
        try:
            if not input_path:
                raise ValueError("Please select an image file")
            
            input_path = Path(input_path)
            if not input_path.exists():
                raise FileNotFoundError(f"File not found: {input_path}")
            
            output_path = self._resizer.process(
                input_path=input_path,
                output_path=output_path,
                size=(width, height),
                progress_callback=self.progress_updated.emit,
                maintain_aspect=maintain_aspect,
                color_mode=color_mode,
                quality=quality,
                resample=resample,
                optimize=True
            )
            
            self.resize_completed.emit(output_path)
            
        except Exception as e:
            self.error_occurred.emit(str(e))
    
    def create_android_icons(self, input_path: str) -> None:
        try:
            if not input_path:
                raise ValueError("Please select an image file")
            
            input_path = Path(input_path)
            if not input_path.exists():
                raise FileNotFoundError(f"File not found: {input_path}")
            
            output_paths = self._resizer.process(
                input_path=input_path,
                android_mode=True,
                progress_callback=self.progress_updated.emit,
                quality=95,
                optimize=True
            )
            
            self.android_resize_completed.emit(output_paths)
            
        except Exception as e:
            self.error_occurred.emit(str(e))
