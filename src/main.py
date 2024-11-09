import pygame
from pygame.locals import *
 
from mika import Mika
from bullet import Bullet
from hog import Hog
from constants import *
import hog
from collider import PartitionedSpace

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
        self.space = PartitionedSpace()
        pygame.time.set_timer(0, 1000) # Hog 생성
 
    def on_event(self, event): # 판정
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == 0:
            h = hog.Hedgehog(self._mika.position)
            self._hog_list.append(h)
            self.space.add(h.collider)
            
    def on_loop(self): # 판정 결과 반영, 틱 이후 진행
        for b in self.bullets:
            got_hit = self.space.do_collide(b.collider)
            # print(got_hit)
            if got_hit != None:
                if type(got_hit.object) is hog.Hedgehog:
                    got_hit.object.hit(100)

        self._mika.update(self.bullets, self.space)
        [b.update(self.space) for b in self.bullets]
        self._camera = self._mika.position.copy()
        for i in self._hog_list:
            i.update(self.space)

        if pygame.key.get_pressed()[K_ESCAPE]:
            self._running = False

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