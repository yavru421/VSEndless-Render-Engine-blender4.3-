bl_info = {
    "name": "VSEndless - GPU Accelerated Render Engine",
    "blender": (4, 3, 0),
    "category": "Render",
    "version": (3, 0, 2),
    "description": "NVIDIA GPU accelerated render engine for Blender's VSE with CUDA, NVENC and advanced post-processing.",
    "author": "John Daniel Dondlinger",
}

import bpy
import subprocess
import shutil
import os
from .operators.render_operator import VSEndlessRenderEngine
from .ui.render_panel import VSEndlessRenderPanel
from .properties.render_properties import register_properties, unregister_properties
from .utils.presets import register_presets, unregister_presets

def check_gpu_capabilities():
    """Check for NVIDIA GPU and FFmpeg with NVENC support"""
    gpu_info = {"has_nvidia": False, "has_nvenc": False, "gpu_name": "", "vram_gb": 0}
    
    # Check for NVIDIA GPU
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
                    pass
    except (FileNotFoundError, subprocess.SubprocessError):
        pass
    
    # Check for FFmpeg with NVENC
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        try:
            result = subprocess.run(
                [ffmpeg_path, "-encoders"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if "h264_nvenc" in result.stdout:
                gpu_info["has_nvenc"] = True
        except (FileNotFoundError, subprocess.SubprocessError):
            pass
    
    return gpu_info

def show_gpu_notification(self, context):
    gpu_info = getattr(bpy.types, "vsendless_gpu_info", {"has_nvidia": False, "has_nvenc": False})
    
    if gpu_info["has_nvidia"] and gpu_info["has_nvenc"]:
        self.layout.label(text=f"VSEndless: GPU Acceleration Ready - {gpu_info.get('gpu_name', 'NVIDIA GPU')} ({gpu_info.get('vram_gb', 0)}GB)")
    elif gpu_info["has_nvidia"]:
        self.layout.label(text="VSEndless: NVIDIA GPU detected, but FFmpeg lacks NVENC support")
    else:
        self.layout.label(text="VSEndless: No NVIDIA GPU detected, falling back to CPU rendering")

def register():
    bpy.utils.register_class(VSEndlessRenderEngine)
    bpy.utils.register_class(VSEndlessRenderPanel)
    register_properties()
    register_presets()
    
    # Store GPU information
    gpu_info = check_gpu_capabilities()
    setattr(bpy.types, "vsendless_gpu_info", gpu_info)
    
    # Show notification about GPU capabilities
    bpy.app.timers.register(
        lambda: bpy.context.window_manager.popup_menu(show_gpu_notification, title="VSEndless GPU Status", icon='INFO'),
        first_interval=1.0
    )
    
    print(f"VSEndless Render Engine initialized. GPU Acceleration: {'Available' if gpu_info['has_nvidia'] and gpu_info['has_nvenc'] else 'Limited or Unavailable'}")

def unregister():
    bpy.utils.unregister_class(VSEndlessRenderEngine)
    bpy.utils.unregister_class(VSEndlessRenderPanel)
    unregister_properties()
    unregister_presets()
    
    if hasattr(bpy.types, "vsendless_gpu_info"):
        delattr(bpy.types, "vsendless_gpu_info")

if __name__ == "__main__":
    register()
