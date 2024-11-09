import pygame
from pygame.locals import *
 
import mika
import hedgehog

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        
    def on_init(self): # 설정 초기화
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._mika = mika.Mika()
        self._hedgehog_list = []
        pygame.time.set_timer(0, 1000)
 
    def on_event(self, event): # 판정
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == 0:
            self._hedgehog_list.append(hedgehog.Hedgehog())
            
    def on_loop(self): # 판정 결과 반영, 틱 이후 진행
        self._mika.update()
        for i in self._hedgehog_list:
            i.update()

    def on_render(self): # 진행 렌더
        self._display_surf.fill((255, 255, 255))
        self._mika.draw(self._display_surf)
        for i in self._hedgehog_list:
            i.draw(self._display_surf)
        pygame.display.update()


    def on_cleanup(self): # self._running이 False가 되면 실행
        pygame.quit()
 
    def on_execute(self): # 메인 루프
        if self.on_init() == False:
            self._running = False
 
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()