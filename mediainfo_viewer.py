#!/usr/bin/env python3
"""
Modern MediaInfo Viewer
A beautiful and intuitive media file information viewer with modern UI
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import customtkinter as ctk
from pymediainfo import MediaInfo
from PIL import Image, ImageTk
import threading
import json
from pathlib import Path
import darkdetect
from translations import get_ui_text, get_attribute_name, get_category_name, get_available_languages

# Set appearance mode
ctk.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class MediaInfoViewer:
    def __init__(self):
        self.root = ctk.CTk()
        self.current_language = 'en'  # Default language
        self.root.title(get_ui_text('title', self.current_language))
        self.root.geometry("1200x800")  # Increased size for better layout
        self.root.minsize(1000, 700)
        
        # Set window icon
        try:
            # Try to set icon if available
            self.root.iconbitmap("icon.ico")
        except:
            pass
            
        self.setup_ui()
        self.media_info = None
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        
        # Check if file was passed as argument
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            if os.path.exists(file_path):
                self.load_file(file_path)
    
    def setup_ui(self):
        # Configure grid weight
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Top frame for controls
        self.top_frame = ctk.CTkFrame(self.root)
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        # Open file button
        self.open_button = ctk.CTkButton(
            self.top_frame, 
            text=get_ui_text('open_file', self.current_language),
            command=self.open_file,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.open_button.pack(side="left", padx=10, pady=10)
        
        # File path label
        self.file_path_label = ctk.CTkLabel(
            self.top_frame, 
            text=get_ui_text('no_file_selected', self.current_language), 
            font=ctk.CTkFont(size=12)
        )
        self.file_path_label.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        # Language selector
        self.language_label = ctk.CTkLabel(
            self.top_frame,
            text=get_ui_text('language', self.current_language) + ":",
            font=ctk.CTkFont(size=12)
        )
        self.language_label.pack(side="right", padx=(10, 5), pady=10)
        
        self.language_combo = ctk.CTkComboBox(
            self.top_frame,
            values=["English", "中文"],
            command=self.change_language,
            width=100,
            height=35
        )
        self.language_combo.set("English")
        self.language_combo.pack(side="right", padx=5, pady=10)
        
        # Export button
        self.export_button = ctk.CTkButton(
            self.top_frame,
            text=get_ui_text('export_info', self.current_language),
            command=self.export_info,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled"
        )
        self.export_button.pack(side="right", padx=10, pady=10)
        
        # Main content area with sidebar
        self.setup_main_content()
        
        # Status bar
        self.status_frame = ctk.CTkFrame(self.root, height=30)
        self.status_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text=get_ui_text('ready', self.current_language), 
            font=ctk.CTkFont(size=11)
        )
        self.status_label.pack(side="left", padx=10, pady=5)
    
    def setup_main_content(self):
        # Left sidebar for track selection
        self.sidebar = ctk.CTkFrame(self.root, width=250)  # Wider sidebar
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)
        self.sidebar.grid_propagate(False)
        
        self.sidebar_label = ctk.CTkLabel(
            self.sidebar, 
            text=get_ui_text('tracks', self.current_language), 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.sidebar_label.pack(pady=10)
        
        # Scrollable frame for track list
        self.track_frame = ctk.CTkScrollableFrame(self.sidebar)
        self.track_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Main content area
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=5)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=1)
        
        # Content title
        self.content_title = ctk.CTkLabel(
            self.content_frame, 
            text=get_ui_text('media_information', self.current_language), 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.content_title.grid(row=0, column=0, pady=10, sticky="w", padx=20)
        
        # Search frame
        self.search_frame = ctk.CTkFrame(self.content_frame)
        self.search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.search_frame.grid_columnconfigure(0, weight=1)
        
        # Search entry
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text=get_ui_text('search_placeholder', self.current_language),
            textvariable=self.search_var,
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.search_entry.pack(fill="x", padx=10, pady=10)
        
        # Create main info display using Treeview for structured data
        self.setup_treeview()
        
        # Default message
        self.show_welcome_message()
    
    def setup_treeview(self):
        """Setup the structured treeview for displaying media information"""
        # Create frame for treeview
        self.tree_frame = ctk.CTkFrame(self.content_frame)
        self.tree_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        
        # Create treeview with scrollbars
        self.tree = ttk.Treeview(self.tree_frame, columns=("value",), show="tree headings")
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Configure columns
        self.tree.heading("#0", text=get_ui_text('attribute', self.current_language))
        self.tree.heading("value", text=get_ui_text('value', self.current_language))
        self.tree.column("#0", width=300, minwidth=200)
        self.tree.column("value", width=400, minwidth=200)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Configure treeview style
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
    
    def change_language(self, language_name):
        """Change the application language"""
        if language_name == "中文":
            self.current_language = 'zh'
        else:
            self.current_language = 'en'
        
        # Update UI elements
        self.update_ui_language()
        
        # Refresh media info display if available
        if self.media_info:
            self.display_media_info()
    
    def update_ui_language(self):
        """Update all UI elements with current language"""
        self.root.title(get_ui_text('title', self.current_language))
        self.open_button.configure(text=get_ui_text('open_file', self.current_language))
        self.export_button.configure(text=get_ui_text('export_info', self.current_language))
        self.sidebar_label.configure(text=get_ui_text('tracks', self.current_language))
        self.content_title.configure(text=get_ui_text('media_information', self.current_language))
        self.language_label.configure(text=get_ui_text('language', self.current_language) + ":")
        self.search_entry.configure(placeholder_text=get_ui_text('search_placeholder', self.current_language))
        self.status_label.configure(text=get_ui_text('ready', self.current_language))
        
        # Update treeview headers
        if hasattr(self, 'tree'):
            self.tree.heading("#0", text=get_ui_text('attribute', self.current_language))
            self.tree.heading("value", text=get_ui_text('value', self.current_language))
    
    def on_search_change(self, *args):
        """Handle search text changes"""
        if hasattr(self, 'current_track_data'):
            self.filter_tree_items()
    
    def filter_tree_items(self):
        """Filter tree items based on search text"""
        search_text = self.search_var.get().lower()
        if not search_text:
            # Show all items
            for item in self.tree.get_children():
                self.show_tree_item(item, True)
        else:
            # Filter items
            for item in self.tree.get_children():
                self.filter_tree_item(item, search_text)
    
    def filter_tree_item(self, item, search_text):
        """Recursively filter tree items"""
        item_text = self.tree.item(item, "text").lower()
        item_value = self.tree.item(item, "values")
        item_value_text = item_value[0].lower() if item_value else ""
        
        # Check if item matches search
        matches = search_text in item_text or search_text in item_value_text
        
        # Check children
        children = self.tree.get_children(item)
        child_matches = False
        for child in children:
            if self.filter_tree_item(child, search_text):
                child_matches = True
        
        # Show item if it matches or has matching children
        show_item = matches or child_matches
        self.show_tree_item(item, show_item)
        
        if show_item and child_matches:
            self.tree.item(item, open=True)
        
    def show_welcome_message(self):
        """Show welcome message in the treeview"""
        # Clear the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add welcome items
        welcome_node = self.tree.insert("", "end", text=get_ui_text('welcome_title', self.current_language), values=("",), open=True)
        
        features = [
            "🎯 快速响应界面" if self.current_language == 'zh' else "🎯 Fast and responsive interface",
            "📊 详细轨道信息" if self.current_language == 'zh' else "📊 Detailed track information", 
            "🎨 现代深色/浅色主题" if self.current_language == 'zh' else "🎨 Modern dark/light theme support",
            "💾 导出功能" if self.current_language == 'zh' else "💾 Export capabilities",
            "🔍 搜索功能" if self.current_language == 'zh' else "🔍 Search functionality",
            "🌍 中英文支持" if self.current_language == 'zh' else "🌍 Chinese/English support"
        ]
        
        features_node = self.tree.insert(welcome_node, "end", text=get_ui_text('welcome_features', self.current_language), values=("",), open=True)
        for feature in features:
            self.tree.insert(features_node, "end", text=feature, values=("",))
        
        # Getting started instructions
        instructions = [
            "1. " + ("点击'打开媒体文件'按钮" if self.current_language == 'zh' else "Click 'Open Media File' button"),
            "2. " + ("从侧边栏选择轨道查看详情" if self.current_language == 'zh' else "Select tracks from sidebar to view details"),
            "3. " + ("使用搜索功能快速查找信息" if self.current_language == 'zh' else "Use search to quickly find information"),
            "4. " + ("如需要可导出信息" if self.current_language == 'zh' else "Export information if needed")
        ]
        
        start_node = self.tree.insert(welcome_node, "end", text=get_ui_text('welcome_to_start', self.current_language), values=("",), open=True)
        for instruction in instructions:
            self.tree.insert(start_node, "end", text=instruction, values=("",))
        
        formats_node = self.tree.insert(welcome_node, "end", text=get_ui_text('supported_formats', self.current_language), values=("",))
    
    def load_file(self, file_path):
        # Update status
        self.update_status(get_ui_text('loading', self.current_language))
        self.file_path_label.configure(text=os.path.basename(file_path))
        
        # Load media info in separate thread to keep UI responsive
        def load_thread():
            try:
                self.media_info = MediaInfo.parse(file_path)
                self.root.after(0, self.display_media_info)
                self.root.after(0, lambda: self.update_status(get_ui_text('file_loaded', self.current_language)))
                self.root.after(0, lambda: self.export_button.configure(state="normal"))
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Error loading file: {str(e)}"))
                self.root.after(0, lambda: self.update_status(get_ui_text('error_loading', self.current_language)))
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def show_tree_item(self, item, show):
        """Show or hide a tree item"""
        if show:
            self.tree.reattach(item, self.tree.parent(item), self.tree.index(item))
        else:
            self.tree.detach(item)
    
    def open_file(self):
        file_types = [
            ("All Media Files", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.mp3 *.wav *.flac *.aac *.m4a *.ogg *.jpg *.jpeg *.png *.gif *.bmp *.tiff"),
            ("Video Files", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.m4v *.3gp"),
            ("Audio Files", "*.mp3 *.wav *.flac *.aac *.m4a *.ogg *.wma"),
            ("Image Files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.webp"),
            ("All Files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Media File",
            filetypes=file_types
        )
        
        if filename:
            self.load_file(filename)
    
    def load_file(self, file_path):
        # Update status
        self.update_status("Loading file...")
        self.file_path_label.configure(text=os.path.basename(file_path))
        
        # Load media info in separate thread to keep UI responsive
        def load_thread():
            try:
                self.media_info = MediaInfo.parse(file_path)
                self.root.after(0, self.display_media_info)
                self.root.after(0, lambda: self.update_status("File loaded successfully"))
                self.root.after(0, lambda: self.export_button.configure(state="normal"))
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Error loading file: {str(e)}"))
                self.root.after(0, lambda: self.update_status("Error loading file"))
        
    def display_media_info(self):
        # Clear previous track buttons
        for widget in self.track_frame.winfo_children():
            widget.destroy()
        
        if not self.media_info:
            return
        
        # Create track buttons
        self.track_buttons = []
        for i, track in enumerate(self.media_info.tracks):
            track_type = track.track_type or "Unknown"
            if self.current_language == 'zh':
                type_map = {
                    'General': '常规',
                    'Video': '视频', 
                    'Audio': '音频',
                    'Text': '文本',
                    'Image': '图像',
                    'Menu': '菜单'
                }
                track_type = type_map.get(track_type, track_type)
            
            track_name = f"{track_type}"
            
            if track.track_id:
                track_name += f" #{track.track_id}"
            
            if hasattr(track, 'format') and track.format:
                track_name += f" ({track.format})"
            
            button = ctk.CTkButton(
                self.track_frame,
                text=track_name,
                command=lambda idx=i: self.show_track_info(idx),
                height=40,
                anchor="w"
            )
            button.pack(fill="x", pady=5)
            self.track_buttons.append(button)
        
        # Show general info by default
        if self.media_info.tracks:
            self.show_track_info(0)
    
    def show_track_info(self, track_index):
        if not self.media_info or track_index >= len(self.media_info.tracks):
            return
        
        track = self.media_info.tracks[track_index]
        self.current_track_data = track
        
        # Clear the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Populate tree with track information
        self.populate_track_tree(track)
        
        # Update title
        track_type = track.track_type or "Unknown"
        if self.current_language == 'zh':
            type_map = {
                'General': '常规',
                'Video': '视频',
                'Audio': '音频', 
                'Text': '文本',
                'Image': '图像',
                'Menu': '菜单'
            }
            track_type = type_map.get(track_type, track_type)
        
        title_text = f"📄 {track_type} " + ("轨道信息" if self.current_language == 'zh' else "Track Information")
        self.content_title.configure(text=title_text)
    
    def populate_track_tree(self, track):
        """Populate the tree with track information in a structured way"""
        track_type = track.track_type or "Unknown"
        
        # Organize attributes by category
        categories = {
            "Basic Information": [
                "format", "format_profile", "codec_id", "duration", "file_size",
                "overall_bit_rate", "track_id", "stream_identifier"
            ],
            "Video Properties": [
                "width", "height", "display_aspect_ratio", "frame_rate", "bit_rate",
                "bit_depth", "chroma_subsampling", "color_space", "scan_type", "pixel_aspect_ratio"
            ],
            "Audio Properties": [
                "channel_s", "sampling_rate", "bit_rate", "compression_mode",
                "channel_layout", "bit_depth", "channel_positions"
            ],
            "Technical Details": [
                "writing_library", "encoded_date", "tagged_date", "color_primaries",
                "transfer_characteristics", "matrix_coefficients", "commercial_name", "internet_media_type"
            ],
            "Metadata": [
                "title", "performer", "album", "track_name", "artist", "genre",
                "recorded_date", "copyright", "comment"
            ]
        }
        
        # Display relevant categories based on track type
        relevant_categories = ["Basic Information"]
        if track_type.lower() == "video":
            relevant_categories.extend(["Video Properties", "Technical Details"])
        elif track_type.lower() == "audio":
            relevant_categories.extend(["Audio Properties", "Metadata"])
        else:
            relevant_categories.extend(["Technical Details", "Metadata"])
        
        # Add categories as tree nodes
        for category in relevant_categories:
            category_items = []
            for attr in categories[category]:
                value = getattr(track, attr, None)
                if value is not None and str(value).strip():
                    category_items.append((attr, value))
            
            if category_items:
                # Translate category name
                category_name = get_category_name(category, self.current_language)
                category_node = self.tree.insert("", "end", text=f"📋 {category_name}", values=("",), open=True)
                
                for attr, value in category_items:
                    # Format the attribute name and value
                    display_name = get_attribute_name(attr, self.current_language)
                    formatted_value = self.format_value(attr, value)
                    self.tree.insert(category_node, "end", text=display_name, values=(formatted_value,))
        
        # Add other properties not in categories
        other_attrs = []
        for attr_name in dir(track):
            if (not attr_name.startswith('_') and 
                not callable(getattr(track, attr_name)) and
                attr_name not in [item for sublist in categories.values() for item in sublist]):
                
                value = getattr(track, attr_name)
                if value is not None and str(value).strip():
                    other_attrs.append((attr_name, value))
        
        if other_attrs:
            other_category = get_category_name("Other Properties", self.current_language)
            other_node = self.tree.insert("", "end", text=f"📋 {other_category}", values=("",), open=False)
            
            for attr_name, value in other_attrs:
                display_name = get_attribute_name(attr_name, self.current_language)
                formatted_value = self.format_value(attr_name, value)
    def export_text(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            title = "媒体信息报告" if self.current_language == 'zh' else "MEDIA INFORMATION REPORT"
            f.write(f"{title}\n")
            f.write("=" * 60 + "\n\n")
            
            for i, track in enumerate(self.media_info.tracks):
                f.write(self.format_track_info_for_export(track))
                f.write("\n\n" + "=" * 60 + "\n\n")
    
    def format_track_info_for_export(self, track):
        """Format track information for export (legacy text format)"""
        info_lines = []
        track_type = track.track_type or "Unknown"
        
        # Header
        info_lines.append(f"{'='*60}")
        info_lines.append(f"{track_type.upper()} TRACK INFORMATION")
        info_lines.append(f"{'='*60}")
        info_lines.append("")
        
        # Organize attributes by category
        categories = {
            "Basic Information": [
                "format", "format_profile", "codec_id", "duration", "file_size",
                "overall_bit_rate", "track_id", "stream_identifier"
            ],
            "Video Properties": [
                "width", "height", "display_aspect_ratio", "frame_rate", "bit_rate",
                "bit_depth", "chroma_subsampling", "color_space", "scan_type"
            ],
            "Audio Properties": [
                "channel_s", "sampling_rate", "bit_rate", "compression_mode",
                "channel_layout", "bit_depth"
            ],
            "Technical Details": [
                "writing_library", "encoded_date", "tagged_date", "color_primaries",
                "transfer_characteristics", "matrix_coefficients"
            ],
            "Metadata": [
                "title", "performer", "album", "track_name", "artist", "genre",
                "recorded_date", "copyright"
            ]
        }
        
        # Display relevant categories based on track type
        relevant_categories = ["Basic Information"]
        if track_type.lower() == "video":
            relevant_categories.extend(["Video Properties", "Technical Details"])
        elif track_type.lower() == "audio":
            relevant_categories.extend(["Audio Properties", "Metadata"])
        else:
            relevant_categories.extend(["Technical Details", "Metadata"])
        # Add categories as tree nodes
        for category in relevant_categories:
            category_items = []
            for attr in categories[category]:
                value = getattr(track, attr, None)
                if value is not None and str(value).strip():
                    category_items.append((attr, value))
            
            if category_items:
                # Translate category name
                category_name = get_category_name(category, self.current_language)
                category_node = self.tree.insert("", "end", text=f"📋 {category_name}", values=("",), open=True)
                
                for attr, value in category_items:
                    # Format the attribute name and value
                    display_name = get_attribute_name(attr, self.current_language)
                    formatted_value = self.format_value(attr, value)
                    self.tree.insert(category_node, "end", text=display_name, values=(formatted_value,))
        
        # Add other properties not in categories
        other_attrs = []
        for attr_name in dir(track):
            if (not attr_name.startswith('_') and 
                not callable(getattr(track, attr_name)) and
                attr_name not in [item for sublist in categories.values() for item in sublist]):
                
                value = getattr(track, attr_name)
                if value is not None and str(value).strip():
                    other_attrs.append((attr_name, value))
        
        if other_attrs:
            other_category = get_category_name("Other Properties", self.current_language)
            other_node = self.tree.insert("", "end", text=f"📋 {other_category}", values=("",), open=False)
            
            for attr_name, value in other_attrs:
                display_name = get_attribute_name(attr_name, self.current_language)
                formatted_value = self.format_value(attr_name, value)
                self.tree.insert(other_node, "end", text=display_name, values=(formatted_value,))
    
    def show_error(self, message):
        messagebox.showerror("Error", message)
        # Clear the tree and show error
        for item in self.tree.get_children():
            self.tree.delete(item)
        error_node = self.tree.insert("", "end", text="❌ Error", values=(message,))
    
    def format_value(self, attr_name, value):
        """Format values for better display"""
        if attr_name in ["duration"]:
            # Convert milliseconds to readable format
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
            # Format file size
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
            # Format bit rate
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
    
    def export_info(self):
        if not self.media_info:
            messagebox.showwarning("Warning", "No media information to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Media Information",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("JSON Files", "*.json"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            try:
                if file_path.endswith('.json'):
                    self.export_json(file_path)
                else:
                    self.export_text(file_path)
                
                messagebox.showinfo("Success", f"Information exported to {file_path}")
                self.update_status(f"Exported to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def export_text(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("MEDIA INFORMATION REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            for i, track in enumerate(self.media_info.tracks):
                f.write(self.format_track_info(track))
                f.write("\n\n" + "=" * 60 + "\n\n")
    
    def export_json(self, file_path):
        data = []
        for track in self.media_info.tracks:
            track_data = {}
            for attr_name in dir(track):
                if (not attr_name.startswith('_') and 
                    not callable(getattr(track, attr_name))):
                    value = getattr(track, attr_name)
                    if value is not None:
                        track_data[attr_name] = str(value)
            data.append(track_data)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def show_error(self, message):
        messagebox.showerror("Error", message)
        self.info_textbox.configure(state="normal")
        self.info_textbox.delete("1.0", tk.END)
        self.info_textbox.insert("1.0", f"❌ Error: {message}")
        self.info_textbox.configure(state="disabled")
    
    def update_status(self, message):
        self.status_label.configure(text=message)
    
    def run(self):
        self.root.mainloop()

def main():
    app = MediaInfoViewer()
    app.run()

if __name__ == "__main__":
    main()