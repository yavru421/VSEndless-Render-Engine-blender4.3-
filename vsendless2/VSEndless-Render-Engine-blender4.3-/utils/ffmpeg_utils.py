import shutil
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
    fps = scene.ffmpeg_frame_rate if getattr(scene, 'ffmpeg_custom_fps', False) else scene.render.fps

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
            scale_filter = ""
            if getattr(scene, 'use_gpu_scaling', False):
                scale_filter = f"scale_cuda={resolution}"
            else:
                scale_filter = f"scale={resolution}"
            # Denoise with GPU if enabled
            if getattr(scene, 'enable_denoising', False) and getattr(scene, 'use_gpu_denoising', False):
                scale_filter += f",hwupload_cuda,tnr_cuda=mode=spatial:strength={getattr(scene, 'denoise_strength', 3.0)}"
            elif getattr(scene, 'enable_denoising', False):
                scale_filter += f",nlmeans=s={getattr(scene, 'denoise_strength', 3.0)}"
            # Stabilization
            if getattr(scene, 'apply_stabilization', False):
                if getattr(scene, 'use_gpu_stabilization', False):
                    scale_filter += ",vidstabtransform_cuda=smoothing=30:input=/tmp/transforms.trf"
                else:
                    scale_filter += ",vidstabtransform=smoothing=30:input=/tmp/transforms.trf"
            # LUT for color correction
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
    if getattr(scene, 'ffmpeg_codec', 'H264') == 'H264':
        codec_settings = ["-c:v", "h264_nvenc"]
        codec_settings.extend([
            "-preset", getattr(scene, 'nvenc_preset', 'p3'),
            "-profile:v", getattr(scene, 'h264_profile', 'high'),
            "-tune", getattr(scene, 'nvenc_tune', 'hq')
        ])
    elif getattr(scene, 'ffmpeg_codec', 'H264') == 'H265':
        codec_settings = ["-c:v", "hevc_nvenc"]
        codec_settings.extend([
            "-preset", getattr(scene, 'nvenc_preset', 'p3'),
            "-profile:v", getattr(scene, 'hevc_profile', 'main'),
            "-tune", getattr(scene, 'nvenc_tune', 'hq')
        ])

    # Rate control settings
    if getattr(scene, 'rate_control_mode', 'VBR') == 'CBR':
        bitrate_kbps = getattr(scene, 'ffmpeg_bitrate', 10) * 1000
        codec_settings.extend(["-b:v", f"{bitrate_kbps}k", "-maxrate", f"{bitrate_kbps}k", "-bufsize", f"{bitrate_kbps*2}k"])
    elif getattr(scene, 'rate_control_mode', 'VBR') == 'VBR':
        bitrate_kbps = getattr(scene, 'ffmpeg_bitrate', 10) * 1000
        codec_settings.extend(["-b:v", f"{bitrate_kbps}k", "-maxrate", f"{int(bitrate_kbps*1.5)}k", "-bufsize", f"{bitrate_kbps*3}k"])
    elif getattr(scene, 'rate_control_mode', 'VBR') == 'CQP':
        codec_settings.extend(["-qp", str(getattr(scene, 'constant_quality_level', 23))])
    elif getattr(scene, 'rate_control_mode', 'VBR') == 'CRF':
        codec_settings.extend(["-crf", str(getattr(scene, 'constant_quality_level', 23))])

    # Multipass encoding
    if getattr(scene, 'use_multipass', False):
        codec_settings.extend(["-multipass", "2"])

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
