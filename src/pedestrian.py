import heapq
import math

class Pedestrian:
    def __init__(self, x, y, destination, graph) -> None:
        # caracteristiques
        self.x = x
        self.y = y
        self.destination = destination
        self.speed = 0.5
        self.on_bus = None

        # trajet
        self.path = []
        self.todo = destination
        self.graph = graph
        self.duration = None


    def behave(self):
        if not self.path:
            self.duration, self.path = self.find_path_to_destination((self.x, self.y), self.destination, self.graph)
            self.todo = self.path.copy()
        
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


    def find_path_to_destination(self, start, end, graph):
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

        return int(distances[end]), path # Retourne le coût et le chemin
