import bpy
from enum import Enum
from abc import abstractmethod
import numpy as np


class pieceType(Enum):
    Cube = 0
    Plane = 1

class Piece:
    
    def __init__(self, name, location, type):
        self.name = name
        self.location = location
        self.type = type
    
    @abstractmethod
    def create(self):
        pass

class Cube(Piece):
    
    def __init__(self, name, location, scale):
        super().__init__(name, location, pieceType.Cube)
        self.scale = scale
    
    def create(self):
        bpy.ops.mesh.primitive_cube_add(location = self.location)
        bpy.context.active_object.name = self.name
        bpy.data.objects[self.name].scale = self.scale

class Plane(Piece):
    
    def __init__(self, name, location, size, nbPoint):
        super().__init__(name, location, pieceType.Plane)
        self.size = size
        self.nbPoint = nbPoint

    def defineAllEdges(self):
        
        myVertices = []
        
        for i in range(self.nbPoint):
            myVertices.append((self.size*np.cos(2*i*np.pi/self.nbPoint),
            self.size*np.sin(2*i*np.pi/self.nbPoint),0))
        
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
        myMesh.from_pydata(self.defineAllEdges(), [], verticesOrder)
        myMesh.update(calc_edges=True)
        
        # Link mesh to a scene object
        myObject = bpy.data.objects.new(self.name, myMesh)
        bpy.context.collection.objects.link(myObject)
        
        #finally, define the location of the object in the scene
        myObject.location = self.location

class exPlane(Piece):
    
    def __init__(self, name, location, size, nbPoint, val):
        super().__init__(name, location, pieceType.Plane)
        self.size = size
        self.nbPoint = nbPoint
        self.val = val

    def defineAllEdges(self):
        
        myVertices = []
        
        for i in range(self.nbPoint):
            myVertices.append((self.size*np.cos(2*i*np.pi/self.nbPoint),
            self.size*np.sin(2*i*np.pi/self.nbPoint),0))
        
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
        myMesh.from_pydata(self.defineAllEdges(), [], verticesOrder)
        myMesh.update(calc_edges=True)
        
        # Link mesh to a scene object
        myObject = bpy.data.objects.new(self.name, myMesh)
        bpy.context.collection.objects.link(myObject)
        
        #finally, define the location of the object in the scene
        myObject.location = self.location
        deselect_all()
        bpy.data.objects[self.name].select_set(state=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0,0,self.val),
        "orient_type" : 'NORMAL'})
        bpy.ops.object.editmode_toggle()

def deselect_all():
    
    all_names = [item.name for item in bpy.data.objects]
    
    for object_name in all_names:
        bpy.data.objects[object_name].select_set(state=False)

def reset_scene():
    
    to_erase = ["MESH", "CURVE", "SURFACE"]
    
    candidate_list = [item.name for item in bpy.data.objects 
                      if item.type in to_erase]
    
    for object_name in candidate_list:
        bpy.data.objects[object_name].select_set(state=True)
    bpy.ops.object.delete()



if __name__ == "__main__":
    reset_scene()
    c = Cube('monCube', (-5,-10,-5), (1,1,1))
    c.create()

    n = 10
    someRandomness = [1 if k == 0 else -1 for k in np.random.randint(0, 2, n)]
    someRandomness2 = [1 if k == 0 else -1 for k in np.random.randint(0, 2, n)]
    #for i in range(n):
    #    Cube('monCube'+str(i), (i*2, 0, 0), (1,1,1)).create()
    #    Cube('monCubeAleaY'+str(i), (i*2, 2*someRandomness[i], 0), (1,1,1)).create()
    #    Cube('monCubeAleaZ'+str(i), (i*2, 0, 2*someRandomness2[i]), (1,1,1)).create()
    p = exPlane('monPlan', (0,0,0), 3, 10, 8)
    p.create()
