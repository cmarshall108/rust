import pygame

class GameObject(object):

    def __init__(self, id=None, surface=None):
        self.id = id
        self.parent = None
        self._surface = surface
        self._rect = surface.get_rect() if surface else None

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
    def xy(self):
        return (self._x, self._y)

    @xy.setter
    def xy(self, xy):
        self.x, self.y = xy

    @property
    def center(self):
        return self.rect.center

    @center.setter
    def center(self, center):
        self.rect.center = center

    @property
    def centerx(self):
        return self.rect.centerx

    @centerx.setter
    def centerx(self, centerx):
        self.rect.centerx = centerx

    @property
    def centery(self):
        return self.rect.centery

    @centery.setter
    def centery(self, centery):
        self.rect.centery = centery

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

    @property
    def size(self):
        return (self.rect.width, self.rect.height)

    @size.setter
    def size(self, size):
        self.width, self.height = size

    def setup(self):
        pass

    def update(self):
        pass

    def destroy(self):
        pass

class GameObjectManager(object):

    def __init__(self, engine):
        self.engine = engine
        self.game_objects = {}

    @property
    def id(self):
        return len(self.game_objects) + 1

    def has_game_object(self, id):
        return id in self.game_objects

    def get_game_objects(self):
        return self.game_objects.values()

    def setup(self):
        self.update_task = self.engine.task_manager.add(self.update)

    def update(self, task):
        for game_object in self.get_game_objects():
            game_object.update()

        return task.cont

    def create(self, *args, **kwargs):
        game_object = GameObject(self.id, *args, **kwargs)
        game_object.setup()

        self.add(game_object)

        return game_object

    def create_with(self, class_object, *args, **kwargs):
        game_object = class_object(self.id, *args, **kwargs)
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

    def destroy(self):
        self.engine.task_manager.remove(self.update_task)

        for game_object in self.get_game_objects():
            game_object.destroy()
