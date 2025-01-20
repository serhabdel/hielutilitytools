import logging
import os
from pathlib import Path
from PIL import Image
import sys

# Configure logging with absolute path
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'logo_converter_debug.log')
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=log_path,
                    filemode='w')

class LogoConverter:
    """
    A specialized service for converting PNG to ICO with precise sizing.
    
    Supports:
    - Converting PNG to multi-size ICO for Windows and Web
    - Specific icon sizes for different use cases
    """
    
    @staticmethod
    def convert_logo(input_path, output_path=None):
        """
        Convert PNG to ICO with specific Windows and Favicon sizes.
        
        Args:
            input_path: Path to the input PNG file
            output_path: Optional output ICO path
        
        Raises:
            ValueError: If input is not a PNG
            FileNotFoundError: If input file does not exist
        """
        input_path = Path(input_path)
        if not input_path.exists():
            logging.error(f"Input file not found: {input_path}")
            print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
            raise FileNotFoundError(f"Logo file not found: {input_path}")
        
        # Validate input is PNG
        if input_path.suffix.lower() != '.png':
            logging.error(f"Invalid input format: {input_path.suffix}")
            print(f"ERROR: Invalid input format: {input_path.suffix}", file=sys.stderr)
            raise ValueError("Input must be a PNG file")
        
        # Determine output path
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}_icon.ico"
        output_path = Path(output_path)
        
        try:
            # Open the image and prepare for conversion
            with Image.open(input_path) as logo:
                logging.info(f"Original image size: {logo.size}")
                print(f"Original image size: {logo.size}")
                logging.info(f"Original image mode: {logo.mode}")
                print(f"Original image mode: {logo.mode}")
                
                # Convert to RGBA to handle transparency
                logo = logo.convert('RGBA')
                
                # Specific icon sizes for Windows and Favicon
                # Prioritize larger sizes, especially for Windows
                icon_sizes = [
                    # Windows icon sizes (largest first)
                    (256, 256),  # Very high DPI Windows icon
                    (128, 128),  # High DPI Windows icon
                    (64, 64),    # Large Windows icon
                    (48, 48),    # Standard Windows icon
                    
                    # Favicon sizes
                    (32, 32),    # Standard favicon
                    (24, 24),    # Small favicon
                    (16, 16)     # Smallest favicon
                ]
                
                # Prepare icon images
                icon_images = []
                for width, height in icon_sizes:
                    logging.debug(f"Processing icon size: {width}x{height}")
                    print(f"Processing icon size: {width}x{height}")
                    
                    # Create a new image with transparent background
                    icon = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                    
                    # Resize and center the logo
                    resized_logo = logo.copy()
                    
                    # Use resize instead of thumbnail to ensure exact size
                    resized_logo = resized_logo.resize((width, height), Image.LANCZOS)
                    logging.debug(f"Resized logo size: {resized_logo.size}")
                    print(f"Resized logo size: {resized_logo.size}")
                    
                    # Paste the resized logo onto the transparent icon
                    icon.paste(resized_logo, (0, 0), resized_logo)
                    icon_images.append(icon)
                
                logging.info(f"Total icon images generated: {len(icon_images)}")
                print(f"Total icon images generated: {len(icon_images)}")
                logging.info(f"Icon sizes: {[im.size for im in icon_images]}")
                print(f"Icon sizes: {[im.size for im in icon_images]}")
                
                # Save multi-size ICO
                # Ensure the largest size (256x256) is the primary image
                icon_images[0].save(
                    output_path,
                    format='ICO',
                    sizes=[(im.width, im.height) for im in icon_images],
                    append_images=icon_images[1:],
                    optimize=True
                )
                
                logging.info(f"ICO file saved: {output_path}")
                print(f"ICO file saved: {output_path}")
            
            return str(output_path)
        
        except Exception as e:
            logging.error(f"Logo conversion failed: {e}", exc_info=True)
            print(f"Logo conversion failed: {e}", file=sys.stderr)
            raise RuntimeError(f"Logo conversion failed: {e}")
