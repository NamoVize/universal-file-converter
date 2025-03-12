"""
Image Converter Module for the Universal File Converter
"""
import os
import logging
from PIL import Image

from utils.file_utils import get_output_path


class ImageConverter:
    """Handles conversion between various image formats using Pillow"""
    
    # Supported formats and their file extensions
    SUPPORTED_INPUT_FORMATS = {
        "png", "jpg", "jpeg", "gif", "webp", "tiff", "bmp", "svg"
    }
    
    SUPPORTED_OUTPUT_FORMATS = {
        "png", "jpg", "jpeg", "gif", "webp", "tiff", "bmp", "svg"
    }
    
    def __init__(self):
        """Initialize the image converter"""
        self.logger = logging.getLogger(__name__)
    
    def convert(self, input_path, output_format, output_dir, **options):
        """
        Convert an image file to the specified format
        
        Args:
            input_path (str): Path to the input image file
            output_format (str): Desired output format (e.g., "png", "jpg")
            output_dir (str): Directory to save the output file
            **options: Additional options for conversion
                - quality (str): "high", "medium", or "low" (default: "high")
                - maintain_aspect_ratio (bool): Whether to maintain aspect ratio (default: True)
                - overwrite (bool): Whether to overwrite existing files (default: False)
        
        Returns:
            bool: True if conversion was successful, False otherwise
        """
        try:
            # Validate input format
            input_extension = os.path.splitext(input_path)[1][1:].lower()
            if input_extension not in self.SUPPORTED_INPUT_FORMATS:
                self.logger.error(f"Unsupported input format: {input_extension}")
                return False
            
            # Validate output format
            output_format = output_format.lower().replace(".", "")
            if output_format not in self.SUPPORTED_OUTPUT_FORMATS:
                self.logger.error(f"Unsupported output format: {output_format}")
                return False
            
            # Get output path
            output_path = get_output_path(input_path, output_format, output_dir)
            
            # Check if output file exists and overwrite is not enabled
            if os.path.exists(output_path) and not options.get("overwrite", False):
                self.logger.warning(f"Output file already exists: {output_path}")
                return False
            
            # Open the image
            with Image.open(input_path) as img:
                # Convert image if necessary (e.g., convert to RGB for JPEG)
                if output_format.lower() in ["jpg", "jpeg"] and img.mode in ["RGBA", "P"]:
                    img = img.convert("RGB")
                    
                # Set quality based on options
                quality = 95  # Default high quality
                if options.get("quality") == "medium":
                    quality = 75
                elif options.get("quality") == "low":
                    quality = 50
                
                # Save the converted image
                save_options = {"quality": quality}
                
                # Format-specific options
                if output_format.lower() == "png":
                    save_options = {"optimize": True}
                elif output_format.lower() == "gif":
                    save_options = {}
                elif output_format.lower() == "webp":
                    save_options = {"quality": quality, "method": 6}
                    
                img.save(output_path, format=output_format.upper(), **save_options)
                
                self.logger.info(f"Successfully converted {input_path} to {output_path}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error converting {input_path}: {str(e)}")
            return False
    
    @staticmethod
    def is_supported_input(file_path):
        """Check if a file is a supported input format"""
        extension = os.path.splitext(file_path)[1][1:].lower()
        return extension in ImageConverter.SUPPORTED_INPUT_FORMATS