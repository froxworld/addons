import menu_Francois
import os
import bpy


# ----------nettoyage de la concole ------------
def nettoyageConsole():
    os.system('clear')


# --------------------prog principal------------
nettoyageConsole()


class Positionnement: # Définition de notre classe Positionnement
    '''Classe définissant une personne caractérisée par :
    - sa valeur en X
    - sa valeur en Y
    - sa valeur en Z'''

    def commentaire(self):
        print('positionnnement de l objet en ({0},{1},{2})'.format(self.x, self.y, self.z))

    def __init__(self):  # Notre méthode constructeur
        """Pour l'instant, on ne va définir qu'un seul attribut"""
        self.x = 0
        self.y = 0
        self.z = 0
        self.coordonnee = (self.x, self.y, self.z)
        self.commentaire()

    def affecte(self, positionx, positiony, positionz):
        self.x = positionx
        self.y = positiony
        self.z = positionz




def nettoyagedeLaScene():
    # pour chaque objet de la scene efface un Vaisseau
    names = [item.name for item in bpy.data.objects]
    for name in names:
        bpy.data.objects[name].select_set(state=True)
    bpy.ops.object.delete()


def ajouteCube(nom, taille, position):
    bpy.ops.mesh.primitive_cube_add(location=position)
    bpy.context.active_object.name = nom
    bpy.data.objects[nom].scale = taille


def ajouteCylindre(nom, taille):
    bpy.ops.mesh.primitive_cylinder_add(location=position)
    bpy.context.active_object.name = nom
    bpy.data.objects[nom].scale = taille


nettoyagedeLaScene()

position = Positionnement()
position.affecte(10,12,3)
ajouteCube("cube1", (10, 2, 3), position.coordonnee)

#ajouteCylindre("ci", (1, 2, 3))
