import pygame


class Render:
    def __init__(self, screen, rows: int, cols: int, cell_size: int) -> None:
        """
        Initialise le moteur de rendu.

        :param screen: écran Pygame
        :param rows: nombre de lignes
        :param cols: nombre de colonnes
        :param cell_size: taille de chaque cellule (en pixels)
        """
        self.screen = screen
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size


    def draw_grid(self, x: int, y: int, meta) -> None:
        """
        Dessine la grille représentant la ville.
        """

        # Dessiner les batiments/parcs
        for j, row in enumerate(meta.buildings):
            for i, buildings in enumerate(row):
                if buildings:
                    pygame.draw.rect(self.screen, (230, 230, 230), (x+100*i, y+100*j, 100, 100))
                else:
                    pygame.draw.rect(self.screen, (148, 255, 141), (x+100*i, y+100*j, 100, 100))

        # Dessiner les lignes horizontales
        for row in range(self.rows + 1):
            start_pos = (x-7, y + row * self.cell_size)
            end_pos = (x+8 + self.cols * self.cell_size, y + row * self.cell_size)
            pygame.draw.line(self.screen, (200, 200, 200), start_pos, end_pos, 16)

        # Dessiner les lignes verticales
        for col in range(self.cols + 1):
            start_pos = (x + col * self.cell_size, y)
            end_pos = (x + col * self.cell_size, y + self.rows * self.cell_size)
            pygame.draw.line(self.screen, (200, 200, 200), start_pos, end_pos, 16)

        # Dessiner les routes horizontales en travaux (pointillés rouges et blancs)
        for j, row in enumerate(meta.horizontal_roads):
            for i, road in enumerate(row):
                if road == 0:
                    road_x = x + 100 * i + 11
                    road_y = y + 100 * j
                    for k in range(0, 80, 10):
                        color = (255, 0, 0) if k % 20 == 0 else (255, 255, 255)
                        pygame.draw.line(self.screen, color, (road_x + k, road_y), (road_x + k + 10, road_y), 16)

        # Dessiner les routes verticales en travaux (pointillés rouges et blancs)
        for j, row in enumerate(meta.vertical_roads):
            for i, road in enumerate(row):
                if road == 0:
                    road_x = x + 100 * i
                    road_y = y + 100 * j + 11
                    for k in range(0, 80, 10):
                        color = (255, 0, 0) if k % 20 == 0 else (255, 255, 255)
                        pygame.draw.line(self.screen, color, (road_x, road_y + k), (road_x, road_y + k + 10), 16)


    def draw_bus_stops(self, line) -> None:
        """
        Dessine les arrêts de bus sur la grille.
        :param bus_stops: Liste des coordonnées des arrêts de bus
        """
        for x, y in line.stops:
            pygame.draw.rect(
                self.screen,
                (0, 0, 0),
                (x-11, y-11, 24, 24)
            )
            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                (x-7, y-7, 16, 16)
            )

    
    def draw_bus_path(self, line) -> None:
        """
        Dessine le chemin du bus sur la grille.
        :param bus_stops: Liste des coordonnées de la ligne de bus
        """

        shifts = {"A": -6, "B": -3, "C": 0, "D": 3, "E": 6}
        shift = shifts[line.name]

        for i in range(len(line.path) - 1):
            start_pos = (line.path[i][0] + shift, line.path[i][1] + shift)
            end_pos = (line.path[i+1][0] + shift, line.path[i+1][1] + shift)
            pygame.draw.line(self.screen, line.color, start_pos, end_pos, 7)
        
        for x, y in line.path:
            pygame.draw.rect(
                self.screen,
                line.color,
                (x - 2 + shift, y - 2 + shift, 5, 5)
            )

    def draw_bus_in_menu(self):
        glass_color = (0, 255, 255)
        bus_colors = [(200, 0, 0), (0, 0, 200), (250, 210, 50), (0, 200, 0), (170, 0, 170)]
        for i, color in enumerate(bus_colors):
            x = 860
            y = 72 + i * 80
            pygame.draw.rect(self.screen, (0, 0, 0), (x-5, y-13, 16, 32))
            pygame.draw.rect(self.screen, color, (x-4, y-12, 14, 30))
            pygame.draw.rect(self.screen, glass_color, (x-3, y-11, 12, 6))


    def draw_bus(self, bus_list):
        """
        Dessine les bus sur la carte.
        :param bus_list: Liste d'objets Bus à dessiner.
        """
        glass_color = (0, 255, 255)
        for bus in bus_list:
            x, y = bus.x, bus.y

            if bus.facing == "N":
                pygame.draw.rect(self.screen, (0, 0, 0), (x-5, y-13, 12, 26))
                pygame.draw.rect(self.screen, bus.color, (x-4, y-12, 10, 24))
                pygame.draw.rect(self.screen, glass_color, (x-3, y-11, 8, 4))

            elif bus.facing == "E":
                pygame.draw.rect(self.screen, (0, 0, 0), (x-13, y-5, 26, 12))
                pygame.draw.rect(self.screen, bus.color, (x-12, y-4, 24, 10))
                pygame.draw.rect(self.screen, glass_color, (x+8, y-3, 4, 8))

            elif bus.facing == "S":
                pygame.draw.rect(self.screen, (0, 0, 0), (x-5, y-13, 12, 26))
                pygame.draw.rect(self.screen, bus.color, (x-4, y-12, 10, 24))
                pygame.draw.rect(self.screen, glass_color, (x-3, y+8, 8, 4))

            elif bus.facing == "W":
                pygame.draw.rect(self.screen, (0, 0, 0), (x-13, y-5, 26, 12))
                pygame.draw.rect(self.screen, bus.color, (x-12, y-4, 24, 10))
                pygame.draw.rect(self.screen, glass_color, (x-11, y-3, 4, 8))
    

    def draw_destination(self, co):
        pygame.draw.circle(self.screen, (0, 255, 255), co, 4)
    
    
    def draw_path_p(self, path):
        for i in range(len(path) - 1):
            start_pos = (path[i][0], path[i][1])
            end_pos = (path[i+1][0], path[i+1][1])
            pygame.draw.line(self.screen, (0, 0, 0), start_pos, end_pos, 2)
            if i < len(path) - 2:
                pygame.draw.circle(self.screen, (0, 0, 0), end_pos, 4)

    
    def draw_pedestrian(self, pedestrian_list):
        for pedestrian in pedestrian_list:
            pygame.draw.circle(self.screen, (165, 42, 42), (pedestrian.x, pedestrian.y), 4)


    def draw_time(self, time):
        font = pygame.font.Font(None, 74)
        text = font.render(str(time.hours).zfill(2) + ":" + str(time.minutes).zfill(2) + ":" + str(time.seconds).zfill(2), True, (0, 0, 0))

        self.screen.blit(text, (700, 100))
    

    def draw_duration(self, duration):
        font = pygame.font.Font(None, 30)
        if duration is not None:
            hours, remainder = divmod(duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"
        else:
            time_str = "--:--:--"

        text = f"Temps de trajet moyen :\n{time_str}"
        self.render_multiline_text(self.screen, text, font, (0, 0, 0), 700, 300)


    def draw_pedestrian_number(self, n):
        font = pygame.font.Font(None, 25)
        text = f"Nombre actuel d'usagers :\n{n}"
        self.render_multiline_text(self.screen, text, font, (0, 0, 0), 700, 250)


    def render_multiline_text(self, surface, text, font, color, x, y, line_spacing=5):
        lines = text.split('\n')
        for i, line in enumerate(lines):
            rendered_line = font.render(line, True, color)
            surface.blit(rendered_line, (x, y + i * (rendered_line.get_height() + line_spacing)))


    def draw_time_chart(self, durations):
        if sum(durations) == 0:
            return

        interval = 5 * 60
        max_duration = max(durations)
        num_intervals = (max_duration // interval) + 1
        interval_counts = [0] * num_intervals

        for duration in durations:
            index = duration // interval
            interval_counts[index] += 1

        bar_width = 200 / len(interval_counts)
        chart_height = 100
        max_count = max(max(interval_counts), 1)

        for i, count in enumerate(interval_counts):
            bar_height = chart_height * (count / max_count)
            pygame.draw.rect(
                self.screen, 
                (200, 200, 200), 
                (705 + i * bar_width, 500 - bar_height, bar_width - 5, bar_height)
            )

        font = pygame.font.Font(None, 20)
        for i in range(len(interval_counts) + 1):
            text = font.render(f"{i * 5}", True, (0, 0, 0))
            self.screen.blit(text, (700 + i * bar_width, 510))
