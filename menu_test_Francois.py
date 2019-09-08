"""
This program explores property initialization for property groups
"""

bl_info = {
    "version": "0.1",
    "name": "Property Group Initialization",
    'author': 'BlenderHawk',
    "location": "Properties &gt; Scene",
    "category": "Blender Experiments"
}

import bpy
from bpy.props import *


class Var_Group(bpy.types.PropertyGroup):
    """ Property Group representing a variable with a name, value, and other potential attributes """
    var_name = StringProperty(name="n", default="Var")
    var_value = FloatProperty(name="v", default=1.0)


class AppPropertyGroup(bpy.types.PropertyGroup):
    """ Properties for this particular application """
    a = PointerProperty(name="a_name", type=Var_Group)
    b = PointerProperty(name="b_name", type=Var_Group)

    def init_variables(self):
        self.a.var_name = "Alpha"
        self.a.var_value = 2.0

        self.b.var_name = "Beta"
        self.b.var_value = 3.0


class APP_OT_init_props(bpy.types.Operator):
    bl_idname = "app.init_props"
    bl_label = "Initialize Properties"
    bl_description = "Initialize Properties to default values"
    bl_options = {'REGISTER'}

    def execute(self, context):
        app = context.scene.app
        app.init_variables()
        return {'FINISHED'}


class APP_OT_print_props(bpy.types.Operator):
    bl_idname = "app.print_props"
    bl_label = "Print Properties"
    bl_description = "Print the Properties"
    bl_options = {'REGISTER'}

    def execute(self, context):
        app = context.scene.app
        print("----- Application Properties -----")
        print("  " + str(app.a.var_name) + " = " + str(app.a.var_value))
        print("  " + str(app.b.var_name) + " = " + str(app.b.var_value))
        return {'FINISHED'}


class APP_PT_Explore_Props(bpy.types.Panel):
    bl_label = "Explore Application Properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    def draw(self, context):
        app = context.scene.app
        row = self.layout.row()
        col = row.column()
        col.operator("app.init_props", text="Initialize Properties")
        col = row.column()
        col.operator("app.print_props", text="Print Properties")


def register():
    print("Registering ", __name__)
    bpy.utils.register_module(__name__)
    bpy.types.Scene.app = bpy.props.PointerProperty(type=AppPropertyGroup)


def unregister():
    print("Unregistering ", __name__)
    del bpy.types.Scene.app
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()