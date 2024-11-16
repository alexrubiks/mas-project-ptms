import pygame
from src.render import Render

ROWS = 6
COLS = 6
CELL_SIZE = 100
SCREEN_WIDTH = COLS * CELL_SIZE + 360
SCREEN_HEIGHT = ROWS * CELL_SIZE + 60
FPS = 60


def main():
    # Initialisation de Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simulation de Mobilité Urbaine")
    clock = pygame.time.Clock()

    # Initialisation de la grille
    render = Render(screen, ROWS, COLS, CELL_SIZE)

    # Initialisation des arrêts de bus
    bus_stops = [(100, 30), (430, 100), (530, 260), (530, 500), (260, 530)]
    bus_path = [(100, 30), (430, 30), (430, 230), (530, 230), (530, 530), (260, 530)]
    # bus_lines = BusLine(path, stops)
    
    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        
        # Affichage des éléments à l'écran
        screen.fill((255, 255, 255))
        render.draw_grid(30, 30)
        render.draw_bus_path(bus_path)
        render.draw_bus_stops(bus_stops)


        # Actualisation de l'affichage
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
