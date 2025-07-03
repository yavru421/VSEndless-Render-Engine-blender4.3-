import bpy
import json
import os

PRESET_FILE = os.path.join(bpy.utils.user_resource('SCRIPTS', path="presets"), "vsendless_presets.json")

def save_preset(context):
    scene = context.scene
    preset_data = {
        # Existing properties
        "ffmpeg_codec": scene.ffmpeg_codec,
        "ffmpeg_bitrate": scene.ffmpeg_bitrate,
        "ffmpeg_preset": scene.ffmpeg_preset,
        "ffmpeg_aspect_ratio": scene.ffmpeg_aspect_ratio,
        "ffmpeg_custom_fps": scene.ffmpeg_custom_fps,
        "ffmpeg_frame_rate": scene.ffmpeg_frame_rate,
        "enable_denoising": scene.enable_denoising,
        "apply_stabilization": scene.apply_stabilization,
        "apply_lut": scene.apply_lut,
        "lut_file_path": scene.lut_file_path,
        
        # New GPU-related settings
        "use_hwaccel": scene.use_hwaccel,
        "hwaccel_method": scene.hwaccel_method,
        "nvenc_preset": scene.nvenc_preset,
        "nvenc_tune": scene.nvenc_tune,
        "h264_profile": scene.h264_profile,
        "hevc_profile": scene.hevc_profile,
        "rate_control_mode": scene.rate_control_mode,
        "constant_quality_level": scene.constant_quality_level,
        "use_multipass": scene.use_multipass,
        "use_gpu_scaling": scene.use_gpu_scaling,
        "use_gpu_denoising": scene.use_gpu_denoising,
        "denoise_strength": scene.denoise_strength,
        "use_gpu_stabilization": scene.use_gpu_stabilization,
    }
    os.makedirs(os.path.dirname(PRESET_FILE), exist_ok=True)
    with open(PRESET_FILE, 'w') as f:
        json.dump(preset_data, f)
    print("Preset saved!")

def load_preset(context):
    scene = context.scene
    if not os.path.exists(PRESET_FILE):
        print("No preset found to load!")
        return
    with open(PRESET_FILE, 'r') as f:
        preset_data = json.load(f)
    for key, value in preset_data.items():
        if hasattr(scene, key):
            setattr(scene, key, value)
    print("Preset loaded!")

def reset_preset(context):
    scene = context.scene
    # Reset existing properties
    scene.ffmpeg_codec = 'H264'
    scene.ffmpeg_bitrate = 10
    scene.ffmpeg_preset = 'p5'
    scene.ffmpeg_aspect_ratio = "16:9"
    scene.ffmpeg_custom_fps = False
    scene.ffmpeg_frame_rate = 30
    scene.enable_denoising = False
    scene.apply_stabilization = False
    scene.apply_lut = False
    scene.lut_file_path = ""
    
    # Reset new GPU-related properties
    scene.use_hwaccel = True
    scene.hwaccel_method = 'CUDA'
    scene.nvenc_preset = 'p3'
    scene.nvenc_tune = 'hq'
    scene.h264_profile = 'high'
    scene.hevc_profile = 'main'
    scene.rate_control_mode = 'VBR'
    scene.constant_quality_level = 23
    scene.use_multipass = False
    scene.use_gpu_scaling = True
    scene.use_gpu_denoising = True
    scene.denoise_strength = 3.0
    scene.use_gpu_stabilization = True
    
    print("Preset reset to defaults!")

class SavePresetOperator(bpy.types.Operator):
    bl_idname = "vsendless.save_preset"
    bl_label = "Save Preset"

    def execute(self, context):
        save_preset(context)
        return {'FINISHED'}

class LoadPresetOperator(bpy.types.Operator):
    bl_idname = "vsendless.load_preset"
    bl_label = "Load Preset"

    def execute(self, context):
        load_preset(context)
        return {'FINISHED'}

class ResetPresetOperator(bpy.types.Operator):
    bl_idname = "vsendless.reset_preset"
    bl_label = "Reset Preset"

    def execute(self, context):
        reset_preset(context)
        return {'FINISHED'}

def register_presets():
    bpy.utils.register_class(SavePresetOperator)
    bpy.utils.register_class(LoadPresetOperator)
    bpy.utils.register_class(ResetPresetOperator)

def unregister_presets():
    bpy.utils.unregister_class(SavePresetOperator)
    bpy.utils.unregister_class(LoadPresetOperator)
    bpy.utils.unregister_class(ResetPresetOperator)
