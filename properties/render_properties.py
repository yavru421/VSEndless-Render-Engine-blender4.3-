# render_properties.py: Advanced properties for VSEndless Render Engine
# Inputs: Blender context
# Outputs: Custom properties for VSEndless

import bpy

def _vsendless_output_path_update(self, context):
    print(f"[VSEndless] Output path updated: {self.output_path}")

def _vsendless_codec_update(self, context):
    print(f"[VSEndless] Codec updated: {self.ffmpeg_codec}")

class VSEndlessProperties(bpy.types.PropertyGroup):
    # Explicit variable definitions
    output_path = bpy.props.StringProperty(
        name="Output Path",
        description="Path to save rendered video",
        default="//output.mp4",
        update=_vsendless_output_path_update
    )
    ffmpeg_codec = bpy.props.EnumProperty(
        name="FFmpeg Codec",
        description="Video codec for ffmpeg output",
        items=[
            ("libx264", "H.264 (libx264)", "Standard MP4 encoding"),
            ("h264_nvenc", "H.264 NVENC", "NVIDIA GPU accelerated H.264"),
            ("libx265", "H.265 (libx265)", "HEVC encoding"),
            ("hevc_nvenc", "H.265 NVENC", "NVIDIA GPU accelerated H.265"),
            ("mpeg4", "MPEG-4", "Legacy MPEG-4 encoding"),
            ("prores_ks", "ProRes (prores_ks)", "Apple ProRes encoding")
        ],
        default="h264_nvenc",
        update=_vsendless_codec_update
    )
    ffmpeg_pix_fmt = bpy.props.EnumProperty(
        name="Pixel Format",
        description="Pixel format for ffmpeg output",
        items=[
            ("yuv420p", "yuv420p", "Standard for MP4 playback"),
            ("yuv422p", "yuv422p", "Higher color fidelity"),
            ("yuv444p", "yuv444p", "Full color fidelity")
        ],
        default="yuv420p"
    )
    ffmpeg_framerate = bpy.props.IntProperty(
        name="Framerate",
        description="Output video framerate",
        default=30,
        min=1,
        max=240
    )
    ffmpeg_resolution_x = bpy.props.IntProperty(
        name="Resolution X",
        description="Output video width",
        default=1920,
        min=16,
        max=8192
    )
    ffmpeg_resolution_y = bpy.props.IntProperty(
        name="Resolution Y",
        description="Output video height",
        default=1080,
        min=16,
        max=8192
    )
    ffmpeg_bitrate = bpy.props.IntProperty(
        name="Bitrate (Mbps)",
        description="Video bitrate in Megabits per second",
        default=10,
        min=1,
        max=100
    )

def register():
    # Advanced GPU/video properties for full feature parity
    bpy.types.Scene.use_hwaccel = bpy.props.BoolProperty(
        name="Use Hardware Acceleration",
        description="Enable hardware acceleration for video decoding",
        default=True
    )
    bpy.types.Scene.hwaccel_method = bpy.props.EnumProperty(
        name="HW Accel Method",
        description="Hardware acceleration method for decoding",
        items=[
            ('NONE', "None", "No hardware acceleration"),
            ('CUDA', "CUDA", "Use CUDA for hardware acceleration"),
            ('NVDEC', "NVDEC", "Use NVDEC for hardware acceleration")
        ],
        default='CUDA'
    )
    bpy.types.Scene.nvenc_preset = bpy.props.EnumProperty(
        name="NVENC Preset",
        description="NVENC encoder preset (speed vs quality)",
        items=[
            ('p1', "Slow (Best Quality)", ""),
            ('p3', "Medium", ""),
            ('p5', "Fast", ""),
            ('p7', "Very Fast", "")
        ],
        default='p3'
    )
    bpy.types.Scene.nvenc_tune = bpy.props.EnumProperty(
        name="NVENC Tuning",
        description="Tuning options for specific content types",
        items=[
            ('hq', "High Quality", ""),
            ('ll', "Low Latency", ""),
            ('ull', "Ultra Low Latency", "")
        ],
        default='hq'
    )
    bpy.types.Scene.h264_profile = bpy.props.EnumProperty(
        name="H.264 Profile",
        description="H.264 encoding profile",
        items=[
            ('baseline', "Baseline", ""),
            ('main', "Main", ""),
            ('high', "High", "")
        ],
        default='high'
    )
    bpy.types.Scene.hevc_profile = bpy.props.EnumProperty(
        name="H.265 Profile",
        description="H.265 encoding profile",
        items=[
            ('main', "Main", ""),
            ('main10', "Main 10", ""),
            ('rext', "Range Extensions", "")
        ],
        default='main'
    )
    bpy.types.Scene.rate_control_mode = bpy.props.EnumProperty(
        name="Rate Control",
        description="Bitrate control method",
        items=[
            ('CBR', "Constant Bitrate", "Fixed bitrate"),
            ('VBR', "Variable Bitrate", "Variable bitrate with max constraint"),
            ('CQP', "Constant QP", "Constant quantization parameter"),
            ('CRF', "Constant Rate Factor", "Constant quality level")
        ],
        default='VBR'
    )
    bpy.types.Scene.constant_quality_level = bpy.props.IntProperty(
        name="Quality Level",
        description="Quality level for CQP/CRF mode (lower is better quality)",
        default=23,
        min=0,
        max=51
    )
    bpy.types.Scene.use_multipass = bpy.props.BoolProperty(
        name="2-Pass Encoding",
        description="Use 2-pass encoding for better quality",
        default=False
    )
    bpy.types.Scene.use_gpu_scaling = bpy.props.BoolProperty(
        name="GPU Scaling",
        description="Use GPU for scaling operations",
        default=True
    )
    bpy.types.Scene.use_gpu_denoising = bpy.props.BoolProperty(
        name="GPU Denoising",
        description="Use GPU acceleration for denoising",
        default=True
    )
    bpy.types.Scene.denoise_strength = bpy.props.FloatProperty(
        name="Denoise Strength",
        description="Strength of the denoising effect",
        default=3.0,
        min=0.1,
        max=10.0
    )
    bpy.types.Scene.use_gpu_stabilization = bpy.props.BoolProperty(
        name="GPU Stabilization",
        description="Use GPU for video stabilization",
        default=True
    )
    bpy.types.Scene.ffmpeg_custom_fps = bpy.props.BoolProperty(
        name="Custom FPS",
        default=False
    )
    bpy.types.Scene.ffmpeg_frame_rate = bpy.props.IntProperty(
        name="Frame Rate",
        default=30,
        min=1,
        max=120
    )
    bpy.types.Scene.ffmpeg_aspect_ratio = bpy.props.StringProperty(
        name="Aspect Ratio",
        default="16:9"
    )
    bpy.types.Scene.enable_denoising = bpy.props.BoolProperty(
        name="Enable Denoising",
        default=False
    )
    bpy.types.Scene.apply_stabilization = bpy.props.BoolProperty(
        name="Apply Stabilization",
        default=False
    )
    bpy.types.Scene.apply_lut = bpy.props.BoolProperty(
        name="Use LUT for Color Correction",
        default=False
    )
    bpy.types.Scene.lut_file_path = bpy.props.StringProperty(
        name="LUT File Path",
        description="Path to the LUT file for color correction",
        subtype='FILE_PATH'
    )
    # Add RTMP URL property for streaming
    bpy.types.Scene.vsendless_rtmp_url = bpy.props.StringProperty(
        name="RTMP URL",
        description="RTMP streaming URL for direct output",
        default="rtmp://localhost/live"
    )
    bpy.utils.register_class(VSEndlessProperties)
    bpy.types.Scene.vsendless_props = bpy.props.PointerProperty(type=VSEndlessProperties)
    # No class property registration for ffmpeg_filter; use ID property system (strip['ffmpeg_filter'])

def unregister():
    del bpy.types.Scene.vsendless_rtmp_url
    del bpy.types.Scene.vsendless_props
    pass  # No class property to unregister for ffmpeg_filter
    bpy.utils.unregister_class(VSEndlessProperties)
