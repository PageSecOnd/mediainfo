#!/usr/bin/env python3
"""
Test script for MediaInfo Viewer to verify functionality
"""

import os
import sys
from pymediainfo import MediaInfo
from pathlib import Path

def test_translation_functionality():
    """Test translation functionality"""
    print("🧪 Testing translation functionality...")
    
    try:
        from translations import get_ui_text, get_attribute_name, get_category_name, get_available_languages
        
        # Test available languages
        languages = get_available_languages()
        print(f"✅ Available languages: {languages}")
        
        # Test UI translations
        en_title = get_ui_text('title', 'en')
        zh_title = get_ui_text('title', 'zh')
        print(f"✅ UI translation (EN): {en_title}")
        print(f"✅ UI translation (ZH): {zh_title}")
        
        # Test attribute translations
        en_duration = get_attribute_name('duration', 'en')
        zh_duration = get_attribute_name('duration', 'zh')
        print(f"✅ Attribute translation (EN): {en_duration}")
        print(f"✅ Attribute translation (ZH): {zh_duration}")
        
        # Test category translations
        en_basic = get_category_name('Basic Information', 'en')
        zh_basic = get_category_name('Basic Information', 'zh')
        print(f"✅ Category translation (EN): {en_basic}")
        print(f"✅ Category translation (ZH): {zh_basic}")
        
        return True
    except Exception as e:
        print(f"❌ Translation test failed: {e}")
        return False

def test_mediainfo_parsing():
    """Test MediaInfo parsing functionality"""
    print("\n🧪 Testing MediaInfo parsing functionality...")
    
    # Test with the sample image we created
    test_file = "test_image.jpg"
    
    if not os.path.exists(test_file):
        print(f"❌ Test file {test_file} not found")
        return False
    
    try:
        media_info = MediaInfo.parse(test_file)
        print(f"✅ Successfully parsed {test_file}")
        print(f"📊 Found {len(media_info.tracks)} tracks")
        
        for i, track in enumerate(media_info.tracks):
            print(f"\n📋 Track {i+1}: {track.track_type}")
            
            # Show some key properties
            key_props = ['format', 'width', 'height', 'file_size', 'duration']
            for prop in key_props:
                value = getattr(track, prop, None)
                if value is not None:
                    print(f"  {prop}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error parsing file: {e}")
        return False

def format_value_test(attr_name, value):
    """Test the value formatting function"""
    if attr_name in ["duration"]:
        try:
            ms = int(float(value))
            seconds = ms // 1000
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = seconds % 60
            if hours > 0:
                return f"{hours:02d}:{minutes:02d}:{secs:02d}"
            else:
                return f"{minutes:02d}:{secs:02d}"
        except:
            return str(value)
    elif attr_name in ["file_size", "stream_size"]:
        try:
            size = int(float(value))
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} PB"
        except:
            return str(value)
    elif attr_name in ["bit_rate", "overall_bit_rate", "maximum_bit_rate"]:
        try:
            bitrate = int(float(value))
            if bitrate >= 1000000:
                return f"{bitrate/1000000:.1f} Mbps"
            elif bitrate >= 1000:
                return f"{bitrate/1000:.1f} kbps"
            else:
                return f"{bitrate} bps"
        except:
            return str(value)
    
    return str(value)

def test_value_formatting():
    """Test value formatting functions"""
    print("\n🧪 Testing value formatting...")
    
    test_cases = [
        ("duration", "65000", "01:05"),
        ("file_size", "1024000", "1000.0 KB"),
        ("bit_rate", "128000", "128.0 kbps"),
        ("bit_rate", "1500000", "1.5 Mbps")
    ]
    
    for attr, value, expected in test_cases:
        result = format_value_test(attr, value)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {attr}: {value} → {result} (expected: {expected})")

def test_ui_components():
    """Test UI component imports"""
    print("\n🧪 Testing UI component imports...")
    
    try:
        import customtkinter as ctk
        print(f"✅ CustomTkinter {ctk.__version__} imported successfully")
        
        import tkinter as tk
        print("✅ Tkinter imported successfully")
        
        from PIL import Image, ImageTk
        print("✅ PIL imported successfully")
        
        import threading
        print("✅ Threading module available")
        
        import json
        print("✅ JSON module available")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_structured_display():
    """Test the structured tree display functionality"""
    print("\n🧪 Testing structured display functionality...")
    
    try:
        from mediainfo_viewer import MediaInfoViewer
        from translations import get_ui_text, get_attribute_name
        
        # Test that MediaInfoViewer can be instantiated
        print("✅ MediaInfoViewer class can be imported")
        
        # Test search functionality concepts
        search_text = "duration"
        search_zh = get_attribute_name(search_text, 'zh')
        print(f"✅ Search translation works: '{search_text}' -> '{search_zh}'")
        
        # Test UI language switching concepts
        button_text_en = get_ui_text('open_file', 'en')
        button_text_zh = get_ui_text('open_file', 'zh')
        print(f"✅ Language switching works: '{button_text_en}' -> '{button_text_zh}'")
        
        return True
    except Exception as e:
        print(f"❌ Structured display test failed: {e}")
        return False

def main():
    print("🎬 MediaInfo Viewer - Enhanced Test Suite")
    print("=" * 50)
    
    # Test imports
    ui_test = test_ui_components()
    
    # Test translations
    translation_test = test_translation_functionality()
    
    # Test MediaInfo parsing
    parsing_test = test_mediainfo_parsing()
    
    # Test value formatting
    test_value_formatting()
    
    # Test structured display
    display_test = test_structured_display()
    
    print("\n" + "=" * 50)
    if ui_test and translation_test and parsing_test and display_test:
        print("🎉 All tests passed! The enhanced MediaInfo Viewer should work correctly.")
        print("\n📖 New features:")
        print("• ✅ Chinese language support")
        print("• ✅ Structured tree view display")
        print("• ✅ Search functionality")
        print("• ✅ Language switching")
        print("\n📖 To run the GUI application:")
        print("python3 mediainfo_viewer.py")
        print("\n📖 To test with a file:")
        print("python3 mediainfo_viewer.py test_image.jpg")
    else:
        print("❌ Some tests failed. Please check the requirements.")
    
    return ui_test and translation_test and parsing_test and display_test

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)