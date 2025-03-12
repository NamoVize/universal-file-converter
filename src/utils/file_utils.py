"""
File utility functions for the Universal File Converter
"""
import os
import mimetypes
import logging
import imghdr


def get_file_type(file_path):
    """
    Determine the type of a file (image, video, document, audio, etc.)
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: File type category ('image', 'video', 'document', 'audio', or 'unknown')
    """
    if not os.path.exists(file_path):
        return "unknown"
        
    # Get file extension
    file_extension = os.path.splitext(file_path)[1].lower().replace(".", "")
    
    # Get MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    
    # Image formats
    image_extensions = {"png", "jpg", "jpeg", "gif", "webp", "tiff", "bmp", "svg", "raw", "psd"}
    
    # Video formats
    video_extensions = {"mp4", "avi", "mkv", "mov", "webm", "flv", "wmv", "m4v", "3gp"}
    
    # Document formats
    document_extensions = {
        "pdf", "docx", "doc", "txt", "rtf", "odt", "xlsx", "xls", 
        "csv", "pptx", "ppt", "html", "md", "json", "xml"
    }
    
    # Audio formats
    audio_extensions = {"mp3", "wav", "flac", "aac", "ogg", "wma", "m4a"}
    
    # Determine file type based on extension or MIME type
    if file_extension in image_extensions or (mime_type and mime_type.startswith("image/")):
        return "image"
    elif file_extension in video_extensions or (mime_type and mime_type.startswith("video/")):
        return "video"
    elif file_extension in document_extensions or (mime_type and (
            mime_type.startswith("application/") or 
            mime_type.startswith("text/")
        )):
        return "document"
    elif file_extension in audio_extensions or (mime_type and mime_type.startswith("audio/")):
        return "audio"
    else:
        # Try more specific detection for images
        if imghdr.what(file_path) is not None:
            return "image"
            
        return "unknown"


def get_output_path(input_path, output_format, output_dir):
    """
    Generate the output file path based on the input path and output format
    
    Args:
        input_path (str): Path to the input file
        output_format (str): Desired output format (e.g., "png", "mp4")
        output_dir (str): Directory to save the output file
        
    Returns:
        str: Full path for the output file
    """
    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    
    # Make sure the output format doesn't start with a dot
    output_format = output_format.lower().replace(".", "")
    
    # Create the output filename
    output_filename = f"{base_name}.{output_format}"
    
    # Combine with the output directory
    return os.path.join(output_dir, output_filename)


def create_directory_if_not_exists(directory):
    """
    Create a directory if it doesn't already exist
    
    Args:
        directory (str): Path to the directory to create
        
    Returns:
        bool: True if directory exists or was created successfully, False otherwise
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except Exception as e:
        logging.error(f"Error creating directory {directory}: {str(e)}")
        return False