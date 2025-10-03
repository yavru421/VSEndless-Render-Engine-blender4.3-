# VSEndless Release Packaging Script
# Creates a clean ZIP package for Blender add-on installation

import zipfile
import os
from pathlib import Path
import datetime

def create_release_package():
    """Create a clean release package for the VSEndless add-on"""

    # Get current directory
    current_dir = Path(__file__).parent

    # Version info (from __init__.py)
    version = "5.0.0"
    date_str = datetime.datetime.now().strftime("%Y%m%d")

    # Package name
    package_name = f"VSEndless_GPU_Render_Engine_v{version}_{date_str}.zip"

    # Files to include (all Python files and documentation)
    include_patterns = [
        "**/*.py",
        "README.md",
        "LICENSE",
        "*.md"
    ]

    # Files/folders to exclude
    exclude_patterns = [
        "__pycache__",
        "*.pyc",
        ".git*",
        "package.py",
        "*.zip"
    ]

    print(f"Creating release package: {package_name}")

    with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for pattern in include_patterns:
            for file_path in current_dir.glob(pattern):
                if file_path.is_file():
                    # Check if file should be excluded
                    should_exclude = any(
                        excl_pattern in str(file_path)
                        for excl_pattern in exclude_patterns
                    )

                    if not should_exclude:
                        # Add file to ZIP with relative path
                        arcname = file_path.relative_to(current_dir)
                        zipf.write(file_path, arcname)
                        print(f"  Added: {arcname}")

    print(f"\n✅ Release package created: {package_name}")
    print(f"📦 Ready for Blender add-on installation!")

    return package_name

if __name__ == "__main__":
    create_release_package()