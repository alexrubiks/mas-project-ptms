import pygame
from concurrent.futures import ThreadPoolExecutor
from src.render import Render
from src.agents import meta, bus_list, bus_lines, pedestrian_list, event_checker, generate_pedestrian

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

    average_duration = None
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
        render.draw_duration(average_duration)
        render.draw_pedestrian(pedestrian_list)
        # for pedestrian in pedestrian_list:
        #     render.draw_path_p(pedestrian.path)
        #     render.draw_destination((pedestrian.destination[0], pedestrian.destination[1]))

        # Actualisation de l'affichage
        pygame.display.flip()
        clock.tick(FPS)

        # Actions des agents
        for bus in bus_list:
            bus.behave()
        import time

        start_time = time.time()  # Enregistre l'heure de départ
        event_checker()

        for pedestrian in pedestrian_list:
            if not pedestrian.behave():
                pedestrian_list.remove(pedestrian)

        # def thread_target(pedestrian):
        #     if not pedestrian.behave():
        #         pedestrian_list.remove(pedestrian)

        # with ThreadPoolExecutor(max_workers=10) as executor:
        #     for pedestrian in pedestrian_list:
        #         executor.submit(thread_target, pedestrian)

        end_time = time.time()  # Enregistre l'heure de fin
        if end_time - start_time > 0.05:
            print(f"Temps d'exécution : {end_time - start_time:.4f} secondes")

        # if average_duration is None:
        #     average_duration = int(sum([p.duration for p in pedestrian_list]) / len(pedestrian_list)) if pedestrian_list else 0
        meta.tick()

    pygame.quit()


if __name__ == "__main__":
    main()
