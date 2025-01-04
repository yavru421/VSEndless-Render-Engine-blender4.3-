import os
import shutil

# Add-on name and folder structure
ADDON_NAME = "vsendless"
BASE_DIR = os.getcwd()  # Get current working directory
ADDON_DIR = os.path.join(BASE_DIR, ADDON_NAME)

# Add-on files and their content
FILES = {
    "__init__.py": """
bl_info = {
    "name": "VSEndless - Advanced Render Engine",
    "blender": (2, 80, 0),
    "version": (1, 0, 0),
    "author": "John Daniel Dondlinger",
    "description": "Customizable render engine for Blender's Video Sequence Editor.",
    "category": "Render",
    "location": "Render Engine Dropdown",
    "support": "COMMUNITY",
}

import bpy
from . import render_operator
from . import render_panel
from . import render_properties

def register():
    render_properties.register()
    render_operator.register()
    render_panel.register()

def unregister():
    render_properties.unregister()
    render_operator.unregister()
    render_panel.unregister()

if __name__ == "__main__":
    register()
""",
    "render_properties.py": """
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
""",
    "render_panel.py": """
import bpy

class VSEndlessRenderPanel(bpy.types.Panel):
    bl_label = "VSEndless Render Settings"
    bl_idname = "RENDER_PT_vsendless"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Render Settings:")
        layout.prop(scene.render, "resolution_x", text="Resolution X")
        layout.prop(scene.render, "resolution_y", text="Resolution Y")
        layout.prop(scene.render, "fps", text="Frame Rate")
        layout.prop(scene, "ffmpeg_codec", text="Codec")
        layout.prop(scene, "ffmpeg_bitrate", text="Bitrate (Mbps)")

        layout.label(text="Post-Processing:")
        layout.prop(scene, "enable_denoising", text="Enable Denoising")
        layout.prop(scene, "apply_stabilization", text="Apply Stabilization")
        layout.prop(scene, "lut_file_path", text="LUT File Path")

def register():
    bpy.utils.register_class(VSEndlessRenderPanel)

def unregister():
    bpy.utils.unregister_class(VSEndlessRenderPanel)
""",
    "render_operator.py": """
import bpy
import subprocess
from .ffmpeg_utils import construct_ffmpeg_command
from .sequence_utils import extract_timeline_data

class VSEndlessRenderEngine(bpy.types.RenderEngine):
    bl_idname = "VSENDLESS_RENDER_ENGINE"
    bl_label = "VSEndless Render Engine"
    bl_use_preview = False

    def render(self, depsgraph):
        scene = depsgraph.scene
        output_path = bpy.path.abspath(scene.render.filepath)

        if not output_path.endswith(".mp4"):
            output_path += ".mp4"

        timeline_data = extract_timeline_data(scene)
        if not timeline_data:
            self.report({'ERROR'}, "No sequences found in VSE!")
            return

        ffmpeg_cmd = construct_ffmpeg_command(scene, timeline_data, output_path)
        if not ffmpeg_cmd:
            self.report({'ERROR'}, "Failed to build FFmpeg command!")
            return

        try:
            process = subprocess.run(ffmpeg_cmd, check=True, text=True, capture_output=True)
            self.report({'INFO'}, f"Render completed: {output_path}")
            print(process.stdout)
        except subprocess.CalledProcessError as e:
            self.report({'ERROR'}, f"FFmpeg failed: {e.stderr}")
            print(e.stderr)

def register():
    bpy.utils.register_class(VSEndlessRenderEngine)

def unregister():
    bpy.utils.unregister_class(VSEndlessRenderEngine)
""",
    "ffmpeg_utils.py": """
import os

def construct_ffmpeg_command(scene, timeline_data, output_path):
    ffmpeg_path = "ffmpeg"
    codec = scene.ffmpeg_codec
    bitrate = f"{scene.ffmpeg_bitrate}M"
    resolution = f"{scene.render.resolution_x}x{scene.render.resolution_y}"
    fps = scene.render.fps
    lut_file = scene.lut_file_path

    inputs = []
    filters = []

    for strip in timeline_data:
        inputs.extend(["-i", strip["filepath"]])
        if lut_file and os.path.exists(lut_file):
            filters.append(f"lut3d=file='{lut_file}'")

    filter_complex = ",".join(filters)
    command = [
        ffmpeg_path, *inputs, "-filter_complex", filter_complex if filter_complex else "",
        "-s", resolution, "-r", str(fps), "-c:v", codec, "-b:v", bitrate, output_path
    ]
    return [arg for arg in command if arg]
"""
}

# Generate all files and structure
def create_files():
    if os.path.exists(ADDON_DIR):
        shutil.rmtree(ADDON_DIR)
    os.makedirs(ADDON_DIR)

    for file_name, content in FILES.items():
        with open(os.path.join(ADDON_DIR, file_name), "w") as f:
            f.write(content)
        print(f"Created: {file_name}")

if __name__ == "__main__":
    create_files()
    print(f"Add-on '{ADDON_NAME}' created. Zip the folder and install it in Blender.")
