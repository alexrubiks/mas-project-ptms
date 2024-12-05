import pygame
from src.render import Render
from src.agents import meta, bus_list, bus_lines, pedestrian_list
from src.pedestrian import Pedestrian

ROWS = 6
COLS = 6
CELL_SIZE = 100
SCREEN_WIDTH = COLS * CELL_SIZE + 360
SCREEN_HEIGHT = ROWS * CELL_SIZE + 60
FPS = 20


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
        render.draw_grid(30, 30, meta)
        for line in bus_lines:
            render.draw_bus_path(line)
            render.draw_bus_stops(line)
        render.draw_bus(bus_list)
        render.draw_time(meta)
        render.draw_pedestrian(pedestrian_list)
        for pede in pedestrian_list:
            render.draw_destination(pede.destination)
            render.draw_path_p(pede.path)

        # Actualisation de l'affichage
        pygame.display.flip()
        clock.tick(FPS)

        # Actions des agents
        for bus in bus_list:
            bus.behave()
        import time

        start_time = time.time()  # Enregistre l'heure de départ




        # for pedestrian in pedestrian_list:
        #     pedestrian.behave(meta.is_walk_area)

        from concurrent.futures import ThreadPoolExecutor

        def thread_target(pedestrian, is_walk_area_func):
            pedestrian.behave(is_walk_area_func)

        # Utiliser un pool de threads pour gérer les tâches
        with ThreadPoolExecutor(max_workers=10) as executor:
            for pedestrian in pedestrian_list:
                executor.submit(thread_target, pedestrian, meta.is_walk_area)





        end_time = time.time()  # Enregistre l'heure de fin
        print(f"Temps d'exécution : {end_time - start_time:.4f} secondes")
        meta.tick()

    pygame.quit()


if __name__ == "__main__":
    main()
