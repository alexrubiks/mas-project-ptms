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
        for co in path:
            pygame.draw.circle(self.screen, (0, 0, 0), co, 1)

    

    def draw_pedestrian(self, pedestrian_list):
        for pedestrian in pedestrian_list:
            pygame.draw.circle(self.screen, (0, 150, 0), (pedestrian.x, pedestrian.y), 4)


    def draw_time(self, time):
        font = pygame.font.Font(None, 74)
        text = font.render(str(time.hours).zfill(2) + ":" + str(time.minutes).zfill(2) + ":" + str(time.seconds).zfill(2), True, (0, 0, 0))

        self.screen.blit(text, (700, 100))
