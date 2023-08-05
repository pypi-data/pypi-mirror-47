import pygame
from pyengine.Exceptions import NoObjectError
from pyengine.GameState import GameState
from pyengine.Utils import Color, Colors
from pygame import locals as const

__all__ = ["Window"]


class Window:
    def __init__(self, width, height, color=Colors.BLACK.value, icon=None, debug=False):
        if icon is not None:
            pygame.display.set_icon(pygame.image.load(icon))

        pygame.init()

        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.states = []
        self.current_state = None
        self.launch = True
        self.debug = debug
        self.color = color
        self.debugfont = pygame.font.SysFont("arial", 15)

        pygame.key.set_repeat(1, 1)

    @staticmethod
    def set_title(title):
        pygame.display.set_caption(title)

    @staticmethod
    def get_title():
        pygame.display.get_caption()

    def get_color(self):
        return self.color

    def set_color(self, color):
        if isinstance(color, Color):
            raise TypeError("Color have not a Color type")
        self.color = color

    def get_size(self):
        return [self.width, self.height]

    def get_debug(self):
        return self.debug

    def set_debug(self, debug):
        self.debug = debug

    def add_state(self, state):
        if not isinstance(state, GameState):
            raise TypeError("Argument is not type of "+str(GameState)+" but "+str(type(state))+".")
        if len(self.states) == 0:
            self.current_state = state
        state.set_window(self)
        self.states.append(state)

    def set_current_state(self, name):
        for i in self.states:
            if i.name == name:
                self.current_state = i

    def get_current_state(self):
        return self.current_state

    def get_state(self, name):
        for i in self.states:
            if i.name == name:
                return i

    def process_event(self, evt):
        if evt.type == const.QUIT:
            self.launch = False
        elif evt.type == const.KEYDOWN:
            self.current_state.keypress(evt)
        elif evt.type == const.MOUSEBUTTONDOWN:
            self.current_state.mousepress(evt)
        elif evt.type == const.KEYUP:
            self.current_state.keyup(evt)
        else:
            self.current_state.event(evt)

    def stop(self):
        self.launch = False

    def run(self):
        if len(self.states) == 0:
            raise NoObjectError("Window have any GameState")
        while self.launch:
            for event in pygame.event.get():
                self.process_event(event)

            self.screen.fill(self.color.get())
            self.clock.tick(60)

            self.current_state.run()

            pygame.display.update()
        pygame.quit()
