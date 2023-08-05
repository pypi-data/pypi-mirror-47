import pygame
from pyengine.Widgets import Entry
from pyengine.Widgets.Widget import Widget

__all__ = ["UISystem"]


class UISystem:
    def __init__(self, state):
        self.state = state
        self.widgets = pygame.sprite.Group()
        self.focus = None

    def get_widget(self, identity):
        for i in self.widgets:
            if i.identity == identity:
                return i

    def add_widget(self, widget):
        if not isinstance(widget, Widget):
            raise TypeError("Argument is not type of "+str(Widget)+" but "+str(type(widget))+".")
        if len(self.widgets):
            widget.set_id(self.widgets.sprites()[-1].id + 1)
        else:
            widget.set_id(0)
        self.widgets.add(widget)
        widget.set_system(self)
        return widget

    def has_widget(self, widget):
        return widget in self.widgets

    def remove_widget(self, widget):
        if widget in self.widgets:
            self.widgets.remove(widget)
        else:
            raise ValueError("Entity has not in EntitySystem")

    def mousepress(self, evt):
        focustemp = None
        for i in self.widgets.sprites():
            if i.mousepress(evt):
                while i.parent is not None:
                    i = i.parent
                focustemp = i
                i.focusin()
            else:
                if self.focus == i:
                    self.focus.focusout()
        self.focus = focustemp

    def keypress(self, evt):
        for i in self.widgets.sprites():
            if isinstance(i, Entry):
                if self.focus == i:
                    i.keypress(evt)

    def keyup(self, evt):
        for i in self.widgets.sprites():
            if isinstance(i, Entry):
                if self.focus == i:
                    i.keyup(evt)

    def update(self):
        for i in self.widgets.sprites():
            if isinstance(i, Entry):
                i.update()

    def show(self, screen):
        for i in self.widgets.sprites():
            if i.isshow:
                screen.blit(i.image, i.rect)

    def show_debug(self, screen):
        for i in self.widgets:
            render = self.state.window.debugfont.render("ID : "+str(i.id), 1, (255, 255, 0))
            screen.blit(render, (i.rect.x + i.rect.width / 2 - render.get_width()/2, i.rect.y - 20))
