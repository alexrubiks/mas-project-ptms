import pygame
from src.bus import Bus
from src.render import Render
from src.agents import meta, bus_list, bus_lines, pedestrian_list, event_checker, is_bus_stop, generate_events

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

    # Menu de sélection des options
    start_button = pygame.Rect(SCREEN_WIDTH - 260, 520, 230, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH - 260, 580, 230, 50)

    meta.used_lines = bus_lines.copy()
    bus_line_buttons = []
    for i, line in enumerate(bus_lines):
        bus_line_buttons.append(pygame.Rect(SCREEN_WIDTH - 280, 40 + i * 80, 70, 70))

    def draw_menu():
        font = pygame.font.Font(None, 28)
        pygame.draw.rect(screen, (0, 220, 0), start_button)
        pygame.draw.rect(screen, (220, 0, 0), quit_button)
        screen.blit(font.render("Lancer la simulation", True, (255, 255, 255)), (SCREEN_WIDTH - 245, 535))
        screen.blit(font.render("Quitter la simulation", True, (255, 255, 255)), (SCREEN_WIDTH - 245, 595))

        font = pygame.font.Font(None, 70)
        for i, line in enumerate(bus_lines):
            pygame.draw.rect(screen, line.color, bus_line_buttons[i])
            screen.blit(font.render(f"{line.name}", True, (255, 255, 255)), (SCREEN_WIDTH - 263, 52 + i * 80))
            
            # ajouter des fleches cliquables pour indiquer le nombre de bus sur la ligne, avec le nombre au centre (un peu comme les boutons de volume)
            left_arrow = pygame.Rect(SCREEN_WIDTH - 190, 50 + i * 80, 30, 50)
            right_arrow = pygame.Rect(SCREEN_WIDTH - 70, 50 + i * 80, 30, 50)
            render.draw_bus_in_menu()
            pygame.draw.polygon(screen, (0, 0, 0), [(SCREEN_WIDTH - 185, 75 + i * 80), (SCREEN_WIDTH - 165, 55 + i * 80), (SCREEN_WIDTH - 165, 95 + i * 80)])
            pygame.draw.polygon(screen, (0, 0, 0), [(SCREEN_WIDTH - 45, 75 + i * 80), (SCREEN_WIDTH - 65, 55 + i * 80), (SCREEN_WIDTH - 65, 95 + i * 80)])
            screen.blit(font.render(f"{meta.bus_numbers[line.name]}", True, (0, 0, 0)), (SCREEN_WIDTH - 140, 52 + i * 80))
            if left_arrow.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and meta.bus_numbers[line.name] > 0:
                meta.bus_numbers[line.name] -= 1

            if right_arrow.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and meta.bus_numbers[line.name] < 9:
                meta.bus_numbers[line.name] += 1
            
            if meta.bus_numbers[line.name] == 0:
                meta.used_lines.remove(line)
            else:
                if line not in meta.used_lines:
                    meta.used_lines.append(line)

            if line not in meta.used_lines:
                pygame.draw.line(screen, (0, 0, 0), (SCREEN_WIDTH - 280, 40 + i * 80), (SCREEN_WIDTH - 210, 110 + i * 80), 10)
                pygame.draw.line(screen, (0, 0, 0), (SCREEN_WIDTH - 280, 110 + i * 80), (SCREEN_WIDTH - 210, 40 + i * 80), 10)
            

    simulation_started = False

    while not simulation_started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                if start_button.collidepoint(event.pos):
                    simulation_started = True
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    return
                elif any(button.collidepoint(event.pos) for button in bus_line_buttons):
                    for i, button in enumerate(bus_line_buttons):
                        if button.collidepoint(event.pos):
                            if bus_lines[i] in meta.used_lines:
                                meta.used_lines.remove(bus_lines[i])
                            else:
                                meta.used_lines.append(bus_lines[i])

        screen.fill((255, 255, 255))
        render.draw_grid(30, 30, meta)
        draw_menu()
        for line in meta.used_lines:
            render.draw_bus_path(line)
            render.draw_bus_stops(line)
        pygame.display.flip()
        clock.tick(FPS)

    generate_events()
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
        for line in meta.used_lines:
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
