#!/usr/bin/env python3
"""
Translation module for MediaInfo Viewer
Provides Chinese translations for all MediaInfo attributes and UI elements
"""

# UI element translations
UI_TRANSLATIONS = {
    'en': {
        'title': 'MediaInfo Viewer',
        'open_file': '📁 Open Media File',
        'export_info': '💾 Export Info',
        'tracks': '📋 Tracks',
        'media_information': '📄 Media Information',
        'no_file_selected': 'No file selected',
        'ready': 'Ready',
        'loading': 'Loading file...',
        'file_loaded': 'File loaded successfully',
        'error_loading': 'Error loading file',
        'search_placeholder': '🔍 Search information...',
        'language': 'Language',
        'category': 'Category',
        'attribute': 'Attribute',
        'value': 'Value',
        'welcome_title': '🎬 Welcome to MediaInfo Viewer',
        'welcome_features': 'Features:',
        'welcome_to_start': 'To get started:',
        'supported_formats': 'Supported formats: Video, Audio, Image, and more!'
    },
    'zh': {
        'title': '媒体信息查看器',
        'open_file': '📁 打开媒体文件',
        'export_info': '💾 导出信息',
        'tracks': '📋 音视频轨道',
        'media_information': '📄 媒体信息',
        'no_file_selected': '未选择文件',
        'ready': '就绪',
        'loading': '正在加载文件...',
        'file_loaded': '文件加载成功',
        'error_loading': '文件加载错误',
        'search_placeholder': '🔍 搜索信息...',
        'language': '语言',
        'category': '类别',
        'attribute': '属性',
        'value': '值',
        'welcome_title': '🎬 欢迎使用媒体信息查看器',
        'welcome_features': '功能特性：',
        'welcome_to_start': '开始使用：',
        'supported_formats': '支持格式：视频、音频、图片等多种格式！'
    }
}

# MediaInfo attribute translations
MEDIAINFO_TRANSLATIONS = {
    'en': {
        # Categories
        'Basic Information': 'Basic Information',
        'Video Properties': 'Video Properties', 
        'Audio Properties': 'Audio Properties',
        'Technical Details': 'Technical Details',
        'Metadata': 'Metadata',
        'Other Properties': 'Other Properties',
        
        # Basic Information
        'format': 'Format',
        'format_profile': 'Format Profile',
        'codec_id': 'Codec ID',
        'duration': 'Duration',
        'file_size': 'File Size',
        'overall_bit_rate': 'Overall Bit Rate',
        'track_id': 'Track ID',
        'stream_identifier': 'Stream ID',
        
        # Video Properties
        'width': 'Width',
        'height': 'Height',
        'display_aspect_ratio': 'Aspect Ratio',
        'frame_rate': 'Frame Rate',
        'bit_rate': 'Bit Rate',
        'bit_depth': 'Bit Depth',
        'chroma_subsampling': 'Chroma Subsampling',
        'color_space': 'Color Space',
        'scan_type': 'Scan Type',
        'pixel_aspect_ratio': 'Pixel Aspect Ratio',
        'resolution': 'Resolution',
        
        # Audio Properties
        'channel_s': 'Channels',
        'sampling_rate': 'Sampling Rate',
        'compression_mode': 'Compression Mode',
        'channel_layout': 'Channel Layout',
        'channel_positions': 'Channel Positions',
        
        # Technical Details
        'writing_library': 'Writing Library',
        'encoded_date': 'Encoded Date',
        'tagged_date': 'Tagged Date',
        'color_primaries': 'Color Primaries',
        'transfer_characteristics': 'Transfer Characteristics',
        'matrix_coefficients': 'Matrix Coefficients',
        'commercial_name': 'Commercial Name',
        'internet_media_type': 'MIME Type',
        
        # Metadata
        'title': 'Title',
        'performer': 'Performer',
        'album': 'Album',
        'track_name': 'Track Name',
        'artist': 'Artist',
        'genre': 'Genre',
        'recorded_date': 'Recorded Date',
        'copyright': 'Copyright',
        'comment': 'Comment',
        
        # Additional common attributes
        'maximum_bit_rate': 'Maximum Bit Rate',
        'minimum_bit_rate': 'Minimum Bit Rate',
        'stream_size': 'Stream Size',
        'frame_count': 'Frame Count',
        'delay': 'Delay',
        'language': 'Language',
        'default': 'Default',
        'forced': 'Forced'
    },
    'zh': {
        # Categories
        'Basic Information': '基本信息',
        'Video Properties': '视频属性',
        'Audio Properties': '音频属性', 
        'Technical Details': '技术细节',
        'Metadata': '元数据',
        'Other Properties': '其他属性',
        
        # Basic Information
        'format': '格式',
        'format_profile': '格式配置',
        'codec_id': '编解码器ID',
        'duration': '时长',
        'file_size': '文件大小',
        'overall_bit_rate': '总比特率',
        'track_id': '轨道ID',
        'stream_identifier': '流标识符',
        
        # Video Properties
        'width': '宽度',
        'height': '高度',
        'display_aspect_ratio': '宽高比',
        'frame_rate': '帧率',
        'bit_rate': '比特率',
        'bit_depth': '位深度',
        'chroma_subsampling': '色度子采样',
        'color_space': '色彩空间',
        'scan_type': '扫描方式',
        'pixel_aspect_ratio': '像素宽高比',
        'resolution': '分辨率',
        
        # Audio Properties
        'channel_s': '声道数',
        'sampling_rate': '采样率',
        'compression_mode': '压缩模式',
        'channel_layout': '声道布局',
        'channel_positions': '声道位置',
        
        # Technical Details
        'writing_library': '编码库',
        'encoded_date': '编码日期',
        'tagged_date': '标记日期',
        'color_primaries': '色彩原色',
        'transfer_characteristics': '传输特性',
        'matrix_coefficients': '矩阵系数',
        'commercial_name': '商业名称',
        'internet_media_type': 'MIME类型',
        
        # Metadata
        'title': '标题',
        'performer': '表演者',
        'album': '专辑',
        'track_name': '曲目名称',
        'artist': '艺术家',
        'genre': '流派',
        'recorded_date': '录制日期',
        'copyright': '版权',
        'comment': '注释',
        
        # Additional common attributes
        'maximum_bit_rate': '最大比特率',
        'minimum_bit_rate': '最小比特率',
        'stream_size': '流大小',
        'frame_count': '帧数',
        'delay': '延迟',
        'language': '语言',
        'default': '默认',
        'forced': '强制'
    }
}

def get_ui_text(key, language='en'):
    """Get UI text translation"""
    return UI_TRANSLATIONS.get(language, UI_TRANSLATIONS['en']).get(key, key)

def get_attribute_name(attribute, language='en'):
    """Get translated attribute name"""
    return MEDIAINFO_TRANSLATIONS.get(language, MEDIAINFO_TRANSLATIONS['en']).get(attribute, attribute.replace('_', ' ').title())

def get_category_name(category, language='en'):
    """Get translated category name"""
    return MEDIAINFO_TRANSLATIONS.get(language, MEDIAINFO_TRANSLATIONS['en']).get(category, category)

def get_available_languages():
    """Get list of available languages"""
    return list(UI_TRANSLATIONS.keys())