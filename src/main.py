import pygame
from pygame.locals import *
 
from mika import Mika
from bullet import Bullet
from hog import Hog
from constants import *

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = SCREEN_WIDTH, SCREEN_HEIGHT
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._camera = pygame.Rect(0, 0, 0, 0)
        self._mika = Mika()
        self._mika2 = Mika()
        self.bullets: list[Bullet] = [] 
        self._hog_list: list[Hog] = []
        pygame.time.set_timer(0, 1000) # Hog 생성
 
    def on_event(self, event): # 판정
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == 0:
            self._hog_list.append(Hog(self._mika.position))
        
        if event.type == 1:
            self.bullets.appdend()
            
    def on_loop(self): # 판정 결과 반영, 틱 이후 진행
        self._mika.update(self.bullets)
        [b.update() for b in self.bullets]
        [h.update() for h in self._hog_list]
        self._camera = self._mika.position.copy()

    def on_render(self): # 진행 렌더
        self._display_surf.fill((255, 255, 255))
        self._mika.draw(self._display_surf, self._camera)
        self._mika2.draw(self._display_surf, self._camera)
        # print(len(self.bullets))
        [b.draw(self._display_surf, self._camera) for b in self.bullets]
        [h.draw(self._display_surf, self._camera) for h in self._hog_list]
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