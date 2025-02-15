import pygame
from design import draw_grid, draw_maze, draw_green_flag  
import heapq
import random
from map_expls import MapExamples
from pathfinding import Pathfinding

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de Labyrinthe avec NPCs")

# Paramètres de la grille
GRID_SIZE = 30
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREY = (169, 169, 169)

# Demander les choix de difficulté et de nombre de NPCs dans la console
def select_options():
    print("Sélectionner la difficulté du jeu :")
    mode = input("1. Facile\n2. Moyenne\n3. Difficile\nChoisissez une option (1, 2, 3): ")

    # Convertir la sélection de difficulté en texte
    if mode == '1':
        selected_mode = 'easy'
    elif mode == '2':
        selected_mode = 'medium'
    elif mode == '3':
        selected_mode = 'hard'
    else:
        print("Choix invalide, par défaut : Moyenne.")
        selected_mode = 'medium'

    print("\nSélectionner le nombre de NPCs :")
    npc_count = input("1. 1 NPC\n2. 2 NPCs\n0. Aucun\nChoisissez une option (1, 2, 0): ")

    # Convertir la sélection du nombre de NPCs en entier
    if npc_count in ['1', '2']:
        selected_npc_count = int(npc_count)
    else:
        selected_npc_count = 0

    return selected_mode, selected_npc_count

# Classe principale du jeu
class LabyrinthGame:
    def __init__(self):
        self.map_ex = MapExamples()
        self.selected_mode, self.selected_npc_count = select_options()
        self.map = self.map_ex.get_map(self.selected_mode)
        self.player_pos = (0, 10)  # The player starts at the entrance (you can keep this as is)
        # Initialize Pathfinding
        self.pathfinding = Pathfinding(self.map)
        # Set the goal position to (19, 9)
        self.goal_pos = (19, 9)

        self.npcs = self.create_npcs(self.selected_npc_count)
        self.clock = pygame.time.Clock()
        self.last_move_time = pygame.time.get_ticks()  # Time since the last NPC move

        # Set NPC move delay based on the difficulty
        if self.selected_mode == 'easy':
            self.npc_move_delay = 1000  # 3 seconds
        elif self.selected_mode == 'medium':
            self.npc_move_delay = 600  # 2 seconds
        else:
            self.npc_move_delay = 250  # 1 second

        self.game_start_time = pygame.time.get_ticks()  # Time when the game starts
        self.npc_start_delay = 3000  # 3 seconds delay for NPCs to start moving

    def get_worst_path(self, start, goal):
        # Use Pathfinding's dijkstra method
        all_paths = []
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == 0:  # Only valid positions
                    path = self.pathfinding.dijkstra(start, (x, y))
                    if path:
                        all_paths.append(path)
        all_paths.sort(key=len, reverse=True)  # Longest path first
        return all_paths[0] if all_paths else []

    def get_second_worst_path(self, start, goal):
        # Use Pathfinding's dijkstra method
        all_paths = []
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == 0:  # Only valid positions
                    path = self.pathfinding.dijkstra(start, (x, y))
                    if path:
                        all_paths.append(path)
        all_paths.sort(key=len, reverse=True)  # Longest path first
        return all_paths[1] if len(all_paths) > 1 else []

    def update_npc_positions(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.npc_move_delay:
            self.last_move_time = current_time
            for i in range(len(self.npcs)):
                npc = self.npcs[i]
                # Mettre à jour la position des NPCs
                path = self.pathfinding.dijkstra(npc, self.goal_pos)
                if path:
                    self.npcs[i] = path[0]

    def create_npcs(self, npc_count):
        npcs = []
        if self.selected_mode == 'easy':
            if npc_count >= 1:
                # First NPC takes the worst path
                worst_path = self.get_worst_path(self.player_pos, self.goal_pos)
                npcs.append(worst_path[0] if worst_path else self.player_pos)
            if npc_count == 2:
                # Second NPC takes the second worst path
                second_worst_path = self.get_second_worst_path(self.player_pos, self.goal_pos)
                npcs.append(second_worst_path[0] if second_worst_path else self.player_pos)
        else:
            for i in range(npc_count):
                npc_start = (random.randint(0, len(self.map[0])-1), random.randint(0, len(self.map)-1))
                npcs.append(npc_start)
        return npcs

    def handle_player_movement(self):
        keys = pygame.key.get_pressed()  # Check if any keys are pressed
        x, y = self.player_pos

        # Track if a move is made, so we only move once per key press
        move_made = False

        if keys[pygame.K_UP] and y > 0 and self.map[y - 1][x] == 0:
            self.player_pos = (x, y - 1)
            move_made = True
        elif keys[pygame.K_DOWN] and y < GRID_HEIGHT - 1 and self.map[y + 1][x] == 0:
            self.player_pos = (x, y + 1)
            move_made = True
        elif keys[pygame.K_LEFT] and x > 0 and self.map[y][x - 1] == 0:
            self.player_pos = (x - 1, y)
            move_made = True
        elif keys[pygame.K_RIGHT] and x < GRID_WIDTH - 1 and self.map[y][x + 1] == 0:
            self.player_pos = (x + 1, y)
            move_made = True

        # After the player moves, we want to ensure no other movement happens until the next key press
        if move_made:
            pygame.time.wait(120)  # Small delay to prevent rapid movement

    def show_start_screen(self):
        start_font = pygame.font.SysFont(None, 50)
        button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
        button_color = GREEN
        button_text = "Start"
        start = False

        while not start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        start = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        start = True

            win.fill(BLACK)
            pygame.draw.rect(win, button_color, button_rect)
            text_surface = start_font.render(button_text, True, BLACK)
            win.blit(text_surface, (button_rect.x + (button_rect.width - text_surface.get_width()) // 2,
                                    button_rect.y + (button_rect.height - text_surface.get_height()) // 2))
            pygame.display.update()

        self.show_countdown()

    def show_countdown(self):
        countdown_font = pygame.font.SysFont(None, 100)
        for count in range(3, 0, -1):
            win.fill(BLACK)
            text_surface = countdown_font.render(str(count), True, WHITE)
            win.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - text_surface.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(1000)


    def show_reload_button(self):
        # Draw the reload button
        button_width, button_height = 200, 50
        button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 50, button_width, button_height)
        button_color = GREEN
        button_text = "Rejouer"

        pygame.draw.rect(win, button_color, button_rect)
        font = pygame.font.SysFont(None, 40)
        text_surface = font.render(button_text, True, BLACK)
        win.blit(text_surface, (button_rect.x + (button_rect.width - text_surface.get_width()) // 2,
                                button_rect.y + (button_rect.height - text_surface.get_height()) // 2))
        return button_rect

    def draw(self):
        # Mise à jour de l'écran
        win.fill(BLACK)
        draw_grid(win)  # Draw the grid
        draw_maze(win, self.map)  # Draw the maze

        # Dessiner le joueur
        pygame.draw.rect(win, GREEN, pygame.Rect(self.player_pos[0] * GRID_SIZE, self.player_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Dessiner les NPCs
        for i, npc in enumerate(self.npcs):
            if i == 0:
                color = RED  # Premier NPC en rouge
            elif i == 1:
                color = (255, 165, 0)  # Deuxième NPC en orange
            else:
                color = YELLOW  # Les autres NPCs en jaune par défaut
            pygame.draw.rect(win, color, pygame.Rect(npc[0] * GRID_SIZE, npc[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Dessiner la position de l'objectif (utiliser draw_green_flag pour le but)
        draw_green_flag(win)  # Draw the green flag instead of the blue rectangle

        # Vérifier si tous les NPCs ont atteint le but
        all_npcs_reached_goal = all(npc == self.goal_pos for npc in self.npcs) and len(self.npcs) > 0

        # Afficher le message "Vous avez gagné !" si le joueur atteint l'objectif
        if self.player_pos == self.goal_pos:
            font = pygame.font.SysFont(None, 40)
            text = font.render("Vous avez gagné !", True, GREEN)
            win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
            self.reload_button = self.show_reload_button()  # Show reload button

        # Afficher le message "Vous avez perdu !" si tous les NPCs ont atteint l'objectif
        elif all_npcs_reached_goal:
            font = pygame.font.SysFont(None, 40)
            text = font.render("Vous avez perdu !", True, RED)
            win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
            self.reload_button = self.show_reload_button()  # Show reload button

        pygame.display.update()

    def run(self):
        self.show_start_screen()  # Show the start screen and countdown
        running = True
        self.reload_button = None  # Track reload button state

        while running:
            # Calculate elapsed time since game start
            elapsed_time = pygame.time.get_ticks() - self.game_start_time
            if elapsed_time >= self.npc_start_delay:  # Start NPCs after 3 seconds
                self.update_npc_positions()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.reload_button:
                    if self.reload_button.collidepoint(event.pos):
                        # Reload the game
                        self.__init__()  # Reinitialize the game instance
                        self.run()  # Restart the game
                        return

            self.handle_player_movement()  # Allow player movement
            self.draw()
            self.clock.tick(30)

        pygame.quit()

# Lancer le jeu
if __name__ == "__main__":
    game = LabyrinthGame()
    game.run()

