import pygame

BLACK = (31, 29, 36)
WHITE = (177, 156, 217)  # (255, 255, 255)
pygame.font.init()


class Neuron:
    pass


class Layer:
    pass


class NNVizBuild:
    def __init__(self, nn=None):
        self.nn = nn
        self.win = pygame.display.set_mode((500, 690))
        self.run = True
        self.layer_pos = []  # column numbers
        self.neuron_pos = []  # column and row (col, row)
        self.to_build_neuron = False
        self.to_build_layer = False
        # self.build_connection = False
        # self.selected_neurons =

    def run_viz(self):
        pygame.init()
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.win.fill(BLACK)

        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    self.key_actions(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    left, mid, right = pygame.mouse.get_pressed()
                    self.mouse_actions(event, (left, mid, right))

    def key_actions(self, event):
        if event.key == pygame.K_q:
            self.run = False
            return

        if event.key == pygame.K_n:
            self.build_neuron()
        elif event.key == pygame.K_l:
            self.build_layer()

    def mouse_actions(self, event, mouse_pressed):

        if self.to_build_neuron and mouse_pressed[0]:
            print('build neuron')
            self.to_build_neuron = False
        elif self.any_activated_parameters and mouse_pressed[2]:
            print('all reset')
            self.reset_parameters()

    def build_neuron(self):
        self.build_param_on_off('neuron')

    def build_layer(self):
        self.build_param_on_off('layer')

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


if __name__ == '__main__':
    viz_build = NNVizBuild()
    viz_build.run_viz()
