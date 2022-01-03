import pygame

BLACK = (31, 29, 36)
BLUE = (36, 64, 120)
ORANGE = (255, 165, 0)
PURPLE = (177, 156, 217)
DARK_GREY = (50, 50, 50)
GREY = (128, 128, 128)
LIGHT_GREY = (150, 150, 150)
WHITE = (255, 255, 255)


class Neuron:
    def __init__(self, layer, neuron_num):
        self.layer = layer
        self.layer_num = layer.layer_num
        self.neuron_num = neuron_num
        self.col = self.layer.col
        self.row = 0

    def draw(self, win):
        pygame.draw.line(win, ORANGE, (self.col - 10, self.row), (self.col + 10, self.row))


class Neurons:
    def __init__(self):
        self.neurons = list()


class Layer:
    def __init__(self, width, height, layer_num, top_offset, left_offset):
        self.width = width
        self.height = height
        self.top_offset = top_offset
        self.left_offset = left_offset
        self.starting_row = 100
        self.ending_row = self.height - 100
        self.neighbourhood = 30
        self.layer_num = layer_num
        self.col = 0
        self.neurons = list()
        self.on = False
        self.clicked = False

    def draw(self, win):
        if self.on:
            pygame.draw.line(
                win, PURPLE, (self.col, self.top_offset), (self.col, self.top_offset + self.height), width=5
            )
        else:
            pygame.draw.line(win, PURPLE, (self.col, self.top_offset), (self.col, self.top_offset + self.height))
        for neuron in self.neurons:
            neuron.draw(win)

    def add_neuron(self):
        print('new neuron')
        self.neurons.append(Neuron(self, len(self.neurons)))
        self.update_neuron_row()

    def update_neuron_row(self):
        if not self.neurons:
            return
        elif len(self.neurons) == 1:
            self.neurons[0].row = self.top_offset + (self.ending_row + self.starting_row) / 2
        else:
            increment = (self.ending_row - self.starting_row) / (len(self.neurons) + 1)
            for neuron_index, neuron in enumerate(self.neurons):
                neuron.row = self.top_offset + self.starting_row + (neuron_index + 1) * increment

    def mouse_on_layer(self, mouse_col, mouse_row):
        if (self.col - self.neighbourhood <= mouse_col) and (mouse_col <= self.col + self.neighbourhood) and \
                (self.top_offset <= mouse_row) and (mouse_row <= self.top_offset + self.height):
            return True
        return False


class Layers:
    def __init__(self, width, height, top_offset, left_offset):
        self.layers = list()
        self.width = width
        self.height = height
        self.top_offset = top_offset
        self.left_offset = left_offset
        self.create_in_out_layer()

    def draw(self, win):
        for layer in self.layers:
            layer.draw(win)

    def add_layer(self):
        layer_num = len(self.layers[0:-1]) + 1
        self.layers = self.layers[0:-1] + \
                      [Layer(self.width, self.height, layer_num, self.top_offset, self.left_offset)] + [self.layers[-1]]
        self.layers[-1].layer_num = len(self.layers)
        self.update_layer_col()

    def update_layer_col(self):
        num_of_layers = len(self.layers)
        col = self.width / (num_of_layers + 1)
        for layer in self.layers:
            layer.col = self.left_offset + layer.layer_num * col

    def create_in_out_layer(self):
        self.layers = [Layer(self.width, self.height, 1, self.top_offset, self.left_offset),
                       Layer(self.width, self.height, 2, self.top_offset, self.left_offset)]
        self.update_layer_col()


class Button:
    def __init__(self, init_col, width, height, text='test', mid=0, colour=GREY, highlight_colour=LIGHT_GREY):
        self.init_col = init_col
        self.mid = mid
        self.width = width
        self.height = height
        self.text = text
        self.colour = colour
        self.highlight_colour = highlight_colour
        self.border_colour = WHITE

    def draw(self, win):
        col, row = pygame.mouse.get_pos()
        if self.over_button(col, row):
            pygame.draw.rect(win, self.highlight_colour,
                             [self.init_col, self.mid - self.height / 2, self.width, self.height],
                             border_radius=3)
        else:
            pygame.draw.rect(win, self.colour, [self.init_col, self.mid - self.height / 2, self.width, self.height],
                             border_radius=3)

        pygame.draw.rect(win, self.border_colour, [self.init_col, self.mid - self.height / 2, self.width, self.height],
                         border_radius=3, width=4)

        self.write_text(win)

    def write_text(self, win):
        font1 = pygame.font.SysFont('chalkduster.ttf', 40)
        img1 = font1.render(self.text, True, BLUE)
        win.blit(img1, (self.init_col + (self.width - img1.get_size()[0]) / 2, self.mid - img1.get_size()[1] / 2))

    def over_button(self, col, row):
        return (self.init_col <= col) and (col <= self.init_col + self.width) and \
               (self.mid - self.height / 2 <= row) and (row <= self.mid + self.height / 2)


class Buttons:
    def __init__(self, win, init_pos, dim):
        self.win = win
        self.init_col = init_pos[0]
        self.init_row = init_pos[1]
        self.width = dim[0]
        self.height = dim[1]
        self.rect_dim = [self.init_col, self.init_row, self.width, self.height]
        self.button_height = 100

        self.buttons = list()
        self.init_buttons()

    def init_buttons(self):
        add_layer = Button(self.init_col, self.width, self.button_height, text='+ Layer')
        remove_layer = Button(self.init_col, self.width, self.button_height, text='- Layer')
        add_neuron = Button(self.init_col, self.width, self.button_height, text='+ Neuron')
        remove_neuron = Button(self.init_col, self.width, self.button_height, text='- Neuron')

        self.buttons = [add_layer, remove_layer, add_neuron, remove_neuron]
        self.update_buttons_mid()

    def add_buttons_border(self):
        pygame.draw.rect(self.win, WHITE, self.rect_dim, width=5, border_radius=2)

    def update_buttons_mid(self):
        if not self.buttons:
            return
        elif len(self.buttons) == 1:
            self.buttons[0].row = self.init_row + self.button_height / 2
        else:
            increment = self.height / (len(self.buttons) + 1)
            for button_index, button in enumerate(self.buttons):
                button.mid = self.init_row + (button_index + 1) * increment

    def draw(self):
        for button_index, button in enumerate(self.buttons):
            button.draw(self.win)
