import pygame

BLACK = (31, 29, 36)
ORANGE = (255, 165, 0)
PURPLE = (177, 156, 217)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
pygame.font.init()


class Neuron:
    def __init__(self, layer, neuron_num):
        self.layer = layer
        self.layer_num = layer.layer_num
        self.neuron_num = neuron_num
        self.col = self.layer.col
        self.row = 0

    def draw(self, win):
        pygame.draw.line(win, ORANGE, (self.col - 10, self.row), (self.col + 10, self.row))


class Layer:
    def __init__(self, width, height, layer_num):
        self.width = width
        self.height = height
        self.starting_row = 100
        self.ending_row = self.height - 100
        self.layer_num = layer_num
        self.col = 0
        self.neurons = list()

    def draw(self, win):
        pygame.draw.line(win, PURPLE, (self.col, 0), (self.col, self.height))
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
            self.neurons[0].row = (self.ending_row + self.starting_row) / 2
        else:
            increment = (self.ending_row - self.starting_row) / (len(self.neurons) + 1)
            for neuron_index, neuron in enumerate(self.neurons):
                neuron.row = self.starting_row + (neuron_index + 1) * increment


class Layers:
    def __init__(self, width, height):
        self.layers = list()
        self.width = width
        self.height = height
        self.create_in_out_layer()

    def draw(self, win):
        for layer in self.layers:
            layer.draw(win)

    def add_layer(self):
        layer_num = len(self.layers[0:-1]) + 1
        self.layers = self.layers[0:-1] + [Layer(self.width, self.height, layer_num)] + [self.layers[-1]]
        self.layers[-1].layer_num = len(self.layers)
        self.update_layer_col()

    def update_layer_col(self):
        num_of_layers = len(self.layers)
        col = self.width / (num_of_layers + 1)
        for layer in self.layers:
            layer.col = layer.layer_num * col

    def create_in_out_layer(self):
        self.layers = [Layer(self.width, self.height, 1), Layer(self.width, self.height, 2)]
        self.update_layer_col()


class NNVizBuild:
    def __init__(self, nn=None):
        self.nn = nn
        self.width = 1600
        self.height = 990
        self.inner_width = 1390
        self.inner_height = 870
        self.win = pygame.display.set_mode((self.width, self.height))
        self.inner_win = (self.inner_width, self.inner_height)
        self.run = True

        self.layers = Layers(self.inner_width, self.inner_height)

        # self.layer_pos = dict()  # column numbers
        # self.neuron_pos = dict()  # column and row (col, row)
        self.to_build_neuron = False
        self.to_build_layer = False
        self.num_layers = 2
        self.reset_counter = 0
        # self.build_connection = False
        # self.selected_neurons =

    def run_viz(self):
        pygame.init()
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.win.fill(BLACK)

        while self.run:
            if self.reset_counter == 100:
                self.win.fill(BLACK)
                self.draw_board()
                self.reset_counter = 0
                pygame.display.update()
                continue
            else:
                self.reset_counter += 1
                self.draw_board()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                    elif event.type == pygame.KEYDOWN:
                        self.key_actions(event)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        left, mid, right = pygame.mouse.get_pressed()
                        self.mouse_actions(event, (left, mid, right))
            pygame.display.update()

    def key_actions(self, event):
        if event.key == pygame.K_q:
            self.run = False
            return

        if event.key == pygame.K_n:
            self.build_param_on_off('neuron')
        elif event.key == pygame.K_l:
            self.build_param_on_off('layer')
        elif event.key == pygame.K_c and self.to_build_layer:
            print('build new layer')
            self.layers.add_layer()
            self.reset_counter = 100
        elif event.key == pygame.K_c and self.to_build_neuron:
            print('build new neuron')
            layer = self.layers.layers[0]
            layer.add_neuron()
            self.reset_counter = 100

    def mouse_actions(self, event, mouse_pressed):

        if self.to_build_neuron and mouse_pressed[0]:
            self.to_build_neuron = False
        elif self.any_activated_parameters and mouse_pressed[2]:
            print('all reset')
            self.reset_parameters()

    def draw_board(self):
        self.draw_border()
        self.draw_layers()
        self.draw_neurons()

    def draw_layers(self):
        self.layers.draw(self.win)
        # self.layer_pos = dict()
        # div_size = self.inner_width / (self.num_layers + 1)
        # for col in range(1, self.num_layers + 1):
        #     self.layer_pos[col] = col * div_size
        #     self.draw_one_column(col)

    def draw_neurons(self):
        pass

    def build_neuron(self):
        closest_col = self.get_closest_layer()

    def build_layer(self):
        pass

    # ---------------------------------------- MISC functions ---------------------------------------------------------

    def build_param_on_off(self, param):
        if param == 'neuron':
            self.to_build_neuron = not self.to_build_neuron
        elif param == 'layer':
            self.to_build_layer = not self.to_build_layer

    def reset_parameters(self):
        self.to_build_neuron = False
        self.to_build_layer = False

    def any_activated_parameters(self):
        return any([self.to_build_neuron, self.to_build_layer])

    def draw_border(self):
        pygame.draw.line(self.win, WHITE, (self.inner_width, 0), (self.inner_width, self.inner_height))
        pygame.draw.line(self.win, WHITE, (0, self.inner_height), (self.inner_width, self.inner_height))

    def get_closest_layer(self):
        col, _ = pygame.mouse.get_pos()
        closest_col, _ = min(
            [(layer_col, abs(col - layer_width)) for layer_col, layer_width in self.layer_pos.items()],
            key=lambda x: x[1]
        )
        return closest_col


if __name__ == '__main__':
    viz_build = NNVizBuild()
    viz_build.run_viz()
