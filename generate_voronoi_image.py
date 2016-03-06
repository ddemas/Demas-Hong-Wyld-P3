from PIL import Image
import random
import math
import sys
import cv2

# Code from https://rosettacode.org/wiki/Voronoi_diagram

def generate_voronoi_diagram(fp):
    cuc_map_file = open(fp, "rb")
    cuc_map_orig = Image.open(cuc_map_file)
    cuc_map = Image.new("RGBA", (cuc_map_orig.width, cuc_map_orig.height))
    cuc_map.paste(cuc_map_orig)
    image = Image.new("RGBA", (cuc_map.width, cuc_map.height))
    num_cells = 6

    putpixel = image.putpixel
    imgx, imgy = image.size
    nx = [944, 1247, 903, 1005, 890,  834]
    ny = [683, 904,  931, 1061, 1143, 1518]
    weights = [1, 2, 2, 2, 2, 2]
    nr = [247, 255,  15,  255,  7,    108]
    ng = [222, 165,  184, 47,   31,   174]
    nb = [27,  0,    0,   5,    186,  245]

    for y in range(imgy):
        for x in range(imgx):
            dmin = math.hypot(imgx - 1, imgy - 1)
            j = -1
            for i in range(num_cells):
                d = math.hypot(nx[i] - x, ny[i] - y) / weights[i]
                if d < dmin:
                    dmin = d
                    j = i
            putpixel((x, y), (nr[j], ng[j], nb[j], 75))

    for i in range(num_cells):
        putpixel((nx[i], ny[i]), (0,0,0))

    new_image = Image.alpha_composite(cuc_map, image)
    new_image.save("7CVoronoiDiagram.png", "PNG")
    new_image.show()

if len(sys.argv) < 2:
    raise Exception("Please input an image file name")

fp = sys.argv[1]

generate_voronoi_diagram(fp)
