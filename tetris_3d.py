import pygame
import sys
import random
# import time # Pas strictement nécessaire si on utilise pygame.time.get_ticks()

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
HAUTEUR_ARENE_3D = 12 

# Couleurs
noir = (0, 0, 0)
blanc = (255, 255, 255)
gris_clair = (200, 200, 200)
rouge = (255, 0, 0)
couleur_vide = (30, 30, 30)
COULEUR_FANTOME = (70, 70, 70)

couleurs_pieces = {
    1: (255, 255, 0), 2: (0, 255, 255), 3: (255, 165, 0),
    4: (0, 0, 255), 5: (128, 0, 128), 6: (0, 255, 0), 7: (255, 0, 0)
}

PIECES_3D_TYPES = {
    "I": {"formes": [[(0,0,0), (1,0,0), (2,0,0), (3,0,0)]], "couleur_idx": 2, "nom": "I"},
    "L": {"formes": [[(0,0,0), (0,0,1), (0,0,2), (1,0,0)]], "couleur_idx": 3, "nom": "L"},
    "O_simple": {"formes": [[(0,0,0), (1,0,0)]], "couleur_idx": 1, "nom": "O_simple"}
}
LISTE_NOMS_PIECES = list(PIECES_3D_TYPES.keys())

piece_actuelle_type_rotations = []
piece_actuelle_rotation_index = 0
piece_actuelle_definition = []
piece_actuelle_gx = 0; piece_actuelle_gy = 0; piece_actuelle_gz = 0
piece_actuelle_couleur = noir; piece_actuelle_couleur_idx = 0
nom_piece_actuelle = ""

DEMI_LARGEUR_ISO = 24
DEMI_HAUTEUR_ISO = 12
HAUTEUR_Z_ISO = 18
origine_iso_x_ecran = largeur_fenetre // 2
origine_iso_y_ecran = hauteur_fenetre // 4

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
    try:
        couleur_top = pygame.Color(min(255, int(r*1.0)), min(255, int(g*1.0)), min(255, int(b*1.0)))
        couleur_cote_droite = pygame.Color(min(255, int(r*0.8)), min(255, int(g*0.8)), min(255, int(b*0.8)))
        couleur_cote_gauche = pygame.Color(min(255, int(r*0.6)), min(255, int(g*0.6)), min(255, int(b*0.6)))
    except TypeError: # Au cas où couleur_base ne serait pas un tuple RGB (ex: un int si erreur de logique)
        couleur_top = couleur_cote_droite = couleur_cote_gauche = pygame.Color("magenta") # Couleur d'erreur

    pygame.draw.polygon(surface, couleur_cote_gauche, [s[2], s[3], s[7], s[6]])
    pygame.draw.polygon(surface, noir, [s[2], s[3], s[7], s[6]], 2)
    pygame.draw.polygon(surface, couleur_cote_droite, [s[1], s[3], s[7], s[5]])
    pygame.draw.polygon(surface, noir, [s[1], s[3], s[7], s[5]], 2)
    pygame.draw.polygon(surface, couleur_top, [s[4], s[5], s[7], s[6]])
    pygame.draw.polygon(surface, noir, [s[4], s[5], s[7], s[6]], 2)

def dessiner_piece_3d(surface, liste_cubes_relatifs, base_gx, base_gy, base_gz, couleur_piece):
    if not liste_cubes_relatifs : return # Sécurité
    for dx, dy, dz in liste_cubes_relatifs:
        dessiner_cube_iso(surface, base_gx + dx, base_gy + dy, base_gz + dz, couleur_piece)

def creer_arene_3d_vide(largeur, profondeur, hauteur):
    arene = [[[0 for _ in range(largeur)] for _ in range(profondeur)] for _ in range(hauteur)]
    return arene

def dessiner_arene_3d_figee(surface, arene_3d, dict_couleurs):
    if not arene_3d or not arene_3d[0] or not arene_3d[0][0]: return # Sécurité
    hauteur, profondeur, largeur = len(arene_3d), len(arene_3d[0]), len(arene_3d[0][0])
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

    if not LISTE_NOMS_PIECES:
        print("ERREUR: LISTE_NOMS_PIECES est vide!")
        return # Ne rien faire si aucune pièce n'est définie

    nom_piece_choisie = random.choice(LISTE_NOMS_PIECES)
    details_piece = PIECES_3D_TYPES[nom_piece_choisie]
    
    nom_piece_actuelle = details_piece.get("nom", "Inconnue") # Utiliser .get pour sécurité
    piece_actuelle_type_rotations = details_piece.get("formes", [[]]) # Sécurité
    piece_actuelle_rotation_index = 0
    if not piece_actuelle_type_rotations or not piece_actuelle_type_rotations[0]:
        print(f"ERREUR: Formes non valides pour la pièce {nom_piece_actuelle}")
        piece_actuelle_definition = [] # Définition vide pour éviter crash
    else:
        piece_actuelle_definition = piece_actuelle_type_rotations[piece_actuelle_rotation_index]
    
    piece_actuelle_couleur_idx = details_piece.get("couleur_idx", 1) # Sécurité
    piece_actuelle_couleur = couleurs_pieces.get(piece_actuelle_couleur_idx, blanc)

    piece_actuelle_gx = LARGEUR_ARENE_3D // 2 - 1 
    piece_actuelle_gy = PROFONDEUR_ARENE_3D // 2 - 1
    piece_actuelle_gz = HAUTEUR_ARENE_3D 
    print(f"Nouvelle pièce: {nom_piece_actuelle} à GZ={piece_actuelle_gz}, Def len: {len(piece_actuelle_definition)}")

def verifier_collision_3d(arene_3d_logique, piece_definition_relative, base_gx, base_gy, base_gz):
    if not piece_definition_relative: return False # Si pas de définition, pas de collision (ou True si on veut bloquer?)
    for dx, dy, dz in piece_definition_relative:
        ax = base_gx + dx; ay = base_gy + dy; az = base_gz + dz
        if not (0 <= ax < LARGEUR_ARENE_3D and 0 <= ay < PROFONDEUR_ARENE_3D): return True
        if az < 0: return True
        if 0 <= az < HAUTEUR_ARENE_3D:
            if arene_3d_logique[az][ay][ax] != 0: return True 
    return False

# NOUVELLE FONCTION calculer_position_fantome avec DEBUG
def calculer_position_fantome(arene_3d_logique, piece_definition_relative, 
                              piece_gx, piece_gy, piece_gz_actuel):
    if not piece_definition_relative:
        print("Fantome AVERTISSEMENT: piece_definition_relative vide dans calculer_position_fantome.")
        return piece_gz_actuel 

    gz_test = piece_gz_actuel
    max_iterations = HAUTEUR_ARENE_3D + len(piece_definition_relative) + 5 # Sécurité
    count = 0
    while not verifier_collision_3d(arene_3d_logique, piece_definition_relative, 
                                     piece_gx, piece_gy, gz_test - 1):
        gz_test -= 1
        count += 1
        if count > max_iterations:
            print("Fantome ERREUR: Boucle potentiellement infinie dans calculer_position_fantome")
            return piece_gz_actuel # Éviter un blocage complet
    return gz_test

ecran = pygame.display.set_mode(taille_fenetre)
pygame.display.set_caption("Tetris 3D")
horloge = pygame.time.Clock()
arene_3d_jeu = creer_arene_3d_vide(LARGEUR_ARENE_3D, PROFONDEUR_ARENE_3D, HAUTEUR_ARENE_3D)
generer_nouvelle_piece_3d()
vitesse_chute = 700
temps_derniere_chute = pygame.time.get_ticks()
game_over = False

# --- Boucle de Jeu Principale ---
running = True
while running:
    temps_actuel = pygame.time.get_ticks()
    
    # S'assurer que la forme actuelle est bien définie
    # Cette vérification est importante pour éviter les erreurs si quelque chose se passe mal
    # pendant la génération de la pièce.
    if not piece_actuelle_type_rotations or \
       piece_actuelle_rotation_index >= len(piece_actuelle_type_rotations) or \
       not piece_actuelle_type_rotations[piece_actuelle_rotation_index]:
        print("Problème avec la définition de la pièce active, tentative de regénération...")
        generer_nouvelle_piece_3d()
        if not piece_actuelle_type_rotations or \
           piece_actuelle_rotation_index >= len(piece_actuelle_type_rotations) or \
           not piece_actuelle_type_rotations[piece_actuelle_rotation_index]:
            print("Erreur critique : Impossible de définir la forme de la pièce après regénération.")
            running = False 
            continue 
    forme_actuelle_pour_logique = piece_actuelle_type_rotations[piece_actuelle_rotation_index]


    # --- Gestion des événements ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            
            if not game_over: # Les contrôles ne fonctionnent que si le jeu n'est pas fini
                # --- DÉBUT DES CONTRÔLES DU JOUEUR (RÉINTÉGRÉS) ---
                if event.key == pygame.K_LEFT: 
                    prochain_gx = piece_actuelle_gx - 1
                    if not verifier_collision_3d(arene_3d_jeu, forme_actuelle_pour_logique, 
                                                 prochain_gx, piece_actuelle_gy, piece_actuelle_gz):
                        piece_actuelle_gx = prochain_gx
                elif event.key == pygame.K_RIGHT: 
                    prochain_gx = piece_actuelle_gx + 1
                    if not verifier_collision_3d(arene_3d_jeu, forme_actuelle_pour_logique, 
                                                 prochain_gx, piece_actuelle_gy, piece_actuelle_gz):
                        piece_actuelle_gx = prochain_gx
                elif event.key == pygame.K_UP: # Déplacer sur l'axe Y (profondeur) en "s'éloignant" (gy--)
                    prochain_gy = piece_actuelle_gy - 1
                    if not verifier_collision_3d(arene_3d_jeu, forme_actuelle_pour_logique, 
                                                 piece_actuelle_gx, prochain_gy, piece_actuelle_gz):
                        piece_actuelle_gy = prochain_gy
                elif event.key == pygame.K_DOWN: # Déplacer sur l'axe Y (profondeur) en "se rapprochant" (gy++)
                    prochain_gy = piece_actuelle_gy + 1
                    if not verifier_collision_3d(arene_3d_jeu, forme_actuelle_pour_logique, 
                                                 piece_actuelle_gx, prochain_gy, piece_actuelle_gz):
                        piece_actuelle_gy = prochain_gy
                elif event.key == pygame.K_f: # Soft drop
                    prochain_gz_soft_drop = piece_actuelle_gz - 1
                    if not verifier_collision_3d(arene_3d_jeu, forme_actuelle_pour_logique,
                                                 piece_actuelle_gx, piece_actuelle_gy, prochain_gz_soft_drop):
                        piece_actuelle_gz = prochain_gz_soft_drop
                        temps_derniere_chute = temps_actuel # Accélère aussi la prochaine chute naturelle
                elif event.key == pygame.K_SPACE: # Hard drop
                    while not verifier_collision_3d(arene_3d_jeu, forme_actuelle_pour_logique,
                                                    piece_actuelle_gx, piece_actuelle_gy, piece_actuelle_gz - 1):
                        piece_actuelle_gz -= 1
                    temps_derniere_chute = temps_actuel - vitesse_chute - 1 # Force atterrissage immédiat au prochain cycle logique
                elif event.key == pygame.K_r: # Pour la rotation future
                    print("Rotation demandée (Logique TODO)")
                # --- FIN DES CONTRÔLES DU JOUEUR ---

    # --- Logique du Jeu (Gravité, Atterrissage, etc.) ---
    if not game_over:
        if temps_actuel - temps_derniere_chute > vitesse_chute:
            prochain_gz = piece_actuelle_gz - 1
            
            if not verifier_collision_3d(arene_3d_jeu, forme_actuelle_pour_logique, 
                                         piece_actuelle_gx, piece_actuelle_gy, prochain_gz):
                piece_actuelle_gz = prochain_gz
            else:
                # La pièce atterrit !
                print(f"Pièce {nom_piece_actuelle} atterrit à GZ={piece_actuelle_gz}")
                if forme_actuelle_pour_logique: # S'assurer qu'il y a une forme à figer
                    for dx, dy, dz_cube in forme_actuelle_pour_logique:
                        ax = piece_actuelle_gx + dx
                        ay = piece_actuelle_gy + dy
                        az = piece_actuelle_gz + dz_cube
                        if 0 <= ax < LARGEUR_ARENE_3D and \
                           0 <= ay < PROFONDEUR_ARENE_3D and \
                           0 <= az < HAUTEUR_ARENE_3D:
                            arene_3d_jeu[az][ay][ax] = piece_actuelle_couleur_idx
                
                # TODO: Vérifier et supprimer les couches complètes
                
                generer_nouvelle_piece_3d() # Génère la suivante
                
                # Vérifier Game Over pour la NOUVELLE pièce
                # S'assurer que la forme de la nouvelle pièce est bien récupérée
                if piece_actuelle_type_rotations : # Vérification supplémentaire
                    forme_nouvelle_piece_logique = piece_actuelle_type_rotations[piece_actuelle_rotation_index]
                    if verifier_collision_3d(arene_3d_jeu, forme_nouvelle_piece_logique, 
                                             piece_actuelle_gx, piece_actuelle_gy, piece_actuelle_gz):
                        game_over = True
                        print("GAME OVER!")
                else: # Si la génération de pièce a échoué à remplir piece_actuelle_type_rotations
                    game_over = True
                    print("GAME OVER! (Erreur de génération de pièce)")

            temps_derniere_chute = temps_actuel

    # --- Dessin ---
    ecran.fill(noir)
    dessiner_arene_3d_figee(ecran, arene_3d_jeu, couleurs_pieces)
    
    if piece_actuelle_definition: # S'assurer qu'une pièce est définie
        # Utiliser la forme actuelle pour le dessin (qui est à jour après une éventuelle rotation)
        forme_a_dessiner = piece_actuelle_type_rotations[piece_actuelle_rotation_index] if piece_actuelle_type_rotations else []
        
        if forme_a_dessiner and not game_over : # Dessiner la pièce fantôme et la pièce active
            gz_fantome = calculer_position_fantome(arene_3d_jeu, forme_a_dessiner, 
                                                   piece_actuelle_gx, piece_actuelle_gy, piece_actuelle_gz)
            dessiner_piece_3d(ecran, forme_a_dessiner, 
                              piece_actuelle_gx, piece_actuelle_gy, gz_fantome, 
                              COULEUR_FANTOME)
            
            dessiner_piece_3d(ecran, forme_a_dessiner, 
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