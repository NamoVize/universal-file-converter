"""
Audio Converter Module for the Universal File Converter
"""
import os
import logging
from pydub import AudioSegment

from utils.file_utils import get_output_path


class AudioConverter:
    """Handles conversion between various audio formats using pydub"""
    
    # Supported formats and their file extensions
    SUPPORTED_INPUT_FORMATS = {
        "mp3", "wav", "flac", "aac", "ogg", "wma", "m4a"
    }
    
    SUPPORTED_OUTPUT_FORMATS = {
        "mp3", "wav", "flac", "aac", "ogg"
    }
    
    # Format mapping for pydub
    FORMAT_MAP = {
        "mp3": "mp3",
        "wav": "wav",
        "flac": "flac",
        "aac": "aac",
        "ogg": "ogg",
        "wma": "wma",  # Note: pydub may not support WMA natively
        "m4a": "mp4"   # pydub uses mp4 for m4a
    }
    
    def __init__(self):
        """Initialize the audio converter"""
        self.logger = logging.getLogger(__name__)
    
    def convert(self, input_path, output_format, output_dir, **options):
        """
        Convert an audio file to the specified format
        
        Args:
            input_path (str): Path to the input audio file
            output_format (str): Desired output format (e.g., "mp3", "wav")
            output_dir (str): Directory to save the output file
            **options: Additional options for conversion
                - quality (str): "high", "medium", or "low" (default: "high")
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
            
            # Set bitrate based on quality option
            bitrate = "320k"  # high quality default
            if options.get("quality") == "medium":
                bitrate = "192k"
            elif options.get("quality") == "low":
                bitrate = "128k"
            
            # Load the audio
            audio = AudioSegment.from_file(
                input_path, 
                format=self.FORMAT_MAP.get(input_extension, input_extension)
            )
            
            # Set export parameters based on format
            export_params = {}
            
            if output_format == "mp3":
                export_params = {
                    "format": "mp3",
                    "bitrate": bitrate,
                    "tags": {"artist": "Universal File Converter"}
                }
            elif output_format == "wav":
                export_params = {
                    "format": "wav",
                    "sample_width": 2,  # 16-bit
                    "frame_rate": 44100  # CD quality
                }
            elif output_format == "flac":
                export_params = {
                    "format": "flac",
                    "sample_width": 2,  # 16-bit
                    "frame_rate": 44100  # CD quality
                }
            elif output_format in ["aac", "m4a"]:
                export_params = {
                    "format": "adts" if output_format == "aac" else "mp4",
                    "bitrate": bitrate
                }
            elif output_format == "ogg":
                export_params = {
                    "format": "ogg",
                    "bitrate": bitrate
                }
                
            # Export the converted audio
            audio.export(output_path, **export_params)
            
            self.logger.info(f"Successfully converted {input_path} to {output_path}")
            return True
                
        except Exception as e:
            self.logger.error(f"Error converting {input_path}: {str(e)}")
            return False
    
    @staticmethod
    def is_supported_input(file_path):
        """Check if a file is a supported input format"""
        extension = os.path.splitext(file_path)[1][1:].lower()
        return extension in AudioConverter.SUPPORTED_INPUT_FORMATS