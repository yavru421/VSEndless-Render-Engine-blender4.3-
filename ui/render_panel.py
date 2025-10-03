# render_panel.py: Advanced UI panels for VSEndless Render Engine
# Inputs: Blender context, properties
# Outputs: UI panels in VSE sidebar and render properties

import bpy
import logging

logger = logging.getLogger("VSEndless.UI")

class VSEndless_PT_VSEPanel(bpy.types.Panel):
    bl_label = "VSEndless Render Settings"
    bl_idname = "VSEQUENCE_PT_vsendless_settings"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'VSEndless'

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = getattr(scene, 'vsendless_props', None)

        # Output Settings
        box = layout.box()
        box.label(text="Output Settings", icon='OUTPUT')
        if props:
            box.prop(props, "output_path")
            box.prop(props, "ffmpeg_codec")
            box.prop(props, "ffmpeg_framerate")
            box.prop(props, "ffmpeg_resolution_x")
            box.prop(props, "ffmpeg_resolution_y")
            box.prop(props, "ffmpeg_bitrate")
        else:
            box.label(text="Properties not loaded", icon='ERROR')

        if hasattr(scene, 'vsendless_output_format'):
            box.prop(scene, "vsendless_output_format")
        if hasattr(scene, 'vsendless_color_management'):
            box.prop(scene, "vsendless_color_management")
        if hasattr(scene, 'vsendless_enable_hdr'):
            box.prop(scene, "vsendless_enable_hdr")

        # GPU & Codec Settings
        box2 = layout.box()
        box2.label(text="GPU & Codec Settings", icon='CONSOLE')
        if hasattr(scene, 'use_hwaccel'):
            box2.prop(scene, "use_hwaccel")
        if hasattr(scene, 'hwaccel_method'):
            box2.prop(scene, "hwaccel_method")
        if hasattr(scene, 'nvenc_preset'):
            box2.prop(scene, "nvenc_preset")
        if hasattr(scene, 'nvenc_tune'):
            box2.prop(scene, "nvenc_tune")
        if hasattr(scene, 'h264_profile'):
            box2.prop(scene, "h264_profile")
        if hasattr(scene, 'hevc_profile'):
            box2.prop(scene, "hevc_profile")
        if hasattr(scene, 'rate_control_mode'):
            box2.prop(scene, "rate_control_mode")
        if hasattr(scene, 'constant_quality_level'):
            box2.prop(scene, "constant_quality_level")
        if hasattr(scene, 'use_multipass'):
            box2.prop(scene, "use_multipass")

        # Post-Processing
        box3 = layout.box()
        box3.label(text="Post-Processing", icon='TOOL_SETTINGS')
        if hasattr(scene, 'enable_denoising'):
            box3.prop(scene, "enable_denoising")
        if hasattr(scene, 'use_gpu_denoising'):
            box3.prop(scene, "use_gpu_denoising")
        if hasattr(scene, 'denoise_strength') and getattr(scene, 'enable_denoising', False):
            box3.prop(scene, "denoise_strength")
        if hasattr(scene, 'apply_stabilization'):
            box3.prop(scene, "apply_stabilization")
        if hasattr(scene, 'use_gpu_stabilization'):
            box3.prop(scene, "use_gpu_stabilization")
        if hasattr(scene, 'use_gpu_scaling'):
            box3.prop(scene, "use_gpu_scaling")
        if hasattr(scene, 'apply_lut'):
            box3.prop(scene, "apply_lut")
        if hasattr(scene, 'lut_file_path') and getattr(scene, 'apply_lut', False):
            box3.prop(scene, "lut_file_path")

        # Operators
        layout.separator()
        layout.operator("vsendless.render", icon='RENDER_ANIMATION')
        layout.operator("vsendless.render_queue", icon='SEQ_SEQUENCER')
        if hasattr(scene, 'vsendless_rtmp_url'):
            layout.operator("vsendless.stream", icon='URL')
        layout.operator("vsendless.check_gpu", icon='CONSOLE')

class VSEndless_PT_StripPanel(bpy.types.Panel):
    bl_label = "VSEndless Strip Filters"
    bl_idname = "VSEQUENCE_PT_vsendless_strip"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'VSEndless'

    @classmethod
    def poll(cls, context):
        return (context.scene and
                context.scene.sequence_editor and
                context.active_sequence_strip is not None)

    def draw(self, context):
        layout = self.layout
        strip = context.active_sequence_strip

        if strip:
            # Custom FFmpeg filter for individual strips
            box = layout.box()
            box.label(text="Strip-specific Filters", icon='FILTER')
            if '["ffmpeg_filter"]' not in dir(strip):
                box.operator("vsendless.add_strip_filter", text="Add Custom Filter")
            else:
                box.prop(strip, '["ffmpeg_filter"]', text="FFmpeg Filter")

class VSEndless_PT_RenderProperties(bpy.types.Panel):
    bl_label = "VSEndless Render Engine"
    bl_idname = "RENDER_PT_vsendless_render"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == 'VSENDLESS_RENDER_ENGINE'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = getattr(scene, 'vsendless_props', None)

        # Main render settings
        box = layout.box()
        box.label(text="Render Settings", icon='RENDER_ANIMATION')
        if props:
            box.prop(props, "output_path")
            box.prop(props, "ffmpeg_codec")
            box.prop(props, "ffmpeg_pix_fmt")
            box.prop(props, "ffmpeg_framerate")
            row = box.row()
            row.prop(props, "ffmpeg_resolution_x")
            row.prop(props, "ffmpeg_resolution_y")
            box.prop(props, "ffmpeg_bitrate")

        # GPU Settings
        box2 = layout.box()
        box2.label(text="GPU Acceleration", icon='CONSOLE')
        if hasattr(scene, 'use_hwaccel'):
            box2.prop(scene, "use_hwaccel")
            if scene.use_hwaccel and hasattr(scene, 'hwaccel_method'):
                box2.prop(scene, "hwaccel_method")

        # Quick actions
        layout.separator()
        layout.operator("vsendless.render", text="Render Animation", icon='RENDER_ANIMATION')
        layout.operator("vsendless.check_gpu", text="Check GPU Capabilities", icon='CONSOLE')

def register():
    try:
        for cls in [VSEndless_PT_RenderProperties, VSEndless_PT_StripPanel, VSEndless_PT_VSEPanel]:
            try:
                bpy.utils.unregister_class(cls)
            except Exception:
                pass
            bpy.utils.register_class(cls)
        logger.info("VSEndless UI panels registered")
    except Exception as e:
        logger.warning(f"UI panel registration issue: {e}")
        raise

def unregister():
    try:
        bpy.utils.unregister_class(VSEndless_PT_RenderProperties)
        bpy.utils.unregister_class(VSEndless_PT_StripPanel)
        bpy.utils.unregister_class(VSEndless_PT_VSEPanel)
        logger.info("VSEndless UI panels unregistered")
    except Exception as e:
        logger.warning(f"UI panel unregistration issue: {e}")
