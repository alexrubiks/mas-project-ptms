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
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
        ]
        self.vertical_roads = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
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