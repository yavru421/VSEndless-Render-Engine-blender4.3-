# workspace_operator.py: APT pipeline module for workspace operator
# Algebraic Notation: Let $x_1$ = Blender context, $y_1$ = workspace tab
# $y_1 = create_workspace(x_1)$
import bpy

class VSENDLESS4_OT_CreateWorkspace(bpy.types.Operator):
    bl_idname = "vsendless4.create_workspace"
    bl_label = "Create VSEndless Workspace Tab"
    bl_description = "Add a new workspace tab for VSEndless Render Engine"

    def execute(self, context):
        if not bpy.data.screens.get("VSEndless"):
            screen = bpy.data.screens.new("VSEndless")
            self.report({'INFO'}, "VSEndless workspace tab created. Configure layout as needed.")
        else:
            self.report({'WARNING'}, "VSEndless workspace tab already exists.")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(VSENDLESS4_OT_CreateWorkspace)

def unregister():
    bpy.utils.unregister_class(VSENDLESS4_OT_CreateWorkspace)
