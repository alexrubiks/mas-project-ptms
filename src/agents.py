from random import randint, seed

from .bus import Bus
from .busLine import BusLine
from .pedestrian import Pedestrian
from .environment_meta import EnvironmentMeta

### Meta ###

meta = EnvironmentMeta()

### Buses ###

# A_line_stops = [(100, 30), (300, 30), (430, 100), (430, 200), (530, 260), (530, 500), (260, 530)]
# A_line_path = [(100, 30), (430, 30), (430, 230), (530, 230), (530, 530), (260, 530)]
# A_line_bus_color = (200, 0, 0)
# A_line_path_color = (255, 0, 0)

# B_line_stops = [(630, 80), (430, 200), (360, 230), (230, 280), (130, 360), (130, 500), (30, 600)]
# B_line_path = [(630, 80), (630, 130), (430, 130), (430, 230), (230, 230), (230, 330), (130, 330), (130, 530), (130, 530), (30, 530), (30, 600)]
# B_line_bus_color = (0, 0, 200)
# B_line_path_color = (0, 0, 255)

# C_line_stops = [(30, 160), (160, 230), (230, 280), (330, 360), (460, 430), (630, 500)]
# C_line_path = [(30, 160), (30, 230), (230, 230), (230, 330), (330, 330), (330, 430), (630, 430), (630, 500)]
# C_line_bus_color = (250, 210, 50)
# C_line_path_color = (255, 255, 0)

# D_line_stops = [(360, 130), (200, 130), (130, 200), (130, 360), (230, 460), (260, 530), (360, 630), (560, 630)]
# D_line_path = [(360, 130), (130, 130), (130, 430), (230, 430), (230, 530), (330, 530), (330, 630), (560, 630)]
# D_line_bus_color = (0, 200, 0)
# D_line_path_color = (0, 255, 0)

# E_line_stops = [(30, 360), (130, 500), (160, 630), (360, 630), (430, 560), (430, 360), (600, 330), (630, 200)]
# E_line_path = [(30, 360), (30, 430), (130, 430), (130, 630), (430, 630), (430, 330), (630, 330), (630, 200)]
# E_line_bus_color = (170, 0, 170)
# E_line_path_color = (200, 0, 200)

bus_lines = []
# bus_lines.append(BusLine("A", A_line_path, A_line_stops, A_line_path_color))
# bus_lines.append(BusLine("B", B_line_path, B_line_stops, B_line_path_color))
# bus_lines.append(BusLine("C", C_line_path, C_line_stops, C_line_path_color))
# bus_lines.append(BusLine("D", D_line_path, D_line_stops, D_line_path_color))
# bus_lines.append(BusLine("E", E_line_path, E_line_stops, E_line_path_color))


bus_list = []
# bus_list.append(Bus(A_line_stops, 0, A_line_bus_color))
# bus_list.append(Bus(A_line_stops, 3, A_line_bus_color))

# bus_list.append(Bus(B_line_stops, 0, B_line_bus_color))
# bus_list.append(Bus(B_line_stops, 2, B_line_bus_color))
# bus_list.append(Bus(B_line_stops, 5, B_line_bus_color))

# bus_list.append(Bus(C_line_stops, 0, C_line_bus_color))
# bus_list.append(Bus(C_line_stops, 1, C_line_bus_color))
# bus_list.append(Bus(C_line_stops, 4, C_line_bus_color))

# bus_list.append(Bus(D_line_stops, 1, D_line_bus_color))
# bus_list.append(Bus(D_line_stops, 2, D_line_bus_color))
# bus_list.append(Bus(D_line_stops, 6, D_line_bus_color))

# bus_list.append(Bus(E_line_stops, 3, E_line_bus_color))
# bus_list.append(Bus(E_line_stops, 4, E_line_bus_color))
# bus_list.append(Bus(E_line_stops, 7, E_line_bus_color))

### Pedestrians ###

pedestrian_graph = meta.pedestrian_graph()

pedestrian_list = []

seed(1)

def generate_pedestrian():
    while not meta.is_walk_area(x := randint(0, 700), y := randint(0, 700)):
        pass
    while not meta.is_walk_area(x_dest := randint(0, 700), y_dest := randint(0, 700)):
        pass
    pedestrian_list.append(Pedestrian(x, y, (x_dest, y_dest), pedestrian_graph))

events = {
    (6, 3, 0): "pedestrian",
    (6, 5, 0): "pedestrian",
    (6, 8, 0): "pedestrian",
    (6, 13, 0): "pedestrian",
    (6, 15, 0): "pedestrian",
    (6, 18, 0): "pedestrian",
    (6, 23, 0): "pedestrian",
    (6, 25, 0): "pedestrian",
    (6, 28, 0): "pedestrian",
    (6, 33, 0): "pedestrian",
    (6, 35, 0): "pedestrian",
    (6, 38, 0): "pedestrian",
}

def event_checker():
    if (meta.hours, meta.minutes, meta.seconds) == (6, 0, 0):
        for i in range(1):
            generate_pedestrian()

    if (meta.hours, meta.minutes, meta.seconds) in events:
        if events[(meta.hours, meta.minutes, meta.seconds)] == "pedestrian":
            generate_pedestrian()
