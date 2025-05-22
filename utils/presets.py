import bpy
import json
import os

PRESET_DIR = os.path.join(bpy.utils.user_resource('SCRIPTS', path="presets"), "vsendless_presets")

# Save a named preset
def save_preset(context, preset_name):
    scene = context.scene
    preset_data = {
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
    }
    os.makedirs(PRESET_DIR, exist_ok=True)
    preset_path = os.path.join(PRESET_DIR, f"{preset_name}.json")
    with open(preset_path, 'w') as f:
        json.dump(preset_data, f)
    print(f"Preset '{preset_name}' saved!")

# Load a named preset
def load_preset(context, preset_name):
    scene = context.scene
    preset_path = os.path.join(PRESET_DIR, f"{preset_name}.json")
    if not os.path.exists(preset_path):
        print(f"No preset named '{preset_name}' found!")
        return
    with open(preset_path, 'r') as f:
        preset_data = json.load(f)
    for key, value in preset_data.items():
        setattr(scene, key, value)
    print(f"Preset '{preset_name}' loaded!")

# List all available presets
def list_presets():
    if not os.path.exists(PRESET_DIR):
        return []
    return [f[:-5] for f in os.listdir(PRESET_DIR) if f.endswith('.json')]

# Export a preset to a user-specified path
def export_preset(preset_name, export_path):
    preset_path = os.path.join(PRESET_DIR, f"{preset_name}.json")
    if not os.path.exists(preset_path):
        print(f"No preset named '{preset_name}' to export!")
        return
    with open(preset_path, 'r') as src, open(export_path, 'w') as dst:
        dst.write(src.read())
    print(f"Preset '{preset_name}' exported to {export_path}")

# Import a preset from a user-specified path
def import_preset(import_path, preset_name):
    os.makedirs(PRESET_DIR, exist_ok=True)
    preset_path = os.path.join(PRESET_DIR, f"{preset_name}.json")
    with open(import_path, 'r') as src, open(preset_path, 'w') as dst:
        dst.write(src.read())
    print(f"Preset '{preset_name}' imported from {import_path}")

class SavePresetOperator(bpy.types.Operator):
    bl_idname = "vsendless.save_preset"
    bl_label = "Save Preset"

    preset_name: bpy.props.StringProperty()

    def execute(self, context):
        save_preset(context, self.preset_name)
        return {'FINISHED'}

class LoadPresetOperator(bpy.types.Operator):
    bl_idname = "vsendless.load_preset"
    bl_label = "Load Preset"

    preset_name: bpy.props.StringProperty()

    def execute(self, context):
        load_preset(context, self.preset_name)
        return {'FINISHED'}

class ResetPresetOperator(bpy.types.Operator):
    bl_idname = "vsendless.reset_preset"
    bl_label = "Reset Preset"

    def execute(self, context):
        reset_preset(context)
        return {'FINISHED'}

class SavePresetNamedOperator(bpy.types.Operator):
    bl_idname = "vsendless.save_preset_named"
    bl_label = "Save Named Preset"

    preset_name: bpy.props.StringProperty(name="Preset Name")

    def execute(self, context):
        from ..utils.presets import save_preset
        if not self.preset_name:
            self.report({'ERROR'}, "Preset name required!")
            return {'CANCELLED'}
        save_preset(context, self.preset_name)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class LoadPresetNamedOperator(bpy.types.Operator):
    bl_idname = "vsendless.load_preset_named"
    bl_label = "Load Named Preset"

    preset_name: bpy.props.StringProperty(name="Preset Name")

    def execute(self, context):
        from ..utils.presets import load_preset
        if not self.preset_name:
            self.report({'ERROR'}, "Preset name required!")
            return {'CANCELLED'}
        load_preset(context, self.preset_name)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class ListPresetsOperator(bpy.types.Operator):
    bl_idname = "vsendless.list_presets"
    bl_label = "List Presets"

    def execute(self, context):
        from ..utils.presets import list_presets
        presets = list_presets()
        self.report({'INFO'}, f"Available presets: {', '.join(presets) if presets else 'None'}")
        return {'FINISHED'}

class ExportPresetOperator(bpy.types.Operator):
    bl_idname = "vsendless.export_preset"
    bl_label = "Export Preset"

    preset_name: bpy.props.StringProperty(name="Preset Name")
    export_path: bpy.props.StringProperty(name="Export Path", subtype='FILE_PATH')

    def execute(self, context):
        from ..utils.presets import export_preset
        if not self.preset_name or not self.export_path:
            self.report({'ERROR'}, "Preset name and export path required!")
            return {'CANCELLED'}
        export_preset(self.preset_name, self.export_path)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class ImportPresetOperator(bpy.types.Operator):
    bl_idname = "vsendless.import_preset"
    bl_label = "Import Preset"

    import_path: bpy.props.StringProperty(name="Import Path", subtype='FILE_PATH')
    preset_name: bpy.props.StringProperty(name="Preset Name")

    def execute(self, context):
        from ..utils.presets import import_preset
        if not self.import_path or not self.preset_name:
            self.report({'ERROR'}, "Import path and preset name required!")
            return {'CANCELLED'}
        import_preset(self.import_path, self.preset_name)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

def register_presets():
    bpy.utils.register_class(SavePresetOperator)
    bpy.utils.register_class(LoadPresetOperator)
    bpy.utils.register_class(ResetPresetOperator)
    bpy.utils.register_class(SavePresetNamedOperator)
    bpy.utils.register_class(LoadPresetNamedOperator)
    bpy.utils.register_class(ListPresetsOperator)
    bpy.utils.register_class(ExportPresetOperator)
    bpy.utils.register_class(ImportPresetOperator)

def unregister_presets():
    bpy.utils.unregister_class(SavePresetOperator)
    bpy.utils.unregister_class(LoadPresetOperator)
    bpy.utils.unregister_class(ResetPresetOperator)
    bpy.utils.unregister_class(SavePresetNamedOperator)
    bpy.utils.unregister_class(LoadPresetNamedOperator)
    bpy.utils.unregister_class(ListPresetsOperator)
    bpy.utils.unregister_class(ExportPresetOperator)
    bpy.utils.unregister_class(ImportPresetOperator)
