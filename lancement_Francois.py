import menu_Francois
import os
import bpy
import platform
from enum import Enum


# -----------------------nettoyage de la console-----------------
def nettoyageConsole():
    plateforme = platform.system()
    if (plateforme == 'darwin' || platform== 'linux'):
        os.system('clear')
    else:
        os.system('cls')


class GenreVaisseau(Enum):  # print(GenreVaisseau(1),GenreVaisseau(1).value, GenreVaisseau(1).name))
    EAU = 1
    TERRE = 2
    FEU = 3
    AIR = 4
    AUTRE = 5



class GenrePiece(Enum):
    CARRE = 1
    CUBE = 2
    TRIANGLE = 3
    PYRAMIDE = 4
    ROND = 5
    BOULE = 6
    CYLINDRE = 7


# -----------------------positionnnement (x,y,z)-----------------

class Positionnement:  # Définition de notre classe Positionnement
    '''Classe définissant une personne caractérisée par :
    - sa valeur en X
    - sa valeur en Y
    - sa valeur en Z'''

    x = 0
    y = 0
    z = 0

    def commentaire(self):
        print('positionnnement de l objet en ({0},{1},{2})'.format(self.x, self.y, self.z))

    def __init__(self, position_x, position_y, position_z):  # Notre méthode constructeur
        """Pour l'instant, on ne va définir qu'un seul attribut"""
        self.x = position_x
        self.y = position_y
        self.z = position_z

        self.commentaire()

    def coordonnee(self):
        return (self.x, self.y, self.z)


# -----------------------vaisseau(nom, genre)--------------------

class Vaisseau:  # Défintion de la classe vaisseau
    # nom, genre

    nom = ''
    genre = ''
    nombre = 0  # nombre de vaiseau (class)
    liste_des_pieces = []  # liste de toutes les pieces (class)

    def __init__(self, nom, genre):
        self.nom = nom
        self.genre = genre
        self.creation()
        Vaisseau.nombre += 1

    def creation(self):
        print('votre vaisseau {0} de genre {1} vient d etre cree'.format(self.nom, self.genre))

    def affiche(cls):
        print('Vaisseau : vous avez deja ajoute {0} vaisseau'.format(cls.nombre))
        print('Vaisseau : le vaisseau contient deja {0}'.format(len(cls.liste_des_pieces)))

    affiche = classmethod(affiche)

    def ajoutePiece(self, piece):
        self.liste_des_pieces.append(piece)
        print('la piece {0} vient d etre ajoutee à la liste {1} des pieces du vaisseau '.format(piece,
                                                                                                self.liste_des_pieces))

    def suprimePiece(cls, piece):
        cls.liste_des_pieces.remove(piece)
        print('la piece {0} vient est suprimee de la liste, il reste {1} pieces du vaisseau '.format(piece,
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


def ajoutePiece(nom, taille, position, piece):
    # ajout de la piece à la position
    if (piece.genre == GenrePiece.CUBE):
        ajouteCube(nom, taille, position)
    if (piece.genre == GenrePiece.CYLINDRE):
        ajouteCylindre(nom, taille, position)


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


def ajouteCylindre(nom, taille, position):
    bpy.ops.mesh.primitive_cylinder_add(location=position)
    bpy.context.active_object.name = nom
    bpy.data.objects[nom].scale = taille


# -----------------------nettoyage de la console-----------------

# -------------------------debut du main-------------------------
nettoyageConsole()
nettoyagedeLaScene()

# creation d un premier vaisseau
vaisseau1 = Vaisseau('test1', GenreVaisseau.AIR)
vaisseau1.affiche()

# creation de position de test
position1 = Positionnement(10, 12, 6)
taille1 = (10, 12, 3)
position2 = Positionnement(8, 15, 3)
taille2 = (5, 5, 5)

# creation de pieces test

piece1 = Piece('cube_1', GenrePiece.CUBE)
piece2 = Piece('cylinde_2', GenrePiece.CYLINDRE)


vaisseau1.ajoutePiece(piece1)

liste_piece = [1, 2, 3]
for piece in liste_piece:
    print(position1.coordonnee())
    ajoutePiece(str(piece), taille1, position1.coordonnee(), piece1)
    ajoutePiece(str(piece), taille2, (position2.x+2*piece, position2.y-2*piece, position2.z-2*piece), piece2)

# affichage des infos d'un objet
print(vaisseau1.__dict__)
