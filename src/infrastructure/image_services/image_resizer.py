from pathlib import Path
from typing import Optional, Union, Tuple, Dict, Callable
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor
from src.domain.interfaces.image_processor import ImageProcessor

class ImageResizer(ImageProcessor):
    ANDROID_ICON_SIZES = {
        'mipmap-mdpi': (48, 48),
        'mipmap-hdpi': (72, 72),
        'mipmap-xhdpi': (96, 96),
        'mipmap-xxhdpi': (144, 144),
        'mipmap-xxxhdpi': (192, 192),
        'playstore': (512, 512)
    }
    
    def process(self, 
                input_path: Union[str, Path],
                output_path: Optional[Union[str, Path]] = None,
                size: Optional[Tuple[int, int]] = None,
                progress_callback: Optional[Callable[[int], None]] = None,
                **kwargs) -> Union[str, Dict[str, str]]:
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Image file not found: {input_path}")
        
        # Load image with optimizations
        with Image.open(input_path) as img:
            # Convert color mode based on requirements
            color_mode = kwargs.get('color_mode', 'RGBA')
            if img.mode != color_mode:
                img = img.convert(color_mode)
            
            # Apply optimizations
            quality = kwargs.get('quality', 95)
            optimize = kwargs.get('optimize', True)
            
            if kwargs.get('android_mode', False):
                return self._create_android_icons(
                    img, input_path, progress_callback, quality, optimize
                )
            
            if size is None:
                raise ValueError("Size must be specified for regular resizing")
            
            maintain_aspect = kwargs.get('maintain_aspect', True)
            resample = self._get_resample_mode(kwargs.get('resample', 'lanczos'))
            resized_img = self._resize_image(img, size, maintain_aspect, resample)
            
            if output_path is None:
                output_path = input_path.parent / f"{input_path.stem}_resized{input_path.suffix}"
            output_path = Path(output_path)
            
            # Save with optimizations
            self._save_optimized(resized_img, output_path, quality, optimize, color_mode)
            if progress_callback:
                progress_callback(100)
                
            return str(output_path)
    
    def _resize_image(self, 
                     img: Image.Image, 
                     size: Tuple[int, int], 
                     maintain_aspect: bool = True,
                     resample: int = Image.Resampling.LANCZOS) -> Image.Image:
        if maintain_aspect:
            img.thumbnail(size, resample)
            return img
        return img.resize(size, resample)
    
    def _get_resample_mode(self, mode: str) -> int:
        modes = {
            'nearest': Image.Resampling.NEAREST,
            'box': Image.Resampling.BOX,
            'bilinear': Image.Resampling.BILINEAR,
            'hamming': Image.Resampling.HAMMING,
            'bicubic': Image.Resampling.BICUBIC,
            'lanczos': Image.Resampling.LANCZOS
        }
        return modes.get(mode.lower(), Image.Resampling.LANCZOS)
    
    def _save_optimized(self, 
                       img: Image.Image, 
                       output_path: Path,
                       quality: int = 95,
                       optimize: bool = True,
                       color_mode: str = 'RGBA') -> None:
        # Use BytesIO for memory efficiency
        with io.BytesIO() as bio:
            img.save(bio, 
                    format='PNG' if color_mode == 'RGBA' else 'JPEG',
                    quality=quality,
                    optimize=optimize)
            with open(output_path, 'wb') as f:
                f.write(bio.getvalue())
    
    def _create_android_icons(self, 
                            img: Image.Image, 
                            input_path: Path,
                            progress_callback: Optional[Callable[[int], None]] = None,
                            quality: int = 95,
                            optimize: bool = True) -> Dict[str, str]:
        output_paths = {}
        base_dir = input_path.parent / f"{input_path.stem}_android_icons"
        base_dir.mkdir(exist_ok=True)
        
        total_icons = len(self.ANDROID_ICON_SIZES)
        completed = 0
        
        def process_icon(args):
            density, size = args
            density_dir = base_dir / density
            density_dir.mkdir(exist_ok=True)
            
            resized = self._resize_image(img.copy(), size)
            output_path = density_dir / f"ic_launcher.png"
            self._save_optimized(resized, output_path, quality, optimize)
            
            nonlocal completed
            completed += 1
            if progress_callback:
                progress_callback(int((completed / total_icons) * 100))
            
            return density, str(output_path)
        
        # Process icons in parallel
        with ThreadPoolExecutor() as executor:
            results = executor.map(process_icon, self.ANDROID_ICON_SIZES.items())
            output_paths = dict(results)
        
        return output_paths