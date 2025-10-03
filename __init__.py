# VSEndless Render Engine: Advanced GPU-accelerated render engine for Blender 4.5+

bl_info = {
    "name": "VSEndless - GPU Accelerated Render Engine",
    "author": "yavru421",
    "version": (5, 0, 0),
    "blender": (4, 5, 0),
    "location": "Video Sequence Editor > Sidebar > VSEndless",
    "description": "Advanced GPU-accelerated render engine with NVENC support for Blender 4.5+ VSE",
    "category": "Sequencer",
    "doc_url": "https://github.com/yavru421/VSEndless-Render-Engine-blender4.5",
    "tracker_url": "https://github.com/yavru421/VSEndless-Render-Engine-blender4.5/issues",
    "support": "COMMUNITY"
}

# Pipeline: Import and register all modules

import bpy

# Minimal Render Engine class

class VSEndlessRenderEngine(bpy.types.RenderEngine):
    bl_idname = "VSENDLESS_RENDER_ENGINE"
    bl_label = "VSEndless GPU Render Engine"
    bl_use_preview = False

    # Standard Render Engine settings integration
    @classmethod
    def register(cls):
        # Add custom properties for bleeding-edge features if needed
        bpy.types.Scene.vsendless_enable_hdr = bpy.props.BoolProperty(
            name="Enable HDR",
            description="Enable High Dynamic Range rendering",
            default=False
        )
        bpy.types.Scene.vsendless_output_format = bpy.props.EnumProperty(
            name="Output Format",
            description="File format for output",
            items=[
                ("PNG", "PNG", "Lossless image sequence"),
                ("JPEG", "JPEG", "Compressed image sequence"),
                ("FFMPEG", "FFmpeg Video", "Video output via ffmpeg")
            ],
            default="FFMPEG"
        )
        bpy.types.Scene.vsendless_color_management = bpy.props.EnumProperty(
            name="Color Management",
            description="Color management mode",
            items=[
                ("FILMIC", "Filmic", "Blender Filmic"),
                ("STANDARD", "Standard", "Standard sRGB")
            ],
            default="FILMIC"
        )

    @classmethod
    def unregister(cls):
        del bpy.types.Scene.vsendless_enable_hdr
        del bpy.types.Scene.vsendless_output_format
        del bpy.types.Scene.vsendless_color_management

    def render(self, depsgraph):
        import subprocess
        from .utils import ffmpeg_utils, sequence_utils
        scene = depsgraph.scene_eval
        output_path = scene.vsendless_props.output_path if hasattr(scene, 'vsendless_props') else scene.render.filepath
        # Collect timeline data and per-strip filters
        timeline_data = []
        if scene.sequence_editor:
            for s in scene.sequence_editor.sequences_all:
                timeline_data.append({
                    'name': s.name,
                    'filepath': getattr(s, 'filepath', ''),
                    'type': s.type,
                    'ffmpeg_filter': getattr(s, 'ffmpeg_filter', '')
                })
        # Build ffmpeg command using all properties
        try:
            ffmpeg_cmd = ffmpeg_utils.construct_ffmpeg_command(scene, timeline_data, output_path)
            if not ffmpeg_cmd:
                self.report({'ERROR'}, "Failed to build FFmpeg command!")
                return
            self.report({'INFO'}, f"Running FFmpeg: {' '.join(map(str, ffmpeg_cmd))}")
            process = subprocess.run(ffmpeg_cmd, check=True, text=True, capture_output=True)
            self.report({'INFO'}, f"Render completed: {output_path}")
            if process.stdout:
                print(process.stdout)
            if process.stderr:
                print(process.stderr)
        except Exception as e:
            self.report({'ERROR'}, f"FFmpeg failed: {e}")
            print(f"FFmpeg failed: {e}")
        return

from . import operators
from . import properties
from . import ui
from . import utils

def register():
    bpy.utils.register_class(VSEndlessRenderEngine)
    VSEndlessRenderEngine.register()
    operators.register()
    properties.register()
    ui.register()
    utils.register()

def unregister():
    ui.unregister()
    properties.unregister()
    operators.unregister()
    utils.unregister()
    try:
        VSEndlessRenderEngine.unregister()
        bpy.utils.unregister_class(VSEndlessRenderEngine)
    except Exception:
        pass
