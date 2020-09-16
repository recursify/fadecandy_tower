import numpy
from PIL import Image


class RotateEffect(object):

    def __init__(self, config={}):
        self.config = config
        self.delay = config.get('delay', 0.1)
        self.img_path = config['img_path']
        self.rotation_degrees = 5
        self.with_distortion = config.get('with_distortion', False)
        self.angle = 0


    def initialize(self):
        img = Image.new(mode='RGB', size=(64, 64))
        img = Image.open(self.img_path)
        a = numpy.asarray(img).copy()
        self.img = Image.fromarray(a)
        self.i = 0
        self.angle = 0


    def run(self):
        if self.with_distortion:
            self.img = self.img.rotate(self.rotation_degrees, Image.BICUBIC)
            output = self.img
        else:
            output = self.img.rotate(self.angle % 360, Image.BICUBIC)
            self.angle += self.rotation_degrees

        # To debug what the pixels look like:
        #output.save(f'/tmp/output/frame_{self.i:03d}.png')

        # Only return a small slice of the original Image, since the
        # corners don't survive rotation
        canvas = numpy.asarray(output)[30:33]
        self.i += 1
        return (canvas, self.delay)
