# VSEndless - GPU Accelerated Render Engine for Blender 4.5+# VSEndless - GPU Accelerated Render Engine for Blender 4.5+# VSEndless Render Engine 4 (vsendless4)



A powerful, GPU-accelerated render engine designed specifically for Blender's Video Sequence Editor (VSE) with advanced NVIDIA NVENC support and hardware acceleration.



---A powerful, GPU-accelerated render engine designed specifically for Blender's Video Sequence Editor (VSE) with advanced NVIDIA NVENC support and hardware acceleration.A modular, robust, and extensible Blender VSE render engine addon, designed using Algebraic Pipeline Theory (APT) methodology.



[![GitHub Release](https://img.shields.io/github/v/release/yavru421/VSEndless-Render-Engine-blender4.3-)](https://github.com/yavru421/VSEndless-Render-Engine-blender4.3-/releases)

[![Blender](https://img.shields.io/badge/Blender-4.5%2B-orange)](https://www.blender.org/)

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)---## Structure

[![Sponsor](https://img.shields.io/badge/Sponsor%20Me-GitHub%20Sponsors-blue)](https://github.com/sponsors/yavru421)

- `operators/`: Rendering and processing operators

---

[![GitHub Release](https://img.shields.io/github/v/release/yavru421/VSEndless-Render-Engine-blender4.5)](https://github.com/yavru421/VSEndless-Render-Engine-blender4.5/releases)- `properties/`: Custom properties and settings

## 🚀 Features

[![Blender](https://img.shields.io/badge/Blender-4.5%2B-orange)](https://www.blender.org/)- `ui/`: Panels and UI integration

### GPU Acceleration

- **NVIDIA NVENC Hardware Encoding**: Blazing-fast H.264 and H.265 encoding[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)- `utils/`: Utilities (ffmpeg, sequence, presets, etc.)

- **CUDA Acceleration**: GPU-powered video processing and filtering

- **Hardware Decoding**: NVDEC support for accelerated input processing[![Sponsor](https://img.shields.io/badge/Sponsor%20Me-GitHub%20Sponsors-blue)](https://github.com/sponsors/yavru421)

- **Smart GPU Detection**: Automatic GPU capability detection and optimization

## APT Pipeline

### Advanced Video Processing

- **Multi-format Support**: H.264, H.265/HEVC, ProRes, and more---Each module is a pipeline stage with explicit input/output variables and dependencies. See code comments for algebraic notation.

- **Flexible Rate Control**: CBR, VBR, CQP, and CRF encoding modes

- **Real-time Filters**: GPU-accelerated denoising, scaling, and stabilization

- **LUT Support**: Professional color grading with Look-Up Tables

- **Custom FFmpeg Filters**: Per-strip filter customization## 🚀 Features## Integration



### Professional Workflow- Ready for API/tool-calling integration (see `llama-chat-completions.yaml`)

- **Render Queue System**: Batch processing with dependency management

- **Live Streaming**: RTMP streaming capabilities (in development)### GPU Acceleration- Designed for maintainability and extensibility

- **Preset Management**: Save and load custom render configurations

- **Comprehensive Logging**: Detailed operation logs for troubleshooting- **NVIDIA NVENC Hardware Encoding**: Blazing-fast H.264 and H.265 encoding

- **CUDA Acceleration**: GPU-powered video processing and filtering

## 📋 Requirements- **Hardware Decoding**: NVDEC support for accelerated input processing

- **Smart GPU Detection**: Automatic GPU capability detection and optimization

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)### Advanced Video Processing

- **Blender Version**: 4.5.0 or newer- **Multi-format Support**: H.264, H.265/HEVC, ProRes, and more

- **RAM**: 8GB minimum, 16GB+ recommended- **Flexible Rate Control**: CBR, VBR, CQP, and CRF encoding modes

- **Storage**: 1GB available space- **Real-time Filters**: GPU-accelerated denoising, scaling, and stabilization

- **LUT Support**: Professional color grading with Look-Up Tables

### GPU Requirements (Recommended)- **Custom FFmpeg Filters**: Per-strip filter customization

- **NVIDIA GPU**: GTX 1000 series or newer (RTX series highly recommended)

- **VRAM**: 4GB minimum, 8GB+ for 4K workflows### Professional Workflow

- **NVIDIA Drivers**: 460.0 or newer- **Render Queue System**: Batch processing with dependency management

- **CUDA**: 11.0 or newer (automatically installed with drivers)- **Live Streaming**: RTMP streaming capabilities (in development)

- **Preset Management**: Save and load custom render configurations

### Software Dependencies- **Comprehensive Logging**: Detailed operation logs for troubleshooting

- **FFmpeg**: Latest version with CUDA and NVENC support

  - Windows: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or [BtbN](https://github.com/BtbN/FFmpeg-Builds/releases)## 📋 Requirements

  - macOS: `brew install ffmpeg` with `--enable-cuda` and `--enable-nvenc`

  - Linux: Build from source or use repository versions with CUDA support### System Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)

## 🔧 Installation- **Blender Version**: 4.5.0 or newer

- **RAM**: 8GB minimum, 16GB+ recommended

### Method 1: Direct Download (Recommended)- **Storage**: 1GB available space

1. Download the latest release ZIP from [Releases](https://github.com/yavru421/VSEndless-Render-Engine-blender4.3-/releases)

2. Open Blender and go to `Edit > Preferences > Add-ons`### GPU Requirements (Recommended)

3. Click `Install...` and select the downloaded ZIP file- **NVIDIA GPU**: GTX 1000 series or newer (RTX series highly recommended)

4. Enable "VSEndless - GPU Accelerated Render Engine"- **VRAM**: 4GB minimum, 8GB+ for 4K workflows

5. Save preferences and restart Blender- **NVIDIA Drivers**: 460.0 or newer

- **CUDA**: 11.0 or newer (automatically installed with drivers)

### Method 2: Manual Installation

1. Clone or download this repository### Software Dependencies

2. Copy the entire folder to your Blender add-ons directory:- **FFmpeg**: Latest version with CUDA and NVENC support

   - **Windows**: `%APPDATA%\Blender Foundation\Blender\4.5\scripts\addons\`  - Windows: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or [BtbN](https://github.com/BtbN/FFmpeg-Builds/releases)

   - **macOS**: `~/Library/Application Support/Blender/4.5/scripts/addons/`  - macOS: `brew install ffmpeg` with `--enable-cuda` and `--enable-nvenc`

   - **Linux**: `~/.config/blender/4.5/scripts/addons/`  - Linux: Build from source or use repository versions with CUDA support

3. Restart Blender and enable the add-on

## 🔧 Installation

## 🎬 Quick Start

### Method 1: Direct Download (Recommended)

### Basic Workflow1. Download the latest release ZIP from [Releases](https://github.com/yavru421/VSEndless-Render-Engine-blender4.5/releases)

1. **Set Render Engine**: In Render Properties, set engine to "VSEndless GPU Render Engine"2. Open Blender and go to `Edit > Preferences > Add-ons`

2. **Configure Output**: Set your output path and video codec in the VSEndless panel3. Click `Install...` and select the downloaded ZIP file

3. **Import Sequences**: Add video files to the VSE timeline4. Enable "VSEndless - GPU Accelerated Render Engine"

4. **Configure GPU Settings**: Enable hardware acceleration in the GPU settings panel5. Save preferences and restart Blender

5. **Render**: Click "Render Animation" or use the VSEndless render operators

### Method 2: Manual Installation

### GPU Setup Verification1. Clone or download this repository

1. In the VSE, open the VSEndless panel in the sidebar2. Copy the entire folder to your Blender add-ons directory:

2. Click "Check GPU Capabilities" to verify your system   - **Windows**: `%APPDATA%\Blender Foundation\Blender\4.5\scripts\addons\`

3. Review the messages for any configuration issues   - **macOS**: `~/Library/Application Support/Blender/4.5/scripts/addons/`

4. Ensure NVENC is detected for optimal performance   - **Linux**: `~/.config/blender/4.5/scripts/addons/`

3. Restart Blender and enable the add-on

## ⚙️ Configuration

## 🎬 Quick Start

### Output Settings

- **Resolution**: Set custom output resolution (up to 8K)### Basic Workflow

- **Frame Rate**: Configure output frame rate (1-240 fps)1. **Set Render Engine**: In Render Properties, set engine to "VSEndless GPU Render Engine"

- **Codec**: Choose from H.264, H.265, ProRes, and more2. **Configure Output**: Set your output path and video codec in the VSEndless panel

- **Bitrate**: Control video quality and file size3. **Import Sequences**: Add video files to the VSE timeline

4. **Configure GPU Settings**: Enable hardware acceleration in the GPU settings panel

### GPU Acceleration5. **Render**: Click "Render Animation" or use the VSEndless render operators

- **Hardware Decoding**: Enable CUDA/NVDEC for input acceleration

- **NVENC Encoding**: GPU-accelerated encoding with quality presets### GPU Setup Verification

- **Rate Control**: Select optimal bitrate control method1. In the VSE, open the VSEndless panel in the sidebar

- **Multi-pass Encoding**: Enhanced quality with 2-pass encoding2. Click "Check GPU Capabilities" to verify your system

3. Review the messages for any configuration issues

### Post-Processing4. Ensure NVENC is detected for optimal performance

- **GPU Denoising**: Real-time noise reduction with configurable strength

- **Video Stabilization**: GPU-accelerated stabilization## ⚙️ Configuration

- **Scaling**: Hardware-accelerated resolution changes

- **Color Grading**: Apply LUTs for professional color correction### Output Settings

- **Resolution**: Set custom output resolution (up to 8K)

## 🔧 Troubleshooting- **Frame Rate**: Configure output frame rate (1-240 fps)

- **Codec**: Choose from H.264, H.265, ProRes, and more

### Common Issues- **Bitrate**: Control video quality and file size



#### GPU Not Detected### GPU Acceleration

1. Verify NVIDIA drivers are installed and up-to-date- **Hardware Decoding**: Enable CUDA/NVDEC for input acceleration

2. Check if `nvidia-smi` command works in terminal/command prompt- **NVENC Encoding**: GPU-accelerated encoding with quality presets

3. Ensure CUDA is properly installed- **Rate Control**: Select optimal bitrate control method

4. Restart Blender after driver updates- **Multi-pass Encoding**: Enhanced quality with 2-pass encoding



#### NVENC Not Available### Post-Processing

1. Verify FFmpeg was compiled with NVENC support- **GPU Denoising**: Real-time noise reduction with configurable strength

2. Test FFmpeg NVENC: `ffmpeg -encoders | grep nvenc`- **Video Stabilization**: GPU-accelerated stabilization

3. Download pre-compiled FFmpeg with CUDA support- **Scaling**: Hardware-accelerated resolution changes

4. Check NVIDIA GPU supports NVENC (GTX 600 series or newer)- **Color Grading**: Apply LUTs for professional color correction



#### Render Failures## 🔧 Troubleshooting

1. Check the Blender console for detailed error messages

2. Verify all input video files exist and are accessible### Common Issues

3. Test with a simple sequence first

4. Ensure sufficient disk space for output#### GPU Not Detected

5. Try different codec settings if issues persist1. Verify NVIDIA drivers are installed and up-to-date

2. Check if `nvidia-smi` command works in terminal/command prompt

#### Performance Issues3. Ensure CUDA is properly installed

1. Monitor GPU usage during rendering4. Restart Blender after driver updates

2. Close other GPU-intensive applications

3. Increase VRAM allocation if available#### NVENC Not Available

4. Use lower quality presets for faster rendering1. Verify FFmpeg was compiled with NVENC support

5. Consider upgrading to a more powerful GPU2. Test FFmpeg NVENC: `ffmpeg -encoders | grep nvenc`

3. Download pre-compiled FFmpeg with CUDA support

### Getting Help4. Check NVIDIA GPU supports NVENC (GTX 600 series or newer)

- **Documentation**: Check the [Wiki](https://github.com/yavru421/VSEndless-Render-Engine-blender4.3-/wiki)

- **Issues**: Report bugs on [GitHub Issues](https://github.com/yavru421/VSEndless-Render-Engine-blender4.3-/issues)#### Render Failures

- **Community**: Join discussions in [GitHub Discussions](https://github.com/yavru421/VSEndless-Render-Engine-blender4.3-/discussions)1. Check the Blender console for detailed error messages

2. Verify all input video files exist and are accessible

## 🤝 Contributing3. Test with a simple sequence first

4. Ensure sufficient disk space for output

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.5. Try different codec settings if issues persist



### Development Setup#### Performance Issues

1. Fork this repository1. Monitor GPU usage during rendering

2. Create a feature branch: `git checkout -b feature-name`2. Close other GPU-intensive applications

3. Make your changes and test thoroughly3. Increase VRAM allocation if available

4. Submit a pull request with a clear description4. Use lower quality presets for faster rendering

5. Consider upgrading to a more powerful GPU

## 📄 License

### Getting Help

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.- **Documentation**: Check the [Wiki](https://github.com/yavru421/VSEndless-Render-Engine-blender4.5/wiki)

- **Issues**: Report bugs on [GitHub Issues](https://github.com/yavru421/VSEndless-Render-Engine-blender4.5/issues)

## 🙏 Acknowledgments- **Community**: Join discussions in [GitHub Discussions](https://github.com/yavru421/VSEndless-Render-Engine-blender4.5/discussions)



- **Blender Foundation**: For the amazing Blender software## 🤝 Contributing

- **NVIDIA**: For CUDA and NVENC technologies

- **FFmpeg Team**: For the powerful media processing libraryWe welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

- **Community Contributors**: Thank you for your support and feedback

### Development Setup

## 💖 Support1. Fork this repository

2. Create a feature branch: `git checkout -b feature-name`

If you find VSEndless useful, consider:3. Make your changes and test thoroughly

- ⭐ Starring this repository4. Submit a pull request with a clear description

- 🐛 Reporting bugs and suggesting features

- 💰 [Sponsoring the project](https://github.com/sponsors/yavru421)## 📄 License

- 📢 Sharing with other Blender users

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

**Made with ❤️ for the Blender community**
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