import bpy
from ObjectCreator import createCube, createSquarePlane
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
    
    def __init__(self, name, location, size):
        super().__init__(name, location, pieceType.Plane)
        self.size = size

    def defineAllEdges(self):
        
        myVertex = []
        
        myVertex.append((-self.size/2, self.size/2, 0))
        myVertex.append((self.size/2, self.size/2, 0))
        myVertex.append((-self.size/2, -self.size/2, 0))
        myVertex.append((self.size/2, -self.size/2, 0))
        #myVertex.append((self.size/3, -self.size/2, 0))
        
        return myVertex
    
    def create(self):
        
        # link the edges to form the face
        # 0 linked to 1 -> 0,1
        # then 1 linked to 3, -> 1,3
        # etc.
        myFace = [(0, 1, 3, 2)]
        #test
        #myFace = [(0, 1, 3, 2, 4)]
        
        # Generate the mesh
        myMesh = bpy.data.meshes.new(self.name)
        myMesh.from_pydata(self.defineAllEdges(), [], myFace)
        myMesh.update(calc_edges=True)
        
        # Link mesh to a scene object
        myObject = bpy.data.objects.new(self.name, myMesh)
        bpy.context.collection.objects.link(myObject)
        
        #finally, define the location of the object in the scene
        myObject.location = self.location


def reset_scene():
    
    to_erase = ["MESH", "CURVE", "SURFACE"]

    candidate_list = [item.name for item in bpy.data.objects 
                      if item.type in to_erase]
    
    for object_name in candidate_list:
        bpy.data.objects[object_name].select_set(state=True)
    bpy.ops.object.delete()



if __name__ == "__main__":
    reset_scene()
    c = Cube('monCube', (-1,-2,-10), (1,1,1))
    c.create()
    p = Plane('monPlan', (1,1,-10), 2)
    p.create()
    n = 10
    someRandomness = [1 if k == 0 else -1 for k in np.random.randint(0, 2, n)]
    someRandomness2 = [1 if k == 0 else -1 for k in np.random.randint(0, 2, n)]
    for i in range(n):
        Cube('monCube'+str(i), (i*2, 0, 0), (1,1,1)).create()
        Cube('monCubeAleaY'+str(i), (i*2, 2*someRandomness[i], 0), (1,1,1)).create()
        Cube('monCubeAleaZ'+str(i), (i*2, 0, 2*someRandomness2[i]), (1,1,1)).create()
