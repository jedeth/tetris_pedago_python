import pygame
import sys
import random
import time # Pas activement utilisé pour les délais ici, mais pygame.time l'est

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
HAUTEUR_ARENE_3D = 12 # Hauteur où les pièces peuvent s'empiler

# Couleurs
noir = (0, 0, 0)
blanc = (255, 255, 255)
gris_clair = (200, 200, 200)
rouge = (255, 0, 0)
couleur_vide = (30, 30, 30) # Pour les cases vides de l'arène si besoin

couleurs_pieces = {
    1: (255, 255, 0),   # Jaune
    2: (0, 255, 255),   # Cyan
    3: (255, 165, 0),   # Orange
    4: (0, 0, 255),     # Bleu foncé
    5: (128, 0, 128),   # Violet
    6: (0, 255, 0),     # Vert
    7: (255, 0, 0)      # Rouge (attention, utilisé aussi pour Game Over)
}

# --- Définitions des Formes de Pièces 3D et Types ---
PIECES_3D_TYPES = {
    "I": {"formes": [[(0,0,0), (1,0,0), (2,0,0), (3,0,0)]], "couleur_idx": 2, "nom": "I"},
    "L": {"formes": [[(0,0,0), (0,0,1), (0,0,2), (1,0,0)]], "couleur_idx": 3, "nom": "L"},
    "O_simple": {"formes": [[(0,0,0), (1,0,0)]], "couleur_idx": 1, "nom": "O_simple"}
    # TODO: Ajouter plus de pièces et leurs rotations
}
LISTE_NOMS_PIECES = list(PIECES_3D_TYPES.keys())

# --- Variables Globales pour la Pièce Active ---
piece_actuelle_type_rotations = [] # Liste des matrices de rotation pour le type de pièce actuel
piece_actuelle_rotation_index = 0  # Index de la rotation actuelle
piece_actuelle_definition = []     # Forme actuelle (liste de (dx,dy,dz))
piece_actuelle_gx = 0
piece_actuelle_gy = 0
piece_actuelle_gz = 0
piece_actuelle_couleur = noir
piece_actuelle_couleur_idx = 0     # Index de la couleur (clé pour couleurs_pieces)
nom_piece_actuelle = ""            # Pour le débogage

# --- Paramètres pour la Projection Isométrique ---
DEMI_LARGEUR_ISO = 24
DEMI_HAUTEUR_ISO = 12
HAUTEUR_Z_ISO = 18
origine_iso_x_ecran = largeur_fenetre // 2
origine_iso_y_ecran = hauteur_fenetre // 4

# --- Fonctions Utilitaires ---
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
    couleur_cote_droite = pygame.Color(min(255, int(r*0.8)), min(255, int(g*0.8)), min(255, int(b*0.8)))
    couleur_cote_gauche = pygame.Color(min(255, int(r*0.6)), min(255, int(g*0.6)), min(255, int(b*0.6)))
    
    # Faces: Top: s[4],s[5],s[7],s[6] | Droite (X-max): s[1],s[3],s[7],s[5] | Gauche (Y-max): s[2],s[3],s[7],s[6]
    # (L'ordre de dessin des faces peut influencer la perception si elles se chevauchent parfaitement)
    pygame.draw.polygon(surface, couleur_cote_gauche, [s[2], s[3], s[7], s[6]])
    pygame.draw.polygon(surface, noir, [s[2], s[3], s[7], s[6]], 2)
    pygame.draw.polygon(surface, couleur_cote_droite, [s[1], s[3], s[7], s[5]])
    pygame.draw.polygon(surface, noir, [s[1], s[3], s[7], s[5]], 2)
    pygame.draw.polygon(surface, couleur_top, [s[4], s[5], s[7], s[6]])
    pygame.draw.polygon(surface, noir, [s[4], s[5], s[7], s[6]], 2)

def dessiner_piece_3d(surface, liste_cubes_relatifs, base_gx, base_gy, base_gz, couleur_piece):
    for dx, dy, dz in liste_cubes_relatifs:
        dessiner_cube_iso(surface, base_gx + dx, base_gy + dy, base_gz + dz, couleur_piece)

def creer_arene_3d_vide(largeur, profondeur, hauteur):
    arene = []
    for _ in range(hauteur): # z
        etage = []
        for _ in range(profondeur): # y
            etage.append([0] * largeur) # x
        arene.append(etage)
    return arene

def dessiner_arene_3d_figee(surface, arene_3d, dict_couleurs):
    if not arene_3d: return
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

def generer_nouvelle_piece_3d():
    global piece_actuelle_type_rotations, piece_actuelle_rotation_index, piece_actuelle_definition
    global piece_actuelle_gx, piece_actuelle_gy, piece_actuelle_gz
    global piece_actuelle_couleur, piece_actuelle_couleur_idx, nom_piece_actuelle

    nom_piece_choisie = random.choice(LISTE_NOMS_PIECES)
    details_piece = PIECES_3D_TYPES[nom_piece_choisie]
    
    nom_piece_actuelle = details_piece["nom"]
    piece_actuelle_type_rotations = details_piece["formes"]
    piece_actuelle_rotation_index = 0 # Toujours la première rotation pour l'instant
    piece_actuelle_definition = piece_actuelle_type_rotations[piece_actuelle_rotation_index]
    
    piece_actuelle_couleur_idx = details_piece["couleur_idx"]
    piece_actuelle_couleur = couleurs_pieces.get(piece_actuelle_couleur_idx, blanc)

    piece_actuelle_gx = LARGEUR_ARENE_3D // 2 - 1 
    piece_actuelle_gy = PROFONDEUR_ARENE_3D // 2 - 1
    piece_actuelle_gz = HAUTEUR_ARENE_3D # Apparaît au-dessus du "plafond" pour tomber
    print(f"Nouvelle pièce: {nom_piece_actuelle} à GZ={piece_actuelle_gz}")

def verifier_collision_3d(arene_3d_logique, piece_definition_relative, base_gx, base_gy, base_gz):
    for dx, dy, dz in piece_definition_relative:
        ax = base_gx + dx
        ay = base_gy + dy
        az = base_gz + dz

        if not (0 <= ax < LARGEUR_ARENE_3D and 0 <= ay < PROFONDEUR_ARENE_3D):
            return True # Collision murs latéraux/profondeur
        if az < 0:
            return True # Collision avec le sol (z=0 est le sol)
        
        # Collision avec des blocs existants (seulement si DANS l'arène)
        if 0 <= az < HAUTEUR_ARENE_3D: # Le cube est à un niveau "figeable"
            if arene_3d_logique[az][ay][ax] != 0:
                return True 
    return False

# --- Création de la Fenêtre et Initialisation des Éléments de Jeu ---
ecran = pygame.display.set_mode(taille_fenetre)
pygame.display.set_caption("Tetris 3D - Atterrissage")
horloge = pygame.time.Clock()

arene_3d_jeu = creer_arene_3d_vide(LARGEUR_ARENE_3D, PROFONDEUR_ARENE_3D, HAUTEUR_ARENE_3D)
generer_nouvelle_piece_3d()

vitesse_chute = 700 # Millisecondes
temps_derniere_chute = pygame.time.get_ticks()
game_over = False

# --- Boucle de Jeu Principale ---
running = True
while running:
    temps_actuel = pygame.time.get_ticks()
    
    # Obtenir la forme actuelle pour les vérifications et le dessin
    # (sera important quand on ajoutera les rotations)
    forme_actuelle_pour_logique = piece_actuelle_type_rotations[piece_actuelle_rotation_index]

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # TODO: Ajouter les contrôles du joueur ici (si pas game_over)

    # --- Logique du Jeu ---
    if not game_over:
        if temps_actuel - temps_derniere_chute > vitesse_chute:
            prochain_gz = piece_actuelle_gz - 1
            
            if not verifier_collision_3d(arene_3d_jeu, forme_actuelle_pour_logique, 
                                         piece_actuelle_gx, piece_actuelle_gy, prochain_gz):
                piece_actuelle_gz = prochain_gz
            else:
                # La pièce atterrit !
                print(f"Pièce {nom_piece_actuelle} atterrit à GZ={piece_actuelle_gz}")
                for dx, dy, dz in forme_actuelle_pour_logique:
                    ax = piece_actuelle_gx + dx
                    ay = piece_actuelle_gy + dy
                    az = piece_actuelle_gz + dz
                    if 0 <= ax < LARGEUR_ARENE_3D and \
                       0 <= ay < PROFONDEUR_ARENE_3D and \
                       0 <= az < HAUTEUR_ARENE_3D:
                        arene_3d_jeu[az][ay][ax] = piece_actuelle_couleur_idx
                
                # TODO: Vérifier et supprimer les couches complètes
                
                generer_nouvelle_piece_3d() # Génère la suivante
                
                # Vérifier Game Over pour la NOUVELLE pièce
                forme_nouvelle_piece = piece_actuelle_type_rotations[piece_actuelle_rotation_index]
                if verifier_collision_3d(arene_3d_jeu, forme_nouvelle_piece, 
                                         piece_actuelle_gx, piece_actuelle_gy, piece_actuelle_gz):
                    game_over = True
                    print("GAME OVER!")
            
            temps_derniere_chute = temps_actuel

    # --- Dessin ---
    ecran.fill(noir)
    dessiner_arene_3d_figee(ecran, arene_3d_jeu, couleurs_pieces)
    
    if piece_actuelle_definition and not game_over: # Ne dessine la pièce active que si le jeu n'est pas fini
        dessiner_piece_3d(ecran, forme_actuelle_pour_logique, 
                          piece_actuelle_gx, piece_actuelle_gy, piece_actuelle_gz, 
                          piece_actuelle_couleur)
    
    if game_over:
        font = pygame.font.Font(None, 74) 
        text_surface = font.render('GAME OVER', True, rouge)
        text_rect = text_surface.get_rect(center=(largeur_fenetre/2, hauteur_fenetre/2))
        ecran.blit(text_surface, text_rect)

    pygame.display.flip()
    horloge.tick(FPS)

# --- Quitter Pygame ---
pygame.quit()
sys.exit()