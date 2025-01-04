
import bpy

class VSEndlessRenderPanel(bpy.types.Panel):
    bl_label = "VSEndless Render Settings"
    bl_idname = "RENDER_PT_vsendless"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Render Settings:")
        layout.prop(scene.render, "resolution_x", text="Resolution X")
        layout.prop(scene.render, "resolution_y", text="Resolution Y")
        layout.prop(scene.render, "fps", text="Frame Rate")
        layout.prop(scene, "ffmpeg_codec", text="Codec")
        layout.prop(scene, "ffmpeg_bitrate", text="Bitrate (Mbps)")

        layout.label(text="Post-Processing:")
        layout.prop(scene, "enable_denoising", text="Enable Denoising")
        layout.prop(scene, "apply_stabilization", text="Apply Stabilization")
        layout.prop(scene, "lut_file_path", text="LUT File Path")

def register():
    bpy.utils.register_class(VSEndlessRenderPanel)

def unregister():
    bpy.utils.unregister_class(VSEndlessRenderPanel)
