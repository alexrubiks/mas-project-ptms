from .bus import Bus
from .busLine import BusLine

A_line_stops = [(100, 30), (300, 30), (430, 100), (430, 200), (530, 260), (530, 500), (260, 530)]
A_line_path = [(100, 30), (430, 30), (430, 230), (530, 230), (530, 530), (260, 530)]
A_line_bus_color = (200, 0, 0)
A_line_path_color = (255, 0, 0)

B_line_stops = [(630, 80), (430, 200), (360, 230), (230, 280), (130, 360), (130, 500), (30, 600)]
B_line_path = [(630, 80), (630, 130), (430, 130), (430, 230), (230, 230), (230, 330), (130, 330), (130, 530), (130, 530), (30, 530), (30, 600)]
B_line_bus_color = (0, 0, 200)
B_line_path_color = (0, 0, 255)

bus_lines = []
bus_lines.append(BusLine(A_line_path, A_line_stops, A_line_path_color))
bus_lines.append(BusLine(B_line_path, B_line_stops, B_line_path_color))


bus_list = []
bus_list.append(Bus(A_line_stops[0], A_line_stops, A_line_bus_color))
bus_list.append(Bus(A_line_stops[3], A_line_stops, A_line_bus_color))
bus_list.append(Bus(B_line_stops[0], B_line_stops, B_line_bus_color))