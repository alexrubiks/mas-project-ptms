import heapq

class Bus:
    def __init__(self, x: int, y: int, stops) -> None:
        self.x = x
        self.y = y
        self.stops = stops
        self.next_stop = stops[0]
        self.path = None
        self.progress = 0
        self.remaining = len(stops)
        self.facing = "N"


    def make_progress(self, speed=1):
        if not self.path or self.next_stop == (self.x, self.y):
            self.progress += 1
            self.remaining -= 1
            if self.progress < len(self.stops):
                self.next_stop = self.stops[self.progress]
                self.path = self.find_path_to_next_stop(self.next_stop)
            else:
                self.path = None

        if self.path:
            target_x, target_y = self.path[0]
            dx = target_x - self.x
            dy = target_y - self.y

            if dx != 0:
                if dx > 0:
                    self.facing = "E"
                    self.x += speed
                else:
                    self.facing = "W"
                    self.x -= speed
            elif dy != 0:
                if dy > 0:
                    self.facing = "S"
                    self.y += speed
                else:
                    self.facing = "N"
                    self.y -= speed

            if (self.x, self.y) == (target_x, target_y):
                self.path.pop(0)

        if not self.path:
            print(f"Bus arrivé à l'arrêt : {self.next_stop}")


    def find_path_to_next_stop(self, next_stop, max_iterations=1000):
        """
        Trouve le chemin le plus court sur la grille de routes vers le prochain arrêt de bus
        avec un nombre maximal d'itérations pour l'exploration.
        :param next_stop: Le prochain arrêt (x, y) vers lequel le bus se dirige.
        :param max_iterations: Nombre maximal d'itérations pour explorer plus longtemps.
        :return: Liste de coordonnées représentant le chemin.
        """
        start = (self.x, self.y)
        goal = next_stop

        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.manhattan_distance(start, goal)}
        best_path = None
        best_path_cost = float("inf")
        iterations = 0
        
        while open_list and iterations < max_iterations:
            _, current = heapq.heappop(open_list)
            iterations += 1

            if current == goal:
                path = self.reconstruct_path(came_from, current)
                path_cost = len(path)

                if path_cost < best_path_cost:
                    best_path = path
                    best_path_cost = path_cost

            # Continuer à explorer les voisins
            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.manhattan_distance(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return best_path


    def manhattan_distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    def get_neighbors(self, position):
        """
        Retourne les voisins valides d'un point sur la grille.
        :param position: Position actuelle du bus (x, y).
        :return: Liste de voisins valides.
        """
        x, y = position
        roads = [30, 130, 230, 330, 430, 530, 630]
        neighbors = []

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx * 10, y + dy * 10
            
            if 30 <= nx <= 630 and 30 <= ny <= 630 and (nx in roads or ny in roads):
                neighbors.append((nx, ny))

        return neighbors
    

    def reconstruct_path(self, came_from, current):
        """
        Reconstruire le chemin en remontant à partir de l'objectif.
        :param came_from: Dictionnaire qui garde trace des chemins suivis.
        :param current: L'objectif (où le bus est actuellement).
        :return: Liste du chemin complet.
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path