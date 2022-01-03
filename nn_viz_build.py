import pygame

from nn_objects import Layers, Buttons, Neurons

BLACK = (31, 29, 36)
BLUE = (36, 64, 120)
ORANGE = (255, 165, 0)
PURPLE = (177, 156, 217)
GREY = (128, 128, 128)
LIGHT_GREY = (150, 150, 150)
WHITE = (255, 255, 255)
pygame.font.init()


class NNVizBuild:
    def __init__(self, nn=None):
        self.nn = nn
        self.width = 1600
        self.height = 990
        self.top_offset = 50
        self.left_offset = 50
        self.inner_width = 1390
        self.inner_height = 870
        self.win = pygame.display.set_mode((self.width, self.height))
        self.inner_win = (self.inner_width, self.inner_height)
        self.run = True

        self.layers = Layers(self.win, self.inner_width, self.inner_height, self.top_offset, self.left_offset)
        self.neurons = Neurons(self.win)
        self.buttons = Buttons(
            self.win, (self.left_offset + self.inner_width + 10, self.top_offset), (140, self.inner_height)
        )

        self.to_build_neuron = False
        self.to_build_layer = False
        self.num_layers = 2
        self.reset_counter = 0
        self.clicked_neuron = list()
        self.clicked_layer = list()
        # self.build_connection = False
        # self.selected_neurons =

    def run_viz(self):
        pygame.init()
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.win.fill(BLACK)

        while self.run:
            self.mouse_movements()
            if self.reset_counter == 100:
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
            if layer := self.get_clicked_layer():
                self.neurons.add_neuron(layer[0])
                self.reset_counter = 100
        elif event.key == pygame.K_DELETE and (self.clicked_neuron or self.clicked_layer):
            for neuron in self.clicked_neuron:
                self.neurons.neurons.remove(neuron)
                neuron.layer.neurons.remove(neuron)
                neuron.layer.update_neuron_row()
            self.clicked_neuron = list()

            for layer in filter(
                    lambda _layer: (_layer.layer_num != 1) and ( _layer.layer_num != len(self.layers.layers)),
                    self.clicked_layer):
                self.layers.layers.remove(layer)
                for neuron in layer.neurons:
                    self.neurons.neurons.remove(neuron)
                    neuron.layer.update_neuron_row()
            self.layers.update_layer_col()
            self.clicked_layer = list()

    def mouse_actions(self, event, mouse_pressed):
        if mouse_pressed[2]:
            print('all reset')
            self.reset_parameters()

        col, row = pygame.mouse.get_pos()
        self.click_neuron(col, row)
        self.click_layer(col, row)
        if self.to_build_neuron and mouse_pressed[0]:
            self.to_build_neuron = False

    def mouse_movements(self):
        col, row = pygame.mouse.get_pos()
        on_neuron = self.highlight_neuron(col, row)
        self.highlight_layer(col, row, on_neuron=on_neuron)

    def draw_board(self):
        self.draw_border()
        self.draw_background()
        self.draw_buttons()
        self.draw_layers()
        self.draw_neurons()

    def draw_layers(self):
        self.layers.draw()

    def draw_background(self):
        self.win.fill(BLACK)
        pygame.draw.rect(
            self.win, BLUE,
            [self.left_offset, self.top_offset, self.inner_width, self.inner_height]
        )

    def draw_buttons(self):
        self.buttons.draw()

    def draw_neurons(self):
        self.neurons.draw()

    def build_neuron(self):
        pass

    def build_layer(self):
        pass

    # ---------------------------------------- MISC functions ---------------------------------------------------------
    def click_neuron(self, col, row):
        closest_neuron = list(filter(lambda _neuron: _neuron.mouse_on_neuron(col, row), self.neurons.neurons))
        if not closest_neuron:
            return
        for neuron in filter(lambda _neuron: _neuron != closest_neuron[0], self.clicked_neuron):
            neuron.turn_off()
        for layer in self.clicked_layer:
            layer.turn_off()

        self.clicked_layer = list()
        closest_neuron[0].turn_on()
        self.clicked_neuron.append(closest_neuron[0])

    def click_layer(self, col, row):
        closest_layer = list(filter(lambda _layer: _layer.mouse_on_layer(col, row), self.layers.layers))
        if not closest_layer:
            return
        for layer in filter(lambda _layer: _layer != closest_layer[0], self.clicked_layer):
            layer.turn_off()
            self.clicked_layer.remove(layer)
        for neuron in self.clicked_neuron:
            neuron.turn_off()

        self.clicked_neuron = list()
        closest_layer[0].turn_on()
        self.clicked_layer.append(closest_layer[0])

    def highlight_neuron(self, col, row):
        closest_neuron = list(filter(lambda _neuron: _neuron.mouse_on_neuron(col, row), self.neurons.neurons))
        if closest_neuron:
            closest_neuron[0].on = True
            return True
        else:
            for neuron in filter(lambda _neuron: _neuron.on and not _neuron.clicked, self.neurons.neurons):
                neuron.on = False
                self.reset_counter = 100
            return False

    def highlight_layer(self, col, row, on_neuron=False):
        closest_layer = list(filter(lambda _layer: _layer.mouse_on_layer(col, row), self.layers.layers))
        if closest_layer and not on_neuron:
            closest_layer[0].on = True
        else:
            for layer in filter(lambda _layer: _layer.on and not _layer.clicked, self.layers.layers):
                self.reset_counter = 100
                layer.turn_off()

    def build_param_on_off(self, param):
        if param == 'neuron':
            self.to_build_neuron = not self.to_build_neuron
        elif param == 'layer':
            self.to_build_layer = not self.to_build_layer

    def reset_parameters(self):
        self.to_build_neuron = False
        self.to_build_layer = False
        for layer in self.layers.layers:
            layer.turn_off()
            layer.turn_off_neurons()
        # for neuron in self.neurons:
        #     neuron.on = False

    def any_activated_parameters(self):
        return any([self.to_build_neuron, self.to_build_layer])

    def draw_border(self):
        pygame.draw.line(self.win, WHITE, (self.inner_width, 0), (self.inner_width, self.inner_height))
        pygame.draw.line(self.win, WHITE, (0, self.inner_height), (self.inner_width, self.inner_height))

    def get_clicked_layer(self):
        return list(filter(lambda _layer: _layer.clicked, self.layers.layers))


if __name__ == '__main__':
    viz_build = NNVizBuild()
    viz_build.run_viz()
