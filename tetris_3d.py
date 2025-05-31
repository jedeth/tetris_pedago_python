import pygame
import sys
import random
import time # Utile pour la gestion du temps

# --- Initialisation de Pygame ---
pygame.init()

# --- Constantes pour la Fenêtre et l'Affichage ---
largeur_fenetre = 800
hauteur_fenetre = 600
taille_fenetre = (largeur_fenetre, hauteur_fenetre)
FPS = 30

# Dimensions de l'arène de jeu 3D (en nombre de blocs)
LARGEUR_ARENE_3D = 6
PROFONDEUR_ARENE_3D = 6
HAUTEUR_ARENE_3D = 10 # Hauteur où les pièces peuvent s'empiler

# Couleurs
noir = (0, 0, 0)
blanc = (255, 255, 255)
gris_clair = (200, 200, 200)
rouge = (255,0,0) # Ajouté pour Game Over et pour tests
couleur_vide = (30, 30, 30)

couleurs_pieces = {
    1: (255, 255, 0),   # Jaune
    2: (0, 255, 255),   # Cyan
    3: (255, 165, 0),   # Orange
    4: (0, 0, 255),     # Bleu foncé
    5: (128, 0, 128),   # Violet
    6: (0, 255, 0),     # Vert
    7: (255, 0, 0)      # Rouge
}

# --- Définitions des Formes de Pièces 3D et Types ---
PIECES_3D_TYPES = {
    "I": {"formes": [[(0,0,0), (1,0,0), (2,0,0), (3,0,0)]], "couleur_idx": 2},
    "L": {"formes": [[(0,0,0), (0,0,1), (0,0,2), (1,0,0)]], "couleur_idx": 3},
    "O_simple": {"formes": [[(0,0,0), (1,0,0)]], "couleur_idx": 1}
}
LISTE_NOMS_PIECES = list(PIECES_3D_TYPES.keys())

# --- Variables Globales pour la Pièce Active ---
piece_actuelle_definition = []
piece_actuelle_gx = 0
piece_actuelle_gy = 0
piece_actuelle_gz = 0
piece_actuelle_couleur = noir

# --- Paramètres pour la Projection Isométrique ---
DEMI_LARGEUR_ISO = 24
DEMI_HAUTEUR_ISO = 12
HAUTEUR_Z_ISO = 18
origine_iso_x_ecran = largeur_fenetre // 2
origine_iso_y_ecran = hauteur_fenetre // 4 # Un peu plus haut pour mieux voir tomber

# --- Fonctions Utilitaires (Projection, Dessin, Logique) ---
def projeter_point_iso(monde_x, monde_y, monde_z):
    ecran_x = origine_iso_x_ecran + (monde_x - monde_y) * DEMI_LARGEUR_ISO
    ecran_y = origine_iso_y_ecran + (monde_x + monde_y) * DEMI_HAUTEUR_ISO - monde_z * HAUTEUR_Z_ISO
    return int(ecran_x), int(ecran_y)

def dessiner_cube_iso(surface, gx, gy, gz, couleur_base):
    sommets_3d = [
        (gx, gy, gz), (gx + 1, gy, gz), (gx, gy + 1, gz), (gx + 1, gy + 1, gz),
        (gx, gy, gz + 1), (gx + 1, gy, gz + 1), (gx, gy + 1, gz + 1), (gx + 1, gy + 1, gz + 1)
    ]
    s = [projeter_point_iso(p[0], p[1], p[2]) for p in sommets_3d]
    r, g, b = couleur_base
    couleur_top = pygame.Color(min(255, int(r*1.0)), min(255, int(g*1.0)), min(255, int(b*1.0)))
    couleur_cote1 = pygame.Color(min(255, int(r*0.8)), min(255, int(g*0.8)), min(255, int(b*0.8))) # Droite (X-max)
    couleur_cote2 = pygame.Color(min(255, int(r*0.6)), min(255, int(g*0.6)), min(255, int(b*0.6))) # Gauche (Y-max)
    
    # Faces (s'assurer que les indices sont corrects pour les faces visibles)
    # Top: s[4],s[5],s[7],s[6] | Droite (X-max): s[1],s[3],s[7],s[5] | Gauche (Y-max): s[2],s[3],s[7],s[6]
    # Ordre pour un effet de recouvrement correct simple (peut nécessiter un tri plus avancé plus tard)
    pygame.draw.polygon(surface, couleur_cote2, [s[2], s[3], s[7], s[6]]) # Face Y-max (avant-gauche)
    pygame.draw.polygon(surface, noir, [s[2], s[3], s[7], s[6]], 2)
    pygame.draw.polygon(surface, couleur_cote1, [s[1], s[3], s[7], s[5]]) # Face X-max (avant-droite)
    pygame.draw.polygon(surface, noir, [s[1], s[3], s[7], s[5]], 2)
    pygame.draw.polygon(surface, couleur_top, [s[4], s[5], s[7], s[6]]) # Face du dessus
    pygame.draw.polygon(surface, noir, [s[4], s[5], s[7], s[6]], 2)

def dessiner_piece_3d(surface, liste_cubes_relatifs, base_gx, base_gy, base_gz, couleur_piece):
    for dx, dy, dz in liste_cubes_relatifs:
        cube_monde_x = base_gx + dx
        cube_monde_y = base_gy + dy
        cube_monde_z = base_gz + dz
        dessiner_cube_iso(surface, cube_monde_x, cube_monde_y, cube_monde_z, couleur_piece)

def creer_arene_3d_vide(largeur, profondeur, hauteur):
    arene = []
    for z_niveau in range(hauteur):
        etage = []
        for y_prof in range(profondeur):
            ligne = [0] * largeur
            etage.append(ligne)
        arene.append(etage)
    return arene

def dessiner_arene_3d_figee(surface, arene_3d, dict_couleurs):
    hauteur = len(arene_3d)
    if hauteur == 0: return
    profondeur = len(arene_3d[0])
    if profondeur == 0: return
    largeur = len(arene_3d[0][0])

    for gz in range(hauteur):
        for gy in range(profondeur):
            for gx in range(largeur):
                valeur_cellule = arene_3d[gz][gy][gx]
                if valeur_cellule != 0:
                    couleur_bloc = dict_couleurs.get(valeur_cellule, couleur_vide)
                    dessiner_cube_iso(surface, gx, gy, gz, couleur_bloc)

# NOUVEAU : Fonction pour générer une nouvelle pièce (met à jour les globales)
def generer_nouvelle_piece_3d():
    global piece_actuelle_definition, piece_actuelle_gx, piece_actuelle_gy, piece_actuelle_gz, piece_actuelle_couleur

    nom_piece_choisie = random.choice(LISTE_NOMS_PIECES)
    details_piece = PIECES_3D_TYPES[nom_piece_choisie]
    piece_actuelle_definition = details_piece["formes"][0] # Prend la première rotation définie
    piece_actuelle_couleur = couleurs_pieces.get(details_piece["couleur_idx"], blanc)

    # Position de départ centrée en X et Y, et en haut en Z
    piece_actuelle_gx = LARGEUR_ARENE_3D // 2 -1 # Ajustez si nécessaire pour centrer la pièce
    piece_actuelle_gy = PROFONDEUR_ARENE_3D // 2 -1 # Ajustez si nécessaire
    piece_actuelle_gz = HAUTEUR_ARENE_3D # Commence au-dessus du "plafond" visible pour tomber

    print(f"Nouvelle pièce: {nom_piece_choisie} à GZ={piece_actuelle_gz}")


# --- Création de la Fenêtre et Initialisation des Éléments de Jeu ---
ecran = pygame.display.set_mode(taille_fenetre)
pygame.display.set_caption("Tetris 3D - Chute de Pièces")
horloge = pygame.time.Clock()

arene_3d_jeu = creer_arene_3d_vide(LARGEUR_ARENE_3D, PROFONDEUR_ARENE_3D, HAUTEUR_ARENE_3D)
# Vous pouvez ajouter un sol pour tester la chute visuellement :
# for x_sol in range(LARGEUR_ARENE_3D):
#    for y_sol in range(PROFONDEUR_ARENE_3D):
#        arene_3d_jeu[0][y_sol][x_sol] = 1 # Sol jaune au niveau gz=0

generer_nouvelle_piece_3d() # Crée la première pièce active

# Paramètres pour la chute automatique
vitesse_chute = 1000 # millisecondes (1 seconde entre chaque descente)
temps_derniere_chute = pygame.time.get_ticks()

# --- Boucle de Jeu Principale ---
running = True
while running:
    temps_actuel = pygame.time.get_ticks()

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # TODO: Ajouter ici les contrôles du joueur (gauche, droite, rotation, etc.)

    # --- Logique du Jeu ---
    # Gravité : faire tomber la pièce active
    if temps_actuel - temps_derniere_chute > vitesse_chute:
        piece_actuelle_gz -= 1 # La pièce descend (Z diminue)
        temps_derniere_chute = temps_actuel
        # print(f"Pièce à GZ: {piece_actuelle_gz}") # Débogage

        # Logique de test très simple : si la pièce sort par le bas, en générer une nouvelle
        # (sera remplacé par la détection de collision et le verrouillage)
        min_gz_piece = piece_actuelle_gz # Le gz du pivot
        for _, _, dz in piece_actuelle_definition: # Trouver le dz le plus bas de la pièce
            if piece_actuelle_gz + dz < min_gz_piece :
                 min_gz_piece = piece_actuelle_gz + dz
        
        # Si le point le plus bas de la pièce (son pivot + son dz le plus bas, qui est souvent 0)
        # est en dessous du "sol" (gz=0), on regénère.
        # Note: si une pièce a des dz négatifs, cette logique doit être adaptée.
        # Nos pièces actuelles ont dz >= 0.
        if piece_actuelle_gz + min([dz for _,_,dz in piece_actuelle_definition]) < 0 : # si le cube le plus bas de la piece est sous le sol
             print(f"Pièce {LISTE_NOMS_PIECES[LISTE_NOMS_PIECES.index(random.choice(LISTE_NOMS_PIECES))]} a atteint le bas, regénération...")
             generer_nouvelle_piece_3d()


    # --- Dessin ---
    ecran.fill(noir)

    # Dessiner l'arène figée
    dessiner_arene_3d_figee(ecran, arene_3d_jeu, couleurs_pieces)
    
    # Dessiner la pièce active qui tombe
    if piece_actuelle_definition:
        dessiner_piece_3d(ecran, piece_actuelle_definition, 
                          piece_actuelle_gx, piece_actuelle_gy, piece_actuelle_gz, 
                          piece_actuelle_couleur)

    pygame.display.flip()
    horloge.tick(FPS)

# --- Quitter Pygame ---
pygame.quit()
sys.exit()