import bpy
import subprocess
import shutil
import logging
from typing import Dict, Any
import requests
from .operators.render_operator import VSEndlessRenderEngine
from .properties.render_properties import register_properties, unregister_properties
from .ui.render_panel import VSEndlessRenderPanel
from .utils.presets import register_presets, unregister_presets

bl_info = {
    "name": "VSEndless Render Engine",
    "author": "yavru421",
    "version": (2, 1, 0),
    "blender": (4, 3, 0),
    "location": "Properties > Output > VSEndless Render Settings",
    "description": "GPU-accelerated render engine for video sequences using FFmpeg with NVENC and Llama API integration",
    "warning": "",
    "doc_url": "https://github.com/yavru421/VSEndless-Render-Engine-blender4.3-",
    "category": "Render",
    "support": "COMMUNITY",
    "bl_module_name": __name__
}

# Setup logging
logger = logging.getLogger("VSEndless")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(name)s: %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

def check_gpu_capabilities() -> Dict[str, Any]:
    """Check for NVIDIA GPU and FFmpeg with NVENC support"""
    gpu_info = {"has_nvidia": False, "has_nvenc": False, "gpu_name": "", "vram_gb": 0}
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False
        )
        if result.returncode == 0 and result.stdout:
            parts = result.stdout.strip().split(',')
            if len(parts) >= 2:
                gpu_info["has_nvidia"] = True
                gpu_info["gpu_name"] = parts[0].strip()
                try:
                    gpu_info["vram_gb"] = round(float(parts[1].strip()) / 1024, 1)
                except (ValueError, IndexError):
                    logger.warning("Failed to parse VRAM info from nvidia-smi output.")
    except (FileNotFoundError, subprocess.SubprocessError) as e:
        logger.warning("nvidia-smi not found or failed: %s", e)
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        try:
            result = subprocess.run(
                [ffmpeg_path, "-encoders"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False
            )
            if "h264_nvenc" in result.stdout:
                gpu_info["has_nvenc"] = True
        except (FileNotFoundError, subprocess.SubprocessError) as e:
            logger.warning("ffmpeg encoder check failed: %s", e)
    return gpu_info

class VSEndlessCheckGPUOperator(bpy.types.Operator):
    bl_idname = "vsendless.check_gpu"
    bl_label = "Check GPU Capabilities"

    def execute(self, context):
        gpu_info = check_gpu_capabilities()
        bpy.types.vsendless_gpu_info = gpu_info  # Store GPU info
        show_gpu_notification(self, context)
        return {'FINISHED'}

def show_gpu_notification(self, _context):
    gpu_info = getattr(bpy.types, "vsendless_gpu_info", {"has_nvidia": False, "has_nvenc": False})
    if gpu_info["has_nvidia"] and gpu_info["has_nvenc"]:
        self.report({'INFO'}, f"VSEndless: GPU Acceleration Ready - {gpu_info.get('gpu_name', 'NVIDIA GPU')} ({gpu_info.get('vram_gb', 0)}GB)")
    elif gpu_info["has_nvidia"]:
        self.report({'WARNING'}, "VSEndless: NVIDIA GPU detected, but FFmpeg lacks NVENC support")
    else:
        self.report({'WARNING'}, "VSEndless: No NVIDIA GPU detected, falling back to CPU rendering")

def register():
    try:
        bpy.utils.register_class(VSEndlessRenderEngine)
        register_properties()
        bpy.utils.register_class(VSEndlessRenderPanel)
        register_presets()
        bpy.utils.register_class(VSEndlessCheckGPUOperator)
        gpu_info = check_gpu_capabilities()
        bpy.types.vsendless_gpu_info = gpu_info
        logger.info(
            "VSEndless Render Engine initialized. GPU Acceleration: %s",
            'Available' if gpu_info['has_nvidia'] and gpu_info['has_nvenc'] else 'Limited or Unavailable'
        )
    except (RuntimeError, ValueError, TypeError) as e:
        logger.error("Error during registration: %s", e)

def unregister():
    try:
        unregister_presets()
        bpy.utils.unregister_class(VSEndlessRenderPanel)
        unregister_properties()
        bpy.utils.unregister_class(VSEndlessRenderEngine)
        bpy.utils.unregister_class(VSEndlessCheckGPUOperator)
        if hasattr(bpy.types, "vsendless_gpu_info"):
            delattr(bpy.types, "vsendless_gpu_info")
        logger.info("VSEndless Render Engine unregistered.")
    except (RuntimeError, ValueError, TypeError) as e:
        logger.error("Error during unregistration: %s", e)

if __name__ == "__main__":
    register()
