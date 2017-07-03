import pygame

class GameObject(object):
    engine = None
    id = 0

    def __init__(self, surface=None, parent=None):
        self.parent = parent
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

class SceneObject(object):
    engine = None
    id = 0

    def setup(self):
        pass

    def update(self):
        pass

    def destroy(self):
        pass

class GameObjectManagerError(RuntimeError):
    """
    A game object manager specific runtime error
    """

class GameObjectManager(object):

    def __init__(self, engine):
        self.engine = engine

        self.game_objects = {}
        self.scene_objects = {}

        self._active_scene = None

    @property
    def id(self):
        return len(self.game_objects) + 1

    @property
    def scene_id(self):
        return len(self.scene_objects) + 1

    @property
    def active_scene(self):
        return self._active_scene

    @active_scene.setter
    def active_scene(self, active_scene):
        if not self.has_scene_object(active_scene.id):
            return

        self._active_scene = active_scene

    def has_game_object(self, id):
        return id in self.game_objects

    def has_scene_object(self, id):
        return id in self.scene_objects

    def get_game_objects(self):
        return self.game_objects.values()

    def get_scene_objects(self):
        return self.scene_objects.values()

    def setup(self):
        self.update_task = self.engine.task_manager.add(self.update)

    def update(self, task):
        for game_object in self.get_game_objects():
            game_object.update()

        return task.cont

    def create(self, *args, **kwargs):
        game_object = GameObject(*args, **kwargs)
        game_object.engine = self.engine
        game_object.id = self.id
        game_object.setup()

        self.add(game_object)

        return game_object

    def create_scene(self, class_object, *args, **kwargs):
        class_object.engine = self.engine
        class_object.id = self.scene_id

        scene_object = class_object(*args, **kwargs)
        scene_object.setup()

        self.add_scene(scene_object)

        return scene_object

    def add(self, game_object):
        if self.has_game_object(game_object.id):
            return

        self.game_objects[game_object.id] = game_object

    def add_scene(self, scene_object):
        if self.has_scene_object(scene_object.id):
            return

        self.scene_objects[scene_object.id] = scene_object

    def remove(self, game_object):
        if not self.has_game_object(game_object.id):
            return

        del self.game_objects[game_object.id]

    def remove_scene(self, scene_object):
        if not self.has_scene_object(scene_object.id):
            return

        del self.scene_objects[scene_object.id]

    def get(self, id):
        if not self.has_game_object(id):
            return None

        return self.game_objects[id]

    def get_scene(self, id):
        if not self.has_scene_object(id):
            return None

        return self.scene_objects[id]

    def clear(self):
        self.game_objects = {}

    def destroy(self):
        self.engine.task_manager.remove(self.update_task)

        if self.active_scene:
            self.active_scene.destroy()

        for game_object in self.get_game_objects():
            game_object.destroy()
