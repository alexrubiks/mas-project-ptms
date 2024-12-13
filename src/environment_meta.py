import math

# meta

# pixel = 2.4 m

# vitesse pieton = ~4.5 km/h
#                = ~1.2 m/s
#                =  0.5 pixel/s

# vitesse max bus = 50 km/h
#                 = 14 m/s
#                 = 6 pixels/s

# distance bloc             = 240 m  = 3 min 20
# distance largeur          = 1440 m = ~20 min
# distance diagonale zigzag = 2640 m = ~35 min


class EnvironmentMeta:
    def __init__(self) -> None:
        # temps
        self.hours = 6
        self.minutes = 0
        self.seconds = 0

        # ville
        self.horizontal_roads = [
            [1, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
        ]
        self.vertical_roads = [
            [1, 1, 1, 1, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ]
        self.buildings = [
            [0, 1, 0, 0, 1, 1],
            [0, 1, 1, 1, 0, 0],
            [0, 1, 0, 1, 1, 0],
            [1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 0],
            [0, 1, 1, 0, 1, 1],
        ]

        self.walk_area = set()
        self.precalculate_walk_areas()

        # bus
        self.used_lines = []
        self.bus_numbers = {
            "A": 7,
            "B": 7,
            "C": 6,
            "D": 7,
            "E": 7,
        }


    def tick(self):
        self.seconds += 1

        if self.seconds == 60:
            self.minutes += 1
            self.seconds = 0
        
        if self.minutes == 60:
            self.hours += 1
            self.minutes = 0


    def precalculate_walk_areas(self):
        # Ajouter les zones marchables pour les routes horizontales
        for i, line in enumerate(self.horizontal_roads):
            for j, street in enumerate(line):
                if street:
                    left   = 30 + j*100 - 10
                    right  = 30 + (j+1)*100 + 10
                    top    = 30 + i*100 - 10
                    bottom = 30 + i*100 + 10
                    for x in range(left, right + 1):
                        for y in range(top, bottom + 1):
                            self.walk_area.add((x, y))

        # Ajouter les zones marchables pour les routes verticales
        for i, line in enumerate(self.vertical_roads):
            for j, street in enumerate(line):
                if street:
                    left   = 30 + j*100 - 10
                    right  = 30 + j*100 + 10
                    top    = 30 + i*100 - 10
                    bottom = 30 + (i+1)*100 + 10
                    for x in range(left, right + 1):
                        for y in range(top, bottom + 1):
                            self.walk_area.add((x, y))

        # Ajouter les jardins publics
        for i, line in enumerate(self.buildings):
            for j, bloc in enumerate(line):
                if not bloc:
                    left   = 30 + j*100 + 8
                    right  = 30 + (j+1)*100 - 8
                    top    = 30 + i*100 + 8
                    bottom = 30 + (i+1)*100 - 8
                    for x in range(left, right + 1):
                        for y in range(top, bottom + 1):
                            self.walk_area.add((x, y))

    
    def is_walk_area(self, x, y) -> bool:
        return (x, y) in self.walk_area
    

    def get_points_between(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        dx = (x2 - x1) / 29
        dy = (y2 - y1) / 29

        points = [(int(x1 + i * dx), int(y1 + i * dy)) for i in range(30)]
        return points


    def is_crossable(self, p1, p2):
        return all(self.is_walk_area(p[0], p[1]) for p in self.get_points_between(p1, p2))
    
    
    def pedestrian_graph(self):
        nodes = []
        for i in range(6):
            for j in range(6):
                nodes.append((30 + j*100 + 10, 30 + i*100 + 10))
                nodes.append((30 + j*100 + 90, 30 + i*100 + 10))
                nodes.append((30 + j*100 + 10, 30 + i*100 + 90))
                nodes.append((30 + j*100 + 90, 30 + i*100 + 90))

        graph = {}
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for i, node1 in enumerate(nodes):
            graph[node1] = {}
            for j, node2 in enumerate(nodes):
                if i == j:
                    continue
                for direction in directions:
                    if node2 == (node1[0] + direction[0]*20, node1[1] + direction[1]*20):
                        graph[node1][node2] = 20 * 2
                        continue
                    elif node2 == (node1[0] + direction[0]*80, node1[1] + direction[1]*80):
                        graph[node1][node2] = 80 * 2
                        continue
                if node1[0] != node2[0] and node1[1] != node2[1]:
                    if self.is_crossable(node1, node2):
                        graph[node1][node2] = math.dist(node1, node2) * 2
        
        return graph
        

    def add_bus_lines_to_graph(self, graph, bus_lines):
        for line in bus_lines:
            for stop in line.stops:
                if stop in graph:
                    continue
                graph[stop] = {}
                for node in graph:
                    if node == stop:
                        continue
                    if self.is_crossable(stop, node):
                        distance = math.dist(node, stop) * 2
                        graph[stop][node] = distance
                        graph[node][stop] = distance
            for i in range(len(line.stops)-1):
                graph[line.stops[i]][line.stops[i+1]] = line.costs[i]
                graph[line.stops[i+1]][line.stops[i]] = line.costs[i]

        return graph


    def add_ends_to_graph(self, graph, start, end):
        for new in [start, end]:
            graph[new] = {}
            for node in graph:
                if node == new:
                    continue
                if self.is_crossable(new, node):
                    distance = math.dist(node, new) * 2
                    graph[new][node] = distance
                    graph[node][new] = distance

        return graph
