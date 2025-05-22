import bpy
from typing import Any

def register_properties() -> None:
    """Register all custom properties for VSEndless2.0 on bpy.types.Scene."""
    try:
        bpy.types.Scene.ffmpeg_codec = bpy.props.EnumProperty(
            name="Codec",
            description="Select video codec",
            items=[('H264', "H.264", ""), ('H265', "H.265", "")],
            default='H264'
        )
        bpy.types.Scene.ffmpeg_bitrate = bpy.props.IntProperty(
            name="Bitrate",
            description="Video bitrate (Mbps)",
            default=10,
            min=1,
            max=100
        )
        bpy.types.Scene.ffmpeg_preset = bpy.props.EnumProperty(
            name="Preset",
            description="FFmpeg encoding preset",
            items=[('p1', "Slow", ""), ('p5', "Medium", ""), ('p7', "Fast", "")],
            default='p5'
        )
        bpy.types.Scene.ffmpeg_aspect_ratio = bpy.props.StringProperty(
            name="Aspect Ratio",
            description="Aspect ratio (e.g. 16:9)",
            default="16:9"
        )
        bpy.types.Scene.ffmpeg_custom_fps = bpy.props.BoolProperty(
            name="Custom FPS",
            description="Enable custom frame rate",
            default=False
        )
        bpy.types.Scene.ffmpeg_frame_rate = bpy.props.IntProperty(
            name="Frame Rate",
            description="Custom frame rate (FPS)",
            default=30,
            min=1,
            max=120
        )
        bpy.types.Scene.enable_denoising = bpy.props.BoolProperty(
            name="Enable Denoising",
            description="Apply denoising post-process",
            default=False
        )
        bpy.types.Scene.apply_stabilization = bpy.props.BoolProperty(
            name="Apply Stabilization",
            description="Apply video stabilization",
            default=False
        )
        bpy.types.Scene.apply_lut = bpy.props.BoolProperty(
            name="Use LUT for Color Correction",
            description="Enable LUT-based color correction",
            default=False
        )
        bpy.types.Scene.lut_file_path = bpy.props.StringProperty(
            name="LUT File Path",
            description="Path to the LUT file for color correction",
            subtype='FILE_PATH'
        )
        bpy.types.Scene.output_format = bpy.props.EnumProperty(
            name="Output Format",
            description="Select output format",
            items=[
                ('MP4', "MP4 (H.264/H.265)", ""),
                ('MKV', "MKV (H.264/H.265)", ""),
                ('MOV', "MOV (ProRes)", ""),
                ('GIF', "GIF Animation", ""),
                ('PNGSEQ', "PNG Image Sequence", ""),
                ('WAV', "WAV Audio Only", ""),
                ('MP3', "MP3 Audio Only", "")
            ],
            default='MP4'
        )
        bpy.types.Scene.audio_codec = bpy.props.EnumProperty(
            name="Audio Codec",
            description="Select audio codec",
            items=[
                ('AAC', "AAC", ""),
                ('MP3', "MP3", ""),
                ('PCM_S16LE', "WAV (PCM S16LE)", "")
            ],
            default='AAC'
        )
        bpy.types.Scene.ffmpeg_advanced_preset = bpy.props.EnumProperty(
            name="Advanced Preset",
            description="Select advanced FFmpeg preset",
            items=[
                ('NONE', "None", ""),
                ('INSTA_IMAGE_SEQUENCE', "Instagram Image Sequence (Square, 30fps, 1080x1080)", ""),
                # Add more advanced presets here as needed
            ],
            default='NONE'
        )
        bpy.types.Scene.groq_api_enabled = bpy.props.BoolProperty(
            name="Enable Groq API",
            description="Use Groq API for AI-powered enhancements",
            default=False
        )
        bpy.types.Scene.groq_api_key = bpy.props.StringProperty(
            name="Groq API Key",
            description="API key for Groq AI integration",
            subtype='PASSWORD',
            default=""
        )
    except Exception as e:
        print(f"[VSEndless2.0] Property registration error: {e}")

def unregister_properties() -> None:
    """Unregister all custom properties for VSEndless2.0 from bpy.types.Scene."""
    for prop in [
        'ffmpeg_codec', 'ffmpeg_bitrate', 'ffmpeg_preset', 'ffmpeg_aspect_ratio',
        'ffmpeg_custom_fps', 'ffmpeg_frame_rate', 'enable_denoising',
        'apply_stabilization', 'apply_lut', 'lut_file_path', 'output_format',
        'audio_codec', 'ffmpeg_advanced_preset', 'groq_api_enabled', 'groq_api_key']:
        try:
            delattr(bpy.types.Scene, prop)
        except AttributeError:
            pass
