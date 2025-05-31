import pygame
import sys

# --- Initialisation de Pygame ---
pygame.init()

# --- Constantes pour la Fenêtre et l'Affichage ---
largeur_fenetre = 800  # Largeur de la fenêtre en pixels
hauteur_fenetre = 600 # Hauteur de la fenêtre en pixels
taille_fenetre = (largeur_fenetre, hauteur_fenetre)
FPS = 30               # Images par seconde

# Dimensions de l'arène de jeu 3D (en nombre de blocs)
# Ces dimensions sont pour la grille logique, pas directement pour la fenêtre Pygame.
LARGEUR_ARENE_3D = 6   # Nombre de blocs en largeur (sur l'axe X du monde)
PROFONDEUR_ARENE_3D = 6 # Nombre de blocs en profondeur (sur l'axe Y du monde)
HAUTEUR_ARENE_3D = 10  # Nombre de blocs en hauteur (sur l'axe Z du monde)

# Couleurs
noir = (0, 0, 0)
blanc = (255, 255, 255)
rouge = (255, 0, 0)
vert = (0, 255, 0)
bleu = (0, 0, 255)

# (À ajouter dans votre fichier tetris_3d.py, par exemple après les couleurs)
piece_I_3D_forme0 = [
    (0, 0, 0),  # Cube à l'origine de la pièce
    (1, 0, 0),  # Cube à côté sur l'axe X
    (2, 0, 0),
    (3, 0, 0)
]
piece_O_3D_forme0 = [
    (0, 0, 0), (1, 0, 0),
    (0, 1, 0), (1, 1, 0)
]
piece_L_3D_forme0 = [
    (0, 0, 0),  # Base du L
    (0, 0, 1),  # Monte
    (0, 0, 2),  # Monte encore
    (1, 0, 0)   # Extension du L à la base
]


# --- Paramètres pour la Projection Isométrique ---
# Ces valeurs déterminent l'apparence de la projection.
# Elles représentent de combien de pixels on se déplace sur l'écran
# pour une unité de déplacement dans le monde 3D.
DEMI_LARGEUR_ISO = 24  # Moitié de la "largeur" d'une tuile/cellule isométrique à l'écran
DEMI_HAUTEUR_ISO = 12  # Moitié de la "hauteur" d'une tuile/cellule isométrique à l'écran
HAUTEUR_Z_ISO = 18     # Hauteur visuelle à l'écran pour chaque unité de Z dans le monde 3D

# Point d'origine sur l'écran pour le dessin isométrique (où le point 3D (0,0,0) sera dessiné)
# Généralement au centre horizontalement, et un peu en haut verticalement.
origine_iso_x_ecran = largeur_fenetre // 2
origine_iso_y_ecran = hauteur_fenetre // 3

# --- Fonctions pour la 3D Isométrique ---

def projeter_point_iso(monde_x, monde_y, monde_z):
    """
    Projete un point 3D (monde_x, monde_y, monde_z) en coordonnées 2D pour l'écran (ecran_x, ecran_y).
    Utilise les constantes globales pour l'origine et les facteurs de projection.
    """
    ecran_x = origine_iso_x_ecran + (monde_x - monde_y) * DEMI_LARGEUR_ISO
    ecran_y = origine_iso_y_ecran + (monde_x + monde_y) * DEMI_HAUTEUR_ISO - monde_z * HAUTEUR_Z_ISO
    return int(ecran_x), int(ecran_y)

def dessiner_cube_iso(surface, gx, gy, gz, couleur_base):
    """
    Dessine un cube en vue isométrique à la position de grille 3D (gx, gy, gz).
    Le cube a une taille de 1x1x1 dans le monde 3D.
    (gx,gy,gz) est le coin "arrière-bas-gauche" du cube.
    """
    
    # Les 8 sommets du cube unitaire.
    # p[0] = (gx,gy,gz), p[1]=(gx+1,gy,gz) ... p[7]=(gx+1,gy+1,gz+1)
    # Ordre: X change le plus vite, puis Y, puis Z.
    # (0,0,0) (1,0,0) (0,1,0) (1,1,0) <-- niveau z=gz
    # (0,0,1) (1,0,1) (0,1,1) (1,1,1) <-- niveau z=gz+1 (relatif à gz)
    
    sommets_3d = [
        (gx    , gy    , gz    ),  # 0: arrière-bas-gauche
        (gx + 1, gy    , gz    ),  # 1: arrière-bas-droite
        (gx    , gy + 1, gz    ),  # 2: avant-bas-gauche
        (gx + 1, gy + 1, gz    ),  # 3: avant-bas-droite
        (gx    , gy    , gz + 1),  # 4: arrière-haut-gauche
        (gx + 1, gy    , gz + 1),  # 5: arrière-haut-droite
        (gx    , gy + 1, gz + 1),  # 6: avant-haut-gauche
        (gx + 1, gy + 1, gz + 1)   # 7: avant-haut-droite
    ]

    # Projeter les 8 sommets en 2D
    s = [projeter_point_iso(p[0], p[1], p[2]) for p in sommets_3d]

    # Définir des teintes pour les 3 faces visibles pour un effet 3D
    # (Plus la face est orientée vers le haut ou une "lumière" imaginaire, plus elle est claire)
    r, g, b = couleur_base
    # Couleur pour la face du dessus (la plus claire)
    couleur_top = pygame.Color(min(255, int(r * 1.0)), min(255, int(g * 1.0)), min(255, int(b * 1.0)))
    # Couleur pour une face latérale (un peu plus sombre)
    couleur_cote1 = pygame.Color(min(255, int(r * 0.8)), min(255, int(g * 0.8)), min(255, int(b * 0.8)))
    # Couleur pour l'autre face latérale (encore un peu plus sombre)
    couleur_cote2 = pygame.Color(min(255, int(r * 0.6)), min(255, int(g * 0.6)), min(255, int(b * 0.6)))

    # Faces visibles (listes de sommets projetés, dans l'ordre pour dessiner le polygone)
    # Ces faces partagent le sommet s[7] (avant-haut-droite), qui est souvent le plus proéminent.
    
    # Face du dessus: s[4], s[5], s[7], s[6]
    face_top_points = [s[4], s[5], s[7], s[6]]
    
    # Face latérale "droite" (par rapport à une vue standard, celle où X est maximum)
    # Vertices: (gx+1,gy,gz), (gx+1,gy+1,gz), (gx+1,gy+1,gz+1), (gx+1,gy,gz+1)
    # Indices: s[1], s[3], s[7], s[5]
    face_droite_points = [s[1], s[3], s[7], s[5]]
    
    # Face latérale "gauche" (par rapport à une vue standard, celle où Y est maximum)
    # Vertices: (gx,gy+1,gz), (gx+1,gy+1,gz), (gx+1,gy+1,gz+1), (gx,gy+1,gz+1)
    # Indices: s[2], s[3], s[7], s[6]
    face_gauche_points = [s[2], s[3], s[7], s[6]]

    # Ordre de dessin des faces : pour éviter des problèmes de recouvrement simples,
    # on peut essayer de dessiner celles qui semblent plus "éloignées" en premier,
    # ou simplement choisir un ordre. Avec des couleurs opaques, la dernière dessinée est au-dessus.
    # Pour un rendu correct, on doit faire attention à la "règle du peintre" ou à un Z-buffer.
    # Ici, pour des cubes séparés ou une pièce unique, l'ordre des 3 faces visibles est moins critique,
    # mais pour un effet d'ombrage cohérent, l'attribution des couleurs (cote1, cote2) est importante.
    # Choisissons cote1 pour la face X-max (face_droite_points) et cote2 pour la face Y-max (face_gauche_points).
    
    pygame.draw.polygon(surface, couleur_cote2, face_gauche_points)
    pygame.draw.polygon(surface, noir, face_gauche_points, 2) # Contour

    pygame.draw.polygon(surface, couleur_cote1, face_droite_points)
    pygame.draw.polygon(surface, noir, face_droite_points, 2) # Contour

    pygame.draw.polygon(surface, couleur_top, face_top_points)
    pygame.draw.polygon(surface, noir, face_top_points, 2) # Contour

# (Ajoutez cette fonction après dessiner_cube_iso)

# (Remplacez votre fonction dessiner_piece_3d par celle-ci)

def dessiner_piece_3d(surface, liste_cubes_relatifs, 
                      base_gx, base_gy, base_gz, 
                      couleur_piece):  # MODIFIÉ : Moins d'arguments
    """
    Dessine une pièce de Tetris 3D complète.
    - liste_cubes_relatifs: Une liste de tuples (dx,dy,dz) définissant la pièce.
    - base_gx, base_gy, base_gz: Position du pivot de la pièce dans la grille 3D du monde.
    - couleur_piece: La couleur de base pour tous les cubes de cette pièce.
    """
    for dx, dy, dz in liste_cubes_relatifs:
        # Calculer les coordonnées absolues du monde pour chaque cube de la pièce
        cube_monde_x = base_gx + dx
        cube_monde_y = base_gy + dy
        cube_monde_z = base_gz + dz
        
        # MODIFIÉ : Appel à dessiner_cube_iso avec 5 arguments
        dessiner_cube_iso(surface, cube_monde_x, cube_monde_y, cube_monde_z, 
                          couleur_piece)

# --- Création de la Fenêtre et Initialisation du Jeu ---
ecran = pygame.display.set_mode(taille_fenetre)
pygame.display.set_caption("Tetris 3D Isométrique - Test Cube")
horloge = pygame.time.Clock()

# Couleur pour notre cube de test
couleur_cube_test = (100, 150, 200) # Un bleu-gris

# (Ajoutez cette fonction avec vos autres fonctions logiques)

def creer_arene_3d_vide(largeur, profondeur, hauteur):
    """Crée une arène de jeu 3D vide (remplie de 0)."""
    # Crée une liste de 'hauteur' étages
    # Chaque étage est une grille 2D de 'profondeur' x 'largeur'
    arene = []
    for z in range(hauteur): # Pour chaque niveau de hauteur (axe Z)
        etage = []
        for y in range(profondeur): # Pour chaque rangée en profondeur (axe Y)
            ligne = [0] * largeur # Crée une ligne de 'largeur' cases vides (axe X)
            etage.append(ligne)
        arene.append(etage)
    return arene


# (Ajoutez cette fonction après vos autres fonctions de dessin)

def dessiner_arene_3d_figee(surface, arene_3d, dict_couleurs):
    """
    Dessine tous les blocs des pièces déjà atterries et figées dans l'arène 3D.
    """
    hauteur = len(arene_3d)
    profondeur = len(arene_3d[0])
    largeur = len(arene_3d[0][0])

    # Pour un rendu correct avec la perspective isométrique (effet du peintre simple),
    # il faut souvent dessiner de "l'arrière vers l'avant", "du bas vers le haut".
    # L'ordre exact peut dépendre de l'orientation de vos axes.
    # Un ordre commun : z (hauteur), puis y (profondeur), puis x (largeur).
    # Ou pour certaines vues : y (profondeur), puis x (largeur), puis z (hauteur).
    # Essayons z, puis y, puis x :
    for gz in range(hauteur):
        for gy in range(profondeur):
            for gx in range(largeur):
                valeur_cellule = arene_3d[gz][gy][gx]
                if valeur_cellule != 0: # Si la cellule contient un bloc figé
                    couleur_bloc = dict_couleurs.get(valeur_cellule, couleur_vide) # Récupère la couleur
                    # On dessine le cube. Les variables globales origine_iso_x_ecran et origine_iso_y_ecran
                    # seront utilisées par dessiner_cube_iso (via projeter_point_iso).
                    dessiner_cube_iso(surface, gx, gy, gz, couleur_bloc)
# Utilisation (à mettre dans la section d'initialisation du jeu, avant la boucle principale) :
# arene_3d_jeu = creer_arene_3d_vide(LARGEUR_ARENE_3D, PROFONDEUR_ARENE_3D, HAUTEUR_ARENE_3D)

# --- Boucle de Jeu Principale ---
# --- Initialisation de Pygame ---
pygame.init()
ecran = pygame.display.set_mode(taille_fenetre)
pygame.display.set_caption("Tetris 3D - Arène")
horloge = pygame.time.Clock()
# origine_iso_x_ecran, origine_iso_y_ecran sont définies

# --- Initialisation du Jeu ---
arene_3d_jeu = creer_arene_3d_vide(LARGEUR_ARENE_3D, PROFONDEUR_ARENE_3D, HAUTEUR_ARENE_3D)

# Mettons quelques blocs manuellement dans l'arène pour tester l'affichage :
if HAUTEUR_ARENE_3D > 0 and PROFONDEUR_ARENE_3D > 0 and LARGEUR_ARENE_3D > 0:
    arene_3d_jeu[0][0][0] = 1 # Bloc type 1 (jaune) au coin (0,0,0) de l'arène (bas, arrière, gauche)
if HAUTEUR_ARENE_3D > 0 and PROFONDEUR_ARENE_3D > 0 and LARGEUR_ARENE_3D > 1:
    arene_3d_jeu[0][0][1] = 2 # Bloc type 2 (cyan) à côté
if HAUTEUR_ARENE_3D > 1 and PROFONDEUR_ARENE_3D > 0 and LARGEUR_ARENE_3D > 0:
    arene_3d_jeu[1][0][0] = 3 # Bloc type 3 (orange) au-dessus du premier

# (Nous n'avons pas encore de pièce "active" qui tombe dans cette version 3D)

# --- Boucle de Jeu Principale ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Logique du jeu (rien pour l'instant)
    # ...

    # Dessin
    ecran.fill(noir) # Fond de l'écran

    # Dessiner les blocs figés dans l'arène 3D
    dessiner_arene_3d_figee(ecran, arene_3d_jeu, couleurs_pieces)
    
    # Plus tard, nous dessinerons ici la pièce qui tombe actuellement, par-dessus l'arène figée.
    # Pour l'instant, nous pouvons redessiner une pièce de test si vous voulez,
    # comme nous l'avons fait à l'étape précédente.
    # base_x_monde = 1
    # base_y_monde = 1
    # base_z_monde = 2
    # couleur_test_L = (255, 165, 0) # Orange
    # dessiner_piece_3d(ecran, piece_L_3D_forme0, 
    #                   base_x_monde, base_y_monde, base_z_monde, 
    #                   couleur_test_L)


    pygame.display.flip()
    horloge.tick(FPS)

# --- Quitter Pygame ---
pygame.quit()
sys.exit()