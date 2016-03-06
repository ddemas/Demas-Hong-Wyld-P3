from PIL import Image
import random
import math
import sys

class GenerateInput():
    def __init__(self, points, weights, metric, size, widget_width, widget_height):
        delta_x = (widget_width - size[0]) / 2
        delta_y = (widget_height - size[1]) / 2

        self.xs = [int(p[0] - delta_x) for p in points]
        self.ys = [int(p[1] - delta_y) for p in points]
        self.weights = [w + 0.001 for w in weights]
        self.metric = metric
        self.height = size[1]
        self.width = size[0]

def euclidean_metric(x, y, weight):
    return math.sqrt(x**2 + y**2) / weight

def manhattan_metric(x, y, weight):
    return (abs(x) + abs(y)) / weight

def inf_metric(x, y, weight):
    return max(abs(x),abs(y)) / weight

# Code from https://rosettacode.org/wiki/Voronoi_diagram

def generate_voronoi_diagram(fp, input):
    background_file = open(fp, "rb")
    background_orig = Image.open(background_file)
    background = Image.new("RGBA", (background_orig.width, background_orig.height))
    background.paste(background_orig)
    image = Image.new("RGBA", (background.width, background.height))
    num_cells = len(input.xs)

    x_scale = background.height / input.height
    y_scale = background.width / input.width

    putpixel = image.putpixel
    imgx, imgy = image.size
    nx = [x*x_scale for x in input.xs]
    ny = [(input.height - y)*y_scale for y in input.ys]
    weights = input.weights
    nr = []
    ng = []
    nb = []

    for i in range(num_cells):
        nr.append(random.randrange(256))
        ng.append(random.randrange(256))
        nb.append(random.randrange(256))
#
# nr = [247, 255,  15,  255,  7,    108]
#     ng = [222, 165,  184, 47,   31,   174]
#     nb = [27,  0,    0,   5,    186,  245]

    for y in range(imgy):
        for x in range(imgx):
            dmin = float('inf')
            j = -1
            for i in range(num_cells):
                d = input.metric(nx[i] - x, ny[i] - y, weights[i])
                if d < dmin:
                    dmin = d
                    j = i
            putpixel((x, y), (nr[j], ng[j], nb[j], 75))


    new_image = Image.alpha_composite(background, image)
    new_image.save("voronoi.png", "PNG")
    return "voronoi.png"
