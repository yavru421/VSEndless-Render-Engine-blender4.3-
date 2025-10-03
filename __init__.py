# VSEndless Render Engine: APT-compliant GPU-accelerated render engine for Blender 4.5+
# Algebraic Pipeline Theory Implementation
# Mathematical Foundation: Compositional video processing with algebraic guarantees

bl_info = {
    "name": "VSEndless - GPU Accelerated Render Engine (APT)",
    "author": "yavru421",
    "version": (5, 0, 1),
    "blender": (4, 5, 0),
    "location": "Video Sequence Editor > Sidebar > VSEndless",
    "description": "APT-compliant GPU-accelerated render engine with AI and cloud capabilities",
    "category": "Sequencer",
    "doc_url": "https://github.com/yavru421/VSEndless-Render-Engine-blender4.3-",
    "tracker_url": "https://github.com/yavru421/VSEndless-Render-Engine-blender4.3-/issues",
    "support": "COMMUNITY",
    "versionsize": "5.0.1",
    "package_size_kb": 48
}

# APT Pipeline: Import and register all modules with algebraic composition

import bpy

# Minimal Render Engine class (APT-compliant)

class VSEndlessRenderEngine(bpy.types.RenderEngine):
    """
    APT-compliant render engine

    Algebraic Notation: Let x₁ = scene_data, y₁ = rendered_output
    y₁ = render_engine(x₁) where render_engine: SceneData → RenderedOutput
    """
    bl_idname = "VSENDLESS_RENDER_ENGINE"
    bl_label = "VSEndless GPU Render Engine (APT)"
    bl_use_preview = False

    # APT Stage: Property registration
    @classmethod
    def register(cls):
        # APT: Define property domain mappings
        bpy.types.Scene.vsendless_enable_hdr = bpy.props.BoolProperty(
            name="Enable HDR",
            description="Enable High Dynamic Range rendering (APT: Bool → RenderMode)",
            default=False
        )
        bpy.types.Scene.vsendless_output_format = bpy.props.EnumProperty(
            name="Output Format",
            description="File format for output (APT: Enum → FileFormat)",
            items=[
                ("PNG", "PNG", "Lossless image sequence"),
                ("JPEG", "JPEG", "Compressed image sequence"),
                ("FFMPEG", "FFmpeg Video", "Video output via ffmpeg")
            ],
            default="FFMPEG"
        )
        bpy.types.Scene.vsendless_color_management = bpy.props.EnumProperty(
            name="Color Management",
            description="Color management mode (APT: Enum → ColorSpace)",
            items=[
                ("FILMIC", "Filmic", "Blender Filmic"),
                ("STANDARD", "Standard", "Standard sRGB")
            ],
            default="FILMIC"
        )

    @classmethod
    def unregister(cls):
        # APT: Clean property domain unmapping
        del bpy.types.Scene.vsendless_enable_hdr
        del bpy.types.Scene.vsendless_output_format
        del bpy.types.Scene.vsendless_color_management

    def render(self, depsgraph):
        """
        APT render function

        Mathematical Definition:
        render: DepsgraphData → RenderedOutput
        render(d) = execute_ffmpeg(construct_command(extract_timeline(d)))
        """
        import subprocess
        from .utils import ffmpeg_utils, sequence_utils

        # APT Stage 1: Data extraction
        scene = depsgraph.scene_eval
        output_path = scene.vsendless_props.output_path if hasattr(scene, 'vsendless_props') else scene.render.filepath

        # APT Stage 2: Timeline data collection
        timeline_data = []
        if scene.sequence_editor:
            for s in scene.sequence_editor.sequences_all:
                timeline_data.append({
                    'name': s.name,
                    'filepath': getattr(s, 'filepath', ''),
                    'type': s.type,
                    'ffmpeg_filter': getattr(s, 'ffmpeg_filter', '')
                })

        # APT Stage 3: Command construction
        try:
            ffmpeg_cmd = ffmpeg_utils.construct_ffmpeg_command(scene, timeline_data, output_path)
            if not ffmpeg_cmd:
                self.report({'ERROR'}, "APT Error: Failed to construct FFmpeg command")
                return

            # APT Stage 4: Execution
            self.report({'INFO'}, f"APT Render: {' '.join(map(str, ffmpeg_cmd))}")
            process = subprocess.run(ffmpeg_cmd, check=True, text=True, capture_output=True)

            # APT Stage 5: Verification
            self.report({'INFO'}, f"APT Render completed: {output_path}")
            if process.stdout:
                print(f"[APT] FFmpeg stdout: {process.stdout}")
            if process.stderr:
                print(f"[APT] FFmpeg stderr: {process.stderr}")

        except Exception as e:
            self.report({'ERROR'}, f"APT Render failed: {e}")
            print(f"[APT] Render error: {e}")
        return

# APT Module imports with dependency tracking
from . import operators
from . import properties
from . import ui
from . import utils

def register():
    """APT registration pipeline"""
    print("[APT] Initializing VSEndless with Algebraic Pipeline Theory")

    # APT Stage 1: Core engine registration
    try:
        bpy.utils.register_class(VSEndlessRenderEngine)
        VSEndlessRenderEngine.register()
    except Exception as e:
        print(f"[APT] Error registering VSEndlessRenderEngine: {e}")
        try:
            VSEndlessRenderEngine.unregister()
            bpy.utils.unregister_class(VSEndlessRenderEngine)
        except Exception:
            pass
        raise

    # APT Stage 2: Module registration (order matters for dependencies)
    try:
        utils.register()      # Base utilities first
        properties.register() # Properties depend on utilities
        operators.register()  # Operators depend on properties and utilities
        ui.register()        # UI depends on all previous stages
    except Exception as e:
        print(f"[APT] Error in module registration: {e}")
        unregister()
        raise

    print("[APT] VSEndless pipeline stages activated successfully")

def unregister():
    """APT unregistration pipeline (reverse order)"""
    print("[APT] Deactivating VSEndless pipeline stages")

    # APT Cleanup: Reverse dependency order
    try:
        ui.unregister()
    except Exception as e:
        print(f"[APT] Error unregistering UI: {e}")
    try:
        operators.unregister()
    except Exception as e:
        print(f"[APT] Error unregistering operators: {e}")
    try:
        properties.unregister()
    except Exception as e:
        print(f"[APT] Error unregistering properties: {e}")
    try:
        utils.unregister()
    except Exception as e:
        print(f"[APT] Error unregistering utils: {e}")

    try:
        VSEndlessRenderEngine.unregister()
    except Exception as e:
        print(f"[APT] Error unregistering VSEndlessRenderEngine: {e}")
    try:
        bpy.utils.unregister_class(VSEndlessRenderEngine)
    except Exception as e:
        print(f"[APT] Error unregistering class VSEndlessRenderEngine: {e}")

    print("[APT] VSEndless pipeline deactivated")
