from abc import ABC, abstractmethod
from typing import List, Optional, Union
from pathlib import Path

class FileConverter(ABC):
    @abstractmethod
    def convert(self, input_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None, **kwargs) -> Union[str, List[str]]:
        """
        Convert a file from one format to another.
        
        Args:
            input_path: Path to the input file
            output_path: Optional path for the output file/directory
            **kwargs: Additional conversion parameters
            
        Returns:
            Path or list of paths to the converted file(s)
        """
        pass 