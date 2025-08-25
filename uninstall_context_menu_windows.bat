@echo off
REM Windows Registry Script to remove MediaInfo Viewer from right-click context menu
REM Run as Administrator

echo Removing MediaInfo Viewer from Windows Context Menu...

REM Remove context menu for all files
reg delete "HKEY_CLASSES_ROOT\*\shell\MediaInfoViewer" /f

REM Remove context menu for specific media file types
for %%i in (.mp4 .avi .mkv .mov .wmv .flv .mp3 .wav .flac .aac .m4a .ogg .jpg .jpeg .png .gif .bmp .tiff .webm .m4v .3gp .wma .webp) do (
    reg delete "HKEY_CLASSES_ROOT\%%i\shell\MediaInfoViewer" /f
)

echo Context menu removal completed!
pause