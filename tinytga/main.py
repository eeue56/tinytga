from __future__ import print_function, division

from io import open as op
from binascii import unhexlify
from struct import unpack, pack

class AlphaColor(object):

    def __init__(self, b=0, g=0, r=0, a=255):
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    def __str__(self):
        return 'AlphaColor(red={}, green={}, blue={}, alpha={})'.format(self.red, self.green, self.blue, self.alpha)

def to_raw_array(pixels):
    return [[p.red, p.green, p.blue] for p in chain.from_iterable(pixels)]
    

class TgaFile(object):

    def __init__(self, ident_size, colour_map_type, 
                 image_type, colour_map_start, colour_map_length, 
                 colour_map_bits, xstart, ystart, width, height, 
                 bits, descriptior):

        self.__dict__ = {k: (_bytes_to_int(v) if v != self else v) for k, v in locals().iteritems()}
        
        print(repr(width))

        self.pixels = [[0 for _ in xrange(self.width)] for _ in xrange(self.height)]

    def populate_pixels(self, file):

        bytes_to_read = self.bits / 8

        file.seek(18)
        n = 0

        for i, row in enumerate(self.pixels[:]):
            for j, column in enumerate(row):
                self.pixels[i][j] = (AlphaColor(
                    *(_bytes_to_int(x) for x in file.read(bytes_to_read))
                ))
            n += 1


    def average(self, pixels):
        d = tuple([
                sum(p.red for p in pixels if p is not None), 
                sum(p.blue for p in pixels if p is not None), 
                sum(p.green for p in pixels if p is not None)
            ])

        return tuple(x / len(pixels) for x in d)


    def redden(self, n=1):
        from random import randint

        for i, row in enumerate(self.pixels):
            for j, pixel in enumerate(row):
                if i + 3 >= len(self.pixels):
                    i -= 2
                if j + 3 >= len(row):
                    j -= 2

                for _ in xrange(n):
                
                    d = self.average(
                            (
                                self.pixels[i - 1][j],
                                self.pixels[i - 1][j + 1],
                                self.pixels[i - 1][j - 1],
                                self.pixels[i + 1][j],
                                self.pixels[i][j],
                                self.pixels[i][j],
                                self.pixels[i][j],
                                self.pixels[i][j],
                                self.pixels[i][j],
                                self.pixels[i + 1][j + 1],
                                self.pixels[i + 1][j - 1],
                                self.pixels[i][j - 1],
                                self.pixels[i][j + 1],
                        ))


                pixel.red = (d[0] + pixel.red) % 255
                pixel.green = (d[2] + pixel.green) % 255
                pixel.blue = (d[1] + pixel.blue) % 255



    def save_to_file(self, file_name):
        with open(file_name, 'wb') as f:
            f.write(chr(self.ident_size))
            f.write(chr(self.colour_map_type))
            f.write(chr(self.image_type))
            f.write(pack("h", self.colour_map_start))
            f.write(pack("h", self.colour_map_length))
            f.write(chr(self.colour_map_bits))
            f.write(pack("h", self.xstart))
            f.write(pack("h", self.ystart))
            f.write(pack("h", self.width)) 
            f.write(pack("h", self.height))
            f.write(chr(self.bits))
            f.write(chr(self.descriptior))

            
            for _ in xrange(20):
                self.redden()

            for row in self.pixels:
                for pixel in row:
                    f.write(chr(pixel.blue))
                    f.write(chr(pixel.green))
                    f.write(chr(pixel.red))
                #f.write(chr(pixel.alpha))

            

    def __str__(self):
        args = """ident_size, colour_map_type, 
                 image_type, colour_map_start, colour_map_length, 
                 colour_map_bits, xstart, ystart, width, height, 
                 bits, descriptior""".split(', ')
        return 'TgaFile({})'.format(
            ', '.join('{}={}'.format(k.strip(), (self.__dict__[k.strip()])) for k in args))

def _bytes_to_int(bytes):
    if len(bytes) < 2:
        return ord(bytes)
    return unpack('h', bytes)[0]

def _int_to_bytes(n):
    return hex(n)

def read_header(file):
    return TgaFile(
            file.read(1), # ident size
            file.read(1), # colour map type
            file.read(1), # image type
            file.read(2), # colour map start
            file.read(2), # colour map length
            file.read(1), # colour map bits
            file.read(2), # x start
            file.read(2), # y start
            file.read(2), # width
            file.read(2), # height
            file.read(1), # bits
            file.read(1)  # descriptor
        )
