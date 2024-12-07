import heapq
import math


class Pedestrian:
    def __init__(self, x, y, destination) -> None:
        # caracteristiques
        self.x = x
        self.y = y
        self.destination = destination
        self.speed = 0.5
        self.path = []

    def behave(self, is_walk_area):
        if not self.path:
            self.path = self.find_path_to_destination(is_walk_area)
        self.move()


    def find_path_to_destination(self, is_walk_area):
        """Calcule le chemin le plus rapide jusqu'à la destination, y compris les déplacements diagonaux."""
        start = (self.x, self.y)
        goal = self.destination

        def heuristic(a, b):
            # Heuristique : distance euclidienne
            return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

        def neighbors(pos):
            # Retourne les voisins possibles, y compris les déplacements diagonaux
            x, y = pos
            return [
                (x + dx, y + dy) 
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1),  # Horizontal/Vertical
                               (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal
            ]

        # A* Algorithm
        open_set = []
        heapq.heappush(open_set, (0, start))  # (coût estimé, position)
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                # Reconstruction du chemin
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for neighbor in neighbors(current):
                if not is_walk_area(neighbor[0], neighbor[1]):
                    continue

                # Calcul du coût pour atteindre ce voisin
                dx = abs(neighbor[0] - current[0])
                dy = abs(neighbor[1] - current[1])
                move_cost = math.sqrt(dx**2 + dy**2)  # 1 pour orthogonal, sqrt(2) pour diagonal
                tentative_g_score = g_score[current] + move_cost

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None  # Pas de chemin trouvé

    def move(self):
        if self.path:
            self.x, self.y = self.path.pop(0)
        else:
            self.x, self.y = self.destination
