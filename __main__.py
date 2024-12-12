import pygame
from src.render import Render
from src.agents import meta, bus_list, bus_lines, pedestrian_list, event_checker, is_bus_stop

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

    travel_durations = []
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
        render.draw_pedestrian_number(len(pedestrian_list))
        render.draw_time_chart(travel_durations)
        for pedestrian in pedestrian_list:
            render.draw_path_p(pedestrian.path)

        pygame.display.flip()
        clock.tick(FPS)
        
        if meta.hours == 7:
            import time
            time.sleep(10)

        # Actions des agents
        event_checker()

        for bus in bus_list:
            bus.behave()

        for pedestrian in pedestrian_list:
            if not pedestrian.behave(bus_list, is_bus_stop):
                travel_durations.append(pedestrian.real_duration)
                pedestrian_list.remove(pedestrian)
        
        if travel_durations:
            average_duration = int(sum(travel_durations) / len(travel_durations))
        meta.tick()

    pygame.quit()


if __name__ == "__main__":
    main()
