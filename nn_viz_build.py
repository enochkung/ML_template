import pygame

from nn_objects import Layers, Buttons

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

        self.layers = Layers(self.inner_width, self.inner_height, self.top_offset, self.left_offset)
        self.buttons = Buttons(
            self.win, (self.left_offset + self.inner_width + 10, self.top_offset), (140, self.inner_height)
        )

        self.to_build_neuron = False
        self.to_build_layer = False
        self.num_layers = 2
        self.reset_counter = 0
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
            layer = self.layers.layers[0]
            layer.add_neuron()
            self.reset_counter = 100

    def mouse_actions(self, event, mouse_pressed):
        if mouse_pressed[2]:
            print('all reset')
            self.reset_parameters()

        col, row = pygame.mouse.get_pos()
        self.click_layer(col, row)
        if self.to_build_neuron and mouse_pressed[0]:
            self.to_build_neuron = False

    def mouse_movements(self):
        col, row = pygame.mouse.get_pos()
        self.highlight_layer(col, row)

    def draw_board(self):
        self.draw_border()
        self.draw_background()
        self.draw_buttons()
        self.draw_layers()

    def draw_layers(self):
        self.layers.draw(self.win)

    def draw_background(self):
        self.win.fill(BLACK)
        pygame.draw.rect(
            self.win, BLUE,
            [self.left_offset, self.top_offset, self.inner_width, self.inner_height]
        )

    def draw_buttons(self):
        self.buttons.draw()

    def draw_neurons(self):
        pass

    def build_neuron(self):
        pass

    def build_layer(self):
        pass

    # ---------------------------------------- MISC functions ---------------------------------------------------------
    def click_layer(self, col, row):
        closest_layer = list(filter(lambda _layer: _layer.mouse_on_layer(col, row), self.layers.layers))
        if not closest_layer:
            return
        closest_layer[0].on = True
        closest_layer[0].clicked = True

    def highlight_layer(self, col, row):
        closest_layer = list(filter(lambda _layer: _layer.mouse_on_layer(col, row), self.layers.layers))
        if closest_layer:
            closest_layer[0].on = True
        else:
            for layer in filter(lambda _layer: _layer.on and not _layer.clicked, self.layers.layers):
                self.reset_counter = 100
                layer.on = False

    def build_param_on_off(self, param):
        if param == 'neuron':
            self.to_build_neuron = not self.to_build_neuron
        elif param == 'layer':
            self.to_build_layer = not self.to_build_layer

    def reset_parameters(self):
        self.to_build_neuron = False
        self.to_build_layer = False
        for layer in self.layers.layers:
            layer.on = False
            layer.clicked = False
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
