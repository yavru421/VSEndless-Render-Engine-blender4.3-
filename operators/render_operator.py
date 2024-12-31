import bpy
import subprocess
from ..utils.ffmpeg_utils import construct_ffmpeg_command
from ..utils.sequence_utils import extract_timeline_data

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
