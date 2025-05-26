import random
import time
import os # Pour effacer la console
import keyboard # Nouvelle bibliothèque !

# --- Configuration de l'Arène de Jeu et Définitions des Pièces ---
# (Tout le code pour largeur_arene, hauteur_arene, les formes des pièces,
# tous_les_types_de_pieces, creer_arene_vide, verifier_collision, creer_nouvelle_piece
# reste identique à la version précédente. Assurez-vous de l'avoir ici.)

# COPIEZ ICI TOUTES LES DÉFINITIONS DE PIÈCES ET LES FONCTIONS:
# largeur_arene, hauteur_arene
# forme_O_rotations, forme_I_rotations, ..., forme_Z_rotations
# tous_les_types_de_pieces
# creer_arene_vide()
# verifier_collision(arene_fixe, piece_forme, piece_x, piece_y)
# creer_nouvelle_piece()
# --- Dimensions de l'arène ---
largeur_arene = 10
hauteur_arene = 20

# --- Définitions des 7 pièces standard de Tetris ---
forme_O_rotations = [[[1,1],[1,1]]]
forme_I_rotations = [[[2,2,2,2]], [[2],[2],[2],[2]]]
forme_L_rotations = [[[3,0,0],[3,3,3]], [[3,3],[3,0],[3,0]], [[3,3,3],[0,0,3]], [[0,3],[0,3],[3,3]]]
forme_J_rotations = [[[0,0,4],[4,4,4]], [[4,0],[4,0],[4,4]], [[4,4,4],[4,0,0]], [[4,4],[0,4],[0,4]]]
forme_T_rotations = [[[5,5,5],[0,5,0]], [[0,5],[5,5],[0,5]], [[0,5,0],[5,5,5]], [[5,0],[5,5],[5,0]]]
forme_S_rotations = [[[0,6,6],[6,6,0]], [[6,0],[6,6],[0,6]]]
forme_Z_rotations = [[[7,7,0],[0,7,7]], [[0,7],[7,7],[7,0]]]
tous_les_types_de_pieces = [forme_O_rotations, forme_I_rotations, forme_L_rotations, forme_J_rotations, forme_T_rotations, forme_S_rotations, forme_Z_rotations]

def creer_arene_vide():
    return [[0 for _ in range(largeur_arene)] for _ in range(hauteur_arene)]

def verifier_collision(arene_fixe, piece_forme, piece_x, piece_y):
    for y_offset_piece, ligne_de_la_piece in enumerate(piece_forme):
        for x_offset_piece, bloc_de_la_piece in enumerate(ligne_de_la_piece):
            if bloc_de_la_piece != 0:
                x_sur_arene = piece_x + x_offset_piece
                y_sur_arene = piece_y + y_offset_piece
                if not (0 <= x_sur_arene < largeur_arene): return True
                if not (y_sur_arene < hauteur_arene): return True
                if y_sur_arene >= 0 and arene_fixe[y_sur_arene][x_sur_arene] != 0: return True
    return False

def creer_nouvelle_piece():
    type_rotations = random.choice(tous_les_types_de_pieces)
    rotation_index = 0
    forme_initiale = type_rotations[rotation_index]
    pos_x = (largeur_arene // 2) - (len(forme_initiale[0]) // 2)
    pos_y = 0
    return type_rotations, rotation_index, pos_x, pos_y
# FIN DES COPIES

# --- Fonction pour effacer la console ---
def effacer_console():
    """Efface la console (multiplateforme)."""
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Nouvelle fonction d'affichage (peut rester la même) ---
def afficher_etat_jeu(arene_fixe, piece_forme, piece_x, piece_y):
    # (Identique à la fonction précédente)
    arene_pour_affichage = [ligne[:] for ligne in arene_fixe]
    for y_offset_piece, ligne_de_la_piece in enumerate(piece_forme):
        for x_offset_piece, bloc_de_la_piece in enumerate(ligne_de_la_piece):
            if bloc_de_la_piece != 0:
                y_sur_arene = piece_y + y_offset_piece
                x_sur_arene = piece_x + x_offset_piece
                if 0 <= y_sur_arene < hauteur_arene and \
                   0 <= x_sur_arene < largeur_arene:
                    arene_pour_affichage[y_sur_arene][x_sur_arene] = bloc_de_la_piece
    effacer_console() # On efface avant d'afficher la nouvelle grille
    print("+" + "---" * largeur_arene + "+")
    for y_idx in range(hauteur_arene):
        ligne_a_afficher = "| "
        for x_idx in range(largeur_arene):
            cellule = arene_pour_affichage[y_idx][x_idx]
            ligne_a_afficher += (str(cellule) if cellule != 0 else ".") + "  "
        ligne_a_afficher += "|"
        print(ligne_a_afficher)
    print("+" + "---" * largeur_arene + "+")
    print("Contrôles: A (Gauche), D (Droite), W (Rotation), S (Bas)")
def verifier_et_supprimer_lignes_completes(arene):
    """
    Vérifie toutes les lignes de l'arène. Si une ligne est complète,
    la supprime et fait descendre les lignes supérieures.
    Retourne le nombre de lignes supprimées.
    """
    lignes_supprimees_count = 0
    y = hauteur_arene - 1  # Commencer par la ligne la plus basse (index hauteur_arene - 1)

    while y >= 0:  # Tant qu'on n'a pas vérifié jusqu'en haut de l'arène
        ligne_est_complete = True
        for x in range(largeur_arene):
            if arene[y][x] == 0:  # Si on trouve une seule case vide dans la ligne
                ligne_est_complete = False
                break  # Inutile de vérifier le reste de la ligne
        
        if ligne_est_complete:
            # La ligne 'y' est complète !
            del arene[y]  # Supprime la ligne de la liste 'arene'
            # Insère une nouvelle ligne vide en haut de l'arène (à l'index 0)
            arene.insert(0, [0 for _ in range(largeur_arene)])
            lignes_supprimees_count += 1
            # Important : On ne décrémente PAS 'y' ici.
            # Puisque les lignes ont bougé, la nouvelle ligne à l'index 'y'
            # est celle qui était juste au-dessus, et elle doit aussi être vérifiée.
        else:
            y -= 1  # Si la ligne n'est pas complète, on passe à la ligne supérieure.
            
    return lignes_supprimees_count

# --- Initialisation du Jeu ---
arene_de_jeu = creer_arene_vide()
piece_actuelle_type_rotations, piece_actuelle_rotation_index, \
    piece_actuelle_x, piece_actuelle_y = creer_nouvelle_piece()
nombre_de_pieces_jouees_total = 0
game_over = False

# Paramètres de vitesse du jeu
vitesse_chute_auto = 0.5  # secondes avant que la pièce ne tombe d'une case
dernier_temps_chute_auto = time.time()
delai_repetition_touche = 0.1 # secondes de délai pour éviter les mouvements trop rapides si touche maintenue
dernier_temps_action_joueur = 0

print("Bienvenue dans Mini-Tetris en console (avec touches directes) !")
print("Contrôles: A (Gauche), D (Droite), W (Rotation), S (Bas). Q pour quitter.")
time.sleep(2) # Pause pour lire le message

# --- Boucle de Jeu Principale (modifiée) ---
while not game_over:
    temps_actuel = time.time()
    
    # Forme actuelle de la pièce
    forme_actuelle_de_la_piece = piece_actuelle_type_rotations[piece_actuelle_rotation_index]

    # --- Gestion des Entrées Utilisateur (non bloquant) ---
    action_effectuee_par_joueur = False
    if temps_actuel - dernier_temps_action_joueur > delai_repetition_touche:
        if keyboard.is_pressed('a') or keyboard.is_pressed('left'):
            test_x = piece_actuelle_x - 1
            if not verifier_collision(arene_de_jeu, forme_actuelle_de_la_piece, test_x, piece_actuelle_y):
                piece_actuelle_x = test_x
            action_effectuee_par_joueur = True
        elif keyboard.is_pressed('d') or keyboard.is_pressed('right'):
            test_x = piece_actuelle_x + 1
            if not verifier_collision(arene_de_jeu, forme_actuelle_de_la_piece, test_x, piece_actuelle_y):
                piece_actuelle_x = test_x
            action_effectuee_par_joueur = True
        elif keyboard.is_pressed('w') or keyboard.is_pressed('up'):
            test_rotation_index = (piece_actuelle_rotation_index + 1) % len(piece_actuelle_type_rotations)
            test_forme = piece_actuelle_type_rotations[test_rotation_index]
            if not verifier_collision(arene_de_jeu, test_forme, piece_actuelle_x, piece_actuelle_y):
                piece_actuelle_rotation_index = test_rotation_index
                # La forme_actuelle_de_la_piece sera mise à jour au début de la prochaine itération
            action_effectuee_par_joueur = True
        elif keyboard.is_pressed('s') or keyboard.is_pressed('down'): # Soft drop
            test_y = piece_actuelle_y + 1
            if not verifier_collision(arene_de_jeu, forme_actuelle_de_la_piece, piece_actuelle_x, test_y):
                piece_actuelle_y = test_y
                dernier_temps_chute_auto = temps_actuel # Réinitialise le timer de chute auto pour ne pas tomber deux fois trop vite
            action_effectuee_par_joueur = True
        elif keyboard.is_pressed('q'): # Quitter
            print("Partie quittée.")
            game_over = True
            break
        
        if action_effectuee_par_joueur:
            dernier_temps_action_joueur = temps_actuel


    # --- Application de la Gravité (basée sur le temps) ---
    if temps_actuel - dernier_temps_chute_auto > vitesse_chute_auto:
        y_apres_gravite = piece_actuelle_y + 1
        if not verifier_collision(arene_de_jeu, forme_actuelle_de_la_piece, piece_actuelle_x, y_apres_gravite):
            # Pas de collision en dessous, la pièce peut descendre
            piece_actuelle_y = y_apres_gravite
        else:
            # COLLISION en dessous ! La pièce atterrit.
            # 1. Figer la pièce actuelle sur l'arène de jeu principale
            for y_offset, ligne_p in enumerate(forme_actuelle_de_la_piece):
                for x_offset, bloc in enumerate(ligne_p):
                    if bloc != 0: 
                        y_figee = piece_actuelle_y + y_offset
                        x_figee = piece_actuelle_x + x_offset
                        if 0 <= y_figee < hauteur_arene and 0 <= x_figee < largeur_arene:
                             arene_de_jeu[y_figee][x_figee] = bloc
            
            # 2. VÉRIFIER ET SUPPRIMER LES LIGNES COMPLÈTES <--- NOUVEAU BLOC DE CODE ICI
            lignes_effacees = verifier_et_supprimer_lignes_completes(arene_de_jeu)
            if lignes_effacees > 0:
                print(f"{lignes_effacees} ligne(s) complétée(s) et supprimée(s) !")
                # Ici, plus tard, on pourrait ajouter des points au score !
                # La fonction afficher_etat_jeu sera appelée après, montrant la mise à jour.

            # 3. Mettre à jour le nombre de pièces jouées total
            nombre_de_pieces_jouees_total += 1
            
            # 4. Créer une nouvelle pièce en haut
            piece_actuelle_type_rotations, piece_actuelle_rotation_index, \
                piece_actuelle_x, piece_actuelle_y = creer_nouvelle_piece()
            
            # 5. Vérifier Game Over
            forme_nouvelle_piece = piece_actuelle_type_rotations[piece_actuelle_rotation_index]
            if verifier_collision(arene_de_jeu, forme_nouvelle_piece, piece_actuelle_x, piece_actuelle_y):
                game_over = True # Sera géré à l'affichage final
        
        dernier_temps_chute_auto = temps_actuel # Réinitialise le timer

    # --- Affichage ---
    # La forme actuelle doit être recalculée ici au cas où une rotation a eu lieu
    forme_actuelle_pour_affichage = piece_actuelle_type_rotations[piece_actuelle_rotation_index]
    afficher_etat_jeu(arene_de_jeu, forme_actuelle_pour_affichage, piece_actuelle_x, piece_actuelle_y)
    
    if game_over: # Affichage final avant de quitter
        print(f"GAME OVER après {nombre_de_pieces_jouees_total} pièces !")
        break

    # Petite pause pour contrôler la vitesse globale de la boucle et l'utilisation du CPU
    time.sleep(0.03) # Ajustez pour la réactivité souhaitée

# Fin du jeu
if game_over and not keyboard.is_pressed('q'): # Évite le double message si 'q' a été pressé
    print("Merci d'avoir joué !")