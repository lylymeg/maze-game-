import pygame
import sys

pygame.init()

# Dimensions et grille
CELL_SIZE = 40
GRID_COLS, GRID_ROWS = 15, 13
WIDTH = GRID_COLS * CELL_SIZE
HEIGHT = GRID_ROWS * CELL_SIZE + 70  # Espace HUD
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Escape Light")
clock = pygame.time.Clock()

# Couleurs
DARK_BG = (20, 24, 33)
WALL_COLOR = (45, 55, 75)
PATH_COLOR = (30, 35, 45)
PLAYER_COLOR = (0, 255, 157)   # Vert néon
GOAL_COLOR = (255, 230, 0)     # Doré / Sortie
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Polices
font_large = pygame.font.SysFont("Arial", 42, bold=True)
font_medium = pygame.font.SysFont("Arial", 26, bold=True)
font_small = pygame.font.SysFont("Arial", 18)

# Définition d'un labyrinthe simple (0 = chemin, 1 = mur)
# 15 colonnes sur 13 lignes
MAZE_LAYOUT = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,1,1,1,1,0,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,1,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,1,1,1,1,0,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,1,1,0,1,1,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

def reset_game():
    return {
        "player_pos": [1, 1],  # [col, row]
        "goal_pos": [13, 11],  # [col, row]
        "steps": 0,
        "victory": False
    }

game = reset_game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game["victory"]:
                if event.key == pygame.K_SPACE:
                    game = reset_game()
            else:
                next_x, next_y = game["player_pos"]
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    next_y -= 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    next_y += 1
                elif event.key == pygame.K_LEFT or event.key == pygame.K_q:
                    next_x -= 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    next_x += 1

                # Vérifier les collisions avec les murs (1)
                if MAZE_LAYOUT[next_y][next_x] == 0:
                    game["player_pos"] = [next_x, next_y]
                    game["steps"] += 1

                    # Vérifier si on a atteint la sortie
                    if game["player_pos"] == game["goal_pos"]:
                        game["victory"] = True

    screen.fill(DARK_BG)

    # 1. Affichage du HUD en haut
    steps_txt = font_medium.render(f"Pas effectués : {game['steps']}", True, WHITE)
    screen.blit(steps_txt, (25, 20))

    # 2. Dessin du Labyrinthe
    grid_offset_y = 60
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE + grid_offset_y, CELL_SIZE, CELL_SIZE)
            if MAZE_LAYOUT[r][c] == 1:
                pygame.draw.rect(screen, WALL_COLOR, rect)
            else:
                pygame.draw.rect(screen, PATH_COLOR, rect)
                pygame.draw.rect(screen, (35, 40, 50), rect, 1) # Bordure légère

    # 3. Dessin de la Sortie (Objectif)
    gx, gy = game["goal_pos"]
    goal_rect = pygame.Rect(gx * CELL_SIZE + 6, gy * CELL_SIZE + grid_offset_y + 6, CELL_SIZE - 12, CELL_SIZE - 12)
    pygame.draw.rect(screen, GOAL_COLOR, goal_rect, border_radius=6)

    # 4. Dessin du Joueur
    px, py = game["player_pos"]
    player_rect = pygame.Rect(px * CELL_SIZE + 8, py * CELL_SIZE + grid_offset_y + 8, CELL_SIZE - 16, CELL_SIZE - 16)
    pygame.draw.ellipse(screen, PLAYER_COLOR, player_rect)

    # 5. Écran de Victoire
    if game["victory"]:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        win_title = font_large.render("SORTIE TROUVÉE !", True, PLAYER_COLOR)
        stats_txt = font_medium.render(f"Réussi en {game['steps']} pas", True, WHITE)
        restart_txt = font_small.render("Appuie sur ESPACE pour rejouer", True, GRAY)

        screen.blit(win_title, (WIDTH // 2 - win_title.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(stats_txt, (WIDTH // 2 - stats_txt.get_width() // 2, HEIGHT // 2 + 15))
        screen.blit(restart_txt, (WIDTH // 2 - restart_txt.get_width() // 2, HEIGHT // 2 + 65))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()