# VSEndless - GPU Accelerated Render Engine for Blender 4.5+# VSEndless Render Engine 4 (vsendless4)



A powerful, GPU-accelerated render engine designed specifically for Blender's Video Sequence Editor (VSE) with advanced NVIDIA NVENC support and hardware acceleration.A modular, robust, and extensible Blender VSE render engine addon, designed using Algebraic Pipeline Theory (APT) methodology.



---## Structure

- `operators/`: Rendering and processing operators

[![GitHub Release](https://img.shields.io/github/v/release/yavru421/VSEndless-Render-Engine-blender4.5)](https://github.com/yavru421/VSEndless-Render-Engine-blender4.5/releases)- `properties/`: Custom properties and settings

[![Blender](https://img.shields.io/badge/Blender-4.5%2B-orange)](https://www.blender.org/)- `ui/`: Panels and UI integration

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)- `utils/`: Utilities (ffmpeg, sequence, presets, etc.)

[![Sponsor](https://img.shields.io/badge/Sponsor%20Me-GitHub%20Sponsors-blue)](https://github.com/sponsors/yavru421)

## APT Pipeline

---Each module is a pipeline stage with explicit input/output variables and dependencies. See code comments for algebraic notation.



## 🚀 Features## Integration

- Ready for API/tool-calling integration (see `llama-chat-completions.yaml`)

### GPU Acceleration- Designed for maintainability and extensibility

- **NVIDIA NVENC Hardware Encoding**: Blazing-fast H.264 and H.265 encoding
- **CUDA Acceleration**: GPU-powered video processing and filtering
- **Hardware Decoding**: NVDEC support for accelerated input processing
- **Smart GPU Detection**: Automatic GPU capability detection and optimization

### Advanced Video Processing
- **Multi-format Support**: H.264, H.265/HEVC, ProRes, and more
- **Flexible Rate Control**: CBR, VBR, CQP, and CRF encoding modes
- **Real-time Filters**: GPU-accelerated denoising, scaling, and stabilization
- **LUT Support**: Professional color grading with Look-Up Tables
- **Custom FFmpeg Filters**: Per-strip filter customization

### Professional Workflow
- **Render Queue System**: Batch processing with dependency management
- **Live Streaming**: RTMP streaming capabilities (in development)
- **Preset Management**: Save and load custom render configurations
- **Comprehensive Logging**: Detailed operation logs for troubleshooting

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Blender Version**: 4.5.0 or newer
- **RAM**: 8GB minimum, 16GB+ recommended
- **Storage**: 1GB available space

### GPU Requirements (Recommended)
- **NVIDIA GPU**: GTX 1000 series or newer (RTX series highly recommended)
- **VRAM**: 4GB minimum, 8GB+ for 4K workflows
- **NVIDIA Drivers**: 460.0 or newer
- **CUDA**: 11.0 or newer (automatically installed with drivers)

### Software Dependencies
- **FFmpeg**: Latest version with CUDA and NVENC support
  - Windows: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or [BtbN](https://github.com/BtbN/FFmpeg-Builds/releases)
  - macOS: `brew install ffmpeg` with `--enable-cuda` and `--enable-nvenc`
  - Linux: Build from source or use repository versions with CUDA support

## 🔧 Installation

### Method 1: Direct Download (Recommended)
1. Download the latest release ZIP from [Releases](https://github.com/yavru421/VSEndless-Render-Engine-blender4.5/releases)
2. Open Blender and go to `Edit > Preferences > Add-ons`
3. Click `Install...` and select the downloaded ZIP file
4. Enable "VSEndless - GPU Accelerated Render Engine"
5. Save preferences and restart Blender

### Method 2: Manual Installation
1. Clone or download this repository
2. Copy the entire folder to your Blender add-ons directory:
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\4.5\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/4.5/scripts/addons/`
   - **Linux**: `~/.config/blender/4.5/scripts/addons/`
3. Restart Blender and enable the add-on

## 🎬 Quick Start

### Basic Workflow
1. **Set Render Engine**: In Render Properties, set engine to "VSEndless GPU Render Engine"
2. **Configure Output**: Set your output path and video codec in the VSEndless panel
3. **Import Sequences**: Add video files to the VSE timeline
4. **Configure GPU Settings**: Enable hardware acceleration in the GPU settings panel
5. **Render**: Click "Render Animation" or use the VSEndless render operators

### GPU Setup Verification
1. In the VSE, open the VSEndless panel in the sidebar
2. Click "Check GPU Capabilities" to verify your system
3. Review the messages for any configuration issues
4. Ensure NVENC is detected for optimal performance

## ⚙️ Configuration

### Output Settings
- **Resolution**: Set custom output resolution (up to 8K)
- **Frame Rate**: Configure output frame rate (1-240 fps)
- **Codec**: Choose from H.264, H.265, ProRes, and more
- **Bitrate**: Control video quality and file size

### GPU Acceleration
- **Hardware Decoding**: Enable CUDA/NVDEC for input acceleration
- **NVENC Encoding**: GPU-accelerated encoding with quality presets
- **Rate Control**: Select optimal bitrate control method
- **Multi-pass Encoding**: Enhanced quality with 2-pass encoding

### Post-Processing
- **GPU Denoising**: Real-time noise reduction with configurable strength
- **Video Stabilization**: GPU-accelerated stabilization
- **Scaling**: Hardware-accelerated resolution changes
- **Color Grading**: Apply LUTs for professional color correction

## 🔧 Troubleshooting

### Common Issues

#### GPU Not Detected
1. Verify NVIDIA drivers are installed and up-to-date
2. Check if `nvidia-smi` command works in terminal/command prompt
3. Ensure CUDA is properly installed
4. Restart Blender after driver updates

#### NVENC Not Available
1. Verify FFmpeg was compiled with NVENC support
2. Test FFmpeg NVENC: `ffmpeg -encoders | grep nvenc`
3. Download pre-compiled FFmpeg with CUDA support
4. Check NVIDIA GPU supports NVENC (GTX 600 series or newer)

#### Render Failures
1. Check the Blender console for detailed error messages
2. Verify all input video files exist and are accessible
3. Test with a simple sequence first
4. Ensure sufficient disk space for output
5. Try different codec settings if issues persist

#### Performance Issues
1. Monitor GPU usage during rendering
2. Close other GPU-intensive applications
3. Increase VRAM allocation if available
4. Use lower quality presets for faster rendering
5. Consider upgrading to a more powerful GPU

### Getting Help
- **Documentation**: Check the [Wiki](https://github.com/yavru421/VSEndless-Render-Engine-blender4.5/wiki)
- **Issues**: Report bugs on [GitHub Issues](https://github.com/yavru421/VSEndless-Render-Engine-blender4.5/issues)
- **Community**: Join discussions in [GitHub Discussions](https://github.com/yavru421/VSEndless-Render-Engine-blender4.5/discussions)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork this repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Blender Foundation**: For the amazing Blender software
- **NVIDIA**: For CUDA and NVENC technologies
- **FFmpeg Team**: For the powerful media processing library
- **Community Contributors**: Thank you for your support and feedback

## 💖 Support

If you find VSEndless useful, consider:
- ⭐ Starring this repository
- 🐛 Reporting bugs and suggesting features
- 💰 [Sponsoring the project](https://github.com/sponsors/yavru421)
- 📢 Sharing with other Blender users

---

**Made with ❤️ for the Blender community**