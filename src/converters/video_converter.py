"""
Video Converter Module for the Universal File Converter
"""
import os
import logging
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from utils.file_utils import get_output_path


class VideoConverter:
    """Handles conversion between various video formats using MoviePy"""
    
    # Supported formats and their file extensions
    SUPPORTED_INPUT_FORMATS = {
        "mp4", "avi", "mkv", "mov", "webm", "flv", "wmv", "m4v", "3gp"
    }
    
    SUPPORTED_OUTPUT_FORMATS = {
        "mp4", "avi", "mkv", "mov", "webm", "gif"
    }
    
    def __init__(self):
        """Initialize the video converter"""
        self.logger = logging.getLogger(__name__)
    
    def convert(self, input_path, output_format, output_dir, **options):
        """
        Convert a video file to the specified format
        
        Args:
            input_path (str): Path to the input video file
            output_format (str): Desired output format (e.g., "mp4", "avi")
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
            
            # Set bitrate based on quality option
            bitrate = "8000k"  # high quality default
            if options.get("quality") == "medium":
                bitrate = "4000k"
            elif options.get("quality") == "low":
                bitrate = "1500k"
            
            # Load the video
            video = mp.VideoFileClip(input_path)
            
            # Handle special case for GIF output
            if output_format == "gif":
                video.write_gif(output_path, fps=15)
            else:
                # Write the output video with specified options
                video.write_videofile(
                    output_path,
                    codec="libx264" if output_format == "mp4" else None,
                    audio_codec="aac" if output_format == "mp4" else "libmp3lame",
                    bitrate=bitrate,
                    preset="slow" if options.get("quality") == "high" else "medium",
                    threads=4,
                    verbose=False,
                    logger=None  # Disable MoviePy's console output
                )
            
            # Close the video to release resources
            video.close()
            
            self.logger.info(f"Successfully converted {input_path} to {output_path}")
            return True
                
        except Exception as e:
            self.logger.error(f"Error converting {input_path}: {str(e)}")
            return False
    
    @staticmethod
    def is_supported_input(file_path):
        """Check if a file is a supported input format"""
        extension = os.path.splitext(file_path)[1][1:].lower()
        return extension in VideoConverter.SUPPORTED_INPUT_FORMATS
    
    def extract_subclip(self, input_path, output_path, start_time, end_time):
        """
        Extract a clip from a video file
        
        Args:
            input_path (str): Path to the input video file
            output_path (str): Path to save the output clip
            start_time (float): Start time in seconds
            end_time (float): End time in seconds
            
        Returns:
            bool: True if extraction was successful, False otherwise
        """
        try:
            ffmpeg_extract_subclip(input_path, start_time, end_time, targetname=output_path)
            return True
        except Exception as e:
            self.logger.error(f"Error extracting clip from {input_path}: {str(e)}")
            return False