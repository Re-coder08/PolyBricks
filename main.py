from PIL import Image, ImageDraw, ImageFilter
import random
import copy
import fit

test_image = "Mona_Lisa_head.png"
# test_image = "2x2dot.png"

Population_size = 50

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

    def __repr__(self):
        return "\n Population  :  % s, " \
              "Image Shape is % s\n" % (self.population, self.shape)

    def draw_image(self, count, save = False, display = False):
        img = Image.new('RGB', self.shape, (0, 0, 0, 255))
        draw = Image.new('RGBA', self.shape)
        draw_polygon = ImageDraw.Draw(draw)

        for polygon in self.population:
            poly = tuple(tuple(sub) for sub in polygon.poly)
            color = tuple(polygon.color)
            draw_polygon.polygon(poly, fill = color, outline = color)
            img.paste(draw, mask = draw)


        if display == True:
            img.show()

        if save == True:
            path = "generation_result/Gen_" + str(count) + ".png"
            img = img.filter(ImageFilter.GaussianBlur(radius=1))
            img.save(path)



        return img

    def mutation(self):
        new_population =copy.deepcopy(self.population)
        pop_idx = random.randrange(0, len(new_population))
        selected_polygon  = new_population[pop_idx]
        selected_polygon.mutate()

        return Canvas(new_population, self.shape)


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
    # print("parent : ", Parent)
    Parent_image = Parent.draw_image(count, save = True, display = False)
    # print("parent image : ", Parent_image)
    # print("reference image : ", Ref_img)
    Parent_fitness = fit.get_fitness(Parent_image, Ref_img, image_shape)


    while True:
        count += 1
        Child = Parent.mutation()
        # print("child : ", Child)
        Child_image = Child.draw_image(count, display = False)
        Child_fitness = fit.get_fitness(Child_image, Ref_img, image_shape)


        if Child_fitness < Parent_fitness:
            print("parent fitness : ", Parent_fitness)
            print("Child fitness : ", Child_fitness)
            Parent = Child
            Parent_image = Child_image
            Parent_fitness = Child_fitness
            print("New parent has been updated with best fitness of : ", Child_fitness)

        if count % 100 == 0:
            print("Saving Generation : ", count)
            Parent.draw_image(count, save = True, display = False)
        # break

if __name__ == '__main__':
    main()
