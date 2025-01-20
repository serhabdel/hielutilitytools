from PySide6.QtCore import QObject, Signal
from src.infrastructure.image_services.logo_converter import LogoConverter

class LogoConverterViewModel(QObject):
    conversion_completed = Signal(str)
    error_occurred = Signal(str)

    def convert_logo(self, input_path):
        """
        Convert 500x500 PNG to ICO
        
        Args:
            input_path: Path to input PNG file
        """
        try:
            # Perform logo conversion
            result_path = LogoConverter.convert_logo(input_path)

            # Emit conversion completed signal
            self.conversion_completed.emit(result_path)
            return result_path

        except Exception as e:
            # Emit error signal if conversion fails
            error_msg = f"Logo Conversion Error: {str(e)}"
            self.error_occurred.emit(error_msg)
            raise
