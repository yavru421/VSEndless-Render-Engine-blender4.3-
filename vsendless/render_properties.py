
import bpy

def register():
    bpy.types.Scene.ffmpeg_codec = bpy.props.EnumProperty(
        name="Codec",
        description="Select the video codec for rendering.",
        items=[
            ('libx264', "H.264", "Widely supported codec."),
            ('libx265', "H.265", "High-efficiency codec."),
            ('vp9', "VP9", "Open-source high-efficiency codec.")
        ],
        default='libx264'
    )
    bpy.types.Scene.ffmpeg_bitrate = bpy.props.IntProperty(
        name="Bitrate (Mbps)",
        description="Set the video bitrate in Mbps.",
        default=10,
        min=1,
        max=100
    )
    bpy.types.Scene.enable_denoising = bpy.props.BoolProperty(
        name="Enable Denoising",
        description="Apply denoising during rendering.",
        default=False
    )
    bpy.types.Scene.apply_stabilization = bpy.props.BoolProperty(
        name="Apply Stabilization",
        description="Reduce jitter in video output.",
        default=False
    )
    bpy.types.Scene.lut_file_path = bpy.props.StringProperty(
        name="LUT File Path",
        description="Path to a LUT (Look-Up Table) file for color grading.",
        default="",
        subtype='FILE_PATH'
    )

def unregister():
    del bpy.types.Scene.ffmpeg_codec
    del bpy.types.Scene.ffmpeg_bitrate
    del bpy.types.Scene.enable_denoising
    del bpy.types.Scene.apply_stabilization
    del bpy.types.Scene.lut_file_path
