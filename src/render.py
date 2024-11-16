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
            start_pos = (x, y + row * self.cell_size)
            end_pos = (x + self.cols * self.cell_size, y + row * self.cell_size)
            pygame.draw.line(self.screen, (200, 200, 200), start_pos, end_pos)

        # Dessiner les lignes verticales
        for col in range(self.cols + 1):
            start_pos = (x + col * self.cell_size, y)
            end_pos = (x + col * self.cell_size, y + self.rows * self.cell_size)
            pygame.draw.line(self.screen, (200, 200, 200), start_pos, end_pos)
