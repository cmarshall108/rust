
class GameObject(object):

    def __init__(self, id, surface):
        self.id = id
        self.parent = None
        self._surface = surface
        self._rect = None

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, surface):
        self._surface = surface
        self._rect = surface.get_rect()

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect):
        self._rect = rect

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, x):
        self.rect.x = x

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, y):
        self.rect.y = y

    @property
    def width(self):
        return self.rect.width

    @width.setter
    def width(self, width):
        self.surface = pygame.transform.scale(self._surface, (width, self._rect.height))

    @property
    def height(self):
        return self.rect.height

    @height.setter
    def height(self, height):
        self.surface = pygame.transform.scale(self._surface, (self._rect.width, height))

    def setup(self):
        pass

    def update(self):
        pass

    def destroy(self):
        pass

class GameObjectManager(object):

    def __init__(self):
        self.game_objects = {}

    def has_game_object(self, id):
        return id in self.game_objects

    def create(self, *args, **kwargs):
        game_object = GameObject(len(self.game_objects) + 1, *args, **kwargs)
        game_object.setup()

        self.add(game_object)

        return game_object

    def add(self, game_object):
        if self.has_game_object(game_object.id):
            return

        self.game_objects[game_object.id] = game_object

    def remove(self, game_object):
        if not self.has_game_object(game_object.id):
            return

        del self.game_objects[game_object.id]

    def get(self, id):
        if not self.has_game_object(id):
            return None

        return self.game_objects[id]

    def clear(self):
        self.game_objects = {}
