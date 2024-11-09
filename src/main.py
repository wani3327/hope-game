import pygame
from pygame.locals import *

from mika import Mika
from bullet import *
from hog import Hog
from constants import *
from collider import PartitionedSpace
from orb import *

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
        # self.space = PartitionedSpace()
        self.hog_space = PartitionedSpace()
        self.orb_space = PartitionedSpace()

        # objects
        self._mika = Mika()
        # self.hog_space.add(self._mika.collider)
        # self.orb_space.add(self._mika.collider)
        self._mika2 = Mika()
        
        self.bullets: set[Bullet] = set() 
        self._hog_list: set[Hog] = set()
        self._orb_list: set[Drop] = set()

        self.explosion_effects: list[(Vector2, int)] = []

        # misc
        pygame.time.set_timer(0, 500) # Hog 생성
 
    def on_event(self, event): # 판정
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == 0:
            h = Hog(self._mika.current_level, self._mika.collider.position)
            self._hog_list.add(h)
            self.hog_space.add(h.collider)
            
    def on_loop(self): # 판정 결과 반영, 틱 이후 진행
        dying_bullet: set[Bullet] = set()
        ## physics
        for b in self.bullets:
            got_hits = self.hog_space.do_collide(b.collider)

            for c in got_hits:
                if type(c.object) is Hog:
                    if c.object.hit(100): # it died
                        self._kill_hog(c.object, b, dying_bullet)
                        
        
        collides_with_mika = self.hog_space.do_collide(self._mika.collider)
        for c in collides_with_mika:
            if type(c.object) is Hog:
                self._mika.hit(c.object.attack())

        collides_with_mika = self.orb_space.do_collide(self._mika.collider)
        for c in collides_with_mika:
            if isinstance(c.object, Drop):
                if type(c.object) is ExpOrb:
                    self._mika.try_level_up(c.object.value, self.orb_space, self._orb_list)

                elif type(c.object) is Item:
                    self._mika.get_item(c.object)

                self._orb_list.remove(c.object)
                self.orb_space.remove(c)

        ## updates
        ### mika
        min_distance = 999999
        closest_hog = None

        for h in self._hog_list:
            d = Vector2.magnitude(h.collider.position - self._mika.collider.position)
            if d < min_distance:
                min_distance = d
                closest_hog = h

        self._mika.update(self.bullets, closest_hog)

        ### bullet    
        for b in self.bullets:
            b.update()

            if b.lifetime == 0:
                dying_bullet.add(b)

        ### hogs
        [h.update(self._mika.collider.position, self.hog_space) for h in self._hog_list]


        ### handle corpse
        for d in dying_bullet:
            if type(d) is Fireball:
                c = CircleCollider(None, d.collider.position, 100)
                in_explosion = self.hog_space.do_collide(c)
                self.explosion_effects.append((d.collider.position, 60))

                for entity in in_explosion:
                    if type(entity.object) is Hog:
                        if entity.object.hit(11):
                            self._kill_hog(entity.object, b, None)


            self.bullets.remove(d)
            # self.space.remove(d.collider)


        self._camera = self._mika.collider.position.copy() # camera follows plater.

        if pygame.key.get_pressed()[K_ESCAPE]: # game terminates
            self._running = False

    def _kill_hog(self, hog: Hog, bullet: Bullet, dying_bullet: set[Bullet] | None):
        # remove hog
        self._hog_list.remove(hog)
        self.hog_space.remove(hog.collider)

        if dying_bullet != None:
            dying_bullet.add(bullet)

        # drop orb
        orb = ExpOrb(hog.collider.position, 3)
        self._orb_list.add(orb)
        self.orb_space.add(orb.collider)


    def on_render(self): # 진행 렌더
        self._display_surf.fill((255, 255, 255))
        self._mika.draw(self._display_surf, self._camera)
        self._mika2.draw(self._display_surf, self._camera)
        # print(len(self.bullets))
        [b.draw(self._display_surf, self._camera) for b in self.bullets]
        [h.draw(self._display_surf, self._camera) for h in self._hog_list]
        [e.draw(self._display_surf, self._camera) for e in self._orb_list]

        ne = []
        for pos, time in self.explosion_effects:
            if time != 0:
                ne.append((pos, time - 1))
            pygame.draw.circle(
                self._display_surf, 
                (255, 0, 0), 
                pos - self._mika.collider.position + SCREEN_CENTER, 
                100)
        self.explosion_effects = ne

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