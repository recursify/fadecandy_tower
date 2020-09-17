import struct
import random

def make_fire_table(grad):
    table = []
    x = 0
    for i in range(len(grad) - 1):
        lo = grad[i]
        hi = grad[i+1]
        lo_color = lo[1]
        hi_color= hi[1]
        while x < hi[0]:
            pct = (x - lo[0])/(hi[0] - lo[0])
            color = (
                int(lo_color[0] + pct * (hi_color[0] - lo_color[0])),
                int(lo_color[1] + pct * (hi_color[1] - lo_color[1])),
                int(lo_color[2] + pct * (hi_color[2] - lo_color[2]))
            )
            table.append(color)
            x += 1
    return table


class FireEffect(object):
    """
    Inspired by: https://www.youtube.com/watch?v=_SzpMBOp1mE
    """

    def __init__(self, config):
        """
        config:  A dict containing these values:
          'delay': A delay, in s, between frame updates
          'reduction': On average, the value decrease of the flame intensity per pixel
          'gradient': A list of (flame_value, (r, g, b)) tuples mapping flame intensity, eg:
                [
                    (0, (0, 0, 0)),
                    (40, (200, 0, 0)),
                    (70, (200, 102, 0)),
                    (100, (255, 220, 90))
                ]

        """
        self.config = config
        self.delay = config['delay']
        self.reduction = config['reduction']
        self.gradient = config['gradient']

    def initialize(self):
        self.fire_table = make_fire_table(self.gradient)
        self.grid = [[0 for i in range(64)] for i in range(16)]

        # Initialize bottom row
        for i in range(len(self.grid)):
            self.grid[i][0] = 99 if random.random() > 0.5 else 0


    def run(self):
        grid = self.grid

        # randomly change a few of the base pixels
        for i in range(len(grid)):
            if random.random() > 0.9:
                # grid[i][0] = random.randint(0, 99)
                grid[i][0] = 0 if random.random() > 0.5 else 99


        # do the rest of the flames
        for i in range(1, len(grid) - 1):
            row = grid[i]
            for j in range(1, len(row)):
                a, b, c = (grid[i-1][j-1], grid[i][j-1], grid[i+1][j-1])
                v = int(max((a + b + c)/3.0 - self.reduction, 0))
                row[j] = v
                #print("i:%s j:%s    %s %s %s -> %s" % (i, j, a, b, c, row[j]))

        new_colors = [
            [self.fire_table[x] for x in grid[4]],
            [self.fire_table[x] for x in grid[5]],
            [self.fire_table[x] for x in grid[6]],
            [self.fire_table[x] for x in grid[7]],
            [self.fire_table[x] for x in grid[8]],
            [self.fire_table[x] for x in grid[9]],
            [self.fire_table[x] for x in grid[10]],
            [self.fire_table[x] for x in grid[11]]
        ]
        return (new_colors, self.delay)
