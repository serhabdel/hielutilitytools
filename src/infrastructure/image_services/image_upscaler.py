from pathlib import Path
from typing import Optional, Union, Tuple
import cv2
import numpy as np
from PIL import Image
from src.domain.interfaces.image_processor import ImageProcessor

class ImageUpscaler(ImageProcessor):
    def process(self, 
                input_path: Union[str, Path],
                output_path: Optional[Union[str, Path]] = None,
                size: Optional[Tuple[int, int]] = None,
                **kwargs) -> str:
        """
        Upscale an image using super-resolution.
        
        Args:
            input_path: Path to the input image
            output_path: Optional output image path
            size: Not used (scale factor is used instead)
            **kwargs: Additional parameters including:
                     - scale_factor: Upscaling factor (2 or 4)
        
        Returns:
            Path to the processed image
        """
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Image file not found: {input_path}")
        
        # Get scale factor
        scale_factor = kwargs.get('scale_factor', 2)
        if scale_factor not in [2, 4]:
            raise ValueError("Scale factor must be 2 or 4")
        
        # Create output path if not specified
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}_upscaled{input_path.suffix}"
        output_path = Path(output_path)
        
        # Load image with PIL and convert to RGB
        pil_img = Image.open(input_path)
        if pil_img.mode != 'RGB':
            pil_img = pil_img.convert('RGB')
        
        # Convert to OpenCV format
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        
        # Create super resolution model
        if scale_factor == 2:
            sr = cv2.dnn_superres.DnnSuperResImpl_create()
            sr.readModel("models/EDSR_x2.pb")
            sr.setModel("edsr", 2)
        else:  # scale_factor == 4
            sr = cv2.dnn_superres.DnnSuperResImpl_create()
            sr.readModel("models/EDSR_x4.pb")
            sr.setModel("edsr", 4)
        
        # Upscale image
        upscaled = sr.upsample(img)
        
        # Convert back to PIL and save
        upscaled_rgb = cv2.cvtColor(upscaled, cv2.COLOR_BGR2RGB)
        Image.fromarray(upscaled_rgb).save(output_path)
        
        return str(output_path) 