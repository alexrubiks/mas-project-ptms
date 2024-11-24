# meta
# vitesse pieton = ~4.5 km/h = ~1.2 m/s = 0.5 pixel/s
# pixel = 2.4 m

# distance bloc             = 240 m  = 3 min 20
# distance largeur          = 1440 m = ~20 min
# distance diagonale zigzag = 2640 m = ~35 min


class EnvironmentMeta:
    def __init__(self) -> None:
        self.hours = 6
        self.minutes = 0
        self.seconds = 0

    def tick(self):
        self.seconds += 1

        if self.seconds == 60:
            self.minutes += 1
            self.seconds = 0
        
        if self.minutes == 60:
            self.hours += 1
            self.minutes = 0
