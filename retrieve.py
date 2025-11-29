import os
import shutil
from pathlib import Path


def retrieve_blender_theme():
    """
    Retrieves the Requin_Blue.xml theme file from Blender's AppData directory
    and copies it to the retrieve directory in the project.
    """
    # Source file path
    source_path = Path(
        r"C:\Users\M\AppData\Roaming\Blender Foundation\Blender\5.0\scripts\presets\interface_theme\Requin_Blue.xml"
    )

    # Destination directory (relative to script location)
    script_dir = Path(__file__).parent
    dest_dir = script_dir / "retrieve"
    dest_path = dest_dir / "Requin_Blue.xml"

    # Create retrieve directory if it doesn't exist
    dest_dir.mkdir(exist_ok=True)

    # Check if source file exists
    if not source_path.exists():
        print(f"Error: Source file not found at {source_path}")
        return False

    try:
        # Copy the file
        shutil.copy2(source_path, dest_path)
        print(f"Successfully retrieved theme file!")
        print(f"  From: {source_path}")
        print(f"  To:   {dest_path}")
        return True
    except Exception as e:
        print(f"Error copying file: {e}")
        return False


if __name__ == "__main__":
    retrieve_blender_theme()
