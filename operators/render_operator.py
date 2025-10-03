# render_operator.py: Advanced rendering operators for VSEndless
# Inputs: Blender context, VSE sequences, properties
# Outputs: Rendered video, logs, GPU diagnostics

import bpy
import os
import json
import subprocess
import logging
from ..utils import ffmpeg_utils, sequence_utils

logger = logging.getLogger("VSEndless.Operators")

class VSEndless_OT_CheckGPU(bpy.types.Operator):
    bl_idname = "vsendless.check_gpu"
    bl_label = "Check GPU Capabilities"
    bl_description = "Check for NVIDIA GPU and FFmpeg NVENC support"

    def execute(self, context):
        # Check for NVIDIA GPU
        try:
            result = subprocess.run([
                "nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
            if result.returncode == 0 and result.stdout:
                gpu_info = result.stdout.strip()
                self.report({'INFO'}, f"NVIDIA GPU detected: {gpu_info}")
                logger.info(f"GPU detected: {gpu_info}")
            else:
                self.report({'WARNING'}, "No NVIDIA GPU detected or nvidia-smi not found.")
                logger.warning("No NVIDIA GPU detected")
        except Exception as e:
            self.report({'ERROR'}, f"GPU check failed: {e}")
            logger.error(f"GPU check failed: {e}")

        # Check for FFmpeg NVENC
        try:
            ffmpeg_result = subprocess.run(["ffmpeg", "-encoders"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
            if "nvenc" in ffmpeg_result.stdout:
                self.report({'INFO'}, "FFmpeg NVENC support detected.")
                logger.info("FFmpeg NVENC support available")
            else:
                self.report({'WARNING'}, "FFmpeg NVENC support NOT detected.")
                logger.warning("FFmpeg NVENC not available")
        except Exception as e:
            self.report({'ERROR'}, f"FFmpeg check failed: {e}")
            logger.error(f"FFmpeg check failed: {e}")
        return {'FINISHED'}

class VSEndless_RenderJob:
    def __init__(self, name, func, dependencies=None):
        self.name = name
        self.func = func
        self.dependencies = dependencies or []
        self.completed = False

class VSEndless_OT_RenderQueue(bpy.types.Operator):
    bl_idname = "vsendless.render_queue"
    bl_label = "Render Queue"
    bl_description = "Batch render queue for VSEndless with dependency management"

    jobs = []

    @classmethod
    def add_job(cls, name, func, dependencies=None):
        cls.jobs.append(VSEndless_RenderJob(name, func, dependencies))

    @classmethod
    def clear_jobs(cls):
        cls.jobs.clear()

    def execute(self, context):
        # Example: Add a test job and run the queue
        def test_job():
            self.report({'INFO'}, "Test job executed.")
        self.add_job("TestJob", test_job)
        executed = set()
        for job in self.jobs:
            self._execute_job(job, executed)
        self.report({'INFO'}, f"Render queue executed: {len(self.jobs)} jobs")
        self.clear_jobs()
        return {'FINISHED'}

    def _execute_job(self, job, executed):
        for dep in job.dependencies:
            if dep not in executed:
                dep_job = next((j for j in self.jobs if j.name == dep), None)
                if dep_job:
                    self._execute_job(dep_job, executed)
        if not job.completed:
            job.func()
            job.completed = True
            executed.add(job.name)

class VSEndless_OT_Stream(bpy.types.Operator):
    bl_idname = "vsendless.stream"
    bl_label = "Stream to RTMP"
    bl_description = "Stream render output directly to RTMP"

    def execute(self, context):
        rtmp_url = getattr(context.scene, 'vsendless_rtmp_url', 'rtmp://localhost/live')
        self.report({'INFO'}, f"Streaming to {rtmp_url} (feature in development)")
        logger.info(f"Stream initiated to {rtmp_url}")
        return {'FINISHED'}

class VSEndless_OT_Render(bpy.types.Operator):
    bl_idname = "vsendless.render"
    bl_label = "VSEndless Render"
    bl_description = "Render the VSE timeline using advanced GPU acceleration"

    def execute(self, context):
        scene = context.scene
        props = scene.vsendless_props if hasattr(scene, 'vsendless_props') else None

        if props:
            output_path = bpy.path.abspath(props.output_path)
        else:
            output_path = bpy.path.abspath(scene.render.filepath)
            if not output_path.endswith(".mp4"):
                output_path += ".mp4"

        # Extract timeline data
        timeline_data = sequence_utils.get_sequences(context)
        if not timeline_data:
            self.report({'ERROR'}, "No sequences found in VSE!")
            logger.error("No sequences found for rendering")
            return {'CANCELLED'}

        # Construct FFmpeg command
        ffmpeg_cmd = ffmpeg_utils.construct_ffmpeg_command(scene, timeline_data, output_path)
        if not ffmpeg_cmd:
            self.report({'ERROR'}, "Failed to build FFmpeg command!")
            logger.error("FFmpeg command construction failed")
            return {'CANCELLED'}

        try:
            logger.info(f"Starting render: {' '.join(map(str, ffmpeg_cmd))}")
            process = subprocess.run(ffmpeg_cmd, check=True, text=True, capture_output=True)
            self.report({'INFO'}, f"Render complete: {output_path}")
            logger.info(f"Render completed successfully: {output_path}")
            if process.stdout:
                logger.debug(f"FFmpeg output: {process.stdout}")
        except subprocess.CalledProcessError as e:
            self.report({'ERROR'}, f"Render failed: {e.stderr}")
            logger.error(f"Render failed: {e.stderr}")
            return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"Unexpected error: {e}")
            logger.error(f"Unexpected render error: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}

class VSEndless_OT_AddonRefresh(bpy.types.Operator):
    bl_idname = "vsendless.addon_refresh"
    bl_label = "Refresh Add-ons"
    bl_description = "Scan add-on directories for new or updated modules (Blender 4.5+)"

    def execute(self, context):
        try:
            bpy.ops.preferences.addon_refresh()
            self.report({'INFO'}, "Add-ons refreshed.")
            logger.info("Add-on refresh completed")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to refresh add-ons: {e}")
            logger.error(f"Add-on refresh failed: {e}")
        return {'FINISHED'}

def register():
    try:
        bpy.utils.register_class(VSEndless_OT_Render)
        bpy.utils.register_class(VSEndless_OT_RenderQueue)
        bpy.utils.register_class(VSEndless_OT_Stream)
        bpy.utils.register_class(VSEndless_OT_CheckGPU)
        bpy.utils.register_class(VSEndless_OT_AddonRefresh)
        logger.info("VSEndless operators registered")
    except RuntimeError as e:
        logger.warning(f"Operator registration issue: {e}")

def unregister():
    try:
        bpy.utils.unregister_class(VSEndless_OT_Render)
        bpy.utils.unregister_class(VSEndless_OT_RenderQueue)
        bpy.utils.unregister_class(VSEndless_OT_Stream)
        bpy.utils.unregister_class(VSEndless_OT_CheckGPU)
        bpy.utils.unregister_class(VSEndless_OT_AddonRefresh)
        logger.info("VSEndless operators unregistered")
    except RuntimeError as e:
        logger.warning(f"Operator unregistration issue: {e}")
