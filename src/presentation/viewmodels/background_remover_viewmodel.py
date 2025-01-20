from PySide6.QtCore import QObject, Signal
from pathlib import Path
from src.infrastructure.image_services.background_remover import BackgroundRemover

class BackgroundRemoverViewModel(QObject):
    processing_completed = Signal(str)
    progress_updated = Signal(int)
    error_occurred = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._remover = BackgroundRemover()
    
    def remove_background(self, input_path: str, output_path: str = None,
                         alpha_matting: bool = True,
                         foreground_threshold: int = 240,
                         background_threshold: int = 10,
                         erode_size: int = 10,
                         quality: int = 95) -> None:
        try:
            if not input_path:
                raise ValueError("Please select an image file")
            
            input_path = Path(input_path)
            if not input_path.exists():
                raise FileNotFoundError(f"File not found: {input_path}")
            
            output_path = self._remover.process(
                input_path=input_path,
                output_path=output_path,
                progress_callback=self.progress_updated.emit,
                alpha_matting=alpha_matting,
                foreground_threshold=foreground_threshold,
                background_threshold=background_threshold,
                erode_size=erode_size,
                quality=quality
            )
            
            self.processing_completed.emit(output_path)
            
        except Exception as e:
            self.error_occurred.emit(str(e))