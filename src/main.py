import pygame
from pygame.locals import *

from mika import Mika
from bullet import *
from hog import Hog
from constants import *
from collider import PartitionedSpace
from orb import *

clock = pygame.time.Clock()

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
        self.hog_space = PartitionedSpace()
        self.orb_space = PartitionedSpace()

        # objects
        self._mika = Mika()
        # self._mika2 = Mika()
        
        self.bullets: set[Bullet] = set()
        self.lightnings: set[Lightning] = set()
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
        dying_lightning: set[Lightning] = set()
        
        ## physics
        for b in self.bullets:
            got_hit = self.hog_space.do_collide(b.collider)
            if got_hit != None and type(got_hit.object) is Hog:
                if got_hit.object.hit(b.damage): # it died
                    self._kill_hog(got_hit.object, b)
                dying_bullet.add(b)
                        
        for l in self.lightnings:
            if not l.used:
                got_hit = self.hog_space.do_collide(l.collider)
                if got_hit != None and type(got_hit.object) is Hog:
                    if got_hit.object.hit(l.damage): # it died
                        self._kill_hog(got_hit.object, None)
                    l.used = True
                            
        
        collides_with_mika = self.hog_space.do_collide(self._mika.collider)
        if collides_with_mika != None and type(collides_with_mika.object) is Hog:
            self._mika.hit(collides_with_mika.object.attack())

        collides_with_mika = self.orb_space.do_collide(self._mika.collider)
        if collides_with_mika != None and isinstance(collides_with_mika.object, Drop):
            if type(collides_with_mika.object) is ExpOrb:
                self._mika.try_level_up(collides_with_mika.object.value, self.orb_space, self._orb_list)
                self._kill_drop(collides_with_mika.object)

            elif type(collides_with_mika.object) is Item:
                self._mika.get_item(collides_with_mika.object)

                for i in collides_with_mika.object.friend:
                    self._kill_drop(i)


        ## updates
        ### mika
        self._mika.update(self.bullets, self.lightnings, self._hog_list)

        ### bullet    
        for b in self.bullets:
            b.update()
            if b.lifetime == 0:
                dying_bullet.add(b)
        
        for b in self.lightnings:
            b.update()
            if b.lifetime == 0:
                dying_lightning.add(b)

        ### orb
        dying_orb = set()
        for d in self._orb_list:
            d.lifetime -= 1
            if d.lifetime == 0:
                dying_orb.add(d)

        ### hogs
        [h.update(self._mika.collider.position, self.hog_space) for h in self._hog_list]


        ### handle corpse
        for d in dying_bullet:
            if type(d) is Fireball:
                c = CircleCollider(None, d.collider.position, 100)
                self.explosion_effects.append((d.collider.position, 60))

                for i in range(10): # this may be while true but lets be safe
                    in_explosion = self.hog_space.do_collide(c)

                    if in_explosion != None and type(in_explosion.object) is Hog:
                        if in_explosion.object.hit(11):
                            self._kill_hog(in_explosion.object, b)
                    else:
                        break

            self.bullets.remove(d)

        for d in dying_lightning:
            self.lightnings.remove(d)

        for d in dying_orb:
            self._kill_drop(d)

        self._camera = self._mika.collider.position.copy() # camera follows plater.

        if pygame.key.get_pressed()[K_ESCAPE]: # game terminates
            self._running = False

    def _kill_hog(self, hog: Hog, bullet: Bullet | None):
        # remove hog
        self._hog_list.remove(hog)
        self.hog_space.remove(hog.collider)

        # drop orb
        orb = ExpOrb(hog.collider.position, hog.image + 1)
        self._orb_list.add(orb)
        self.orb_space.add(orb.collider)

    def _kill_drop(self, drop: Drop):
        self._orb_list.remove(drop)
        self.orb_space.remove(drop.collider)

    def on_render(self): # 진행 렌더
        self._display_surf.fill((255, 255, 255))
        self._mika.draw(self._display_surf, self._camera)
        # self._mika2.draw(self._display_surf, self._camera)
        # print(len(self.bullets))
        [b.draw(self._display_surf, self._camera) for b in self.bullets]
        [l.draw(self._display_surf, self._camera) for l in self.lightnings]
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
            clock.tick(60)
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()