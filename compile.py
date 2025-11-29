import os
import re
import zipfile
from pathlib import Path


def get_version_from_manifest():
    """
    Reads the version from blender_manifest.toml
    Returns the version string (not schema_version)
    """
    script_dir = Path(__file__).parent
    manifest_path = script_dir / "blender_manifest.toml"

    if not manifest_path.exists():
        raise FileNotFoundError(f"blender_manifest.toml not found at {manifest_path}")

    with open(manifest_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find version = "x.x.x" (not schema_version)
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)

    if match:
        return match.group(1)
    else:
        raise ValueError("Version not found in blender_manifest.toml")


def get_theme_name_from_xml():
    """
    Gets the XML filename (without extension) from the retrieve directory
    """
    script_dir = Path(__file__).parent
    retrieve_dir = script_dir / "retrieve"

    if not retrieve_dir.exists():
        raise FileNotFoundError(f"Retrieve directory not found at {retrieve_dir}")

    # Find the first .xml file in retrieve directory
    xml_files = list(retrieve_dir.glob("*.xml"))

    if not xml_files:
        raise FileNotFoundError("No XML file found in retrieve directory")

    # Return the stem (filename without extension)
    return xml_files[0].stem


def compile_theme():
    """
    Zips the contents of retrieve directory and blender_manifest.toml
    Names the zip as: <theme_name>_<version>.zip
    """
    script_dir = Path(__file__).parent
    retrieve_dir = script_dir / "retrieve"
    manifest_path = script_dir / "blender_manifest.toml"

    # Get version and theme name
    version = get_version_from_manifest()
    theme_name = get_theme_name_from_xml()

    # Create output filename in dist directory
    dist_dir = script_dir / "dist"
    dist_dir.mkdir(exist_ok=True)

    zip_filename = f"{theme_name}_{version}.zip"
    zip_path = dist_dir / zip_filename

    print(f"Creating theme package: {zip_filename}")
    print(f"  Theme: {theme_name}")
    print(f"  Version: {version}")

    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Add blender_manifest.toml
            zipf.write(manifest_path, manifest_path.name)
            print(f"  Added: {manifest_path.name}")

            # Add all files from retrieve directory (without the retrieve folder structure)
            for file_path in retrieve_dir.rglob("*"):
                if file_path.is_file():
                    # Add files directly to zip root (without retrieve/ prefix)
                    arcname = file_path.name
                    zipf.write(file_path, arcname)
                    print(f"  Added: {arcname}")

        print(f"\nSuccessfully created: {zip_path}")
        return True

    except Exception as e:
        print(f"Error creating zip file: {e}")
        return False


if __name__ == "__main__":
    compile_theme()
