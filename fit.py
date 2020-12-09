
from PIL import Image
import math

def get_fitness(img_1, img_2, img_size):
    fitness = 0.0
    for y in range(0, img_size[1]):
        for x in range(0, img_size[0]):
            r1, g1, b1 = img_1.getpixel((x, y))
            r2, g2, b2 = img_2.getpixel((x, y))
            # get delta per color
            d_r = r1 - r2
            d_b = b1 - b2
            d_g = g1 - g2
            # measure the distance between the colors in 3D space
            pixel_fitness = math.sqrt(d_r * d_r + d_g * d_g + d_b * d_b )
            # add the pixel fitness to the total fitness (lower is better)
            fitness += pixel_fitness

    # print("fitness : ", fitness )
    return fitness
