#!/bin/bash
# Linux installation script for MediaInfo Viewer context menu

echo "Installing MediaInfo Viewer for Linux..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create desktop entry
cat > ~/.local/share/applications/mediainfo-viewer.desktop << EOF
[Desktop Entry]
Type=Application
Name=MediaInfo Viewer
Comment=View media file information with modern UI
Exec=python3 "$SCRIPT_DIR/mediainfo_viewer.py" %f
Icon=multimedia-player
MimeType=video/mp4;video/x-msvideo;video/x-matroska;video/quicktime;video/x-ms-wmv;video/x-flv;audio/mpeg;audio/x-wav;audio/flac;audio/aac;audio/mp4;audio/ogg;image/jpeg;image/png;image/gif;image/bmp;image/tiff;video/webm;video/3gpp;audio/x-ms-wma;image/webp;
Categories=AudioVideo;Player;
NoDisplay=false
StartupNotify=true
EOF

# Update desktop database
update-desktop-database ~/.local/share/applications/ 2>/dev/null || true

# Install dependencies
echo "Installing Python dependencies..."
pip3 install --user -r "$SCRIPT_DIR/requirements.txt"

echo "Installation completed!"
echo "You can now right-click on media files and select 'Open with MediaInfo Viewer'"
echo "Or launch the application from your application menu."