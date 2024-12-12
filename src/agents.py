from random import randint, seed

from .bus import Bus
from .busLine import BusLine
from .pedestrian import Pedestrian
from .environment_meta import EnvironmentMeta

### Meta ###

seed(1)
meta = EnvironmentMeta()

### Buses ###

A_line_stops = [(100, 30), (300, 30), (430, 100), (430, 200), (530, 260), (530, 500), (260, 530)]
A_line_path = [(100, 30), (430, 30), (430, 230), (530, 230), (530, 530), (260, 530)]
A_line_costs = [33, 33, 17, 27, 40, 50]
A_line_bus_color = (200, 0, 0)
A_line_path_color = (255, 0, 0)

B_line_stops = [(630, 80), (430, 200), (360, 230), (230, 280), (130, 360), (130, 500), (30, 600)]
B_line_path = [(630, 80), (630, 130), (430, 130), (430, 230), (230, 230), (230, 330), (130, 330), (130, 530), (130, 530), (30, 530), (30, 600)]
B_line_costs = [53, 17, 30, 17, 23, 33]
B_line_bus_color = (0, 0, 200)
B_line_path_color = (0, 0, 255)

C_line_stops = [(30, 160), (160, 230), (230, 280), (330, 360), (460, 430), (630, 500)]
C_line_path = [(30, 160), (30, 230), (230, 230), (230, 330), (330, 330), (330, 430), (630, 430), (630, 500)]
C_line_costs = [33, 20, 30, 33, 40]
C_line_bus_color = (250, 210, 50)
C_line_path_color = (255, 255, 0)

D_line_stops = [(360, 130), (200, 130), (130, 200), (130, 360), (230, 460), (260, 530), (360, 630), (560, 630)]
D_line_path = [(360, 130), (130, 130), (130, 430), (230, 430), (230, 530), (330, 530), (330, 630), (560, 630)]
D_line_costs = [27, 23, 27, 33, 17, 33, 33]
D_line_bus_color = (0, 200, 0)
D_line_path_color = (0, 255, 0)

E_line_stops = [(30, 360), (130, 500), (160, 630), (360, 630), (430, 560), (430, 360), (600, 330), (630, 200)]
E_line_path = [(30, 360), (30, 430), (130, 430), (130, 630), (430, 630), (430, 330), (630, 330), (630, 200)]
E_line_costs = [27, 33, 33, 23, 33, 27, 40]
E_line_bus_color = (170, 0, 170)
E_line_path_color = (200, 0, 200)


bus_lines = []

bus_lines.append(BusLine("A", A_line_path, A_line_stops, A_line_costs, A_line_path_color))
bus_lines.append(BusLine("B", B_line_path, B_line_stops, B_line_costs, B_line_path_color))
bus_lines.append(BusLine("C", C_line_path, C_line_stops, C_line_costs, C_line_path_color))
bus_lines.append(BusLine("D", D_line_path, D_line_stops, D_line_costs, D_line_path_color))
bus_lines.append(BusLine("E", E_line_path, E_line_stops, E_line_costs, E_line_path_color))


bus_list = []

def generate_bus(line_name, start=0):
    if line_name == "A":
        bus_list.append(Bus(A_line_stops, start, "A", A_line_bus_color))
    elif line_name == "B":
        bus_list.append(Bus(B_line_stops, start, "B", B_line_bus_color))
    elif line_name == "C":
        bus_list.append(Bus(C_line_stops, start, "C", C_line_bus_color))
    elif line_name == "D":
        bus_list.append(Bus(D_line_stops, start, "D", D_line_bus_color))
    elif line_name == "E":
        bus_list.append(Bus(E_line_stops, start, "E", E_line_bus_color))

def is_bus_stop(point):
    x, y = point
    lines = []
    for line in bus_lines:
        if (x, y) in line.stops:
            lines.append(line.name)

    return lines if lines else False

### Pedestrians ###

grid_graph = meta.pedestrian_graph()
pedestrian_list = []

def generate_pedestrian():
    while not meta.is_walk_area(x := randint(0, 700), y := randint(0, 700)):
        pass
    while not meta.is_walk_area(x_dest := randint(0, 700), y_dest := randint(0, 700)):
        pass
    p_graph = meta.add_bus_lines_to_graph(grid_graph, bus_lines)
    full_graph = meta.add_ends_to_graph(p_graph, (x, y), (x_dest, y_dest))
    pedestrian_list.append(Pedestrian(x, y, (x_dest, y_dest), full_graph))


### Events ###

events = {}
events[(6, 0, 0)] = [["pedestrian", 150]]

# ajout de piétons durant la journée
for h in range(6, 20):
    for m in range(0, 60):
        for s in range(0, 60, 10):
            if (h, m, s) != (6, 0, 0):
                events[(h, m, s)] = [["pedestrian", randint(1, 2)]]

# ligne A
for b in range(7):
    h, m = divmod(b*2, 60)
    if (key := (6+h, m, 0)) not in events:
        events[key] = [["bus", "A"]]
    else:
        events[key].append(["bus", "A"])

# ligne B
for b in range(7):
    h, m = divmod(b*2, 60)
    if (key := (6+h, m, 0)) not in events:
        events[key] = [["bus", "B"]]
    else:
        events[key].append(["bus", "B"])

# ligne C
for b in range(6):
    h, m = divmod(b*2, 60)
    if (key := (6+h, m, 0)) not in events:
        events[key] = [["bus", "C"]]
    else:
        events[key].append(["bus", "C"])

# ligne D
for b in range(7):
    h, m = divmod(b*2, 60)
    if (key := (6+h, m, 0)) not in events:
        events[key] = [["bus", "D"]]
    else:
        events[key].append(["bus", "D"])

# ligne E
for b in range(7):
    h, m = divmod(b*2, 60)
    if (key := (6+h, m, 0)) not in events:
        events[key] = [["bus", "E"]]
    else:
        events[key].append(["bus", "E"])


def event_checker():
    if (key := (meta.hours, meta.minutes, meta.seconds)) in events:
        for event in events[key]:
            if event[0] == "pedestrian":
                for _ in range(event[1]):
                    generate_pedestrian()
            elif event[0] == "bus":
                generate_bus(event[1])
