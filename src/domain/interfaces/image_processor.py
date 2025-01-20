from abc import ABC, abstractmethod
from typing import Optional, Union, Tuple
from pathlib import Path

class ImageProcessor(ABC):
    @abstractmethod
    def process(self, 
                input_path: Union[str, Path], 
                output_path: Optional[Union[str, Path]] = None,
                size: Optional[Tuple[int, int]] = None,
                **kwargs) -> str:
        """
        Process an image file.
        
        Args:
            input_path: Path to the input image
            output_path: Optional path for the output image
            size: Optional tuple of (width, height) for resizing
            **kwargs: Additional processing parameters
            
        Returns:
            Path to the processed image
        """
        pass 