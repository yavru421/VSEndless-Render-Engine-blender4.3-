import bpy

def register_properties():
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

def unregister_properties():
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
