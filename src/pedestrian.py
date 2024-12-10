import heapq
import math

class Pedestrian:
    def __init__(self, x, y, destination, graph) -> None:
        # caracteristiques
        self.x = x
        self.y = y
        self.destination = destination
        self.speed = 0.5

        # trajet
        self.path = []
        self.todo = destination
        self.graph = graph
        self.duration = None


    def behave(self, is_walk_area):
        if not self.path:
            self.duration, self.path = self.find_path_to_destination(is_walk_area)
            self.todo = self.path.copy()
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


    def find_path_to_destination(self, is_walk_area):
        start = (self.x, self.y)
        end = self.destination

        key_start = self.find_closest_point(start)
        key_end = self.find_closest_point(end)

        cost, path = self.shortest_path(key_start, key_end, self.graph)
        path = [start] + path + [end]
        cost += math.dist(start, path[1]) + math.dist(path[-2], end)
        cost, path = self.optimize_ends(path, cost, is_walk_area)
        
        return int(cost), path
    

    def optimize_ends(self, path, cost, is_walk_area):
        if len(path) > 2:
            if is_crossable(path[0], path[2]):
                cost -= math.dist(path[0], path[1]) + math.dist(path[1], path[2])
                path.pop(1)
                cost += math.dist(path[0], path[1])

        if len(path) > 2:
            if is_crossable(path[-1], path[-3]):
                cost -= math.dist(path[-1], path[-2]) + math.dist(path[-2], path[-3])
                path.pop(-2)
                cost += math.dist(path[-2], path[-1])

        return cost, path
    

    def shortest_path(self, start, end, graph):
        pq = [] # Priority Queue
        heapq.heappush(pq, (0, start))  # (coût, nœud)
        distances = {node: float('inf') for node in graph}  # Distance du nœud au start
        distances[start] = 0
        previous = {node: None for node in graph}  # Pour reconstruire le chemin
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_node == end:
                break

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        # Reconstituer le chemin
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()

        return distances[end], path # Retourne le coût et le chemin


    def find_closest_point(self, start):
        return min(self.graph, key=lambda p: math.dist(start, p))

