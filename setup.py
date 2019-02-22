from setuptools import setup

setup(
   name='blockus',
   version='0.0.0',
   description='Blockus RL environment',
   author='Caleb Pitts',
   author_email='',
   packages=['blockus'],  #same as name
   install_requires=['numpy', 'spacetime', 'spacetimerl', 'dill', 'pygame'],
)