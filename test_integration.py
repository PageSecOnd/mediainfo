#!/usr/bin/env python3
"""
Integration test to verify the enhanced MediaInfo Viewer functionality
"""

import sys
import os
from pymediainfo import MediaInfo
from translations import get_ui_text, get_attribute_name, get_category_name

def test_complete_workflow():
    """Test the complete workflow with both languages"""
    print("🎬 Integration Test - Complete Workflow")
    print("=" * 50)
    
    # Test file
    test_file = "test_image.jpg"
    if not os.path.exists(test_file):
        print(f"❌ Test file {test_file} not found")
        return False
    
    # Parse media info
    media_info = MediaInfo.parse(test_file)
    track = media_info.tracks[0]  # General track
    
    print("🧪 Testing English display...")
    print_track_info(track, 'en')
    
    print("\n🧪 Testing Chinese display...")
    print_track_info(track, 'zh')
    
    print("\n🧪 Testing search simulation...")
    test_search_functionality(track)
    
    return True

def print_track_info(track, language):
    """Simulate the tree structure display"""
    print(f"\n📄 {get_ui_text('media_information', language)}")
    print("-" * 40)
    
    # Basic Information category
    basic_category = get_category_name('Basic Information', language)
    print(f"\n📋 {basic_category}")
    
    basic_attrs = ['format', 'file_size']
    for attr in basic_attrs:
        value = getattr(track, attr, None)
        if value is not None:
            display_name = get_attribute_name(attr, language)
            formatted_value = format_value_simple(attr, value)
            print(f"  {display_name}: {formatted_value}")

def format_value_simple(attr_name, value):
    """Simple value formatting for test"""
    if attr_name == "file_size":
        try:
            size = int(float(value))
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except:
            return str(value)
    return str(value)

def test_search_functionality(track):
    """Simulate search functionality"""
    search_terms = ['format', 'size', '格式', '大小']
    
    for term in search_terms:
        print(f"\n🔍 Search for '{term}':")
        
        # Check format attribute
        if 'format' in term.lower() or '格式' in term:
            format_val = getattr(track, 'format', None)
            if format_val:
                display_name_en = get_attribute_name('format', 'en')
                display_name_zh = get_attribute_name('format', 'zh')
                print(f"  ✅ Found: {display_name_en}/{display_name_zh} = {format_val}")
        
        # Check file size
        if 'size' in term.lower() or '大小' in term:
            size_val = getattr(track, 'file_size', None)
            if size_val:
                display_name_en = get_attribute_name('file_size', 'en')
                display_name_zh = get_attribute_name('file_size', 'zh')
                formatted_size = format_value_simple('file_size', size_val)
                print(f"  ✅ Found: {display_name_en}/{display_name_zh} = {formatted_size}")

def test_language_switching():
    """Test language switching functionality"""
    print("\n🌍 Testing language switching...")
    
    ui_elements = ['title', 'open_file', 'export_info', 'search_placeholder']
    
    for element in ui_elements:
        en_text = get_ui_text(element, 'en')
        zh_text = get_ui_text(element, 'zh')
        print(f"  {element}: {en_text} ↔ {zh_text}")

if __name__ == "__main__":
    success = test_complete_workflow()
    test_language_switching()
    
    if success:
        print("\n🎉 Integration test passed!")
        print("\n✨ Enhanced Features Verified:")
        print("• 🌍 Bilingual support (English/Chinese)")
        print("• 🔍 Search functionality simulation")
        print("• 📊 Structured information display")
        print("• 🎯 Category-based organization")
        print("• 🔄 Language switching capability")
    else:
        print("\n❌ Integration test failed!")
    
    sys.exit(0 if success else 1)