import bpy
import subprocess
import logging
from typing import Any
from ..utils.ffmpeg_utils import construct_ffmpeg_command
from ..utils.sequence_utils import extract_timeline_data

logger = logging.getLogger("VSEndless.Render")

class VSEndlessRenderEngine(bpy.types.RenderEngine):
    bl_idname = "VSENDLESS_RENDER_ENGINE"
    bl_label = "VSEndless"
    bl_use_preview = False
    bl_use_exclude_layers = True
    bl_use_shading_nodes_custom = False

    def render(self, depsgraph: Any) -> None:
        """Render the scene using FFmpeg and GPU acceleration if available."""
        scene = depsgraph.scene
        output_path = bpy.path.abspath(scene.render.filepath)
        if not output_path.endswith(".mp4"):
            output_path += ".mp4"

        # Input validation
        if not output_path or not isinstance(output_path, str):
            self.report({'ERROR'}, "Invalid output file path.")
            logger.error("Invalid output file path: %s", output_path)
            return

        timeline_data = extract_timeline_data(scene)
        if not timeline_data:
            self.report({'ERROR'}, "No sequences found in VSE!")
            logger.error("No sequences found in VSE!")
            return

        ffmpeg_cmd = construct_ffmpeg_command(scene, timeline_data, output_path)
        if not ffmpeg_cmd:
            self.report({'ERROR'}, "Failed to build FFmpeg command!")
            logger.error("Failed to build FFmpeg command!")
            return

        try:
            logger.info("Running FFmpeg command: %s", ' '.join(map(str, ffmpeg_cmd)))
            process = subprocess.run(ffmpeg_cmd, check=True, text=True, capture_output=True)
            self.report({'INFO'}, f"Render completed: {output_path}")
            logger.info("Render completed: %s", output_path)
            if process.stdout:
                logger.info("FFmpeg output: %s", process.stdout)
            if process.stderr:
                logger.warning("FFmpeg warnings/errors: %s", process.stderr)
        except subprocess.CalledProcessError as e:
            self.report({'ERROR'}, f"FFmpeg failed: {e.stderr}")
            logger.error("FFmpeg failed: %s", e.stderr)
        except (OSError, ValueError, RuntimeError) as e:
            self.report({'ERROR'}, f"Unexpected error: {e}")
            logger.error("Unexpected error during render: %s", e)
