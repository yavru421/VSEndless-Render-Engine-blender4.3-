bl_info = {
    "name": "VSEndless - Advanced FFmpeg Render Engine",
    "blender": (4, 3, 0),
    "category": "Render",
    "version": (3, 0, 1),
    "description": "Highly customizable render engine for Blender's VSE with advanced FFmpeg post-processing and preset management.",
    "author": "John Daniel Dondlinger",
}

import bpy
from .operators.render_operator import VSEndlessRenderEngine
from .ui.render_panel import VSEndlessRenderPanel
from .properties.render_properties import register_properties, unregister_properties
from .utils.presets import register_presets, unregister_presets

def register():
    bpy.utils.register_class(VSEndlessRenderEngine)
    bpy.utils.register_class(VSEndlessRenderPanel)
    register_properties()
    register_presets()

def unregister():
    bpy.utils.unregister_class(VSEndlessRenderEngine)
    bpy.utils.unregister_class(VSEndlessRenderPanel)
    unregister_properties()
    unregister_presets()

if __name__ == "__main__":
    register()
