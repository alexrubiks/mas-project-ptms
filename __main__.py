import pygame
from src.render import Render
from src.agents import bus_list, bus_lines

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

    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Affichage des éléments à l'écran
        screen.fill((255, 255, 255))
        render.draw_grid(30, 30)
        for line in bus_lines:
            render.draw_bus_path(line.path, line.color)
            render.draw_bus_stops(line.stops, line.color)
        render.draw_bus(bus_list)

        # Actualisation de l'affichage
        pygame.display.flip()
        clock.tick(FPS)

        # Actions des agents
        for bus in bus_list:
            bus.behave(speed=1)

    pygame.quit()


if __name__ == "__main__":
    main()
