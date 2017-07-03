from rust import core

engine = core.CoreEngine()
engine.setup()

cursor = engine.loader.load_image('cursor.png')
cursor.size = (50, 50)
engine.renderer.render(cursor)

engine.run()
