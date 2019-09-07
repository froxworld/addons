bl_info = {
    "name": "Cursor Array",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
from ObjectCreator import createCube, createSquarePlane

def reset_scene():
    
    to_erase = ["MESH", "CURVE", "SURFACE"]

    candidate_list = [item.name for item in bpy.data.objects 
                      if item.type in to_erase]
    
    for object_name in candidate_list:
        bpy.data.objects[object_name].select_set(state=True)
    bpy.ops.object.delete()
    
if __name__ == "__main__":
    reset_scene()
    createCube('monCube', (1,2,3), (2,5,10))
    createSquarePlane('monPlan', (1,1,1), 2)
    
