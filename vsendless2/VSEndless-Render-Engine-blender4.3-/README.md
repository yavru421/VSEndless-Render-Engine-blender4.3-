# VSEndless Render Engine 3.0

A GPU-accelerated render engine for Blender's Video Sequence Editor (VSE) that leverages the power of NVIDIA GPUs through CUDA and NVENC for high-speed video rendering and processing.

## Features

- **NVIDIA GPU Acceleration**: Harness the power of your RTX/GTX GPU for faster rendering
- **Hardware Decoding**: Use NVDEC to accelerate video decoding
- **NVENC Encoding**: High-quality, high-speed encoding with NVIDIA's NVENC
- **GPU-Accelerated Filters**: Scale, denoise, and stabilize video using CUDA
- **Flexible Rate Control**: Choose between CBR, VBR, CQP, and CRF modes
- **LUT Support**: Apply color correction using LUT files
- **Customizable Presets**: Save and load your favorite settings

## Requirements

- Blender 4.3 or newer
- NVIDIA GPU (GTX 1000 series or newer recommended)
- FFmpeg with CUDA and NVENC support
- NVIDIA drivers (450.0 or newer)

## Installation

### Downloading from GitHub

1. Go to the [Releases](https://github.com/yavru421/VSEndless-Render-Engine-blender4.3-/releases) page
2. Download the latest ZIP file (e.g., `VSEndless_Render_Engine_v3.0.2_20240615.zip`)

### Installing in Blender

1. Open Blender and go to Edit > Preferences
2. Select the "Add-ons" tab
3. Click "Install..." button at the top
4. Browse to the downloaded ZIP file and select it
5. Click "Install Add-on"
6. Find "VSEndless - GPU Accelerated Render Engine" in the add-ons list
7. Enable it by checking the box
8. You may need to restart Blender for all features to work properly

### Manual Installation

If you prefer manual installation:

1. Extract the ZIP file
2. Copy the entire folder to your Blender add-ons directory:
   - Windows: `%APPDATA%\Blender Foundation\Blender\4.3\scripts\addons\`
   - macOS: `~/Library/Application Support/Blender/4.3/scripts/addons/`
   - Linux: `~/.config/blender/4.3/scripts/addons/`
3. Restart Blender and enable the add-on as described above

## Testing Your System

Before using the add-on, verify your system has the necessary GPU acceleration capabilities:

1. Download and extract the full repository
2. Install the required Python dependencies: `pip install psutil`
3. Run `python utils/test_some_shit.py` in a terminal
4. Review the results to ensure your system meets the requirements

## Usage

1. Open Blender and switch to the Video Editing workspace
2. Add your video sequences to the VSE
3. Go to the Output Properties panel
4. Configure the VSEndless Render settings according to your needs
5. Render using the regular Blender render controls

## GPU Settings

### Hardware Acceleration

- **Use Hardware Acceleration**: Enable GPU decoding of source videos
- **Method**: Choose between CUDA and NVDEC for decoding

### Video Codec Settings

- **Codec**: Choose between H.264 and H.265 (both use NVENC)
- **Profile**: Select the appropriate codec profile
- **Quality Preset**: Balance between quality and encoding speed
- **Rate Control**: Select your preferred bitrate control method

### GPU Processing

- **GPU Scaling**: Use CUDA for faster video scaling
- **GPU Denoising**: Apply temporal noise reduction using CUDA
- **GPU Stabilization**: Accelerate video stabilization with CUDA

## Troubleshooting

If you encounter issues with GPU acceleration:

1. Ensure your NVIDIA drivers are up-to-date
2. Verify FFmpeg is installed with CUDA and NVENC support
3. Run the test script to check system compatibility
4. For Windows users, ensure you're using the latest FFmpeg build from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or [BtbN's builds](https://github.com/BtbN/FFmpeg-Builds/releases)

## License

MIT License
