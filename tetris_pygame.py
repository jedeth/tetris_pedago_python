import pygame
import sys # On aura besoin de sys pour quitter proprement le programme

# (À ajouter au début de votre fichier tetris_pygame.py, après les imports)

# Dimensions de l'arène de Tetris (en nombre de blocs)
largeur_arene_blocs = 10
hauteur_arene_blocs = 20

# Taille de chaque bloc de Tetris en pixels
taille_cellule = 30  # Chaque bloc fera 30x30 pixels

# Calculer la taille de la fenêtre Pygame en fonction de cela
largeur_fenetre = largeur_arene_blocs * taille_cellule
hauteur_fenetre = hauteur_arene_blocs * taille_cellule
taille_fenetre = (largeur_fenetre, hauteur_fenetre) # Sera utilisé pour pygame.display.set_mode()

# Définir quelques couleurs (vous pouvez en ajouter d'autres !)
noir = (0, 0, 0)
blanc = (255, 255, 255)
gris_clair = (200, 200, 200) # Pour les lignes de la grille
rouge = (255, 0, 0)
vert = (0, 255, 0)
bleu = (0, 0, 255)


# Couleurs pour les pièces (un exemple, on les utilisera plus tard)
couleur_piece_L = (255, 165, 0) # Orange
couleur_piece_I = (0, 255, 255) # Cyan
# ... et ainsi de suite pour les autres pièces.


# (Cette fonction peut être ajoutée après vos définitions de couleurs)

def dessiner_grille(surface):
    """Dessine les lignes de la grille sur la surface donnée."""
    for x in range(0, largeur_fenetre, taille_cellule): # Lignes verticales
        pygame.draw.line(surface, gris_clair, (x, 0), (x, hauteur_fenetre))
    for y in range(0, hauteur_fenetre, taille_cellule): # Lignes horizontales
        pygame.draw.line(surface, gris_clair, (0, y), (largeur_fenetre, y))

# tetris_pygame.py - Un jeu de Tetris simple avec Pygame
# 1. Initialisation de Pygame
pygame.init()

# 2. Définition des dimensions de la fenêtre
largeur_fenetre = 800  # en pixels
hauteur_fenetre = 600 # en pixels
taille_fenetre = (largeur_fenetre, hauteur_fenetre)

# 3. Création de la fenêtre de jeu
#    pygame.display.set_mode() retourne une "Surface", c'est notre écran principal
ecran = pygame.display.set_mode(taille_fenetre)

# 4. Définir le titre de la fenêtre
pygame.display.set_caption("Mon Premier Jeu Pygame - Tetris en préparation !")

# 5. Définir quelques couleurs (Rouge, Vert, Bleu - RVB)
noir = (0, 0, 0)
blanc = (255, 255, 255)
bleu_clair = (173, 216, 230) # Une couleur pour le fond

# 6. La Boucle de Jeu Principale
#    C'est le coeur de tout jeu Pygame. Elle tourne en continu.
running = True
while running:
    # 7. Gestion des Événements
    #    Pygame vérifie toutes les actions du joueur (clavier, souris, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Si le joueur clique sur la croix pour fermer
            running = False           # On met 'running' à False pour sortir de la boucle

    # 8. Logique du Jeu (pour l'instant, rien ici)
    #    C'est ici qu'on mettrait à jour les positions des objets, le score, etc.

    # 9. Dessin / Rendu
    #    On efface l'écran avec une couleur de fond
    ecran.fill(bleu_clair) # Remplir l'écran avec notre couleur bleu_clair

    #    C'est ici qu'on dessinerait tous les éléments du jeu (pièces, grille, score...)
    #    Pour l'instant, on n'a rien d'autre à dessiner.

    # 10. Mettre à jour l'affichage complet de l'écran
    pygame.display.flip() # Ou pygame.display.update()

# 11. Quitter Pygame proprement (quand la boucle 'while' est terminée)
pygame.quit()
sys.exit() # Ferme le programme Python