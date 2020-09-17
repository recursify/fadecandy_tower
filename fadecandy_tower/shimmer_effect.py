import random


class ShimmerEffect(object):

    def __init__(self, config):
        self.delay = config.get('delay', 0.7)
        self.base_value = 96
        self.offset_range = (-80, 48)


    def initialize(self):
        pass

    def run(self):
        output = []
        for i in range(8):
            row = []
            for j in range(64):
                v = self.base_value + random.randint(*self.offset_range)
                row.append((v, v, v))
            output.append(row)
        return (output, self.delay)
