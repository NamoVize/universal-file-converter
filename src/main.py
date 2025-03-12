#!/usr/bin/env python3
"""
Universal File Converter - Main Application
"""
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox, 
                           QLabel, QPushButton, QComboBox, QLineEdit, QProgressBar,
                           QListWidget, QCheckBox, QVBoxLayout, QHBoxLayout, QWidget,
                           QTabWidget, QGridLayout, QGroupBox, QSplitter, QFrame)
from PyQt5.QtGui import QIcon, QPixmap, QDragEnterEvent, QDropEvent
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize

from converters.image_converter import ImageConverter
from converters.video_converter import VideoConverter
from converters.document_converter import DocumentConverter
from converters.audio_converter import AudioConverter
from utils.file_utils import get_file_type, create_directory_if_not_exists
from ui.style import STYLESHEET

class ConversionWorker(QThread):
    """Worker thread for handling conversions without blocking the UI"""
    progress_update = pyqtSignal(int, str)
    conversion_complete = pyqtSignal(bool, str)
    
    def __init__(self, converter, input_files, output_format, output_dir, options=None):
        super().__init__()
        self.converter = converter
        self.input_files = input_files
        self.output_format = output_format
        self.output_dir = output_dir
        self.options = options or {}
        
    def run(self):
        """Run the conversion process"""
        total_files = len(self.input_files)
        success_count = 0
        
        for i, file_path in enumerate(self.input_files):
            try:
                file_name = os.path.basename(file_path)
                self.progress_update.emit(int((i / total_files) * 100), f"Converting {file_name}...")
                
                # Call the appropriate converter
                success = self.converter.convert(
                    file_path, 
                    self.output_format,
                    self.output_dir,
                    **self.options
                )
                
                if success:
                    success_count += 1
                    
            except Exception as e:
                self.progress_update.emit(int((i / total_files) * 100), f"Error: {str(e)}")
                
        success = success_count == total_files
        message = f"Converted {success_count} of {total_files} files successfully"
        self.conversion_complete.emit(success, message)


class FileConverterApp(QMainWindow):
    """Main application window for the Universal File Converter"""
    
    def __init__(self):
        super().__init__()
        self.input_files = []
        self.output_directory = ""
        
        # Initialize converters
        self.image_converter = ImageConverter()
        self.video_converter = VideoConverter()
        self.document_converter = DocumentConverter()
        self.audio_converter = AudioConverter()
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Universal File Converter")
        self.setMinimumSize(900, 650)
        self.setAcceptDrops(True)
        
        # Set stylesheet
        self.setStyleSheet(STYLESHEET)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Create the file selection area
        file_section = self.create_file_selection_section()
        main_layout.addWidget(file_section)
        
        # Create conversion options section
        options_section = self.create_conversion_options_section()
        main_layout.addWidget(options_section)
        
        # Create action buttons
        button_section = self.create_action_buttons()
        main_layout.addWidget(button_section)
        
        # Create status area
        status_section = self.create_status_section()
        main_layout.addWidget(status_section)
        
        self.setCentralWidget(main_widget)
        
        # Load app icon
        # self.setWindowIcon(QIcon("icons/app_icon.png"))

    def create_file_selection_section(self):
        """Create the file selection UI section"""
        group_box = QGroupBox("Input Files")
        layout = QVBoxLayout()
        
        # File list
        self.file_list = QListWidget()
        self.file_list.setMinimumHeight(150)
        layout.addWidget(self.file_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.add_files_btn = QPushButton("Add Files")
        self.add_files_btn.clicked.connect(self.add_files)
        button_layout.addWidget(self.add_files_btn)
        
        self.clear_files_btn = QPushButton("Clear")
        self.clear_files_btn.clicked.connect(self.clear_files)
        button_layout.addWidget(self.clear_files_btn)
        
        layout.addLayout(button_layout)
        
        # Drag & drop label
        drag_drop_label = QLabel("Or drag and drop files here")
        drag_drop_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(drag_drop_label)
        
        group_box.setLayout(layout)
        return group_box
    
    def create_conversion_options_section(self):
        """Create the conversion options UI section"""
        group_box = QGroupBox("Conversion Options")
        layout = QGridLayout()
        
        # Output format selector
        layout.addWidget(QLabel("Output Format:"), 0, 0)
        
        self.format_combo = QComboBox()
        self.format_combo.setMinimumWidth(200)
        
        # Add format categories with separators
        self.format_combo.addItem("-- Image Formats --")
        for fmt in ["png", "jpg", "gif", "webp", "tiff", "bmp", "svg"]:
            self.format_combo.addItem(fmt.upper())
            
        self.format_combo.addItem("-- Video Formats --")
        for fmt in ["mp4", "avi", "mkv", "mov", "webm", "gif"]:
            self.format_combo.addItem(fmt.upper())
            
        self.format_combo.addItem("-- Document Formats --")
        for fmt in ["pdf", "docx", "txt", "rtf", "odt", "xlsx", "csv", "pptx", "html"]:
            self.format_combo.addItem(fmt.upper())
            
        self.format_combo.addItem("-- Audio Formats --")
        for fmt in ["mp3", "wav", "flac", "aac", "ogg"]:
            self.format_combo.addItem(fmt.upper())
            
        # Disable the separator items
        self.format_combo.model().item(0).setEnabled(False)
        self.format_combo.model().item(8).setEnabled(False)
        self.format_combo.model().item(15).setEnabled(False)
        self.format_combo.model().item(25).setEnabled(False)
        
        # Set default to first real option
        self.format_combo.setCurrentIndex(1)
        
        layout.addWidget(self.format_combo, 0, 1)
        
        # Output directory selector
        layout.addWidget(QLabel("Output Directory:"), 1, 0)
        
        output_dir_layout = QHBoxLayout()
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setReadOnly(True)
        self.output_dir_edit.setPlaceholderText("Select output directory...")
        output_dir_layout.addWidget(self.output_dir_edit)
        
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_output_directory)
        output_dir_layout.addWidget(self.browse_btn)
        
        layout.addLayout(output_dir_layout, 1, 1)
        
        # Quality options (for images/videos)
        layout.addWidget(QLabel("Quality:"), 2, 0)
        
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["High", "Medium", "Low"])
        layout.addWidget(self.quality_combo, 2, 1)
        
        # Additional options
        self.maintain_aspect_ratio = QCheckBox("Maintain aspect ratio")
        self.maintain_aspect_ratio.setChecked(True)
        layout.addWidget(self.maintain_aspect_ratio, 3, 0, 1, 2)
        
        self.overwrite_existing = QCheckBox("Overwrite existing files")
        self.overwrite_existing.setChecked(True)
        layout.addWidget(self.overwrite_existing, 4, 0, 1, 2)
        
        group_box.setLayout(layout)
        return group_box
    
    def create_action_buttons(self):
        """Create action buttons UI section"""
        frame = QFrame()
        layout = QHBoxLayout(frame)
        
        spacer = QWidget()
        layout.addWidget(spacer)
        
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.setMinimumSize(120, 40)
        self.convert_btn.clicked.connect(self.start_conversion)
        layout.addWidget(self.convert_btn)
        
        return frame
    
    def create_status_section(self):
        """Create status UI section"""
        group_box = QGroupBox("Status")
        layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        group_box.setLayout(layout)
        return group_box
    
    def add_files(self):
        """Open file dialog to add input files"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Files to Convert", "", "All Files (*.*)"
        )
        
        if file_paths:
            self.add_files_to_list(file_paths)
    
    def add_files_to_list(self, file_paths):
        """Add files to the list widget"""
        for file_path in file_paths:
            if file_path not in self.input_files:
                self.input_files.append(file_path)
                file_name = os.path.basename(file_path)
                self.file_list.addItem(file_name)
        
        # Enable conversion if we have files and output dir
        self.update_convert_button_state()
                
    def clear_files(self):
        """Clear the file list"""
        self.file_list.clear()
        self.input_files = []
        self.update_convert_button_state()
        
    def browse_output_directory(self):
        """Open dialog to select output directory"""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Output Directory", ""
        )
        
        if directory:
            self.output_directory = directory
            self.output_dir_edit.setText(directory)
            self.update_convert_button_state()
    
    def update_convert_button_state(self):
        """Update the convert button enabled state"""
        self.convert_btn.setEnabled(
            len(self.input_files) > 0 and 
            self.output_directory != ""
        )
    
    def start_conversion(self):
        """Start the conversion process"""
        if not self.input_files:
            QMessageBox.warning(self, "Error", "No input files selected")
            return
        
        if not self.output_directory:
            QMessageBox.warning(self, "Error", "No output directory selected")
            return
        
        # Get the selected output format
        output_format = self.format_combo.currentText().lower()
        
        # Get conversion options
        options = {
            "quality": self.quality_combo.currentText().lower(),
            "maintain_aspect_ratio": self.maintain_aspect_ratio.isChecked(),
            "overwrite": self.overwrite_existing.isChecked()
        }
        
        # Create output directory if it doesn't exist
        create_directory_if_not_exists(self.output_directory)
        
        # Determine converter for the files
        converter = self.get_converter_for_format(output_format)
        if not converter:
            QMessageBox.warning(self, "Error", f"No converter available for {output_format} format")
            return
        
        # Start conversion in a separate thread
        self.conversion_thread = ConversionWorker(
            converter, self.input_files, output_format, self.output_directory, options
        )
        self.conversion_thread.progress_update.connect(self.update_progress)
        self.conversion_thread.conversion_complete.connect(self.conversion_finished)
        
        # Disable UI during conversion
        self.set_ui_enabled(False)
        
        # Start conversion
        self.conversion_thread.start()
    
    def get_converter_for_format(self, output_format):
        """Get the appropriate converter for the output format"""
        # Image formats
        if output_format in ["png", "jpg", "jpeg", "gif", "webp", "tiff", "bmp", "svg"]:
            return self.image_converter
        
        # Video formats
        elif output_format in ["mp4", "avi", "mkv", "mov", "webm"]:
            return self.video_converter
        
        # Document formats
        elif output_format in ["pdf", "docx", "txt", "rtf", "odt", "xlsx", "csv", "pptx", "html"]:
            return self.document_converter
        
        # Audio formats
        elif output_format in ["mp3", "wav", "flac", "aac", "ogg"]:
            return self.audio_converter
        
        return None
    
    def update_progress(self, value, message):
        """Update progress bar and status message"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
    
    def conversion_finished(self, success, message):
        """Handle conversion completion"""
        self.progress_bar.setValue(100)
        self.status_label.setText(message)
        
        # Re-enable UI
        self.set_ui_enabled(True)
        
        # Show completion message
        if success:
            QMessageBox.information(self, "Conversion Complete", message)
        else:
            QMessageBox.warning(self, "Conversion Completed with Errors", message)
    
    def set_ui_enabled(self, enabled):
        """Enable or disable UI elements during conversion"""
        self.add_files_btn.setEnabled(enabled)
        self.clear_files_btn.setEnabled(enabled)
        self.browse_btn.setEnabled(enabled)
        self.format_combo.setEnabled(enabled)
        self.quality_combo.setEnabled(enabled)
        self.maintain_aspect_ratio.setEnabled(enabled)
        self.overwrite_existing.setEnabled(enabled)
        self.convert_btn.setEnabled(enabled)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter events for drag and drop"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop events for drag and drop"""
        file_paths = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                file_paths.append(file_path)
        
        if file_paths:
            self.add_files_to_list(file_paths)


def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use Fusion style for a modern look
    
    window = FileConverterApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()