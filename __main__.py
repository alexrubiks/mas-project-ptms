import pygame
from src.bus import Bus
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

    bus_list = []
    bus_list.append(Bus(bus_stops[0][0], bus_stops[0][1], bus_stops))
    
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
        render.draw_bus(bus_list)

        # Actualisation de l'affichage
        pygame.display.flip()
        clock.tick(FPS)

        # Actions des agents
        for bus in bus_list:
            if bus.remaining:
                bus.make_progress(speed=1)

    pygame.quit()


if __name__ == "__main__":
    main()
