import os
import shutil
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DownloadsOrganizer:
    def __init__(self, downloads_path=None):
        # Set downloads path (default to user's downloads folder)
        if downloads_path:
            self.downloads_path = Path(downloads_path)
        else:
            self.downloads_path = Path.home() / "Downloads"
        
        # Define folder categories and their file extensions
        self.categories = {
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
            "Video": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
            "Executables": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php", ".rb", ".json", ".xml"],
            "Spreadsheets": [".csv", ".xls", ".xlsx", ".ods"],
            "Presentations": [".ppt", ".pptx", ".odp"],
            "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
            "Torrents": [".torrent"],
            "Others": []  # For files with unknown extensions
        }
        
        # Create reverse mapping for quick lookup
        self.extension_to_category = {}
        for category, extensions in self.categories.items():
            for ext in extensions:
                self.extension_to_category[ext] = category

    def get_file_category(self, file_extension):
        """Determine the category for a file based on its extension"""
        return self.extension_to_category.get(file_extension.lower(), "Others")

    def create_category_folders(self):
        """Create all category folders if they don't exist"""
        for category in self.categories.keys():
            category_path = self.downloads_path / category
            if not category_path.exists():
                category_path.mkdir(exist_ok=True)
                logger.info(f"Created folder: {category}")

    def organize_files(self, dry_run=False):
        """Organize files into their respective category folders"""
        if not self.downloads_path.exists():
            logger.error(f"Downloads folder not found: {self.downloads_path}")
            return
        
        self.create_category_folders()
        
        files_moved = 0
        files_skipped = 0
        
        for item in self.downloads_path.iterdir():
            # Skip directories and hidden files
            if item.is_dir() or item.name.startswith('.'):
                continue
            
            # Get file extension
            file_extension = item.suffix.lower()
            
            # Determine category
            category = self.get_file_category(file_extension)
            
            # Skip if file is already in the correct folder
            if item.parent.name == category:
                continue
            
            # Destination path
            dest_path = self.downloads_path / category / item.name
            
            # Handle file name conflicts
            counter = 1
            original_dest_path = dest_path
            while dest_path.exists():
                stem = original_dest_path.stem
                suffix = original_dest_path.suffix
                dest_path = original_dest_path.parent / f"{stem}_{counter}{suffix}"
                counter += 1
            
            if dry_run:
                logger.info(f"Would move: {item.name} -> {category}/")
            else:
                try:
                    shutil.move(str(item), str(dest_path))
                    logger.info(f"Moved: {item.name} -> {category}/")
                    files_moved += 1
                except Exception as e:
                    logger.error(f"Error moving {item.name}: {e}")
                    files_skipped += 1
        
        logger.info(f"Organization complete. Moved: {files_moved}, Skipped: {files_skipped}")

    def list_files_by_category(self):
        """List all files organized by category"""
        if not self.downloads_path.exists():
            logger.error(f"Downloads folder not found: {self.downloads_path}")
            return
        
        file_count = 0
        print("\nFiles in Downloads folder:")
        print("-" * 50)
        
        for category in self.categories.keys():
            category_path = self.downloads_path / category
            if category_path.exists() and category_path.is_dir():
                files = list(category_path.iterdir())
                if files:
                    print(f"\n{category}:")
                    for file in files:
                        if file.is_file():
                            print(f"  📄 {file.name}")
                            file_count += 1
        
        print(f"\nTotal files: {file_count}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Organize your Downloads folder")
    parser.add_argument("--path", "-p", help="Path to downloads folder (default: ~/Downloads)")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Show what would be moved without actually moving files")
    parser.add_argument("--list", "-l", action="store_true", help="List files by category after organization")
    
    args = parser.parse_args()
    
    organizer = DownloadsOrganizer(args.path)
    
    if args.dry_run:
        print("DRY RUN - No files will be moved")
        print("=" * 50)
    
    organizer.organize_files(dry_run=args.dry_run)
    
    if args.list:
        organizer.list_files_by_category()

if __name__ == "__main__":
    main()
