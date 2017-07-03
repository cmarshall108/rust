import os
import pygame
from PIL import Image
from rust import objects

class CoreDisplay(object):

    def __init__(self, engine, resolution=[800, 600], flags=pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE, depth=0):
        self.engine = engine
        self.fill_color = pygame.Color(0, 0, 0)
        self._surface = pygame.display.set_mode(resolution, flags, depth)
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
    def width(self):
        return self.rect.width

    @property
    def height(self):
        return self.rect.height

    def fill(self, color=None):
        self.surface.fill(color or self.fill_color)

    def flip(self, *args, **kwargs):
        pygame.display.update(*args, **kwargs)

    def destroy(self):
        pygame.display.quit()

class CoreLoaderError(IOError):
    """
    A core loader specific io error
    """

class CoreLoader(object):

    def __init__(self, engine):
        self.engine = engine

    def load_image(self, filename, is_transparent=False, flipped=False):
        if not os.path.exists(filename):
            raise CoreLoaderError('Failed to load image %s!' % filename)

        image = Image.load(filename)
        image = pygame.image.fromstring(image.tobytes(), image.size, image.mode, flipped)

        if is_transparent:
            image = image.convert_alpha()

        return self.engine.renderer.game_object_manager.create(image)

    def load_transparent_image(self, filename, flipped=False):
        return self.load_image(filename, True, flipped)

    def load_audio(self, filename, is_music=False):
        pass

    def destroy(self):
        pass

class CoreRendererError(RuntimeError):
    """
    A core render specific runtime error
    """

class CoreRenderer(object):

    def __init__(self, engine):
        self.engine = engine

    def get_game_objects(self):
        return self.game_object_manager.game_objects

    def renderable(self, game_object):
        return game_object.parent is not None

    def setup(self):
        self.game_object_manager = objects.GameObjectManager()

    def update(self):
        for game_object in self.get_game_objects():
            if not self.renderable(game_object):
                continue

            game_object.parent.blit(game_object.surface, game_object.rect)

        self.engine.display.flip([game_object.rect for game_object in self.get_game_objects()])

    def render(self, parent, surface):
        if self.renderable(surface):
            raise CoreRendererError('Cannot render an object that\'s already rendered!')

        surface.parent = parent

    def clear(self):
        self.engine.display.fill()

    def destroy(self):
        pass

class CoreEngine(object):

    def __init__(self):
        self.display = CoreDisplay(self)
        self.loader = CoreLoader(self)
        self.renderer = CoreRenderer(self)
        self.shutdown = False

    def setup(self):
        self.renderer.setup()

    def update(self):
        self.renderer.update()

    def destroy(self):
        self.display.destroy()
        self.renderer.destroy()

    def mainloop(self):
        while not self.shutdown:
            for event in pygame.event.get():
                pass

            self.renderer.clear()
            self.update()

    def run(self):
        try:
            self.mainloop()
        except (KeyboardInterrupt, SystemExit):
            self.shutdown()

        self.destroy()

    def shutdown(self):
        self.shutdown = True
