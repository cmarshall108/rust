try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = '''
A cross-platform elegant 2d game engine written on top of pygame.
'''

setup(name='Rust',
      description='Cross-platform 2d game engine',
      long_description=long_description,
      license='BSD 3-clause "New" or "Revised"',
      version='1.0.0',
      author='Caleb Marshall',
      author_email='anythingtechpro@gmail.com',
      maintainer='Caleb Marshall',
      maintainer_email='anythingtechpro@gmail.com',
      url='https://github.com/AnythingTechPro/rust',
      packages=['rust'],
      classifiers=[
          'Programming Language :: Python :: 2',
      ])
