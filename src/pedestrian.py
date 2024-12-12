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
        self.waiting_for = None

        # trajet
        self.path = []
        self.todo = destination
        self.graph = graph
        self.theorical_duration = None
        self.real_duration = 0


    def behave(self, bus_list, is_bus_stop):
        self.real_duration += 1
        
        # calcul du trajet
        if not self.path:
            self.duration, self.path = self.find_path_to_destination((self.x, self.y), self.destination, self.graph)
            self.todo = self.path.copy()
        
        # chemin terminé
        if not self.todo:
            return False

        # prendre un bus
        if self.on_bus is not None:
            self.x = bus_list[self.on_bus].x
            self.y = bus_list[self.on_bus].y
            if self.todo[0] == (self.x, self.y):
                self.todo.pop(0)
                self.on_bus = None
            return True
        
        if self.waiting_for:
            for i, bus in enumerate(bus_list):
                if bus.line_name == self.waiting_for and (self.x, self.y) == (bus.x, bus.y) and self.todo[0] in bus.todo:
                    self.waiting_for = None
                    self.on_bus = i
            return True
        
        if self.todo[0] == (self.x, self.y):
            self.todo.pop(0)
            if not self.todo:
                return False
            if is_bus_stop((self.x, self.y)):
                return True

        current_pos = is_bus_stop((self.x, self.y))
        next_pos = is_bus_stop(self.todo[0])
        if current_pos and next_pos:
            if line := set(current_pos) & set(next_pos):
                if len(line) > 1:
                    raise Exception("au secours")
                self.waiting_for = list(line)[0]
                return True
        
        # se déplacer à pied
        left = self.speed
        
        while left > 0:
            if self.todo[0] == (self.x, self.y):
                self.todo.pop(0)
                if not self.todo:
                    return False
                if is_bus_stop((self.x, self.y)):
                    return True

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
