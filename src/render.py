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


    def draw_grid(self, x: int, y: int) -> None:
        """
        Dessine la grille représentant la ville.
        """

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


    def draw_bus_stops(self, bus_stops) -> None:
        """
        Dessine les arrêts de bus sur la grille.
        :param bus_stops: Liste des coordonnées des arrêts de bus
        """
        for x, y in bus_stops:
            pygame.draw.rect(
                self.screen,
                (255, 0, 0),
                (x-11, y-11, 24, 24)
            )
            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                (x-6, y-6, 14, 14)
            )
    
    def draw_bus_path(self, bus_path) -> None:
        """
        Dessine le chemin du bus sur la grille.
        :param bus_stops: Liste des coordonnées de la ligne de bus
        """

        for i in range(len(bus_path) - 1):
            start_pos = (bus_path[i][0], bus_path[i][1])
            end_pos = (bus_path[i+1][0], bus_path[i+1][1])
            pygame.draw.line(self.screen, (255, 0, 0), start_pos, end_pos, 10)
        
        for x, y in bus_path:
            pygame.draw.rect(
                self.screen,
                (255, 0, 0),
                (x-4, y-4, 10, 10)
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
                pygame.draw.rect(self.screen, (200, 0, 0), (x-4, y-12, 10, 24))
                pygame.draw.rect(self.screen, glass_color, (x-3, y-11, 8, 4))

            elif bus.facing == "E":
                pygame.draw.rect(self.screen, (0, 0, 0), (x-13, y-5, 26, 12))
                pygame.draw.rect(self.screen, (200, 0, 0), (x-12, y-4, 24, 10))
                pygame.draw.rect(self.screen, glass_color, (x+8, y-3, 4, 8))

            elif bus.facing == "S":
                pygame.draw.rect(self.screen, (0, 0, 0), (x-5, y-13, 12, 26))
                pygame.draw.rect(self.screen, (200, 0, 0), (x-4, y-12, 10, 24))
                pygame.draw.rect(self.screen, glass_color, (x-3, y+8, 8, 4))

            elif bus.facing == "W":
                pygame.draw.rect(self.screen, (0, 0, 0), (x-13, y-5, 26, 12))
                pygame.draw.rect(self.screen, (200, 0, 0), (x-12, y-4, 24, 10))
                pygame.draw.rect(self.screen, glass_color, (x-11, y-3, 4, 8))
