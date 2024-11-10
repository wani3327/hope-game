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
        return (int(vec.x) // 100, int(vec.y) // 100)

    def add(self, collider: Collider):
        key = self._find_key(collider.position)
        if key not in self.map:
            self.map[key] = []
        self.map[key].append(collider)

    def remove(self, collider: Collider):
        key = self._find_key(collider.position)
        self.map[key].remove(collider)
        if not self.map[key]:
            self.map.pop(key)

    def move(self, collider: Collider, new_position: Vector2):
        self.remove(collider)
        collider.position = new_position
        self.add(collider)

    def do_collide(self, collider: Collider) -> list[Collider]:
        key_x, key_y = self._find_key(collider.position)
        res = []

        for key in [(key_x - 1, key_y + 1), (key_x, key_y + 1), (key_x + 1, key_y + 1),
                    (key_x - 1, key_y),     (key_x, key_y),     (key_x + 1, key_y),
                    (key_x - 1, key_y - 1), (key_x, key_y - 1), (key_x + 1, key_y - 1)]:

            if key not in self.map:
                continue
            
            for c in self.map[key]:
                if collider.do_collide(c):
                    if c is collider:
                        continue

                    res.append(c)
                    return res
            
        return res


class CircleCollider(Collider):
    def __init__(self, object, position: Vector2, radius: float) -> None:
        super().__init__(object, position)
        self.radius = radius

    def do_collide(self, other: Collider) -> bool:
        if type(other) is CircleCollider:
            return self.position.distance_to(other.position) < self.radius + other.radius

        return False