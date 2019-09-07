import bpy
from ObjectCreator import createCube, createSquarePlane
from enum import Enum
from abc import abstractmethod

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
    
    def create(self):
        halfLength = self.size/2
        myVertex = []
        myFaces =  []
        myVertex.extend([(-self.size/2, self.size/2, self.location[2])])
        myVertex.extend([(self.size/2, self.size/2, self.location[2])])
        myVertex.extend([(-self.size/2, -self.size/2, self.location[2])])
        myVertex.extend([(self.size/2, -self.size/2, self.location[2])])
        myFace = [(0, 1, 3, 2)]
        myFaces.extend(myFace)


        myMesh = bpy.data.meshes.new(self.name)

        myObject = bpy.data.objects.new(self.name, myMesh)

        bpy.context.collection.objects.link(myObject)

        # Generate mesh data
        myMesh.from_pydata(myVertex, [], myFaces)
        # Calculate the edges
        myMesh.update(calc_edges=True)

        # Set Location
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
    c = Cube('monCube', (1,2,3), (2,5,10))
    c.create()
    p = Plane('monPlan', (1,1,1), 2)
    p.create()
