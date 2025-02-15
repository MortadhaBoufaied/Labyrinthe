# design.py
import pygame

# Définir les couleurs
WHITE = (255, 255, 255)
GREY = (169, 169, 169)  # Gris pour les murs
BLACK = (0, 0, 0)  # Noir pour le joueur
RED = (255, 0, 0)  # Rouge pour le premier NPC
ORANGE = (255, 165, 0)  # Orange pour le deuxième NPC
YELLOW = (255, 255, 0)  # Jaune pour l'objectif

# Fonction pour dessiner la grille
def draw_grid(win):
    grid_size = 30  # Taille des cases de la grille
    for x in range(0, 600, grid_size):
        for y in range(0, 600, grid_size):
            rect = pygame.Rect(x, y, grid_size, grid_size)
            pygame.draw.rect(win, WHITE, rect, 1)  # Dessiner la grille en blanc

# Fonction pour dessiner le labyrinthe
def draw_maze(win, maze):
    grid_size = 30
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:  # Si la case est un mur
                rect = pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)
                pygame.draw.rect(win, GREY, rect)  # Dessiner un mur en gris
            elif cell == 0:  # Si la case est libre
                rect = pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)
                pygame.draw.rect(win, WHITE, rect)  # Dessiner une case libre en blanc

# Fonction pour dessiner un drapeau vert à une position fixe
def draw_green_flag(win):
    # Load flag image
    flag_image = pygame.image.load('./images/green_flag.png')

    # Scale the image to match the grid size (30x30 pixels)
    grid_size = 30
    flag_image = pygame.transform.scale(flag_image, (grid_size, grid_size))

    # Fixed flag position (adjust this to the grid position you want)
    flag_position = (19 * grid_size, 9 * grid_size)

    # Draw the flag at the position
    win.blit(flag_image, flag_position)
