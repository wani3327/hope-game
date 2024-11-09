import pygame
from pygame.locals import *
 
import mika

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._mika = mika.Mika()
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        self._mika.update()

    def on_render(self):
        self._display_surf.fill((255, 255, 255))
        self._mika.draw(self._display_surf)
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