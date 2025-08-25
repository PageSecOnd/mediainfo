# 🎬 MediaInfo Viewer

一个现代化、直观的媒体文件信息查看器，具有美观的UI界面和右键菜单集成功能。

*A modern, intuitive media file information viewer with beautiful UI and right-click menu integration.*

## ✨ 特性 (Features)

- 🎨 **现代化UI设计** - 使用CustomTkinter构建的现代深色/浅色主题界面
- ⚡ **快速响应** - 多线程处理，启动速度快，操作流畅
- 📊 **详细信息显示** - 完整显示视频、音频、图片等媒体文件的技术参数
- 🖱️ **右键菜单集成** - 支持Windows和Linux的右键菜单集成
- 💾 **信息导出** - 支持导出为文本或JSON格式
- 🎯 **多轨道支持** - 清晰显示多个音视频轨道信息
- 🌍 **跨平台支持** - 支持Windows、Linux和macOS

## 🚀 快速开始

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/PageSecOnd/mediainfo.git
cd mediainfo

# 运行安装脚本
python setup.py
```

### 手动安装

```bash
# 安装依赖包
pip install -r requirements.txt

# 运行程序
python mediainfo_viewer.py
```

## 🔧 右键菜单集成

### Windows
以管理员身份运行：
```cmd
install_context_menu_windows.bat
```

卸载右键菜单：
```cmd
uninstall_context_menu_windows.bat
```

### Linux
```bash
bash install_context_menu_linux.sh
```

### macOS
可以通过Finder直接打开应用程序，或创建Automator服务。

## 📖 使用方法

1. **打开文件**: 点击"打开媒体文件"按钮或通过右键菜单启动
2. **查看信息**: 在左侧轨道列表中选择不同轨道查看详细信息
3. **导出信息**: 点击"导出信息"按钮保存信息到文件

## 🎯 支持的文件格式

- **视频**: MP4, AVI, MKV, MOV, WMV, FLV, WebM, M4V, 3GP
- **音频**: MP3, WAV, FLAC, AAC, M4A, OGG, WMA
- **图片**: JPG, PNG, GIF, BMP, TIFF, WebP

## 📋 系统要求

- Python 3.7+
- 支持的操作系统：Windows 7+, Linux, macOS 10.12+

## 📦 依赖包

- `customtkinter>=5.2.0` - 现代化UI框架
- `pymediainfo>=6.0.1` - MediaInfo库的Python绑定
- `pillow>=10.0.0` - 图像处理
- `darkdetect>=0.8.0` - 系统主题检测

## 🖼️ 界面预览

应用程序提供现代化的界面设计：
- 深色/浅色主题自动切换
- 直观的轨道选择侧栏
- 详细的信息展示区域
- 响应式布局设计

## 🛠️ 开发说明

### 项目结构
```
mediainfo/
├── mediainfo_viewer.py          # 主应用程序
├── requirements.txt             # Python依赖
├── setup.py                    # 安装脚本
├── install_context_menu_windows.bat  # Windows右键菜单安装
├── uninstall_context_menu_windows.bat # Windows右键菜单卸载
├── install_context_menu_linux.sh     # Linux右键菜单安装
└── README.md                   # 文档
```

### 核心特性实现

- **现代UI**: 使用CustomTkinter库实现现代化界面
- **性能优化**: 多线程加载文件，避免UI阻塞
- **信息格式化**: 智能格式化显示时长、文件大小、比特率等
- **跨平台兼容**: 针对不同操作系统的右键菜单集成方案

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

本项目采用MIT许可证。

## 🙏 致谢

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - 现代化UI框架
- [PyMediaInfo](https://github.com/sbraz/pymediainfo) - MediaInfo Python绑定
- [MediaInfo](https://mediaarea.net/MediaInfo) - 强大的媒体分析工具