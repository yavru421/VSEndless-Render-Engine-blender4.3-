import bpy

def register_properties():
    # Existing properties
    bpy.types.Scene.ffmpeg_codec = bpy.props.EnumProperty(
        name="Codec",
        description="Select video codec",
        items=[('H264', "H.264", ""), ('H265', "H.265", "")],
        default='H264'
    )
    bpy.types.Scene.ffmpeg_bitrate = bpy.props.IntProperty(
        name="Bitrate",
        default=10,
        min=1,
        max=100
    )
    bpy.types.Scene.ffmpeg_preset = bpy.props.EnumProperty(
        name="Preset",
        items=[('p1', "Slow", ""), ('p5', "Medium", ""), ('p7', "Fast", "")],
        default='p5'
    )
    bpy.types.Scene.ffmpeg_aspect_ratio = bpy.props.StringProperty(
        name="Aspect Ratio",
        default="16:9"
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
    
    # New GPU-related properties
    # Hardware acceleration
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
    
    # NVENC settings
    bpy.types.Scene.nvenc_preset = bpy.props.EnumProperty(
        name="NVENC Preset",
        description="NVENC encoder preset (speed vs quality)",
        items=[
            ('p1', "Slow (Best Quality)", ""),
            ('p3', "Medium", ""),
            ('p7', "Fast (Lower Quality)", "")
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
    
    # Rate control modes
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
    
    # GPU processing options
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

def unregister_properties():
    # Existing property removal
    del bpy.types.Scene.ffmpeg_codec
    del bpy.types.Scene.ffmpeg_bitrate
    del bpy.types.Scene.ffmpeg_preset
    del bpy.types.Scene.ffmpeg_aspect_ratio
    del bpy.types.Scene.ffmpeg_custom_fps
    del bpy.types.Scene.ffmpeg_frame_rate
    del bpy.types.Scene.enable_denoising
    del bpy.types.Scene.apply_stabilization
    del bpy.types.Scene.apply_lut
    del bpy.types.Scene.lut_file_path
    
    # New GPU-related property removal
    del bpy.types.Scene.use_hwaccel
    del bpy.types.Scene.hwaccel_method
    del bpy.types.Scene.nvenc_preset
    del bpy.types.Scene.nvenc_tune
    del bpy.types.Scene.h264_profile
    del bpy.types.Scene.hevc_profile
    del bpy.types.Scene.rate_control_mode
    del bpy.types.Scene.constant_quality_level
    del bpy.types.Scene.use_multipass
    del bpy.types.Scene.use_gpu_scaling
    del bpy.types.Scene.use_gpu_denoising
    del bpy.types.Scene.denoise_strength
    del bpy.types.Scene.use_gpu_stabilization
