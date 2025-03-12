# Universal File Converter

A powerful application that converts between various file formats including images, videos, documents, and code files with batch processing support.

![Universal File Converter](screenshots/app_preview.png)

## Features

- **Multi-format Support**: Convert between various formats:
  - Images (PNG, JPEG, GIF, WebP, TIFF, BMP, etc.)
  - Videos (MP4, AVI, MKV, MOV, WebM, etc.)
  - Documents (PDF, DOCX, TXT, XLSX, CSV, etc.)
  - Code files (various syntax highlighting formats)
  - Audio files (MP3, WAV, FLAC, AAC, etc.)
  
- **Batch Processing**: Convert multiple files at once to save time
- **Custom Output Settings**: Adjust quality, resolution, and other parameters
- **Modern UI**: User-friendly interface with drag-and-drop support
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

### Prerequisites

- Python 3.8 or higher
- Required system libraries for specific conversions:
  - FFmpeg (for video conversions)
  - LibreOffice (for document conversions)
  - ImageMagick (for advanced image processing)

### Option 1: Using pip (Recommended)

```bash
# Clone the repository
git clone https://github.com/NamoVize/universal-file-converter.git
cd universal-file-converter

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

### Option 2: Using the standalone executable

Download the latest release for your operating system from the [Releases](https://github.com/NamoVize/universal-file-converter/releases) page.

## Usage

1. Launch the application
2. Select the input files or drag and drop them into the application
3. Choose the desired output format
4. Configure conversion settings (if needed)
5. Select the output directory
6. Click "Convert" to start the conversion process

## Supported Conversions

### Images
- **Input**: PNG, JPEG, JPG, GIF, WebP, TIFF, BMP, RAW, SVG, PSD
- **Output**: PNG, JPEG, JPG, GIF, WebP, TIFF, BMP, SVG

### Videos
- **Input**: MP4, AVI, MKV, MOV, WebM, FLV, WMV, M4V, 3GP
- **Output**: MP4, AVI, MKV, MOV, WebM, GIF

### Documents
- **Input**: PDF, DOCX, DOC, TXT, RTF, ODT, XLSX, XLS, CSV, PPTX, PPT
- **Output**: PDF, DOCX, TXT, RTF, ODT, XLSX, CSV, PPTX, HTML

### Audio
- **Input**: MP3, WAV, FLAC, AAC, OGG, WMA, M4A
- **Output**: MP3, WAV, FLAC, AAC, OGG

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.