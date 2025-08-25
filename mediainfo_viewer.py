#!/usr/bin/env python3
"""
Modern MediaInfo Viewer
A beautiful and intuitive media file information viewer with modern UI
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from pymediainfo import MediaInfo
from PIL import Image, ImageTk
import threading
import json
from pathlib import Path
import darkdetect

# Set appearance mode
ctk.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class MediaInfoViewer:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("MediaInfo Viewer")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Set window icon
        try:
            # Try to set icon if available
            self.root.iconbitmap("icon.ico")
        except:
            pass
            
        self.setup_ui()
        self.media_info = None
        
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
            text="📁 Open Media File",
            command=self.open_file,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.open_button.pack(side="left", padx=10, pady=10)
        
        # File path label
        self.file_path_label = ctk.CTkLabel(
            self.top_frame, 
            text="No file selected", 
            font=ctk.CTkFont(size=12)
        )
        self.file_path_label.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        # Export button
        self.export_button = ctk.CTkButton(
            self.top_frame,
            text="💾 Export Info",
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
            text="Ready", 
            font=ctk.CTkFont(size=11)
        )
        self.status_label.pack(side="left", padx=10, pady=5)
    
    def setup_main_content(self):
        # Left sidebar for track selection
        self.sidebar = ctk.CTkFrame(self.root, width=200)
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)
        self.sidebar.grid_propagate(False)
        
        self.sidebar_label = ctk.CTkLabel(
            self.sidebar, 
            text="📋 Tracks", 
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
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Content title
        self.content_title = ctk.CTkLabel(
            self.content_frame, 
            text="📄 Media Information", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.content_title.grid(row=0, column=0, pady=10, sticky="w", padx=20)
        
        # Scrollable text area for media info
        self.info_textbox = ctk.CTkTextbox(
            self.content_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word"
        )
        self.info_textbox.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Default message
        self.show_welcome_message()
    
    def show_welcome_message(self):
        welcome_text = """
🎬 Welcome to MediaInfo Viewer

This modern and intuitive application displays comprehensive media file information.

Features:
• 🎯 Fast and responsive interface
• 📊 Detailed track information
• 🎨 Modern dark/light theme support
• 💾 Export capabilities
• 🖱️ Right-click integration

To get started:
1. Click "Open Media File" or drag & drop a file
2. Select tracks from the sidebar to view details
3. Export information if needed

Supported formats: Video, Audio, Image, and more!
        """
        self.info_textbox.delete("1.0", tk.END)
        self.info_textbox.insert("1.0", welcome_text)
        self.info_textbox.configure(state="disabled")
    
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
        
        threading.Thread(target=load_thread, daemon=True).start()
    
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
        
        # Format track information nicely
        info_text = self.format_track_info(track)
        
        # Update content
        self.info_textbox.configure(state="normal")
        self.info_textbox.delete("1.0", tk.END)
        self.info_textbox.insert("1.0", info_text)
        self.info_textbox.configure(state="disabled")
        
        # Update title
        track_type = track.track_type or "Unknown"
        self.content_title.configure(text=f"📄 {track_type} Track Information")
    
    def format_track_info(self, track):
        """Format track information in a beautiful and organized way"""
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
        
        for category in relevant_categories:
            category_data = []
            for attr in categories[category]:
                value = getattr(track, attr, None)
                if value is not None:
                    # Format the attribute name nicely
                    display_name = attr.replace("_", " ").title()
                    
                    # Format specific values
                    formatted_value = self.format_value(attr, value)
                    category_data.append(f"  {display_name:<25}: {formatted_value}")
            
            if category_data:
                info_lines.append(f"📋 {category}")
                info_lines.append("-" * 40)
                info_lines.extend(category_data)
                info_lines.append("")
        
        # Additional attributes not in categories
        other_attrs = []
        for attr_name in dir(track):
            if (not attr_name.startswith('_') and 
                not callable(getattr(track, attr_name)) and
                attr_name not in [item for sublist in categories.values() for item in sublist]):
                
                value = getattr(track, attr_name)
                if value is not None and str(value).strip():
                    display_name = attr_name.replace("_", " ").title()
                    formatted_value = self.format_value(attr_name, value)
                    other_attrs.append(f"  {display_name:<25}: {formatted_value}")
        
        if other_attrs:
            info_lines.append("📋 Other Properties")
            info_lines.append("-" * 40)
            info_lines.extend(other_attrs)
        
        return "\n".join(info_lines)
    
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