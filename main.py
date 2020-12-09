from PIL import Image, ImageDraw, ImageFilter
import random

import fit

test_image = "Mona_Lisa_head.png"
# test_image = "2x2dot.png"

Population_size = 10

class Polygon:
    def __init__(self, poly, color, size):
        self.poly = poly
        self.color = color
        self.size = size

    def __repr__(self):
        return "cordinates :  % s, " \
              "Color is % s" % (self.poly, self.color)

    def mutate(self):
        r = random.random()
        if r > 0.5:
            W, H = (self.size[0], self.size[1])
            O = 10
            index = random.randrange(0, len(self.poly))
            self.poly[index] = [random.randrange(0 - O, W + 10), random.randrange(0 - O, H + O)]

        else:
            temp = list(self.color)
            index = random.randrange(0, 4)
            temp[index] = random.randrange(0, 256)
            self.color = tuple(temp)




class Generator:
    def __init__(self, nr):
        self.nr = nr

    def generate_cordinates(self, image_shape):
        W, H = (image_shape[0], image_shape[1])
        O = 10
        self.cords = []
        for i in range(self.nr):
            cord = [random.randrange(0 - O, W + 10), random.randrange(0 - O, H + O)]
            self.cords.append(cord)

        # print("Cords : ", self.cords)
        return self.cords

    def generate_color(self):
        self.color = tuple(random.randrange(0, 255) for _ in range(0, self.nr))
        # print("color : ", self.color)
        return self.color




class Canvas:
    def __init__(self, population, image_shape):
        self.population = population
        self.shape = image_shape

    # def __repr__(self):
    #     return "\ncordinates :  % s, " \
    #           "Color is % s\n" % (self.poly, self.color)

    def draw_image(self, count, save = False, display = False):
        img = Image.new('RGB', self.shape, (0, 0, 0, 255))
        draw = Image.new('RGBA', self.shape)
        draw_polygon = ImageDraw.Draw(draw)

        for polygon in self.population:
            poly = tuple(tuple(sub) for sub in polygon.poly)
            color = tuple(polygon.color)
            draw_polygon.polygon(poly, fill = color, outline = color)
            img.paste(draw, mask = draw)

        if save == True:
            path = "generation_result/Gen_" + str(count) + ".png"
            img = img.filter(ImageFilter.GaussianBlur(radius=3))
            img.save(path)

        if display == True:
            img.show()

        return img

    def mutation(self):
        print("before : ", self.population)
        pop_idx = random.randrange(0, len(self.population))
        selected_polygon  = self.population[pop_idx]
        result = selected_polygon.mutate()
        print("result : ", result)
        print("after : ", self.population)
        return self.population


def init_population(pop_size, image_shape):
    population = []
    G = Generator(4)

    for i in range(pop_size):
        p = Polygon(G.generate_cordinates(image_shape), G.generate_color(), image_shape)
        population.append(p)

    return population

def main():
    # read the reference image and extract the shape of the image.
    Ref_img = Image.open(test_image)
    image_shape = Ref_img.size

    count = 0
    population = init_population(Population_size, image_shape)
    Parent = Canvas(population, image_shape)

    Parent_image = Parent.draw_image(count, save = True)
    # print("parent image : ", Parent_image)
    # print("reference image : ", Ref_img)
    Parent_fitness = fit.get_fitness(Parent_image, Ref_img, image_shape)

    while True:
        Child = Parent.mutation()


        break


if __name__ == '__main__':
    main()
