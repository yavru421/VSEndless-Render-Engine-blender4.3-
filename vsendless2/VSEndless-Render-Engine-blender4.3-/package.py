#!/usr/bin/env python3
"""
VSEndless Render Engine Packaging Script
Creates a ZIP file that can be installed in Blender
"""

import os
import zipfile
import datetime
import shutil
import sys
from pathlib import Path

# Files/folders to exclude from the package
EXCLUDED_ITEMS = [
    "__pycache__",
    ".git",
    ".github",
    ".gitignore",
    "package.py",
    ".vscode",
    "tests",
    "dist",
    "utils/test_some_shit.py"  # Exclude the test script
]

def create_addon_zip(source_dir, version_number=None):
    """Create a ZIP file for Blender add-on installation"""
    source_path = Path(source_dir)
    
    # Create 'dist' directory if it doesn't exist
    dist_dir = source_path / "dist"
    dist_dir.mkdir(exist_ok=True)
    
    # Read version from __init__.py if not provided
    if not version_number:
        init_path = source_path / "__init__.py"
        if init_path.exists():
            with open(init_path, 'r') as f:
                content = f.read()
                import re
                version_match = re.search(r'"version":\s*\((\d+),\s*(\d+),\s*(\d+)\)', content)
                if version_match:
                    version_number = f"{version_match.group(1)}.{version_match.group(2)}.{version_match.group(3)}"
    
    # Default version number if still not available
    if not version_number:
        version_number = "3.0.2"
    
    # Use today's date for filename uniqueness
    today = datetime.datetime.now().strftime("%Y%m%d")
    zip_filename = f"VSEndless_Render_Engine_v{version_number}_{today}.zip"
    zip_path = dist_dir / zip_filename
    
    # Create the ZIP file
    print(f"Creating add-on package: {zip_path}")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        # Walk through the directory tree
        for root, dirs, files in os.walk(source_path):
            rel_path = os.path.relpath(root, source_path)
            
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDED_ITEMS]
            
            # If we're in the root directory
            if rel_path == ".":
                # Add files from root directory, excluding specified files
                for file in files:
                    if file not in EXCLUDED_ITEMS and not file.startswith("."):
                        zipf.write(os.path.join(root, file), file)
            else:
                # Skip excluded directories at deeper levels
                if any(excluded in rel_path.split(os.sep) for excluded in EXCLUDED_ITEMS):
                    continue
                
                # Add all other files
                for file in files:
                    if file not in EXCLUDED_ITEMS and not file.startswith("."):
                        file_path = os.path.join(root, file)
                        arcname = os.path.join(rel_path, file)
                        zipf.write(file_path, arcname)
    
    print(f"Package created successfully: {zip_path}")
    return zip_path

if __name__ == "__main__":
    # Get current directory where the script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Optional: Allow version number as a command line argument
    version = None
    if len(sys.argv) > 1:
        version = sys.argv[1]
    
    # Create the ZIP package
    zip_path = create_addon_zip(current_dir, version)
    
    print("\nInstallation Instructions:")
    print("1. Open Blender")
    print("2. Go to Edit > Preferences > Add-ons")
    print("3. Click 'Install...' and select the ZIP file")
    print("4. Enable the 'VSEndless - GPU Accelerated Render Engine' add-on")
    print("5. Save preferences if you want to keep it enabled")
