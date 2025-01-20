from PIL import Image
from pathlib import Path
import os
from typing import Union, Optional, Dict, Tuple


class AndroidLogoGenerator:
    """
    Service for generating Android app icons in various densities.
    Supports both mipmap and drawable resources.
    """
    
    ANDROID_SIZES = {
        'mipmap-hdpi': (72, 72),
        'mipmap-mdpi': (48, 48),
        'mipmap-xhdpi': (96, 96),
        'mipmap-xxhdpi': (144, 144),
        'mipmap-xxxhdpi': (192, 192),
        'drawable-mdpi': (48, 48),
        'drawable-hdpi': (72, 72),
        'drawable-xhdpi': (96, 96),
        'drawable-xxhdpi': (144, 144),
        'drawable-xxxhdpi': (192, 192)
    }

    def generate_icons(self, 
                      input_path: Union[str, Path],
                      output_base_dir: Optional[Union[str, Path]] = None,
                      progress_callback: Optional[callable] = None) -> Dict[str, str]:
        """
        Generate Android app icons in various densities.
        
        Args:
            input_path: Path to the input image
            output_base_dir: Optional base directory for output. If None, uses input file's directory
            progress_callback: Optional callback for progress updates (0-100)
            
        Returns:
            Dictionary mapping density folders to generated icon paths
        """
        try:
            input_path = Path(input_path)
            if not input_path.exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")
            
            # Set output directory
            if output_base_dir is None:
                output_base_dir = input_path.parent / f"{input_path.stem}_android_res"
            output_base_dir = Path(output_base_dir)
            
            # Create output directory
            output_base_dir.mkdir(parents=True, exist_ok=True)
            
            generated_paths = {}
            total_sizes = len(self.ANDROID_SIZES)
            
            # Open and process image
            with Image.open(input_path) as img:
                for idx, (folder, size) in enumerate(self.ANDROID_SIZES.items(), 1):
                    # Create density-specific folder
                    folder_path = output_base_dir / folder
                    folder_path.mkdir(parents=True, exist_ok=True)
                    
                    # Determine output filename based on resource type
                    output_filename = 'ic_launcher.png' if folder.startswith('mipmap') else 'ic_launcher_foreground.png'
                    output_path = folder_path / output_filename
                    
                    # Resize and save
                    resized_img = img.resize(size, Image.Resampling.LANCZOS)
                    resized_img.save(str(output_path), 'PNG')
                    
                    generated_paths[folder] = str(output_path)
                    
                    # Update progress
                    if progress_callback:
                        progress = int((idx / total_sizes) * 100)
                        progress_callback(progress)
            
            return generated_paths
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate Android icons: {str(e)}")
