import bpy
import bmesh
from enum import Enum
from abc import abstractmethod
import numpy as np
import mathutils
import math

class pieceType(Enum):
    Cube = 0
    Plane = 1
    extrudedPlane = 2
    Ball = 3

class Piece:
    
    def __init__(self, name, type, location, rotation):
        self.name = name
        self.type = type
        self.location = location
        self.rotation = rotation
    
    @abstractmethod
    def create(self):
        pass

class Cube(Piece):
    
    def __init__(self, name, location = (0,0,0), rotation = (0,0,0), scale = (1,1,1)):
        super().__init__(name, pieceType.Cube, location, rotation)
        self.scale = scale
    
    def create(self):
        bpy.ops.mesh.primitive_cube_add(location = self.location, rotation = self.rotation)
        bpy.context.active_object.name = self.name
        bpy.data.objects[self.name].scale = self.scale

class Plane(Piece):
    
    def __init__(self, name, type = pieceType.Plane, location = (0,0,0), rotation = (0,0,0), radius = 1, nbPoint = 4):
        super().__init__(name, type, location, rotation)
        self.radius = radius
        self.nbPoint = nbPoint

    def defineAllVertices(self):
        
        myVertices = []
        
        for i in range(self.nbPoint):
            myVertices.append((self.radius*np.cos(2*i*np.pi/self.nbPoint),self.radius*np.sin(2*i*np.pi/self.nbPoint),0))
        
        return myVertices
    
    def create(self):
        
        # link the edges to form the face
        # 0 linked to 1 -> 0,1
        # then 1 linked to 3, -> 1,3
        # etc.
        #myFace = [(0, 1, 3, 2)]
        #test
        verticesOrder = [tuple([ k for k in range(self.nbPoint)])]
        
        # Generate the mesh
        myMesh = bpy.data.meshes.new(self.name)
        myMesh.from_pydata(self.defineAllVertices(), [], verticesOrder)
        myMesh.update(calc_edges=True)
        
        # Link mesh to a scene object
        myObject = bpy.data.objects.new(self.name, myMesh)
        bpy.context.collection.objects.link(myObject)
        
        #finally, define the location of the object in the scene
        myObject.location = self.location
        
class extrudedPlane(Plane):
    
    def __init__(self, name, location = (0,0,0), rotation = (0,0,0), radius = 1, nbPoint = 8, height = 1):
        super().__init__(name, pieceType.extrudedPlane, location, rotation, radius, nbPoint)
        self.height = height
    
    def create(self):
        super().create()
        Scene().select_one(self.name)
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(bpy.data.objects[self.name].data)
        r = bmesh.ops.extrude_face_region(bm, geom=bm.faces)
        verts = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, vec=mathutils.Vector((0,0,self.height)), verts=verts)
        bmesh.update_edit_mesh(bpy.context.object.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.transform.rotate(value=self.rotation[0], orient_axis= "X")
        bpy.ops.transform.rotate(value=self.rotation[1], orient_axis= "Y")
        bpy.ops.transform.rotate(value=self.rotation[2], orient_axis= "Z")

class Ball(Piece):
    
    def __init__(self, name, location = (0,0,0), rotation = (0,0,0), radius = 1, subdivisions = 5, scale = (1,1,1)):
        super().__init__(name, pieceType.Ball, location, rotation)
        self.radius = radius
        self.subdivisions = subdivisions
        self.scale = scale
    
    def create(self):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=self.subdivisions, radius=self.radius, location = self.location, rotation = self.rotation)
        bpy.context.active_object.name = self.name
        bpy.data.objects[self.name].scale = self.scale
        
class Cloud(Piece):
    
    def __init__(self, name, location = (0,0,0), rotation = (0,0,0), scale = (2,5,1), max_radius = 0.1, step = 20):
        super().__init__(name, pieceType.Cube, location, rotation)
        self.scale = scale
        self.id = Scene().gen_id()
        self.step = step
    
    def create(self):
        Ball(self.name+str(self.id), subdivisions = 5, scale = self.scale).create()
        #sphere_max_size = np.array(self.scale)/2
        sphere_max_size = np.array([1,1,1])
        min_val = 0.4
        max_val = 0.6
        for i in np.linspace(np.pi, 2*np.pi, self.step):
            for j in np.linspace(0, 2*np.pi, self.step):
                sphere_scale = [k*min(max(min_val,np.random.uniform()),max_val) for k in sphere_max_size]
                Ball(self.name+str(self.id)+Scene().gen_id(5), location = (self.scale[0]*np.cos(i)*np.sin(j), self.scale[1]*np.sin(i)*np.sin(j),self.scale[2]*np.cos(j)), scale = sphere_scale).create()
        Scene().select_object_begin_name(self.name+str(self.id))
        bpy.ops.object.join()
        bpy.context.active_object.name = self.name

class Scene(object):
    
    #Singleton pattern
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Scene, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    # select one object in the scene with its name
    def select_one(self, object_name):
        self.deselect_all()
        all_names = [item.name for item in bpy.data.objects]
        
        for name in all_names:
            if name == object_name:
                bpy.data.objects[name].select_set(state=True)
                
    # select many objects in the scene with the beginning of the name
    def select_object_begin_name(self, object_name):
        self.deselect_all()
        all_names = [item.name for item in bpy.data.objects]
        
        for name in all_names:
            if name[0:min(len(name), len(object_name))] == object_name[0:min(len(name), len(object_name))]:
                bpy.data.objects[name].select_set(state=True)
        
    # select all object in the scene
    def select_all(self):
    
        all_names = [item.name for item in bpy.data.objects]
        
        for object_name in all_names:
            bpy.data.objects[object_name].select_set(state=True)
    
    # deselect all object in the scene
    def deselect_all(self):
    
        all_names = [item.name for item in bpy.data.objects]
        
        for object_name in all_names:
            bpy.data.objects[object_name].select_set(state=False)
    
    #generate an id to distinct the objects in the scene
    def gen_id(self, size = 10):
        
        chars = "azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN0123456789"
        final_id = ""
        
        for i in range(size):
            final_id += str(chars[np.random.randint(0, len(chars)-1)])
        
        return final_id
    
    # erase all the objects in the scene (meshes, curves, surfaces) 
    def reset_scene(self):
        
        to_erase = ["MESH", "CURVE", "SURFACE"]
        
        candidate_list = [item.name for item in bpy.data.objects if item.type in to_erase]
        
        for object_name in candidate_list:
            bpy.data.objects[object_name].select_set(state=True)
        bpy.ops.object.delete()
        
        
if __name__ == "__main__":
    Scene().reset_scene()
    c = Cube(name = 'monCube', location = (-10,-10,-5), scale = (1,1,1), rotation = (0,np.pi/4,0))
    c.create()
    n = 10
    someRandomness = [1 if k == 0 else -1 for k in np.random.randint(0, 2, n)]
    someRandomness2 = [1 if k == 0 else -1 for k in np.random.randint(0, 2, n)]
    p = extrudedPlane(name = 'monPlan', location = (-20,20,20), rotation = (3*np.pi/2,0,0), radius = 2, nbPoint = 5, height = 20)
    p.create()
    Cloud("nuage", scale = (2, 3, 1), step = 20).create()
