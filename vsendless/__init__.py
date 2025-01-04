
bl_info = {
    "name": "VSEndless - Advanced Render Engine",
    "blender": (2, 80, 0),
    "version": (1, 0, 0),
    "author": "John Daniel Dondlinger",
    "description": "Customizable render engine for Blender's Video Sequence Editor.",
    "category": "Render",
    "location": "Render Engine Dropdown",
    "support": "COMMUNITY",
}

import bpy
from . import render_operator
from . import render_panel
from . import render_properties

def register():
    render_properties.register()
    render_operator.register()
    render_panel.register()

def unregister():
    render_properties.unregister()
    render_operator.unregister()
    render_panel.unregister()

if __name__ == "__main__":
    register()
