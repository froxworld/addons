import bpy

def createCube(name, center, scale):
    bpy.ops.mesh.primitive_cube_add(location = center)
    bpy.context.active_object.name = name
    bpy.data.objects[name].scale = scale

def createSquarePlane(name, center, length):
    halfLength = length/2
    myVertex = []
    myFaces =  []
    myVertex.extend([(-length/2, length/2, center[2])])
    myVertex.extend([(length/2, length/2, center[2])])
    myVertex.extend([(-length/2, -length/2, center[2])])
    myVertex.extend([(length/2, -length/2, center[2])])
    myFace = [(0, 1, 3, 2)]
    myFaces.extend(myFace)


    myMesh = bpy.data.meshes.new(name)

    myObject = bpy.data.objects.new(name, myMesh)

    bpy.context.collection.objects.link(myObject)

    # Generate mesh data
    myMesh.from_pydata(myVertex, [], myFaces)
    # Calculate the edges
    myMesh.update(calc_edges=True)

    # Set Location
    myObject.location.x = center[0]
    myObject.location.y = center[1]
    myObject.location.z = center[2]