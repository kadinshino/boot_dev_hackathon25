# Build & Distribution Directories

## windows_builder/
Automated Windows build system for the Python project:
- `.bat` scripts for one-click Windows executable generation
- Handles Python-to-EXE compilation (likely using PyInstaller or similar)
- Automates dependency bundling and executable packaging
- Simplifies the build process for Windows distributions

**Usage:** Run the batch files to automatically build Windows executables from the Python source.

## store_assets/
Distribution materials for digital storefronts (itch.io, Steam, etc.):
- Store page graphics (banners, screenshots, thumbnails)
- Marketing materials and promotional images
- Basic documentation for players
- Store descriptions and feature lists
- Platform-specific assets (icons, capsule art, etc.)

**Purpose:** Everything needed to publish the game on various distribution platforms. These assets are not required to run the game but are essential for proper store presentation.

## Notes
- `windows_builder/` is only needed when creating Windows builds
- `store_assets/` is only needed when publishing to distribution platforms
- Both directories can be excluded from source distributions