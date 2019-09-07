import menu_Francois
import os
import bpy
import platform

from enum import Enum
from random import randint, uniform


# -----------------------nettoyage de la console-----------------
def nettoyageConsole():
    plateforme = platform.system()
    if (plateforme == 'Darwin') or (platform == 'linux'):
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
        a = 0
        # print('positionnnement de l objet en ({0},{1},{2})'.format(self.x, self.y, self.z))

    def __init__(self, position_x, position_y, position_z):  # Notre méthode constructeur
        """Pour l'instant, on ne va définir qu'un seul attribut"""
        self.x = position_x
        self.y = position_y
        self.z = position_z

        self.commentaire()

    def coordonnee(self):
        return (self.x, self.y, self.z)

    def coordonneeAleatoire(self, x, y):
        return (randint(x, y))

    def rendX(self):
        return self.x

    def rendY(self):
        return self.y

    def rendZ(self):
        return self.z


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

    def ajoutePiece(self, nom, piece, position):
        self.liste_des_pieces.append((nom, piece, position))
        print('{0} {1} est ajoutee à la position {2}'.format(nom, piece.genre, position))

    def suprimePiece(self, nom, piece, position):
        self.liste_des_pieces.remove((nom, piece, position))
        print('{0} {1} est enlevee à la position {2}'.format(nom, piece.genre, position))


class Piece:
    nom = ''
    genre = ''
    position = ''

    def creation(self):
        print('La piece de nom {0} et de genre {1} vient d etre cree'.format(self.nom, self.genre))

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


def creationBiseau():
    context = bpy.context
    obj = context.active_object
    # bpy.ops.object.editmode_toggle()
    bevel_modifier = obj.modifiers.new('Bevel', 'BEVEL')
    bevel_modifier.width = uniform(5, 20)
    bevel_modifier.offset_type = 'PERCENT'
    bevel_modifier.segments = 2
    bevel_modifier.profile = 0.25
    bevel_modifier.limit_method = 'NONE'


def ajouteForme(nom, taille, position, piece, type):
    if type == GenrePiece.CUBE:
        bpy.ops.mesh.primitive_cube_add(location=position)
        creationBiseau()
        vaisseau1.ajoutePiece(nom, piece, position)

    if type == GenrePiece.CYLINDRE:
        bpy.ops.mesh.primitive_cylinder_add(location=position)
        creationBiseau()
        vaisseau1.ajoutePiece(nom, piece, position)

    if type == GenrePiece.BOULE:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=tailleBoule, enter_editmode=False, location=position)
        vaisseau1.ajoutePiece(nom, piece, position)

    bpy.context.active_object.name = nom
    if type != GenrePiece.BOULE:
        bpy.data.objects[nom].scale = taille


def ajouteMilieu(position1, position2):
    a = position1.rendX()
    b = position2.rendX()
    intermediare = int((a + b) / 2)
    return (intermediare)

def aleatoire():
    return randint(1,5)

# -----------------------nettoyage de la console-----------------

# -------------------------debut du main-------------------------
nettoyageConsole()
nettoyagedeLaScene()

# creation d un premier vaisseau
vaisseau1 = Vaisseau('test1', GenreVaisseau.AIR)
vaisseau1.affiche()

# creation de pieces test

piece1 = Piece('cube_1', GenrePiece.CUBE)
piece2 = Piece('cylinde_2', GenrePiece.CYLINDRE)
piece3 = Piece('boule_3', GenrePiece.BOULE)

liste_piece = range(50)

for piece in liste_piece:
    # creation de position de test
    taille1 = (aleatoire(), aleatoire(), aleatoire())
    taille2 = (5*aleatoire(), 5*aleatoire(), 5*aleatoire())
    position1 = Positionnement(3*piece, 0, 0)
    if (aleatoire()>1):
        ajouteForme(str(piece), taille1, position1.coordonnee(), piece1, GenrePiece.CUBE)
    else:
        ajouteForme(str(piece), taille2, (position1.coordonnee()), piece2, GenrePiece.CYLINDRE)


    # taille2 = (1, 1, 1)
    # tailleBoule = Positionnement.coordonneeAleatoire(Positionnement, 1, 10)
    #
    # position2 = Positionnement(5 * piece * Positionnement.coordonneeAleatoire(Positionnement, 1, 3), 1, 1)
    #
    #
    # position3 = ajouteMilieu(position1, position2)
    # ajouteForme(str(piece), tailleBoule, (position3, position1.rendY(), position1.rendZ()), piece3, GenrePiece.BOULE)

# affichage des infos d'un objet
print(vaisseau1.__dict__)
