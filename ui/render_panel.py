import bpy

class VSEndlessRenderPanel(bpy.types.Panel):
    bl_label = "VSEndless Render Settings"
    bl_idname = "RENDER_PT_vsendless_settings"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Resolution Settings
        layout.label(text="Resolution Settings:")
        layout.prop(scene.render, "resolution_x", text="Resolution X")
        layout.prop(scene.render, "resolution_y", text="Resolution Y")
        layout.prop(scene.render, "fps", text="Frame Rate")

        layout.separator()

        # VSEndless Video Settings
        layout.label(text="VSEndless Video Settings:")
        layout.prop(scene, "output_format", text="Output Format")
        layout.prop(scene, "ffmpeg_codec", text="Codec")
        layout.prop(scene, "audio_codec", text="Audio Codec")
        layout.prop(scene, "ffmpeg_bitrate", text="Bitrate (Mbps)")
        layout.prop(scene, "ffmpeg_preset", text="Encoding Preset")
        layout.prop(scene, "ffmpeg_advanced_preset", text="Advanced Preset")
        layout.prop(scene, "ffmpeg_aspect_ratio", text="Aspect Ratio")
        layout.prop(scene, "ffmpeg_custom_fps", text="Custom FPS")
        if scene.ffmpeg_custom_fps:
            layout.prop(scene, "ffmpeg_frame_rate", text="Frame Rate")

        layout.separator()

        # Groq API Integration
        layout.label(text="Groq AI Integration:")
        layout.prop(scene, "groq_api_enabled", text="Enable Groq API")
        if scene.groq_api_enabled:
            layout.prop(scene, "groq_api_key", text="Groq API Key")

        layout.separator()

        # Post-Processing Options
        layout.label(text="Post-Processing:")
        layout.prop(scene, "enable_denoising", text="Enable Denoising")
        layout.prop(scene, "apply_stabilization", text="Apply Stabilization")
        layout.prop(scene, "apply_lut", text="Use LUT for Color Correction")
        if scene.apply_lut:
            layout.prop(scene, "lut_file_path", text="LUT File Path")

        layout.separator()

        # Presets
        layout.label(text="Presets:")
        row = layout.row(align=True)
        row.operator("vsendless.save_preset_named", text="Save Preset")
        row.operator("vsendless.load_preset_named", text="Load Preset")
        row.operator("vsendless.list_presets", text="List Presets")
        row = layout.row(align=True)
        row.operator("vsendless.export_preset", text="Export Preset")
        row.operator("vsendless.import_preset", text="Import Preset")
        row.operator("vsendless.reset_preset", text="Reset to Defaults")
