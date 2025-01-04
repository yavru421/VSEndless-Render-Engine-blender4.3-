
import bpy
import subprocess
<<<<<<< HEAD:operators/render_operator.py
from ..utils.ffmpeg_utils import construct_ffmpeg_command, call_groq_api
from ..utils.sequence_utils import extract_timeline_data
=======
from .ffmpeg_utils import construct_ffmpeg_command
from .sequence_utils import extract_timeline_data
>>>>>>> 05119fb (zipped correct format for direct download and install into blender):vsendless/render_operator.py

class VSEndlessRenderEngine(bpy.types.RenderEngine):
    bl_idname = "VSENDLESS_RENDER_ENGINE"
    bl_label = "VSEndless Render Engine"
    bl_use_preview = False

    def render(self, depsgraph):
        scene = depsgraph.scene
        output_path = bpy.path.abspath(scene.render.filepath)

        # Use Groq API for AI-powered enhancements if enabled
        if getattr(scene, 'groq_api_enabled', False) and getattr(scene, 'groq_api_key', None):
            prompt = f"Suggest creative post-processing for a {scene.output_format} render, {scene.ffmpeg_codec} codec, {scene.ffmpeg_bitrate} Mbps, preset {scene.ffmpeg_preset}. User LUT: {scene.lut_file_path if scene.apply_lut else 'None'}."
            ai_suggestion = call_groq_api(prompt, scene.groq_api_key)
            self.report({'INFO'}, f"Groq AI Suggestion: {ai_suggestion}")
            print(f"Groq AI Suggestion: {ai_suggestion}")

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
