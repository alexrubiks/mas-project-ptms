import heapq
import math

class Pedestrian:
    def __init__(self, x, y, destination) -> None:
        # caracteristiques
        self.x = x
        self.y = y
        self.destination = destination
        self.speed = 0.5

        # trajet
        self.path = []
        self.todo = destination
        self.key_points = self.pedestrian_key_points()
        self.duration = None


    def behave(self, is_walk_area):
        if not self.path:
            self.path = self.find_path_to_destination(is_walk_area)
            self.todo = self.path.copy()
            self.duration = self.calculate_duration()
            print(self.duration)
        
        if not self.todo:
            return False

        left = self.speed
        
        while left > 0:
            if self.todo[0] == (self.x, self.y):
                self.todo.pop(0)
                if not self.todo:
                    return False

            target_x, target_y = self.todo[0]
            dx = target_x - self.x
            dy = target_y - self.y

            distance = (dx**2 + dy**2)**0.5

            if distance <= left:
                self.x = target_x
                self.y = target_y
                left -= distance
            else:
                ratio = left / distance
                self.x += ratio * dx
                self.y += ratio * dy
                left = 0
        return True
    

    def calculate_duration(self):
        if not self.path or len(self.path) < 2:
            return 0

        total_distance = 0

        for i in range(len(self.path) - 1):
            x1, y1 = self.path[i]
            x2, y2 = self.path[i + 1]
            total_distance += ((x2 - x1)**2 + (y2 - y1)**2)**0.5

        return int(total_distance / self.speed)


    def find_path_to_destination(self, is_walk_area):
        start = (self.x, self.y)
        end = self.destination

        key_start = self.find_closest_point(start)
        key_end = self.find_closest_point(end)

        path = self.shortest_path(key_start, key_end, is_walk_area)
        path = [start] + path + [end]
        path = self.optimize_ends(path, is_walk_area)
        
        return path
    

    def optimize_ends(self, path, is_walk_area):
        if len(path) > 2:
            if self.is_crossable(path[0], path[2], is_walk_area):
                path.pop(1)

        if len(path) > 2:
            if self.is_crossable(path[-1], path[-3], is_walk_area):
                path.pop(-2)

        return path
    
        
    def is_crossable(self, p1, p2, is_walk_area):
        return all(is_walk_area(p[0], p[1]) for p in self.get_points_between(p1, p2))
    

    def get_points_between(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        dx = (x2 - x1) / 14
        dy = (y2 - y1) / 14

        points = [(int(x1 + i * dx), int(y1 + i * dy)) for i in range(15)]
        return points


    def shortest_path(self, start, end, is_walk_area):

        # Fonction pour calculer la distance entre deux points
        def distance(p1, p2):
            return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
        
        def get_direction(p1, p2):
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            gcd = math.gcd(dx, dy)
            return dx // gcd, dy // gcd

        # Trouver tous les premiers points atteignables dans une direction
        def get_accessible_neighbors(point):
            neighbors = {}
            for candidate in self.key_points:
                if candidate == point:
                    continue

                direction = get_direction(point, candidate)

                # Si c'est le premier dans cette direction ou plus proche, l'ajouter
                if direction not in neighbors or distance(point, candidate) < distance(point, neighbors[direction]):
                    if self.is_crossable(point, candidate, is_walk_area):
                        neighbors[direction] = candidate
            return list(neighbors.values())

        # Initialisation de Dijkstra
        heap = []
        heapq.heappush(heap, (0, start))  # (coût accumulé, point courant)
        came_from = {start: None}  # Pour reconstruire le chemin
        cost_so_far = {start: 0}  # Coût total pour atteindre chaque point

        while heap:
            current_cost, current = heapq.heappop(heap)

            # Si nous atteignons la destination, arrêter la recherche
            if current == end:
                break

            # Trouver tous les voisins atteignables depuis le point courant
            neighbors = get_accessible_neighbors(current)
            for neighbor in neighbors:
                new_cost = current_cost + distance(current, neighbor)

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost
                    heapq.heappush(heap, (priority, neighbor))
                    came_from[neighbor] = current

        # Reconstruire le chemin si possible
        if end not in came_from:
            return None  # Pas de chemin trouvé

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path
        

    def find_closest_point(self, start):
        return min(self.key_points, key=lambda point: math.dist(start, point))
    

    def pedestrian_key_points(self):
        keys = []
        for i in range(6):
            for j in range(6):
                keys.append((30 + j*100 + 10, 30 + i*100 + 10))
                keys.append((30 + j*100 + 90, 30 + i*100 + 10))
                keys.append((30 + j*100 + 10, 30 + i*100 + 90))
                keys.append((30 + j*100 + 90, 30 + i*100 + 90))
        return keys
