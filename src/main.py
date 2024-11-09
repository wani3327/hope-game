import pygame
from pygame.locals import *
 
from mika import Mika
from bullet import Bullet
from hog import Hog
from constants import *
from hog import Hog
from collider import PartitionedSpace

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = SCREEN_WIDTH, SCREEN_HEIGHT
 
    def on_init(self):
        pygame.init()
        # application
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        # game status
        self._camera = Vector2(0, 0)
        self.space = PartitionedSpace()
        self.current_level = 5

        # objects
        self._mika = Mika()
        self.space.add(self._mika.collider)
        self._mika2 = Mika()
        
        self.bullets: list[Bullet] = [] 
        self._hog_list: list[Hog] = []

        # misc
        pygame.time.set_timer(0, 500) # Hog 생성
 
    def on_event(self, event): # 판정
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == 0:
            h = Hog(self.current_level, self._mika.collider.position)
            self._hog_list.append(h)
            self.space.add(h.collider)
            
    def on_loop(self): # 판정 결과 반영, 틱 이후 진행
        
        ## physics
        for b in self.bullets:
            got_hits = self.space.do_collide(b.collider)
            # print(got_hit)
            for c in got_hits:
                if type(c.object) is Hog:
                    if c.object.hit(100): # it died
                        self._hog_list.remove(c.object)
                        self.space.remove(c)
        
        collides_with_mika = self.space.do_collide(self._mika.collider)
        for c in collides_with_mika:
            if type(c.object) is Hog:
                self._mika.hit(c.object.attack())

        ## updates
        min_distance = 999999
        closest_hog = None

        for h in self._hog_list:
            d = Vector2.magnitude(h.collider.position - self._mika.collider.position)
            if d < min_distance:
                min_distance = d
                closest_hog = h

        self._mika.update(self.bullets, self.space, closest_hog)
    
        [b.update(self.space) for b in self.bullets]
        [h.update(self.space) for h in self._hog_list]

        self._camera = self._mika.collider.position.copy() # camera follows plater.

        if pygame.key.get_pressed()[K_ESCAPE]: # game terminates
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