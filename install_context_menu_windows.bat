@echo off
REM Windows Registry Script to add MediaInfo Viewer to right-click context menu
REM Run as Administrator

echo Adding MediaInfo Viewer to Windows Context Menu...

set SCRIPT_PATH=%~dp0
set PYTHON_SCRIPT=%SCRIPT_PATH%mediainfo_viewer.py

REM Add context menu for all files
reg add "HKEY_CLASSES_ROOT\*\shell\MediaInfoViewer" /ve /d "View with MediaInfo" /f
reg add "HKEY_CLASSES_ROOT\*\shell\MediaInfoViewer" /v "Icon" /d "shell32.dll,23" /f
reg add "HKEY_CLASSES_ROOT\*\shell\MediaInfoViewer\command" /ve /d "python \"%PYTHON_SCRIPT%\" \"%%1\"" /f

REM Add context menu specifically for media files
for %%i in (.mp4 .avi .mkv .mov .wmv .flv .mp3 .wav .flac .aac .m4a .ogg .jpg .jpeg .png .gif .bmp .tiff .webm .m4v .3gp .wma .webp) do (
    reg add "HKEY_CLASSES_ROOT\%%i\shell\MediaInfoViewer" /ve /d "View with MediaInfo" /f
    reg add "HKEY_CLASSES_ROOT\%%i\shell\MediaInfoViewer" /v "Icon" /d "shell32.dll,23" /f
    reg add "HKEY_CLASSES_ROOT\%%i\shell\MediaInfoViewer\command" /ve /d "python \"%PYTHON_SCRIPT%\" \"%%1\"" /f
)

echo Context menu registration completed!
echo You can now right-click on media files and select "View with MediaInfo"
pause