import heapq

class Bus:
    def __init__(self, stops, start_at, color) -> None:
        # caracteristiques
        self.x, self.y = stops[start_at]
        self.speed = 6

        # trajet
        self.todo = stops[start_at:]
        self.done = stops[:start_at]
        self.current_path = None
        self.wait = 0

        # Apparence
        self.facing = "N"
        self.color = color


    def behave(self):
        # Est en train d'attendre
        if self.wait > 0:
            self.wait -= 1
            return

        # Plus d'arrêts à faire
        if not self.todo:
            self.todo.extend(list(reversed(self.done)))
            self.done = []
            return
        
        next_stop = self.todo[0]
        
        # Arrivé à un arrêt
        if next_stop == (self.x, self.y):
            self.current_path = None
            self.done.append(self.todo.pop(0))
            self.wait = 20
            return

        # Calcul de destination
        if not self.current_path:
            self.current_path = self.find_path_to_next_stop()

        # En cours de trajet
        left = self.speed
        while left:
            if self.current_path[0] == (self.x, self.y):
                self.current_path.pop(0)
                if not self.current_path:
                    return

            target_x, target_y = self.current_path[0]
            dx = target_x - self.x
            dy = target_y - self.y

            if dx != 0:
                if dx > 0:
                    self.facing = "E"
                    self.x += min(left, dx)
                    left -= min(left, dx)

                else:
                    self.facing = "W"
                    self.x -= min(left, -dx)
                    left -= min(left, -dx)
            
            elif dy != 0:
                if dy > 0:
                    self.facing = "S"
                    self.y += min(left, dy)
                    left -= min(left, dy)

                else:
                    self.facing = "N"
                    self.y -= min(left, -dy)
                    left -= min(left, -dy)



    def find_path_to_next_stop(self, max_iterations=1000):
        """
        Trouve le chemin le plus court sur la grille de routes vers le prochain arrêt de bus
        avec un nombre maximal d'itérations pour l'exploration.
        :param next_stop: Le prochain arrêt (x, y) vers lequel le bus se dirige.
        :param max_iterations: Nombre maximal d'itérations pour explorer plus longtemps.
        :return: Liste de coordonnées représentant le chemin.
        """
        start = (self.x, self.y)
        goal = self.todo[0]

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