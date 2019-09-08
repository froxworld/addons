import lancement_Francois
import platform
import os

bl_info = {"name": "Vaisseau", "blender": (2, 80, 0), "category": "Object", }
addons = []

import bpy

# Assign a collection.
class SceneSettingItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Test Property", default="Unknown")
    value: bpy.props.IntProperty(name="Test Property", default=22)


class ObjectFenetre(bpy.types.Operator):  # fenetre pour lancer les generation de vaisseaux avec parametres
    bl_idname = "add.fenetre"
    bl_label = "Generateur Vaisseau2"
    bl_options = {'REGISTER', 'UNDO'}

    Vaisseau_Eau: bpy.props.IntProperty(name="Vaisseau_Eau", default=20, min=1, max=100)
    Vaisseau_Terre: bpy.props.IntProperty(name="Vaisseau_Terre", default=30, min=1, max=100)
    Vaisseau_Feu: bpy.props.IntProperty(name="Vaisseau_Feu", default=50, min=1, max=100)
    Vaisseau_Air: bpy.props.IntProperty(name="Vaisseau_Air", default=20, min=1, max=100)
    Aleatoire: bpy.props.FloatProperty(name="Aleatoire", default=20.0, min=1, max=100)
    my_bool: bpy.props.BoolProperty(name="Toggle Option")

    def execute(self, context):
        if __name__ == '__main__':
            lancement_Francois.tout()
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(ObjectFenetre.bl_idname)

def register():
    bpy.utils.register_class(ObjectFenetre)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    gestionnnaire_fenetre = bpy.context.window_manager
    cle = gestionnnaire_fenetre.keyconfigs.addon

    if cle:
        cles_config = gestionnnaire_fenetre.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        nombre_cles_config = cles_config.keymap_items.new(ObjectFenetre.bl_idname, 'T', 'PRESS', ctrl=True, shift=True)
        nombre_cles_config.properties.Vaisseau_Eau = 4
        addons.append((cles_config, nombre_cles_config))

def unregister():
    # Note: when unregistering, it's usually good practice to do it in reverse order you registered.
    # Can avoid strange issues like keymap still referring to operators already unregistered...
    # handle the keymap
    for cles_config, nombre_cles_config in addons:
        cles_config.keymap_items.remove(nombre_cles_config)
    addons.clear()

    bpy.utils.unregister_class(ObjectFenetre)
    bpy.types.VIEW3D_MT_object.remove(menu_func)




if __name__ == "__main__":
    plateforme = platform.system()
    if (plateforme == 'Darwin') or (platform == 'linux'):
        os.system('clear')
    else:
        os.system('cls')
    register()

    bpy.utils.register_class(SceneSettingItem)
    bpy.types.Scene.my_settings = bpy.props.CollectionProperty(type=SceneSettingItem)
    my_item = bpy.context.scene.my_settings.add()
    my_item.name = "Spam"
    my_item.value = 1000

    my_item = bpy.context.scene.my_settings.add()
    my_item.name = "Eggs"
    my_item.value = 30

    for my_item in bpy.context.scene.my_settings:
        print(my_item.name, my_item.value)


    #fenetre = Fenetre().execute()
