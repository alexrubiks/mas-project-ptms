import heapq
import math

from heapq import heappop, heappush


class Pedestrian:
    def __init__(self, x, y, destination) -> None:
        # caracteristiques
        self.x = x
        self.y = y
        self.destination = destination
        self.speed = 0.5
        self.path = []
        self.key_points = self.pedestrian_key_points()


    def behave(self, is_walk_area):
        if not self.path:
            self.path = self.find_path_to_destination(is_walk_area)


    def find_path_to_destination(self, is_walk_area):
        start = (self.x, self.y)
        end = self.destination

        key_start = self.find_closest_point(start)
        key_end = self.find_closest_point(end)

        path = self.shortest_path(key_start, key_end)
        path = self.optimize_path(path, is_walk_area)
        
        return [start] + path + [end]
    

    def optimize_path(self, path, is_walk_area):
        if len(path) <= 2:
            return path

        optimized_path = [path[0]]

        i = 0
        while i < len(path) - 2:
            if self.is_crossable(path[i], path[i + 2], is_walk_area):
                i += 1
            else:
                optimized_path.append(path[i + 1])
            i += 1

        optimized_path.append(path[-1])
        return optimized_path

        
    def is_crossable(self, p1, p2, is_walk_area):
        return all(is_walk_area(p[0], p[1]) for p in self.get_points_between(p1, p2))
    
    def get_points_between(self, p1, p2):
        if p1 == p2:
            return [p1]
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        x_step = dx / steps
        y_step = dy / steps
        return [(int(x1 + i * x_step), int(y1 + i * y_step)) for i in range(steps)]
    

    def shortest_path(self, start, end):
        """Trouver le chemin le plus court entre start et end en utilisant les points clés."""
        # Étape 1 : Ajouter les points de départ et d'arrivée à la liste des points clés
        graph = {point: self.find_neighbors(point, self.key_points) for point in self.key_points}
        
        # Dijkstra
        queue = [(0, start, [start])]  # (coût, point courant, chemin)
        visited = set()

        while queue:
            cost, current, path = heappop(queue)
            
            if current in visited:
                continue
            visited.add(current)

            if current == end:
                return path  # Chemin trouvé
            
            for neighbor in graph[current]:
                if neighbor not in visited:
                    heappush(queue, (cost + 1, neighbor, path + [neighbor]))
        
        raise Exception(f"Aucun chemin trouvé entre {start} et {end}.")


    def find_neighbors(self, point, key_points):
        """Trouver les voisins directs horizontalement ou verticalement."""
        neighbors = []
        for candidate in key_points:
            if candidate != point:
                if (point[0] == candidate[0] and abs(point[1] - candidate[1]) <= 100) or \
                   (point[1] == candidate[1] and abs(point[0] - candidate[0]) <= 100):
                    neighbors.append(candidate)
        return neighbors
    

    def find_closest_point(self, start):
        """Trouver le point le plus proche de start dans la liste des points clés."""
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
