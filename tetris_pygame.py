import pygame
import sys
import random # Nécessaire pour choisir les pièces au hasard
import time # NOUVEAU (était dans ma version précédente, mais peut-être pas dans la vôtre)

# Dimensions de l'arène de Tetris (en nombre de blocs)
largeur_arene_blocs = 10
hauteur_arene_blocs = 20

# Taille de chaque bloc de Tetris en pixels
taille_cellule = 30  # Chaque bloc fera 30x30 pixels

# Calculer la taille de la fenêtre Pygame
largeur_fenetre = largeur_arene_blocs * taille_cellule
hauteur_fenetre = hauteur_arene_blocs * taille_cellule
taille_fenetre = (largeur_fenetre, hauteur_fenetre)

# Définition des couleurs
noir = (0, 0, 0)
blanc = (255, 255, 255)
gris_clair = (200, 200, 200) # Pour les lignes de la grille
rouge = (255, 0, 0)
couleur_vide = (0,0,0)

# Dictionnaire pour mapper le numéro du type de pièce à sa couleur
couleurs_pieces = {
    1: (255, 255, 0),   # Jaune pour la pièce O
    2: (0, 255, 255),   # Cyan pour la pièce I
    3: (255, 165, 0),   # Orange pour la pièce L
    4: (0, 0, 255),     # Bleu foncé pour la pièce J
    5: (128, 0, 128),   # Violet pour la pièce T
    6: (0, 255, 0),     # Vert pour la pièce S
    7: (255, 0, 0)      # Rouge pour la pièce Z (attention, même couleur que 'rouge' pour GAME OVER)
}

# Définitions complètes des formes des pièces et de leurs rotations
forme_O_rotations = [[[1,1],[1,1]]]
forme_I_rotations = [[[2,2,2,2]], [[2],[2],[2],[2]]]
forme_L_rotations = [[[3,0,0],[3,3,3]], [[3,3],[3,0],[3,0]], [[3,3,3],[0,0,3]], [[0,3],[0,3],[3,3]]]
forme_J_rotations = [[[0,0,4],[4,4,4]], [[4,0],[4,0],[4,4]], [[4,4,4],[4,0,0]], [[4,4],[0,4],[0,4]]]
forme_T_rotations = [[[5,5,5],[0,5,0]], [[0,5],[5,5],[0,5]], [[0,5,0],[5,5,5]], [[5,0],[5,5],[5,0]]]
forme_S_rotations = [[[0,6,6],[6,6,0]], [[6,0],[6,6],[0,6]]]
forme_Z_rotations = [[[7,7,0],[0,7,7]], [[0,7],[7,7],[7,0]]]
tous_les_types_de_pieces = [
    forme_O_rotations, forme_I_rotations, forme_L_rotations,
    forme_J_rotations, forme_T_rotations, forme_S_rotations,
    forme_Z_rotations
]

# --- Fonctions de Dessin ---
def dessiner_grille(surface):
    for x in range(0, largeur_fenetre, taille_cellule):
        pygame.draw.line(surface, gris_clair, (x, 0), (x, hauteur_fenetre))
    for y in range(0, hauteur_fenetre, taille_cellule):
        pygame.draw.line(surface, gris_clair, (0, y), (largeur_fenetre, y))

def dessiner_bloc(surface, couleur, x_position_grille, y_position_grille):
    x_pixel = x_position_grille * taille_cellule
    y_pixel = y_position_grille * taille_cellule
    bloc_rect = pygame.Rect(x_pixel, y_pixel, taille_cellule, taille_cellule)
    pygame.draw.rect(surface, couleur, bloc_rect)
    pygame.draw.rect(surface, noir, bloc_rect, 1)

def dessiner_piece(surface, piece_matrice, x_piece_grille, y_piece_grille, dict_couleurs):
    for y_offset_matrice, ligne in enumerate(piece_matrice):
        for x_offset_matrice, valeur_cellule in enumerate(ligne):
            if valeur_cellule != 0:
                couleur_bloc = dict_couleurs.get(valeur_cellule, couleur_vide)
                x_bloc_grille = x_piece_grille + x_offset_matrice
                y_bloc_grille = y_piece_grille + y_offset_matrice
                dessiner_bloc(surface, couleur_bloc, x_bloc_grille, y_bloc_grille)

def dessiner_arene_figee(surface, arene_logique, dict_couleurs):
    for y_grille, ligne in enumerate(arene_logique):
        for x_grille, valeur_cellule in enumerate(ligne):
            if valeur_cellule != 0:
                couleur_bloc = dict_couleurs.get(valeur_cellule, couleur_vide)
                dessiner_bloc(surface, couleur_bloc, x_grille, y_grille)

# --- Fonctions Logiques du Jeu ---
def creer_arene_vide():
    return [[0 for _ in range(largeur_arene_blocs)] for _ in range(hauteur_arene_blocs)]

def creer_nouvelle_piece():
    type_rotations = random.choice(tous_les_types_de_pieces)
    rotation_index = 0
    forme_initiale = type_rotations[rotation_index]
    pos_x = (largeur_arene_blocs // 2) - (len(forme_initiale[0]) // 2)
    pos_y = 0
    return type_rotations, rotation_index, pos_x, pos_y

def verifier_collision(arene_fixe, piece_forme, piece_x, piece_y):
    for y_offset_piece, ligne_de_la_piece in enumerate(piece_forme):
        for x_offset_piece, bloc_de_la_piece in enumerate(ligne_de_la_piece):
            if bloc_de_la_piece != 0:
                x_sur_arene = piece_x + x_offset_piece
                y_sur_arene = piece_y + y_offset_piece
                if not (0 <= x_sur_arene < largeur_arene_blocs): return True
                if not (y_sur_arene < hauteur_arene_blocs): return True
                if y_sur_arene >= 0 and arene_fixe[y_sur_arene][x_sur_arene] != 0: return True
    return False

def verifier_et_supprimer_lignes_completes(arene):
    lignes_supprimees_count = 0
    y = hauteur_arene_blocs - 1
    while y >= 0:
        ligne_est_complete = True
        for x in range(largeur_arene_blocs):
            if arene[y][x] == 0:
                ligne_est_complete = False
                break
        if ligne_est_complete:
            del arene[y]
            arene.insert(0, [0 for _ in range(largeur_arene_blocs)])
            lignes_supprimees_count += 1
        else:
            y -= 1
    return lignes_supprimees_count

# --- Initialisation de Pygame ---
pygame.init()

# Variables pour le jeu
game_over = False
horloge = pygame.time.Clock()
FPS = 30 # Visez 30 FPS pour commencer
vitesse_chute_initiale = 500 # millisecondes (0.5 secondes)
temps_derniere_chute_auto = pygame.time.get_ticks()

# Création de la fenêtre et initialisation du jeu
ecran = pygame.display.set_mode(taille_fenetre)
pygame.display.set_caption("Tetris Pygame !")

arene_de_jeu = creer_arene_vide()
piece_actuelle_type_rotations, piece_actuelle_rotation_index, \
    piece_actuelle_x, piece_actuelle_y = creer_nouvelle_piece()
nombre_de_pieces_jouees_total = 0 # Optionnel, pour suivi

# --- Boucle de Jeu Principale ---
running = True
while running:
    # MODIFIÉ : Tout ce qui suit est maintenant correctement indenté dans la boucle while
    temps_actuel_ticks = pygame.time.get_ticks()
    forme_actuelle_de_la_piece = piece_actuelle_type_rotations[piece_actuelle_rotation_index]

    # --- Gestion des Événements (Entrées Clavier) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                test_x = piece_actuelle_x - 1
                if not verifier_collision(arene_de_jeu, forme_actuelle_de_la_piece, test_x, piece_actuelle_y):
                    piece_actuelle_x = test_x
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                test_x = piece_actuelle_x + 1
                if not verifier_collision(arene_de_jeu, forme_actuelle_de_la_piece, test_x, piece_actuelle_y):
                    piece_actuelle_x = test_x
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                test_rotation_index = (piece_actuelle_rotation_index + 1) % len(piece_actuelle_type_rotations)
                test_forme = piece_actuelle_type_rotations[test_rotation_index]
                if not verifier_collision(arene_de_jeu, test_forme, piece_actuelle_x, piece_actuelle_y):
                    piece_actuelle_rotation_index = test_rotation_index
                    # forme_actuelle_de_la_piece sera mis à jour au début de la prochaine itération
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                test_y = piece_actuelle_y + 1
                if not verifier_collision(arene_de_jeu, forme_actuelle_de_la_piece, piece_actuelle_x, test_y):
                    piece_actuelle_y = test_y
                    temps_derniere_chute_auto = temps_actuel_ticks
            elif event.key == pygame.K_SPACE:
                while not verifier_collision(arene_de_jeu, forme_actuelle_de_la_piece, piece_actuelle_x, piece_actuelle_y + 1):
                    piece_actuelle_y += 1
                temps_derniere_chute_auto = temps_actuel_ticks - vitesse_chute_initiale - 1

    # --- Logique du Jeu ---
    if not game_over:
        if temps_actuel_ticks - temps_derniere_chute_auto > vitesse_chute_initiale:
            prochain_y = piece_actuelle_y + 1
            if not verifier_collision(arene_de_jeu, forme_actuelle_de_la_piece, piece_actuelle_x, prochain_y):
                piece_actuelle_y = prochain_y
            else:
                # La pièce atterrit !
                for y_offset, ligne_p in enumerate(forme_actuelle_de_la_piece):
                    for x_offset, bloc in enumerate(ligne_p):
                        if bloc != 0:
                            y_figee = piece_actuelle_y + y_offset
                            x_figee = piece_actuelle_x + x_offset
                            if 0 <= y_figee < hauteur_arene_blocs and 0 <= x_figee < largeur_arene_blocs:
                                 arene_de_jeu[y_figee][x_figee] = bloc
                
                lignes_effacees = verifier_et_supprimer_lignes_completes(arene_de_jeu)
                if lignes_effacees > 0:
                    print(f"{lignes_effacees} ligne(s) complétée(s)!")
                
                nombre_de_pieces_jouees_total +=1 # Pour info

                piece_actuelle_type_rotations, piece_actuelle_rotation_index, \
                    piece_actuelle_x, piece_actuelle_y = creer_nouvelle_piece()
                
                forme_nouvelle_piece = piece_actuelle_type_rotations[piece_actuelle_rotation_index]
                if verifier_collision(arene_de_jeu, forme_nouvelle_piece, piece_actuelle_x, piece_actuelle_y):
                    game_over = True
                    print("GAME OVER!")
            
            temps_derniere_chute_auto = temps_actuel_ticks

    # --- Dessin / Rendu ---
    ecran.fill(noir)
    dessiner_grille(ecran)
    dessiner_arene_figee(ecran, arene_de_jeu, couleurs_pieces)
    
    # Toujours dessiner la pièce active, même si game_over (pour voir où elle a causé le game over)
    # Sauf si on préfère un écran de game over "propre"
    dessiner_piece(ecran, forme_actuelle_de_la_piece,
                   piece_actuelle_x, piece_actuelle_y,
                   couleurs_pieces)
    
    if game_over:
        font = pygame.font.Font(None, 74) # Police par défaut, taille 74
        text_surface = font.render('GAME OVER', True, rouge) # La variable 'rouge' doit être définie
        text_rect = text_surface.get_rect(center=(largeur_fenetre/2, hauteur_fenetre/2))
        ecran.blit(text_surface, text_rect)

    pygame.display.flip()
    horloge.tick(FPS)

# --- Quitter Pygame ---
pygame.quit()
sys.exit()