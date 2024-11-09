import pygame
from pygame.locals import *
 
import mika
from constants import *

class App:
    _instance = None

    @staticmethod
    def get_instance():
        if App._instance == None:
            App()
        else:
            return App._instance

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = SCREEN_WIDTH, SCREEN_HEIGHT
        App._instance = self
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._camera = pygame.Rect(0, 0, 0, 0)
        self._mika = mika.Mika()
        self._mika2 = mika.Mika()
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        self._mika.update()
        self._camera = self._mika.position

    def on_render(self):
        self._display_surf.fill((255, 255, 255))
        self._mika.draw(self._display_surf, self._camera)
        self._mika2.draw(self._display_surf, self._camera)
        pygame.display.update()


    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()