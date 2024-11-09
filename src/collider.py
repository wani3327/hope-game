from pygame.math import Vector2

class Collider:
    def __init__(self, object, position: Vector2) -> None:
        self.object = object
        self.position = position

    def do_collide(self, collider) -> bool:
        pass

class PartitionedSpace:
    def __init__(self) -> None:
        self.map: dict[tuple[int, int], list[Collider]] = dict()

    @staticmethod
    def _find_key(vec: Vector2):
        return (int(vec.x) // 1000, int(vec.y) // 1000)

    def add(self, collider: Collider):
        key = self._find_key(collider.position)
        if key not in self.map:
            self.map[key] = []
        self.map[key].append(collider)

    def remove(self, collider: Collider):
        key = self._find_key(collider.position)
        self.map[key].remove(collider)

    def move(self, collider: Collider, new_position: Vector2):
        self.remove(collider)
        collider.position = new_position
        self.add(collider)

    def do_collide(self, collider: Collider) -> Collider | None:
        key = self._find_key(collider.position)
        if key not in self.map:
            return None
        for c in self.map[key]:
            if collider.do_collide(c):
                if c is collider:
                    continue

                return c
            
        return None


class CircleCollider(Collider):
    def __init__(self, object, position: Vector2, radius: float) -> None:
        super().__init__(object, position)
        self.radius = radius

    def do_collide(self, other: Collider) -> bool:
        if type(other) is CircleCollider:
            return self.position.distance_to(other.position) < self.radius + other.radius

        return False