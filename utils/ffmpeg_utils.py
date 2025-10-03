# ffmpeg_utils.py: Advanced FFmpeg utilities for VSEndless Render Engine
# Inputs: file paths, render settings, GPU acceleration options
# Outputs: ffmpeg command execution, logs

import subprocess
import shutil
import bpy
import logging
from typing import List, Dict, Any

logger = logging.getLogger("VSEndless.FFmpeg")

def get_ffmpeg_path() -> str:
    """Get the FFmpeg executable path or just 'ffmpeg' if it's in PATH."""
    ffmpeg_path = shutil.which("ffmpeg")
    return ffmpeg_path if ffmpeg_path else "ffmpeg"

def construct_ffmpeg_command(scene: Any, timeline_data: List[Dict[str, Any]], output_path: str) -> List[str]:
    """
    Construct the FFmpeg command for rendering the video sequence.
    Includes GPU acceleration, denoising, stabilization, LUT, and audio settings.
    """
    ffmpeg_path = get_ffmpeg_path()
    inputs = []
    filter_complex = []

    # Base settings
    resolution = f"{scene.render.resolution_x}x{scene.render.resolution_y}"
    fps = scene.render.fps

    # Hardware acceleration for input decoding
    hw_accel_in = []
    if getattr(scene, 'use_hwaccel', False) and getattr(scene, 'hwaccel_method', 'NONE') != 'NONE':
        if scene.hwaccel_method == 'CUDA':
            hw_accel_in = ["-hwaccel", "cuda", "-hwaccel_output_format", "cuda"]
        elif scene.hwaccel_method == 'NVDEC':
            hw_accel_in = ["-hwaccel", "nvdec", "-hwaccel_output_format", "cuda"]

    # Input files with hardware acceleration
    for index, strip in enumerate(timeline_data):
        if not strip.get("filepath"):
            logger.warning("Timeline strip %d missing filepath.", index)
            continue
        inputs.extend([*hw_accel_in, "-i", strip["filepath"]])

    # Prepare filter complex chains
    v_inputs = []
    for index, strip in enumerate(timeline_data):
        if strip.get("type") == 'MOVIE':
            input_str = f"[{index}:v]"
            scale_filter = f"scale={resolution}"

            # GPU scaling if available
            if getattr(scene, 'use_gpu_scaling', False):
                scale_filter = f"scale_cuda={resolution}"

            # Apply filters based on scene settings
            if getattr(scene, 'enable_denoising', False):
                if getattr(scene, 'use_gpu_denoising', False):
                    scale_filter += f",tnr_cuda=mode=spatial:strength={getattr(scene, 'denoise_strength', 3.0)}"
                else:
                    scale_filter += f",nlmeans=s={getattr(scene, 'denoise_strength', 3.0)}"

            if getattr(scene, 'apply_stabilization', False):
                scale_filter += ",vidstabtransform=smoothing=30"

            if getattr(scene, 'apply_lut', False) and getattr(scene, 'lut_file_path', None):
                scale_filter += f",lut3d=file='{scene.lut_file_path}'"

            filter_complex.append(f"{input_str}{scale_filter}[v{index}]")
            v_inputs.append(f"[v{index}]")

    # Concat all videos if there are multiple strips
    if len(v_inputs) > 1:
        filter_complex.append(f"{''.join(v_inputs)}concat=n={len(v_inputs)}:v=1:a=0[outv]")
        video_map = "[outv]"
    elif v_inputs:
        video_map = v_inputs[0]
    else:
        logger.error("No video inputs for FFmpeg filter complex.")
        return []

    # Output codec settings
    codec_settings = []
    codec = getattr(scene, 'ffmpeg_codec', 'libx264')

    if 'nvenc' in codec or getattr(scene, 'use_hwaccel', False):
        # Use hardware encoding when available
        if codec == 'H264' or codec == 'libx264':
            codec_settings = ["-c:v", "h264_nvenc"]
        elif codec == 'H265' or codec == 'libx265':
            codec_settings = ["-c:v", "hevc_nvenc"]
        else:
            codec_settings = ["-c:v", codec]
    else:
        codec_settings = ["-c:v", codec]

    # Bitrate settings
    bitrate = getattr(scene, 'ffmpeg_bitrate', 10)
    codec_settings.extend(["-b:v", f"{bitrate}M"])

    # Audio settings
    audio_settings = ["-c:a", "aac", "-b:a", "192k"]

    # Build the final command
    command = [
        ffmpeg_path,
        *inputs,
        "-filter_complex", ";".join(filter_complex),
        "-map", video_map,
        *codec_settings,
        "-r", str(fps),
        *audio_settings,
        "-y", output_path
    ]

    logger.info("Constructed FFmpeg command: %s", ' '.join(map(str, command)))
    return command

def run_ffmpeg(input_path, output_path, extra_args=None):
    # x_1 = input_path, x_2 = output_path, x_3 = extra_args
    cmd = ["ffmpeg", "-i", input_path, output_path]
    if extra_args:
        cmd.extend(extra_args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def check_ffmpeg_version(min_version=(4, 3, 0)):
    """Warn if Blender's FFmpeg version is below min_version."""
    ffmpeg_info = getattr(bpy.app, 'ffmpeg', None)
    if ffmpeg_info and hasattr(ffmpeg_info, 'version'):
        version = ffmpeg_info.version
        if tuple(version) < min_version:
            print(f"[VSEndless] Warning: FFmpeg version {version} is below required {min_version}.")
            return False
    return True
