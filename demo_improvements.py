#!/usr/bin/env python3
"""
Demo script showing the enhanced MediaInfo Viewer features
"""

import os
from pymediainfo import MediaInfo
from translations import get_ui_text, get_attribute_name, get_category_name

def demo_old_vs_new():
    """Demonstrate the difference between old and new display"""
    print("🎬 MediaInfo Viewer - Before vs After Demo")
    print("=" * 60)
    
    # Parse test file
    test_file = "test_image.jpg"
    if not os.path.exists(test_file):
        print("❌ Test file not found. Please run: python3 test_mediainfo.py first")
        return
    
    media_info = MediaInfo.parse(test_file)
    track = media_info.tracks[0] if media_info.tracks else None
    
    if not track:
        print("❌ No track information found")
        return
    
    print("\n📋 OLD APPROACH - Text-based Display")
    print("=" * 40)
    demo_old_style(track)
    
    print("\n\n📊 NEW APPROACH - Structured Tree Display")
    print("=" * 40)
    demo_new_style(track)
    
    print("\n\n🔍 SEARCH FUNCTIONALITY DEMO")
    print("=" * 40)
    demo_search_functionality(track)
    
    print("\n\n🌍 BILINGUAL SUPPORT DEMO")
    print("=" * 40)
    demo_bilingual_support(track)

def demo_old_style(track):
    """Show how the old text-based display looked"""
    print("Problems with old approach:")
    print("• Hard to scan for specific information")
    print("• No search capability") 
    print("• English only")
    print("• Plain text format\n")
    
    print("Old display output:")
    print("-" * 30)
    print("GENERAL TRACK INFORMATION")
    print("-" * 30)
    print("Format                   : JPEG")
    print("File Size                : 825 bytes")
    print("Width                    : 100")
    print("Height                   : 100")
    print("(... lots more text to scroll through ...)")

def demo_new_style(track):
    """Show the new structured tree display"""
    print("Improvements in new approach:")
    print("✅ Hierarchical tree structure")
    print("✅ Real-time search functionality")
    print("✅ Bilingual support (EN/中文)")
    print("✅ Expandable categories")
    print("✅ Better visual organization\n")
    
    print("New structured display:")
    print("-" * 30)
    
    # Simulate tree structure
    categories = {
        "Basic Information": ["format", "file_size"],
        "Image Properties": ["width", "height"]
    }
    
    for category, attrs in categories.items():
        print(f"├── 📋 {category}")
        for attr in attrs:
            value = getattr(track, attr, None)
            if value is not None:
                display_name = get_attribute_name(attr, 'en')
                formatted_value = format_value_demo(attr, value)
                print(f"│   ├── {display_name}: {formatted_value}")
        print("│")

def demo_search_functionality(track):
    """Demonstrate search capabilities"""
    print("Search examples (case-insensitive, works in both languages):")
    print("")
    
    search_demos = [
        ("format", "Find format information"),
        ("size", "Find file size"),
        ("width", "Find image dimensions"),
        ("格式", "Search in Chinese for format"),
        ("大小", "Search in Chinese for size")
    ]
    
    for search_term, description in search_demos:
        print(f"🔍 Search: '{search_term}' ({description})")
        
        # Simulate search results
        found_items = []
        for attr_name in dir(track):
            if not attr_name.startswith('_') and not callable(getattr(track, attr_name)):
                value = getattr(track, attr_name)
                if value is not None:
                    en_name = get_attribute_name(attr_name, 'en').lower()
                    zh_name = get_attribute_name(attr_name, 'zh').lower()
                    
                    if (search_term.lower() in en_name or 
                        search_term.lower() in zh_name or
                        search_term.lower() in str(value).lower()):
                        found_items.append((attr_name, value))
        
        if found_items:
            for attr, value in found_items[:2]:  # Show first 2 matches
                en_name = get_attribute_name(attr, 'en')
                zh_name = get_attribute_name(attr, 'zh')
                formatted_value = format_value_demo(attr, value)
                print(f"  ✅ {en_name} ({zh_name}): {formatted_value}")
        else:
            print("  ❌ No matches found")
        print()

def demo_bilingual_support(track):
    """Demonstrate bilingual capabilities"""
    print("Complete bilingual support for all elements:")
    print("")
    
    # UI elements
    print("📱 UI Elements:")
    ui_elements = ['title', 'open_file', 'export_info', 'search_placeholder']
    for element in ui_elements:
        en = get_ui_text(element, 'en')
        zh = get_ui_text(element, 'zh')
        print(f"  {element}: {en} ↔ {zh}")
    
    print("\n📊 Category Names:")
    categories = ['Basic Information', 'Video Properties', 'Audio Properties']
    for category in categories:
        en = get_category_name(category, 'en')
        zh = get_category_name(category, 'zh')
        print(f"  {en} ↔ {zh}")
    
    print("\n🏷️ Attribute Names:")
    attributes = ['format', 'duration', 'file_size', 'width', 'height']
    for attr in attributes:
        en = get_attribute_name(attr, 'en')
        zh = get_attribute_name(attr, 'zh')
        print(f"  {en} ↔ {zh}")

def format_value_demo(attr_name, value):
    """Simple value formatting for demo"""
    if attr_name == "file_size":
        try:
            size = int(float(value))
            if size < 1024:
                return f"{size} B"
            elif size < 1024*1024:
                return f"{size/1024:.1f} KB"
            else:
                return f"{size/(1024*1024):.1f} MB"
        except:
            return str(value)
    return str(value)

if __name__ == "__main__":
    demo_old_vs_new()
    
    print("\n" + "=" * 60)
    print("🎉 SUMMARY OF IMPROVEMENTS")
    print("=" * 60)
    print("✅ Replaced hard-to-scan text with structured tree view")
    print("✅ Added real-time search for instant information access")
    print("✅ Implemented complete Chinese language support")
    print("✅ Enhanced user experience with expandable categories")
    print("✅ Maintained all original functionality while improving usability")
    print("\nThe MediaInfo Viewer is now much more user-friendly! 🚀")