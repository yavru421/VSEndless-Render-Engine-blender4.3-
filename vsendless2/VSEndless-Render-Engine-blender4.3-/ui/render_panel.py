import bpy
import logging

logger = logging.getLogger("VSEndless.UI")

class VSEndlessRenderPanel(bpy.types.Panel):
    bl_label = "VSEndless Render Settings"
    bl_idname = "RENDER_PT_vsendless_settings"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        try:
            # Resolution Settings
            box = layout.box()
            box.label(text="Resolution Settings:", icon='MOD_UVPROJECT')
            col = box.column(align=True)
            col.prop(scene.render, "resolution_x", text="Resolution X")
            col.prop(scene.render, "resolution_y", text="Resolution Y")
            col.prop(scene.render, "fps", text="Frame Rate")

            # GPU Acceleration Settings
            box = layout.box()
            box.label(text="GPU Acceleration:", icon='CONSOLE')
            col = box.column()
            col.prop(scene, "use_hwaccel", text="Hardware Acceleration")
            if getattr(scene, "use_hwaccel", False):
                col.prop(scene, "hwaccel_method", text="Method")
            col.separator()
            col.label(text="GPU Processing:")
            col.prop(scene, "use_gpu_scaling", text="GPU Scaling")
            col.prop(scene, "use_gpu_denoising", text="GPU Denoising")
            col.prop(scene, "use_gpu_stabilization", text="GPU Stabilization")

            # Add GPU check button
            layout.operator("vsendless.check_gpu", text="Check GPU Capabilities", icon='GPU')

            # VSEndless Video Settings
            box = layout.box()
            box.label(text="Video Codec Settings:", icon='RENDER_ANIMATION')
            col = box.column()
            col.prop(scene, "ffmpeg_codec", text="Codec")
            # Profile based on selected codec
            if getattr(scene, "ffmpeg_codec", "H264") == 'H264':
                col.prop(scene, "h264_profile", text="Profile")
            else:
                col.prop(scene, "hevc_profile", text="Profile")
            # NVENC settings
            col.label(text="NVENC Settings:")
            col.prop(scene, "nvenc_preset", text="Quality Preset")
            col.prop(scene, "nvenc_tune", text="Tuning")
            col.prop(scene, "use_multipass", text="2-Pass Encoding")
            # Bitrate settings
            col.separator()
            col.label(text="Bitrate Control:")
            col.prop(scene, "rate_control_mode", text="Rate Control")
            if getattr(scene, "rate_control_mode", "VBR") in ['CBR', 'VBR']:
                col.prop(scene, "ffmpeg_bitrate", text="Bitrate (Mbps)")
            elif getattr(scene, "rate_control_mode", "VBR") in ['CQP', 'CRF']:
                col.prop(scene, "constant_quality_level", text="Quality (Lower is better)")
            col.separator()
            col.prop(scene, "ffmpeg_aspect_ratio", text="Aspect Ratio")
            col.prop(scene, "ffmpeg_custom_fps", text="Custom FPS")
            if getattr(scene, "ffmpeg_custom_fps", False):
                col.prop(scene, "ffmpeg_frame_rate", text="Frame Rate")

            # Post-Processing Options
            box = layout.box()
            box.label(text="Post-Processing:", icon='COLORSET_01_VEC')
            col = box.column()
            # Denoising
            row = col.row()
            row.prop(scene, "enable_denoising", text="Enable Denoising")
            if getattr(scene, "enable_denoising", False):
                row.prop(scene, "denoise_strength", text="Strength")
            # Stabilization
            col.prop(scene, "apply_stabilization", text="Apply Stabilization")
            # LUT
            col.prop(scene, "apply_lut", text="Use LUT for Color Correction")
            if getattr(scene, "apply_lut", False):
                col.prop(scene, "lut_file_path", text="LUT File")

            # Presets
            box = layout.box()
            box.label(text="Presets:", icon='PRESET')
            row = box.row(align=True)
            row.operator("vsendless.save_preset", text="Save")
            row.operator("vsendless.load_preset", text="Load")
            row.operator("vsendless.reset_preset", text="Reset")
        except (RuntimeError, ValueError, TypeError) as e:
            logger.error("Error drawing VSEndlessRenderPanel: %s", e)
