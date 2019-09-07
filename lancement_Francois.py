import menu_Francois
import os
import bpy
from enum import Enum


# ----------nettoyage de la concole ------------
def nettoyageConsole():
    os.system('clear')


# --------------------prog principal------------
nettoyageConsole()


class GenreVaisseau(Enum):
    EAU = 1
    TERRE = 2
    FEU = 3
    AIR = 4
    AUTRE = 5
    # print(GenreVaisseau(1))
    # print(GenreVaisseau(1).value)
    # print(GenreVaisseau(1).name)


class GenrePiece(Enum):
    CARRE = 1
    CUBE = 2
    TRIANGLE = 3
    PYRAMIDE = 4
    ROND = 5
    BOULE = 6


class Positionnement:  # Définition de notre classe Positionnement
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


class Vaisseau:  # Défintion de la classe vaisseau
    # nom, genre

    nom = ''
    nombre = 0  # nombre de piece du vaiseau (class)
    liste_des_pieces = []  # liste de toutes les pieces (class)

    def __init__(self, nom, genre):
        self.nom = nom
        self.genre = genre
        self.creation()
        self.nombre += 1
        self.creation()

    def creation(self):
        print('votre vaisseau {0} de genre {1} vient d etre cree'.format(self.nom, self.genre))

    def affiche(cls):
        print('Vaisseau : vous avez deja ajoute {0}'.format(cls.nombre))
        print('Vaisseau : le vaisseau contient deja {0}'.format(len(cls.liste_des_pieces)))

    affiche = classmethod(affiche)

    def ajoutePiece(cls, piece):
        print('la piece {0} vient d etre a jouteee à la liste {1} des pieces du vaisseau '.format(piece,
                                                                                                  cls.liste_des_pieces))
        cls.liste_des_pieces.append(piece)

    ajoutePiece = classmethod(ajoutePiece)

    def suprimePiece(cls, piece):
        cls.liste_des_pieces.remove(piece)
        print('la piece {0} vient d etre suprimee de la liste et il reste {1} des pieces du vaisseau '.format(piece,
                                                                                                              cls.liste_des_pieces))


class Piece:
    nom = ''
    genre = ''

    def creation(self):
        print('votre piece de nom {0} et de genre {1} vient d etre cree'.format(self.nom, self.genre))

    def __init__(self, nom, genre):
        self.nom = nom
        self.genre = genre
        self.creation()


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


# -------------------------debut du main-------------------------
nettoyagedeLaScene()

position = Positionnement()
position.affecte(10, 12, 3)
ajouteCube("cube1", (10, 2, 3), position.coordonnee)
# ajouteCylindre("ci", (1, 2, 3))

# creation d un premier vaisseau
vaisseau1 = Vaisseau
vaisseau1.nom = 'test1'
vaisseau1.genre = GenreVaisseau.AIR
vaisseau1.affiche()
piece1 = Piece('piece1', GenreVaisseau.AIR)
