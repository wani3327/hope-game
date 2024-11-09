import pygame
from pygame.locals import *
 
from mika import Mika
from bullet import Bullet
from hog import Hog
from constants import *
from collider import PartitionedSpace
from orb import ExpOrb

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

        # objects
        self._mika = Mika()
        self.space.add(self._mika.collider)
        self._mika2 = Mika()
        
        self.bullets: list[Bullet] = [] 
        self._hog_list: list[Hog] = []
        self._orb_list: list[ExpOrb] = []

        # misc
        pygame.time.set_timer(0, 1000) # Hog 생성
 
    def on_event(self, event): # 판정
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == 0:
            h = Hog(self._mika.collider.position)
            self._hog_list.append(h)
            self.space.add(h.collider)
            
    def on_loop(self): # 판정 결과 반영, 틱 이후 진행
        
        ## physics
        for b in self.bullets:
            got_hits = self.space.do_collide(b.collider)

            for c in got_hits:
                if type(c.object) is Hog:

                    if c.object.hit(100): # it died
                        # remove hog
                        self._hog_list.remove(c.object)
                        self.space.remove(c)

                        # drop orb
                        orb = ExpOrb(c.position, 3)
                        self._orb_list.append(orb)
                        self.space.add(orb.collider)
                        
        
        collides_with_mika = self.space.do_collide(self._mika.collider)
        for c in collides_with_mika:
            if type(c.object) is Hog:
                self._mika.hit(c.object.attack())

        ## updates
        ### mika
        min_distance = 999999
        closest_hog = None

        for h in self._hog_list:
            d = Vector2.magnitude(h.collider.position - self._mika.collider.position)
            if d < min_distance:
                min_distance = d
                closest_hog = h

        self._mika.update(self.bullets, self.space, closest_hog)
        print(len(self.bullets))
        ### bullet    
        to_die: list[Bullet] = []
        for b in self.bullets:
            b.update(self.space)

            if b.lifetime == 0:
                to_die.append(b)

        for d in to_die:
            self.bullets.remove(d)
            self.space.remove(d.collider)

        ### hogs
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
        [e.draw(self._display_surf, self._camera) for e in self._orb_list]
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